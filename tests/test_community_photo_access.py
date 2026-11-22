import importlib.util,json,tempfile,unittest,sys
from pathlib import Path
from types import ModuleType,SimpleNamespace
from unittest.mock import Mock,patch
from sqlalchemy import create_engine,text
import requests
from flask import Flask
from jinja2 import ChoiceLoader,DictLoader,FileSystemLoader
ROOT=Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0,str(ROOT/'app'))

class AccessTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
  self.preferences={'enabled':False,'auto_upload':False,'auto_download':False,'terms_version':'fixture','token':'','credit':'','email':'','access_status':'pending'}
  self.service=SimpleNamespace(preferences=lambda:self.preferences,download_headers=Mock(return_value=None),requests=requests,BASE_URL='https://repository.example.invalid',MAX_BYTES=1024,root=lambda:Path(self.temp.name),read_json=lambda *a:{},TERMS_VERSION='fixture',LICENSE_URL='https://creativecommons.org/licenses/by/4.0/')
  engine=create_engine('sqlite://');self.addCleanup(engine.dispose);self.connection=engine.connect();self.addCleanup(self.connection.close)
  self.connection.execute(text('CREATE TABLE aircraft(AircraftID INT,Registration TEXT,Aircraft_Type TEXT,MSN TEXT)'))
  self.connection.execute(text("INSERT INTO aircraft VALUES (1,'VH-TEST','Test','123')"))
  self.connection.execute(text('ALTER TABLE aircraft ADD COLUMN ICAO_Address TEXT'))
  util=ModuleType('utils');util.community_photo_client=self.service;ext=ModuleType('extensions');ext.db=SimpleNamespace(session=self.connection)
  with patch.dict(sys.modules,{'utils':util,'extensions':ext}):
   spec=importlib.util.spec_from_file_location('routes_fixture',ROOT/'app/routes/community_photos.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  self.app=Flask(__name__);self.app.secret_key='isolated';self.app.jinja_loader=ChoiceLoader([DictLoader({'header.html':''}),FileSystemLoader(ROOT/'app/templates')]);self.app.jinja_env.globals['csrf_token']=lambda:'test'
  self.app.add_url_rule('/cockpit',endpoint='admin.admin_dashboard',view_func=lambda:'')
  self.app.register_blueprint(m.community_photos_bp);self.client=self.app.test_client()
 def test_optout_direct_urls_hidden_without_network(self):
  with patch.object(requests,'get',side_effect=AssertionError('network')):
   self.assertEqual(self.client.get('/community-photos/library').status_code,404)
   self.assertEqual(self.client.get('/community-photos/library/'+'a'*32+'/image').status_code,404)
   page=self.client.get('/community-photos/settings');self.assertEqual(page.status_code,200)
   self.assertNotIn('Browse the contributor library',page.text);self.assertNotIn('Automatic downloads',page.text);self.assertNotIn('Recent submissions',page.text)
  self.service.download_headers.assert_not_called()
 def test_unapproved_member_cannot_browse_or_fetch(self):
  self.preferences['enabled']=True
  self.assertEqual(self.client.get('/community-photos/library').status_code,403)
  self.assertEqual(self.client.get('/community-photos/library/'+'a'*32+'/image').status_code,403)
 def test_approved_proxy_keeps_token_out_of_browser(self):
  self.preferences['enabled']=True;self.service.download_headers.return_value={'Authorization':'Bearer private-fixture'}
  response=Mock();response.status_code=200;response.json.return_value={'photos':[{'id':'a'*32,'registration':'VH-TEST','aircraft_type':'Test','msn':'123','access_grant':'secret-grant','photographer':'Fixture','license':'CC BY 4.0','license_url':self.service.LICENSE_URL}]}
  with patch.object(requests,'get',return_value=response)as get:
   page=self.client.get('/community-photos/library?q=VH-TEST&aircraft_id=1');self.assertEqual(page.status_code,200);self.assertNotIn('private-fixture',page.text);self.assertNotIn('secret-grant',page.text);self.assertNotIn('repository.example.invalid',page.text);self.assertIn('/community-photos/library/',page.text)
   self.assertEqual(get.call_args.kwargs['headers'],self.service.download_headers.return_value)
 def test_optout_settings_cannot_offer_independent_downloads(self):
  page=self.client.get('/community-photos/settings');self.assertNotIn('No contribution is required',page.text);self.assertNotIn('Browse the public library',page.text)

 def test_only_database_members_and_matching_identity_offered(self):
  self.preferences['enabled']=True;self.service.download_headers.return_value={'Authorization':'Bearer private-fixture'}
  with patch.object(requests,'get',side_effect=AssertionError('Unknown aircraft network')):
   self.assertEqual(self.client.get('/community-photos/library?aircraft_id=999').status_code,404)
   self.assertEqual(self.client.get('/community-photos/library/'+'a'*32+'/image?aircraft_id=999').status_code,404)
  response=Mock();response.status_code=200;response.json.return_value={'photos':[{'id':'a'*32,'registration':'VH-OTHER','msn':'123','aircraft_type':'Test','access_grant':'fake'}]}
  with patch.object(requests,'get',return_value=response):
   page=self.client.get('/community-photos/library?aircraft_id=1');self.assertNotIn('VH-OTHER',page.text)
   self.assertEqual(self.client.get('/community-photos/library/'+'a'*32+'/image?aircraft_id=1').status_code,404)



 def test_hex_mismatch_is_not_offered(self):
  self.preferences['enabled']=True;self.service.download_headers.return_value={'Authorization':'Bearer fixture'}
  self.connection.execute(text("UPDATE aircraft SET ICAO_Address='7C1234' WHERE AircraftID=1"))
  response=Mock();response.status_code=200;response.json.return_value={'photos':[{'id':'a'*32,'registration':'VH-TEST','msn':'123','aircraft_type':'Test','icao_hex':'7C9999','access_grant':'fake'}]}
  with patch.object(requests,'get',return_value=response)as get:
   self.assertEqual(self.client.get('/community-photos/library/'+'a'*32+'/image?aircraft_id=1').status_code,404)
   self.assertEqual(get.call_args.kwargs['params']['icao_hex'],'7C1234')
