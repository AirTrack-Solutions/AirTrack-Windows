"""Regression checks for release trust, anti-downgrade and bounded downloads."""
import base64
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

spec=importlib.util.spec_from_file_location('windows_updates',Path(__file__).parents[1]/'app/core/windows_updates.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class Releases(unittest.TestCase):
 def setUp(self):
  self.key=Ed25519PrivateKey.generate();self.public=self.key.public_key().public_bytes(Encoding.PEM,PublicFormat.SubjectPublicKeyInfo)
  self.now=datetime.now(timezone.utc);self.binary=b'MZ'+b'x'*2046
  self.payload=dict(format=1,product=m.PRODUCT,version='1.0.2',url='https://example.com/update.exe',size=len(self.binary),sha256=hashlib.sha256(self.binary).hexdigest(),published_at=(self.now-timedelta(minutes=1)).isoformat(),expires_at=(self.now+timedelta(days=2)).isoformat(),notes='Test')
 def sign(self,payload=None,key=None):
  p=payload or self.payload;sig=(key or self.key).sign(m.DOMAIN+m.canonical(p));return json.dumps({'release':p,'signature':base64.b64encode(sig).decode()}).encode()
 def verify(self,data=None,version='1.0.1'):return m.verify_manifest(data or self.sign(),self.public,version,self.now)
 def test_valid_new_and_equal(self):
  self.assertTrue(self.verify()['available']);self.assertFalse(self.verify(version='1.0.2')['available'])
 def test_tamper_and_wrong_key(self):
  d=json.loads(self.sign());d['release']['url']='https://example.com/evil.exe'
  for data in (json.dumps(d).encode(),self.sign(key=Ed25519PrivateKey.generate())):
   with self.assertRaises(m.UpdateError):self.verify(data)
 def test_older_expired_future_and_invalid_fields(self):
  cases=[('version','1.0.0'),('version','../1.0.2'),('product','Other'),('url','http://example.com/a'),('url','https://user:secret@example.com/a'),('size',True),('size',m.MAX_INSTALLER_BYTES+1),('sha256','bad'),('expires_at',(self.now-timedelta(days=1)).isoformat()),('published_at',(self.now+timedelta(days=1)).isoformat())]
  for k,v in cases:
   with self.subTest(field=k,value=v):
    p={**self.payload,k:v}
    with self.assertRaises(m.UpdateError):self.verify(self.sign(p))
 def test_duplicate_envelope_and_size(self):
  for data in (b'{"release":{},"release":{}}',b'x'*(m.MAX_MANIFEST_BYTES+1)):
   with self.assertRaises(m.UpdateError):self.verify(data)
 def test_download_hash_length_and_cleanup(self):
  release=self.verify()
  for binary,valid in ((self.binary,True),(b'MZ'+b'y'*2046,False),(self.binary[:-1],False),(self.binary+b'x',False)):
   with tempfile.TemporaryDirectory() as td:
    if valid:
     result=m.download_installer(release,td,lambda url:io.BytesIO(binary));self.assertEqual(result.read_bytes(),binary)
    else:
     with self.assertRaises(m.UpdateError):m.download_installer(release,td,lambda url:io.BytesIO(binary))
     self.assertEqual(list(Path(td).iterdir()),[])
 def test_download_failure_cleans_partial(self):
  def fail(url):raise OSError('offline')
  with tempfile.TemporaryDirectory() as td:
   with self.assertRaises(m.UpdateError):m.download_installer(self.verify(),td,fail)
   self.assertEqual(list(Path(td).iterdir()),[])
 def test_redirect_refuses_http(self):
  with self.assertRaises(m.UpdateError):m._HTTPSRedirect().redirect_request(None,None,302,'',{},'http://example.com/a')

if __name__=='__main__':unittest.main()
