"""Local-only consent, explicit-own-photo outbox and approved-photo downloads.

Preferences/tokens never enter app_settings or Field Sync SQL. No network calls
occur unless the user enabled the corresponding option.
"""
import contextlib
try:
    import fcntl
except ImportError:
    fcntl = None
import hashlib
import io
import json
import os
from pathlib import Path
import re
import tempfile
import threading
import time
import uuid
from datetime import datetime, timezone
import requests

TERMS_VERSION = '2026-11-21-cc-by-4.0-contributors-v2'
LICENSE_URL = 'https://creativecommons.org/licenses/by/4.0/'
BASE_URL = os.environ.get('AIRTRACK_PHOTO_LIBRARY_URL', 'https://www.airtracksolutions.com').rstrip('/')
MAX_BYTES = 12 * 1024 * 1024
DEFAULTS = dict(enabled=False, auto_upload=False, auto_download=False, credit='', email='',
                terms_version='', acknowledged_at='', access_status='not_requested')


def now():
    return datetime.now(timezone.utc).isoformat()


def root():
    home = os.environ.get('AIRTRACK_HOME')
    return Path(home) / 'community_photos' if home else Path(__file__).resolve().parents[1] / 'data/community_photos'


def read_json(path, fallback):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return fallback


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, name = tempfile.mkstemp(dir=path.parent)
    temp = Path(name)
    try:
        with os.fdopen(fd, 'wb') as output:
            output.write(json.dumps(value, sort_keys=True).encode())
            output.flush()
            os.fsync(output.fileno())
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)



def preferences():
    return {**DEFAULTS, **read_json(root() / 'preferences.json', {})}


@contextlib.contextmanager
def lock(name='preferences.lock', blocking=True):
    folder = root()
    folder.mkdir(parents=True, exist_ok=True, mode=0o700)
    with (folder / name).open('a+b') as handle:
        try:
            if fcntl is not None:
                fcntl.flock(handle, fcntl.LOCK_EX | (0 if blocking else fcntl.LOCK_NB))
            else:
                import msvcrt
                if handle.seek(0,2)==0:
                    handle.write(b'\0');handle.flush()
                handle.seek(0)
                msvcrt.locking(handle.fileno(),msvcrt.LK_LOCK if blocking else msvcrt.LK_NBLCK,1)
        except (BlockingIOError, OSError):
            if blocking:
                raise
            yield False
            return
        try:
            yield True
        finally:
            if fcntl is not None:
                fcntl.flock(handle, fcntl.LOCK_UN)
            else:
                handle.seek(0);msvcrt.locking(handle.fileno(),msvcrt.LK_UNLCK,1)


def save_preferences(data):
    with lock():
        old = preferences()
        enabled = data.get('enabled') == 'yes'
        auto_download = data.get('auto_download') == 'yes'
        if enabled:
            if data.get('license_ack') != 'yes':
                raise ValueError('Acknowledge the contribution licence before enabling sharing.')
            credit = old.get('credit') if old.get('token') else str(data.get('credit', '')).strip()
            email = old.get('email') if old.get('token') else str(data.get('email', '')).strip().casefold()
            if not 2 <= len(credit) <= 100 or any(ord(c) < 32 for c in credit) or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', email or ''):
                raise ValueError('Enter a photographer credit and private contact email.')
            acknowledged = old.get('acknowledged_at') if old.get('enabled') and old.get('terms_version') == TERMS_VERSION else now()
            old.update(credit=credit, email=email, terms_version=TERMS_VERSION, acknowledged_at=acknowledged)
        old.update(enabled=enabled, auto_upload=enabled and data.get('auto_upload') == 'yes',
                   auto_download=enabled and auto_download, installation_id=old.get('installation_id') or uuid.uuid4().hex)
        if not enabled:
            for path in (root() / 'outgoing').glob('*.json'):
                job = read_json(path, {})
                if job.get('status') == 'queued':
                    job.update(status='cancelled', error='Sharing opted out before submission.')
                    write_json(path, job)
        write_json(root() / 'preferences.json', old)
        # Append-only local acknowledgement history; never transmitted through SQL.
        history = root() / 'consent-history.jsonl'
        with history.open('a') as output:
            history.chmod(0o600)
            output.write(json.dumps({k: old.get(k) for k in ('enabled', 'auto_upload', 'auto_download', 'terms_version', 'acknowledged_at', 'installation_id')}) + '\n')
        return old


