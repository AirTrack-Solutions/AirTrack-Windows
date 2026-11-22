import importlib.util,json,tempfile,unittest,os
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('community_backup_fixture',ROOT/'app/utils/photo_backup.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class CommunityBackup(unittest.TestCase):
 def test_private_community_state_is_recoverable_and_reused(self):
  with tempfile.TemporaryDirectory()as tmp:
   root=Path(tmp);published=root/'photos';published.mkdir();(published/'own.jpg').write_bytes(b'photo')
   private=root/'private';private.mkdir();(private/'automation.lock').write_bytes(b'0');(private/'preferences.lock').write_bytes(b'0')
   m.write_json(private/'preferences.json',{'enabled':True,'token':'fixture-only'})
   backups=root/'backups';backups.mkdir()
   first=m.backup_photos(backups/'first',{'published':published,'community':private})
   manifest=json.loads((backups/first['file']).read_text());record=manifest['files']['community/preferences.json']
   self.assertEqual(json.loads((backups/'photo_store'/record['sha256']).read_text()),{'enabled':True,'token':'fixture-only'})
   second=m.backup_photos(backups/'second',{'published':published,'community':private});self.assertEqual(second['new_or_changed'],0)
 def test_incomplete_photo_backup_cannot_look_like_complete_sql(self):
  with tempfile.TemporaryDirectory()as tmp,patch.dict(os.environ,{'AIRTRACK_HOME':tmp}):
   root=Path(tmp);sql=root/'backup.sql';sql.write_text('fixture SQL')
   with self.assertRaises(RuntimeError):m.backup_for_app(sql,root/'missing-static')
   self.assertFalse(sql.exists());self.assertTrue(root.joinpath('backup.sql.incomplete').exists())
