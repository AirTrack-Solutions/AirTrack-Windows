"""Imageless theme stays selectable after generation and cache reuse."""
import importlib.util
import json
from pathlib import Path
import tempfile
import os
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('theme_fixture', ROOT/'app/utils/theme_scanner.py')
theme = importlib.util.module_from_spec(spec)
spec.loader.exec_module(theme)

class VintageThemeTests(unittest.TestCase):
    def test_imageless_theme_cached_list_and_existing_photo_theme_survive(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);themes=root/'themes';css=root/'css';themes.mkdir();css.mkdir()
            (css/'vintage-brass.css').write_text('body.theme-vintage_brass {background:#252725}')
            for kind in ['cockpit','background','thumb']:
                (themes/f'night_{kind}.png').write_bytes(b'fixture')
            with patch.multiple(theme,THEMES_DIR=themes,CSS_DIR=css,THEMES_JSON=themes/'themes.json',THEMES_CSS=css/'themes.css',LOCKFILE=themes/'.lock'):
                first=theme.scan_and_generate();second=theme.scan_and_generate()
                for result in (first,second):
                    self.assertEqual({t['value'] for t in result},{'vintage_brass','night'})
                    brass=next(t for t in result if t['value']=='vintage_brass')
                    self.assertIsNone(brass['background_url'])
                    self.assertIsNone(brass['cockpit_url'])
                generated=(css/'themes.css').read_text()
                self.assertLess(generated.index('@import'),generated.index('.background'))
                self.assertIn('night_background.png',generated)
                self.assertNotIn('vintage_brass_background',generated)
                self.assertEqual(json.loads((themes/'themes.json').read_text()),first)

    def test_frozen_static_root_matches_pyinstaller_app_data(self):
        with patch.object(theme.sys, 'frozen', True, create=True), patch.object(theme.sys, '_MEIPASS', '/fixture/bundle', create=True):
            self.assertEqual(theme._default_static_dir(), Path('/fixture/bundle/app/static'))

    def test_newer_legacy_cache_is_rebuilt_and_keeps_photo_themes(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);themes=root/'themes';css=root/'css';themes.mkdir();css.mkdir()
            (css/'vintage-brass.css').write_text('body {}')
            for kind in ['cockpit','background','thumb']:
                (themes/f'night_{kind}.png').write_bytes(b'fixture')
            (themes/'themes.json').write_text('[{"key":"night"}]')
            (css/'themes.css').write_text('/* old generated cache */')
            for p in [themes/'themes.json', css/'themes.css']:
                os.utime(p, (4102444800,4102444800))
            with patch.multiple(theme,THEMES_DIR=themes,CSS_DIR=css,THEMES_JSON=themes/'themes.json',THEMES_CSS=css/'themes.css',LOCKFILE=themes/'.lock'):
                result=theme.scan_and_generate()
                self.assertEqual({x['key'] for x in result},{'vintage_brass','night'})
                self.assertIn('vintage-brass.css',(css/'themes.css').read_text())

if __name__=='__main__':unittest.main()