def request_access():
    with lock():
        p = preferences()
        if not p['enabled'] or p.get('token'):
            return p
        response = requests.post(BASE_URL + '/api/photo-library/contributors', json=dict(
            credit=p['credit'], email=p['email'], terms_version=TERMS_VERSION, license_ack=True), timeout=15, allow_redirects=False)
        if response.status_code != 202:
            raise ValueError('Contributor access could not be requested. Your local photo settings are saved; please retry or contact AirTrack.')
        data = response.json()
        if not re.fullmatch(r'[0-9a-f]{32}', str(data.get('id', ''))) or not 40 <= len(str(data.get('token', ''))) <= 100:
            raise ValueError('Unexpected contributor response.')
        p.update(token=data['token'], contributor_id=data['id'], access_status='pending')
        write_json(root() / 'preferences.json', p)
        return p


def access_status(p):
    if not p.get('token'):
        return 'not_requested'
    response = requests.get(BASE_URL + '/api/photo-library/contributor', headers={'Authorization': 'Bearer ' + p['token']}, timeout=10, allow_redirects=False)
    if response.status_code == 401:
        return 'blocked'
    response.raise_for_status()
    data = response.json()
    return data.get('status') if data.get('status') in ('pending', 'active', 'blocked', 'rejected') else 'pending'


def enqueue_owned_photo(path, registration, aircraft_type='', msn='', explicit=False, owned_import=None, expected_sha256=None):
    """Only call for a current per-photo own/right/privacy confirmation or AS_ import."""
    with lock():
        p = preferences()
        if not p['enabled'] or p['terms_version'] != TERMS_VERSION or not (explicit or p['auto_upload']):
            return False
        if owned_import is not None:
            try:
                imported = datetime.fromisoformat(owned_import['imported_at'])
                acknowledged = datetime.fromisoformat(p['acknowledged_at'])
                if (not p['auto_upload'] or imported.tzinfo is None or acknowledged.tzinfo is None
                        or imported < acknowledged or owned_import['acknowledged_at'] != p['acknowledged_at']
                        or owned_import['terms_version'] != p['terms_version']):
                    return False
            except (ValueError, KeyError, TypeError):
                return False
        if p.get('access_status') in ('blocked', 'rejected'):
            raise ValueError('Uploads are paused for this contributor. Contact AirTrack.')
        from PIL import Image, ImageOps
        path = Path(path)
        if not path.is_file() or path.stat().st_size > MAX_BYTES:
            raise ValueError('Photo is missing or larger than 12 MB; the Logbook copy is unchanged.')
        if path.is_symlink():
            raise ValueError('Symlink photos cannot be shared.')
        raw = path.read_bytes()
        if len(raw) > MAX_BYTES or (expected_sha256 and hashlib.sha256(raw).hexdigest() != expected_sha256):
            raise ValueError('The selected photo changed before sharing.')
        with Image.open(io.BytesIO(raw)) as source:
            if source.width * source.height > 24_000_000:
                raise ValueError('Resize this photo before sharing (maximum 24 megapixels).')
            image = ImageOps.exif_transpose(source).convert('RGB')
            image.thumbnail((2400, 2400))
            output = io.BytesIO()
            from utils.aircraft_photo_metadata import identity, packet, parse_xmp, NS
            parsed = parse_xmp(source.info.get('xmp', source.info.get('XML:com.adobe.xmp')))
            hex_code = None
            if parsed is not None:
                if parsed.find('.//{'+NS+'}PhotoID') is not None:
                    raise ValueError('Community downloads cannot be resubmitted as your own photo.')
                hex_code = parsed.findtext('.//{'+NS+'}ICAOHex')
                embedded_reg = parsed.findtext('.//{'+NS+'}Registration')
                if embedded_reg and embedded_reg.strip().upper() != registration.strip().upper():
                    raise ValueError('Photo registration differs from the selected aircraft.')
            identifiers = identity(registration, msn, hex_code)
            image.save(output, 'JPEG', quality=90, xmp=packet(identifiers))
        data = output.getvalue()
        key = hashlib.sha256((p['installation_id'] + registration + TERMS_VERSION + p['acknowledged_at']).encode() + data).hexdigest()
        folder = root() / 'outgoing'
        folder.mkdir(exist_ok=True, mode=0o700)
        target = folder / (key + '.json')
        if target.exists():
            return True
        if sum(read_json(f, {}).get('status') == 'queued' for f in folder.glob('*.json')) >= 20:
            raise ValueError('Twenty photos are already queued. Please wait for them before sharing more.')
        image_path = folder / (key + '.jpg')
        if image_path.exists():
            if image_path.is_symlink() or hashlib.sha256(image_path.read_bytes()).hexdigest() != hashlib.sha256(data).hexdigest():
                raise ValueError('Existing queued photo failed verification.')
        else:
            with image_path.open('xb') as output:
                image_path.chmod(0o600)
                output.write(data);output.flush();os.fsync(output.fileno())
        write_json(root() / 'automation.json', {'last_attempt': 0, 'status': 'photo_queued'})
        write_json(target, dict(request_id=key, registration=registration, aircraft_type=aircraft_type or '',
                   msn=msn or '', icao_hex=identifiers.get('ICAOHex',''), photographer=p['credit'], contact=p['email'], terms_version=TERMS_VERSION,
                   consent_at=now(), rights_ack='yes', license_ack='yes', no_people_ack='yes',
                   status='queued', source='explicit-own-photo'))
        return True


