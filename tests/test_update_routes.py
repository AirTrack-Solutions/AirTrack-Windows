"""Isolated route contract tests; no live DB, network or executable launch."""
import hashlib
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch
from flask import Flask
from flask_wtf import CSRFProtect

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'app'))
settings = types.ModuleType('utils.settings_utils')
settings.get_current_theme = lambda: 'default'
sys.modules['utils.settings_utils'] = settings
ext = types.ModuleType('extensions')
ext.db = types.SimpleNamespace(session=types.SimpleNamespace(execute=lambda _: None))
sys.modules['extensions'] = ext
from routes import update_routes as routes


class UpdateRoutesTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'test-only'
        CSRFProtect(self.app)
        self.app.register_blueprint(routes.updates_bp)
        self.client = self.app.test_client()

    def test_prepare_requires_csrf(self):
        with patch.object(routes, 'check_release') as check:
            self.assertEqual(self.client.post('/updates/prepare').status_code, 400)
            check.assert_not_called()

    def test_health_requires_tables_and_completed_migrations(self):
        names = [(p.name,) for p in (routes.ASSETS / 'migrations').glob('*.sql')]
        with patch.object(routes.db.session, 'execute', return_value=types.SimpleNamespace(fetchall=lambda: names)):
            self.assertEqual(self.client.get('/updates/api/version').status_code, 200)
        with patch.object(routes.db.session, 'execute', return_value=types.SimpleNamespace(fetchall=lambda: [])):
            self.assertEqual(self.client.get('/updates/api/version').status_code, 503)
        with patch.object(routes.db.session, 'execute', side_effect=RuntimeError('DB unavailable')):
            self.assertEqual(self.client.get('/updates/api/version').status_code, 503)

    def test_delivery_rechecks_prepared_file(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            data = b'MZ' + b'x' * 2000
            digest = hashlib.sha256(data).hexdigest()
            name = 'AirTrackUpdate-1.0.2-' + digest[:16] + '.exe'
            (folder / name).write_bytes(data)
            release = dict(version='1.0.2', sha256=digest, size=len(data), available=True)
            token = 'a' * 32
            (folder / (token + '.json')).write_text(json.dumps({'release': release, 'path': name}))
            with patch.object(routes, '_directory', lambda: folder), patch.object(routes, 'check_release', lambda *_: release), patch.object(routes, '_key', lambda: b'fixture'):
                response = self.client.get('/updates/download/' + token)
                self.assertEqual(response.data, data)
                response.close()
                (folder / name).write_bytes(b'changed')
                self.assertEqual(self.client.get('/updates/download/' + token).status_code, 409)
                self.assertEqual(self.client.get('/updates/download/invalid').status_code, 404)


if __name__ == '__main__':
    unittest.main()
