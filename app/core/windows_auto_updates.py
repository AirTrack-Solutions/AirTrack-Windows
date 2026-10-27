"""Signed update staging for the external Windows scheduled task.

This process exits before the task starts the installer, so the frozen
application's files can be replaced without locking the updater executable.
"""
import configparser
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from core.windows_updates import DEFAULT_FEED, UpdateError, check_release, download_installer


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.new')
    temporary.write_text(json.dumps(value), encoding='utf-8')
    os.replace(temporary, path)


def postpone(home, days, now=None):
    if type(days) is not int or not 0 <= days <= 7:
        raise UpdateError('Choose between zero and seven days')
    now = now or datetime.now(timezone.utc)
    value = {'postpone_until': (now + timedelta(days=days)).isoformat()}
    write_json(Path(home) / 'update-preferences.json', value)
    return value


def is_postponed(home, now=None):
    path = Path(home) / 'update-preferences.json'
    if not path.exists():
        return False
    try:
        until = datetime.fromisoformat(json.loads(path.read_text())['postpone_until'])
        now = now or datetime.now(timezone.utc)
        if until.tzinfo is None or until > now + timedelta(days=7, minutes=5):
            raise ValueError()
        return until > now
    except (KeyError, TypeError, ValueError) as exc:
        raise UpdateError('Invalid update postponement; check update settings') from exc


def stage(install_dir, home, feed=DEFAULT_FEED):
    install_dir, home = Path(install_dir), Path(home)
    if (home / 'update-in-progress.json').exists():
        raise UpdateError('An earlier installation requires recovery')
    if is_postponed(home):
        return {'status': 'postponed'}
    assets = install_dir / '_internal' / 'app'
    version = json.loads((assets / 'windows_release.json').read_text())['version']
    key = (assets / 'core' / 'airtrack_solutions.pub').read_bytes()
    release = check_release(feed, key, version)
    if not release['available']:
        return {'status': 'current', 'version': version}
    failed_file = home / 'updates' / 'failed-release.json'
    if failed_file.exists():
        failed = json.loads(failed_file.read_text(encoding='utf-8-sig'))
        if failed.get('sha256') == release['sha256']:
            return {'status': 'failed_release', 'version': release['version'],
                    'error': 'This release failed previously. Your previous version was retained; waiting for a corrected release.'}
    installer = download_installer(release, home / 'updates' / 'downloads')
    return {'status': 'ready', 'installer': str(installer),
            'version': release['version'], 'sha256': release['sha256'], 'size': release['size']}


def cli():
    install_dir = Path(sys.executable).parent
    cfg = configparser.ConfigParser()
    cfg.read(install_dir / 'airtrack.cfg')
    home = Path(cfg.get('app', 'data_dir', fallback=str(Path(os.environ['ProgramData']) / 'AirTrack')))
    status_file = home / 'updates' / 'automatic-status.json'
    try:
        # Task command uses the stable feed. An explicit administrator test
        # override still requires the bundled signature trust root.
        feed = sys.argv[2] if len(sys.argv) == 3 else DEFAULT_FEED
        result = stage(install_dir, home, feed)
        result['checked_at'] = datetime.now(timezone.utc).isoformat()
        write_json(status_file, result)
        print(json.dumps(result))
        return 0
    except Exception as exc:
        result = {'status': 'error', 'error': str(exc), 'checked_at': datetime.now(timezone.utc).isoformat()}
        write_json(status_file, result)
        print(json.dumps(result))
        return 1