def process_outgoing():
    # Keep preference lock through the small batch: opt-out cannot race a new send.
    with lock():
        p = preferences()
        if not p['enabled'] or p['terms_version'] != TERMS_VERSION:
            return
        status = access_status(p)
        p['access_status'] = status
        write_json(root() / 'preferences.json', p)
        if status != 'active':
            if status in ('blocked', 'rejected'):
                for file in (root() / 'outgoing').glob('*.json'):
                    job = read_json(file, {})
                    if job.get('status') == 'queued':
                        job.update(status='blocked', error='Contributor access ' + status)
                        write_json(file, job)
            return
        queued = [f for f in (root() / 'outgoing').glob('*.json') if read_json(f, {}).get('status') == 'queued'][:3]
        for file in queued:
            job = read_json(file, {})
            if job.get('terms_version') != p['terms_version']:
                continue
            with file.with_suffix('.jpg').open('rb') as image:
                response = requests.post(BASE_URL + '/api/photo-library/submissions',
                    headers={'Authorization': 'Bearer ' + p['token']}, data={k: str(v) for k, v in job.items()},
                    files={'image': ('photo.jpg', image, 'image/jpeg')}, timeout=20, allow_redirects=False)
            if response.status_code == 202:
                result = response.json()
                job.update(status='submitted', repository_id=result['id'], submitted_at=now())
                write_json(file, job)
            elif response.status_code in (401, 403):
                p.update(access_status='blocked')
                write_json(root() / 'preferences.json', p)
                job.update(status='blocked', error='Contributor uploads are paused.')
                write_json(file, job)
                break
            elif response.status_code in (400, 413):
                job.update(status='needs_attention', error='Repository could not accept this photo. Review it before retrying.')
                write_json(file, job)
            else:
                break  # Offline, rate-limited or full: retain queue for a later check.


def credits():
    return read_json(root() / 'download-credits.json', {})


def download_headers(p=None):
    p = preferences() if p is None else p
    if not p['enabled'] or p.get('terms_version') != TERMS_VERSION or not p.get('token'):
        return None
    headers = {'Authorization': 'Bearer ' + p['token']}
    response = requests.get(BASE_URL + '/api/photo-library/contributor', headers=headers, timeout=10, allow_redirects=False)
    if response.status_code in (401, 403):
        return None
    response.raise_for_status()
    data = response.json()
    return headers if data.get('status') == 'active' and data.get('download_allowed') is True else None


