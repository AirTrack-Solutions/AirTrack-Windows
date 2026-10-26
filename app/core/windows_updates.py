"""User-approved Windows releases. Verification never executes downloaded code."""
from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, HTTPRedirectHandler, build_opener

from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

DOMAIN = b"AirTrack Windows installer release v1\n"
PRODUCT = "AirTrack-Windows"
MAX_INSTALLER_BYTES = 512 * 1024 * 1024
MAX_MANIFEST_BYTES = 64 * 1024
DEFAULT_FEED = "https://airtracksolutions.com/api/wombat/windows-release"


class UpdateError(ValueError):
    """Untrusted, incompatible or unavailable release; no install is permitted."""


def version_tuple(value):
    if not isinstance(value, str) or not re.fullmatch(r"(?:0|[1-9][0-9]{0,4})\.(?:0|[1-9][0-9]{0,4})\.(?:0|[1-9][0-9]{0,4})", value):
        raise UpdateError("Invalid stable release version")
    return tuple(map(int, value.split(".")))


def https_url(value):
    if not isinstance(value, str) or len(value) > 2048:
        raise UpdateError("Invalid release URL")
    try:
        url = urlsplit(value)
        if url.scheme != "https" or not url.hostname or url.username or url.password or url.fragment or url.port not in (None, 443):
            raise ValueError()
    except ValueError as exc:
        raise UpdateError("Updates require an HTTPS URL without credentials") from exc
    return value


def canonical(payload):
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("utf-8")


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise UpdateError("Duplicate manifest field")
        result[key] = value
    return result


def verify_manifest(data, public_key_pem, installed_version, now=None):
    """Verify exact signed fields before interpreting URLs or offering an update."""
    if not isinstance(data, bytes) or len(data) > MAX_MANIFEST_BYTES:
        raise UpdateError("Release manifest is too large")
    try:
        envelope = json.loads(data, object_pairs_hook=_unique_object)
        if not isinstance(envelope, dict) or set(envelope) != {"release", "signature"}:
            raise UpdateError("Invalid release envelope")
        payload = envelope["release"]
        if not isinstance(payload, dict):
            raise UpdateError("Invalid release payload")
        key = load_pem_public_key(public_key_pem)
        if not isinstance(key, Ed25519PublicKey):
            raise UpdateError("Unexpected update signing key")
        key.verify(base64.b64decode(envelope["signature"], validate=True), DOMAIN + canonical(payload))
        required = {"format", "product", "version", "url", "sha256", "size", "published_at", "expires_at", "notes"}
        if set(payload) != required or type(payload["format"]) is not int or payload["format"] != 1 or payload["product"] != PRODUCT:
            raise UpdateError("Unsupported release manifest")
        released = version_tuple(payload["version"])
        installed = version_tuple(installed_version)
        if released < installed:
            raise UpdateError("Older releases cannot replace this installation")
        https_url(payload["url"])
        if not isinstance(payload["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", payload["sha256"]):
            raise UpdateError("Invalid installer digest")
        if type(payload["size"]) is not int or not 1024 <= payload["size"] <= MAX_INSTALLER_BYTES:
            raise UpdateError("Invalid installer size")
        if not isinstance(payload["notes"], str) or len(payload["notes"]) > 8000:
            raise UpdateError("Invalid release notes")
        dates = []
        for field in ("published_at", "expires_at"):
            date = datetime.fromisoformat(payload[field].replace("Z", "+00:00"))
            if date.tzinfo is None:
                raise UpdateError("Release times must include a timezone")
            dates.append(date.astimezone(timezone.utc))
        now = now or datetime.now(timezone.utc)
        published, expires = dates
        if (published-now).total_seconds() > 600 or expires <= now or expires <= published:
            raise UpdateError("Release information has expired or has an invalid publication time")
        return dict(payload, available=released > installed)
    except UpdateError:
        raise
    except Exception as exc:
        raise UpdateError("Release signature or manifest could not be verified") from exc


class _HTTPSRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        https_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _open(url):
    request = Request(https_url(url), headers={"User-Agent": "AirTrack-Windows-Updater/1", "Accept-Encoding": "identity"})
    return build_opener(_HTTPSRedirect()).open(request, timeout=20)


def check_release(feed, public_key_pem, installed_version, opener=None):
    try:
        with (opener or _open)(https_url(feed)) as response:
            data = response.read(MAX_MANIFEST_BYTES + 1)
        return verify_manifest(data, public_key_pem, installed_version)
    except UpdateError:
        raise
    except Exception as exc:
        raise UpdateError("The update service is unavailable; your installation was not changed") from exc


def download_installer(release, directory, opener=None):
    """Only accept a verified-manifest result; leave no partial executable behind."""
    if not release.get("available"):
        raise UpdateError("No newer release is available")
    target = Path(directory)
    target.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix="download-", suffix=".part", dir=target)
    partial = Path(name)
    count = 0
    digest = hashlib.sha256()
    try:
        with os.fdopen(fd, "wb") as output, (opener or _open)(https_url(release["url"])) as response:
            while True:
                chunk = response.read(min(1024 * 1024, release["size"] - count + 1))
                if not chunk:
                    break
                count += len(chunk)
                if count > release["size"] or count > MAX_INSTALLER_BYTES:
                    raise UpdateError("Installer exceeds its signed size")
                output.write(chunk)
                digest.update(chunk)
            output.flush()
            os.fsync(output.fileno())
        if count != release["size"] or digest.hexdigest() != release["sha256"]:
            raise UpdateError("Installer size or signature-bound hash does not match")
        with partial.open("rb") as file:
            if file.read(2) != b"MZ":
                raise UpdateError("Release is not a Windows installer")
        destination = target / ("AirTrackUpdate-" + release["version"] + "-" + release["sha256"][:16] + ".exe")
        os.replace(partial, destination)
        return destination
    except UpdateError:
        raise
    except Exception as exc:
        raise UpdateError("Installer download failed; your installation was not changed") from exc
    finally:
        partial.unlink(missing_ok=True)
