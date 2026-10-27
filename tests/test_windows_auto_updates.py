"""Automatic staging must honor postponement, trust checks and recovery gates."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / 'app'))
from core import windows_auto_updates as m
from core.windows_updates import UpdateError


class Automatic(unittest.TestCase):
    def test_postponement_and_resume(self):
        now = datetime.now(timezone.utc)
        with tempfile.TemporaryDirectory() as td:
            self.assertFalse(m.is_postponed(td, now))
            m.postpone(td, 7, now)
            self.assertTrue(m.is_postponed(td, now))
            self.assertFalse(m.is_postponed(td, now + timedelta(days=8)))
            m.postpone(td, 0, now)
            self.assertFalse(m.is_postponed(td, now))
            for value in (-1, 8, True, '7', None):
                with self.assertRaises(UpdateError):
                    m.postpone(td, value, now)

    def test_invalid_preferences_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            Path(td, 'update-preferences.json').write_text('{"postpone_until":"bad"}')
            with self.assertRaises(UpdateError):
                m.is_postponed(td)

    def test_pending_recovery_or_postponement_does_not_download(self):
        with tempfile.TemporaryDirectory() as td, patch.object(m, 'check_release') as check:
            home = Path(td)
            m.postpone(home, 7)
            self.assertEqual(m.stage(home, home)['status'], 'postponed')
            (home / 'update-in-progress.json').touch()
            with self.assertRaises(UpdateError):
                m.stage(home, home)
            check.assert_not_called()

    def test_only_verified_available_release_is_downloaded(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            assets = home / '_internal/app'
            (assets / 'core').mkdir(parents=True)
            (assets / 'windows_release.json').write_text('{"version":"1.0.1"}')
            (assets / 'core/airtrack_solutions.pub').write_bytes(b'trust root')
            with patch.object(m, 'check_release', side_effect=UpdateError('signature')):
                with patch.object(m, 'download_installer') as download:
                    with self.assertRaises(UpdateError):
                        m.stage(home, home)
                    download.assert_not_called()
            with patch.object(m, 'check_release', return_value={'available': False}):
                with patch.object(m, 'download_installer') as download:
                    self.assertEqual(m.stage(home, home)['status'], 'current')
                    download.assert_not_called()


if __name__ == '__main__':
    unittest.main()
