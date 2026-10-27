"""User-approved verified installer download. Never starts an installer/service."""
import hashlib
import json
import os
import re
import sys
import uuid
from pathlib import Path
from flask import Blueprint, abort, jsonify, render_template, request, send_file
from extensions import db
from sqlalchemy import text
from core.windows_updates import DEFAULT_FEED, UpdateError, check_release, download_installer, version_tuple
from utils.settings_utils import get_current_theme
from core.windows_auto_updates import postpone

updates_bp = Blueprint('updates', __name__, url_prefix='/updates')
ASSETS = Path(sys._MEIPASS) / 'app' if getattr(sys, 'frozen', False) else Path(__file__).resolve().parents[1]


def installed_version():
    version = json.loads((ASSETS / 'windows_release.json').read_text())['version']
    version_tuple(version)
    return version


def _key():
    return (ASSETS / 'core' / 'airtrack_solutions.pub').read_bytes()


def _feed():
    return os.environ.get('AIRTRACK_UPDATE_MANIFEST_URL', DEFAULT_FEED)


def _directory():
    return Path(os.environ.get('AIRTRACK_HOME', Path.home() / 'AirTrack')) / 'updates' / 'downloads'


@updates_bp.get('/api/version')
def running_version():
    try:
        db.session.execute(text('SELECT 1 FROM aircraft LIMIT 1'))
        db.session.execute(text('SELECT 1 FROM app_settings LIMIT 1'))
        applied = {row[0] for row in db.session.execute(text('SELECT migration FROM migrations')).fetchall()}
        migrations = ASSETS / 'migrations'
        if not migrations.is_dir() or any(path.name not in applied for path in migrations.glob('*.sql')):
            raise UpdateError('Database migrations are incomplete')
        return jsonify(product='AirTrack-Windows', version=installed_version(), database_ready=True)
    except Exception:
        return jsonify(product='AirTrack-Windows', version=installed_version(), database_ready=False), 503


@updates_bp.get('/')
def updates_page():
    home = Path(os.environ.get('AIRTRACK_HOME', Path.home() / 'AirTrack'))
    status = {}
    try:
        status = json.loads((home / 'updates' / 'automatic-status.json').read_text(encoding='utf-8-sig'))
    except (OSError, ValueError):
        pass
    return render_template('updates.html', installed_version=installed_version(), selected_theme=get_current_theme(), automatic_status=status)


@updates_bp.post('/postpone')
def postpone_update():
    try:
        days = (request.get_json(silent=True) or {}).get('days')
        value = postpone(os.environ.get('AIRTRACK_HOME', Path.home() / 'AirTrack'), days)
        return jsonify(ok=True, **value)
    except UpdateError as exc:
        return jsonify(ok=False, error=str(exc)), 400


@updates_bp.get('/check')
def check():
    try:
        release = check_release(_feed(), _key(), installed_version())
        return jsonify(ok=True, installed=installed_version(), release=release)
    except UpdateError as exc:
        return jsonify(ok=False, error=str(exc)), 502


@updates_bp.post('/prepare')
def prepare():
    # Blueprint is deliberately NOT CSRF-exempt. A cross-site page cannot
    # initiate downloads/preparation through the local Windows service.
    try:
        release = check_release(_feed(), _key(), installed_version())
        path = download_installer(release, _directory())
        token = uuid.uuid4().hex
        # Re-verify hash and expiry on delivery; callers cannot choose paths.
        record = {'release': release, 'path': path.name}
        record_path = _directory() / (token + '.json')
        record_path.write_text(json.dumps(record), encoding='utf-8')
        return jsonify(ok=True, url='/updates/download/' + token, version=release['version'])
    except UpdateError as exc:
        return jsonify(ok=False, error=str(exc)), 400


@updates_bp.get('/download/<token>')
def download(token):
    if not re.fullmatch(r'[0-9a-f]{32}', token):
        abort(404)
    try:
        record = json.loads((_directory() / (token + '.json')).read_text())
        # Fetch the signed release again: a cached unsigned receipt is not
        # authority to serve a different executable or version.
        release = check_release(_feed(), _key(), installed_version())
        if not release['available'] or record['release'] != release:
            raise UpdateError('Release changed; prepare the update again')
        name = 'AirTrackUpdate-' + release['version'] + '-' + release['sha256'][:16] + '.exe'
        if record['path'] != name:
            raise UpdateError('Invalid prepared installer')
        file = (_directory() / name).open('rb')
        try:
            digest = hashlib.sha256()
            count = 0
            while chunk := file.read(1024 * 1024):
                count += len(chunk)
                if count > release['size']:
                    raise UpdateError('Prepared installer changed; download refused')
                digest.update(chunk)
            if count != release['size'] or digest.hexdigest() != release['sha256']:
                raise UpdateError('Prepared installer changed; download refused')
            file.seek(0)
            response = send_file(file, as_attachment=True, download_name='AirTrackUpdate-' + release['version'] + '.exe', mimetype='application/octet-stream')
            response.call_on_close(file.close)
            return response
        except Exception:
            file.close()
            raise
    except (OSError, ValueError, KeyError, UpdateError):
        abort(409, description='This verified download is no longer available. Check for updates again.')