def download_missing(app):
    p = preferences()
    if not p['enabled'] or not p['auto_download']:
        return
    headers = download_headers(p)
    if headers is None:
        return
    from extensions import db
    from sqlalchemy import text
    folder = Path(app.static_folder) / 'uploads/aircraft'
    folder.mkdir(parents=True, exist_ok=True)
    cursor = read_json(root() / 'download-cursor.json', {}).get('before_id', 0)
    with db.engine.connect() as conn:
        rows = [dict(row) for row in conn.execute(text('SELECT AircraftID,Registration,Aircraft_Image,MSN,Aircraft_Type,ICAO_Address FROM aircraft WHERE (:cursor=0 OR AircraftID<:cursor) ORDER BY AircraftID DESC LIMIT 200'), {'cursor': cursor}).mappings()]
    last_id = 0
    attempted = 0
    for row in rows:
        if attempted >= 3:
            break
        last_id = row['AircraftID']
        filename = row['Aircraft_Image']
        if filename and (Path(str(filename)).name != filename or (folder / filename).exists()):
            continue
        reg = str(row['Registration'] or '').strip().upper()
        if not re.fullmatch(r'[A-Z0-9][A-Z0-9-]{1,19}', reg):
            continue
        attempted += 1
        response = requests.get(BASE_URL + '/api/photo-library', params={'registration': reg, 'msn': row['MSN'] or '', 'aircraft_type': row['Aircraft_Type'] or '', 'icao_hex':row.get('ICAO_Address') or ''}, headers=headers, timeout=10, allow_redirects=False)
        response.raise_for_status()
        options = response.json().get('photos', [])
        chosen = next((photo for photo in options if photo.get('registration') == reg
                       and (not row['MSN'] or str(photo.get('msn', '')).strip() == str(row['MSN']).strip())
                       and (not row['Aircraft_Type'] or str(photo.get('aircraft_type', '')).strip().casefold() == str(row['Aircraft_Type']).strip().casefold())
                       and (row['MSN'] or row['Aircraft_Type'])
                       and isinstance(photo.get('access_grant'), str)
                       and photo.get('license') == 'CC BY 4.0'
                       and photo.get('license_url') == LICENSE_URL
                       and (not row.get('ICAO_Address') or str(photo.get('icao_hex') or '').upper() == str(row['ICAO_Address']).upper())
                       and re.fullmatch(r'[0-9a-f]{32}', str(photo.get('id', '')))), None)
        if not chosen:
            continue
        result = requests.get(BASE_URL + '/photos/' + chosen['id'] + '/image.jpg', headers={**headers, 'X-Photo-Grant': chosen['access_grant']}, timeout=15, stream=True, allow_redirects=False)
        result.raise_for_status()
        data = bytearray()
        try:
            for chunk in result.iter_content(65536):
                data.extend(chunk)
                if len(data) > MAX_BYTES:
                    raise ValueError('Community photo download too large')
        finally:
            result.close()
        if hashlib.sha256(data).hexdigest() != chosen.get('sha256') or not data.startswith(b'\xff\xd8'):
            raise ValueError('Community photo download verification failed')
        name = filename or ('COMM_' + chosen['id'] + '.jpg')
        created = False
        with lock():
            if not preferences()['enabled'] or not preferences()['auto_download']:
                return
            with db.engine.begin() as conn:
                current = conn.execute(text('SELECT Aircraft_Image FROM aircraft WHERE AircraftID=:id FOR UPDATE'), {'id': row['AircraftID']}).scalar()
                if current != filename:
                    continue
                if current and (folder / current).exists():
                    continue
                with tempfile.NamedTemporaryFile(dir=folder, delete=False) as out:
                    temp = Path(out.name)
                    try:
                        out.write(data);out.flush();os.fsync(out.fileno());temp.chmod(0o644)
                        try:
                            os.link(temp, folder / name)
                            created = True
                        except FileExistsError:
                            continue
                    finally:
                        temp.unlink(missing_ok=True)
                try:
                    known = credits()
                    known[name] = {key: chosen[key] for key in ('id', 'photographer', 'license', 'license_url', 'sha256')}
                    write_json(root() / 'download-credits.json', known)
                    conn.execute(text('UPDATE aircraft SET Aircraft_Image=:name,Aircraft_Updated=Aircraft_Updated WHERE AircraftID=:id'), {'name': name, 'id': row['AircraftID']})
                except Exception:
                    if created:
                        (folder / name).unlink(missing_ok=True)
                    raise

    write_json(root() / 'download-cursor.json', {'before_id': last_id if rows else 0})


def tick(app):
    try:
        with lock('automation.lock', blocking=False) as acquired:
            if not acquired:
                return
            p = preferences()
            if not p['enabled']:
                return
            state = read_json(root() / 'automation.json', {})
            if time.time() - state.get('last_attempt', 0) < 900:
                return
            write_json(root() / 'automation.json', {'last_attempt': time.time(), 'status': 'running'})
            with app.app_context():
                if p['enabled']:
                    process_outgoing()
                if preferences()['auto_download']:
                    download_missing(app)
            write_json(root() / 'automation.json', {'last_attempt': time.time(), 'status': 'ok'})
    except Exception:
        # No credentials/contact details or remote bodies in logs.
        app.logger.warning('Community photo check deferred; local photos are unchanged.')


def start_check(app):
    p = preferences()
    if p['enabled'] and time.time() - read_json(root() / 'automation.json', {}).get('last_attempt', 0) >= 900:
        threading.Thread(target=tick, args=(app,), daemon=True).start()
