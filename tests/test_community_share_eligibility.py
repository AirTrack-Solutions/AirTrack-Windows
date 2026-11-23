"""Synthetic files and isolated Flask routes; no real DB, account, network or photos."""
import ast,hashlib,os,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock
from flask import Flask,current_app,request,flash,redirect,url_for
from PIL import Image
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'app'))
from utils.aircraft_photo_metadata import community_packet,identity

class ShareEligibilityTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);root=Path(self.tmp.name);folder=root/'uploads/aircraft';folder.mkdir(parents=True)
  self.app=Flask(__name__,static_folder=str(root));self.app.secret_key='isolated fixture'
  self.credits={};self.queue=Mock();self.record=Mock();self.render=Mock(return_value='share form')
  service=SimpleNamespace(preferences=lambda:{'enabled':True,'terms_version':'fixture'},TERMS_VERSION='fixture',credits=lambda:self.credits,enqueue_owned_photo=self.queue,start_check=Mock(),LICENSE_URL='https://creativecommons.org/licenses/by/4.0/')
  source=Path(os.getenv('COMMUNITY_SHARE_ROUTE_SOURCE',str(ROOT/'app/routes/community_photos.py'))).read_text()
  tree=ast.parse(source);nodes=[x for x in tree.body if isinstance(x,ast.FunctionDef)and x.name in {'_shareable_photo','_has_shareable_photo','share'}]
  for node in nodes:node.decorator_list=[]
  self.ns=dict(Path=Path,current_app=current_app,service=service,_record=self.record,request=request,flash=flash,redirect=redirect,url_for=url_for,render_template=self.render)
  exec(compile(ast.Module(body=nodes,type_ignores=[]),'actual sharing functions','exec'),self.ns)
  self.app.add_url_rule('/share/<int:aircraft_id>',endpoint='community_photos.share',view_func=self.ns['share'],methods=['GET','POST'])
  self.app.add_url_rule('/aircraft/<int:aircraft_id>',endpoint='aircraft.aircraft_info',view_func=lambda aircraft_id:'aircraft')
  self.client=self.app.test_client();self.folder=folder
  Image.new('RGB',(100,100),'green').save(folder/'own.jpg')
  Image.new('RGB',(100,100),'blue').save(folder/'renamed.jpg',xmp=community_packet(identity('VH-TEST'),'Fixture photographer',service.LICENSE_URL,'a'*32))
 def test_pool_marker_hides_renamed_photo(self):
  with self.app.app_context():
   self.assertFalse(self.ns['_shareable_photo']('renamed.jpg'));self.assertTrue(self.ns['_shareable_photo']('own.jpg'))
   self.assertFalse(self.ns['_has_shareable_photo']({'carousel_images':[{'filename':'renamed.jpg'}]}))
   self.assertTrue(self.ns['_has_shareable_photo']({'carousel_images':[{'filename':'renamed.jpg'},{'filename':'own.jpg'}]}))
 def test_hash_bound_local_provenance(self):
  path=self.folder/'own.jpg';self.credits['own.jpg']={'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
  with self.app.app_context():
   self.assertFalse(self.ns['_shareable_photo']('own.jpg'))
   Image.new('RGB',(100,100),'red').save(path)
   self.assertTrue(self.ns['_shareable_photo']('own.jpg'))
 def test_pool_only_direct_page_redirects_without_form_or_submission(self):
  self.record.return_value=({'AircraftID':1},['renamed.jpg'])
  for response in (self.client.get('/share/1'),self.client.post('/share/1',data={'filename':'renamed.jpg','own_photo':'yes'})):
   self.assertEqual(response.status_code,302);self.assertTrue(response.location.endswith('/aircraft/1'))
  self.render.assert_not_called();self.queue.assert_not_called()
 def test_mixed_selector_and_forged_pool_post(self):
  self.record.return_value=({'AircraftID':1},['renamed.jpg','own.jpg'])
  self.assertEqual(self.client.get('/share/1').status_code,200)
  self.assertEqual(self.render.call_args.kwargs['filenames'],['own.jpg'])
  self.assertEqual(self.client.post('/share/1',data={'filename':'renamed.jpg','own_photo':'yes'}).status_code,302)
  self.queue.assert_not_called()
 def test_original_in_mixed_gallery_still_submits(self):
  self.record.return_value=({'AircraftID':1,'Registration':'VH-TEST','Aircraft_Type':'Test','MSN':'123'},['renamed.jpg','own.jpg'])
  self.assertEqual(self.client.post('/share/1',data={'filename':'own.jpg','own_photo':'yes'}).status_code,302)
  self.queue.assert_called_once()
  self.assertTrue(self.queue.call_args.kwargs['explicit'])
 def test_missing_traversal_and_symlink_not_shareable(self):
  (self.folder/'link.jpg').symlink_to(self.folder/'own.jpg')
  with self.app.app_context():
   for name in ('missing.jpg','../own.jpg','link.jpg',''):
    self.assertFalse(self.ns['_shareable_photo'](name))
if __name__=='__main__':unittest.main()
