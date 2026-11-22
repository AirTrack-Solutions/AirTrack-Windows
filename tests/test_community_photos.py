import importlib.util
import io
import json
from pathlib import Path
import tempfile
from types import ModuleType,SimpleNamespace
import unittest
from unittest.mock import patch,MagicMock
from PIL import Image
from flask import Flask
from sqlalchemy import create_engine,text

ROOT=Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0,str(ROOT/'app'))
spec=importlib.util.spec_from_file_location('community_fixture',ROOT/'app/utils/community_photo_client.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class ConsentTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.folder=Path(self.temp.name)
        p=patch.object(m,'root',return_value=self.folder/'private');p.start();self.addCleanup(p.stop)
        out=io.BytesIO();Image.new('RGB',(320,200),'blue').save(out,'JPEG');self.data=out.getvalue();self.photo=self.folder/'own.jpg';self.photo.write_bytes(self.data)
    def enable(self,**extra):
        return m.save_preferences(dict(enabled='yes',license_ack='yes',credit='Fixture Photographer',email='fixture@example.invalid',**extra))
    def test_optout_and_download_choice_need_no_contribution_consent(self):
        with patch.object(m.requests,'post',side_effect=AssertionError('Unexpected upload')):
            p=m.save_preferences({'enabled':'no','auto_download':'yes'});self.assertFalse(p['enabled']);self.assertFalse(p['auto_download'])
            self.assertFalse(m.enqueue_owned_photo(self.photo,'VH-ABC',explicit=True))
    def test_optin_requires_ack_and_manual_ownership_queue_is_not_auto(self):
        with self.assertRaises(ValueError):m.save_preferences({'enabled':'yes','credit':'Fixture','email':'fixture@example.invalid'})
        self.enable()
        self.assertFalse(m.enqueue_owned_photo(self.photo,'VH-ABC'))
        self.assertTrue(m.enqueue_owned_photo(self.photo,'VH-ABC',explicit=True))
        job=list((m.root()/'outgoing').glob('*.json'))[0]
        self.assertEqual(json.loads(job.read_text())['status'],'queued')
        m.save_preferences({'enabled':'no'})
        self.assertEqual(json.loads(job.read_text())['status'],'cancelled')
    def test_blocked_contributor_stops_retrying(self):
        self.enable();m.enqueue_owned_photo(self.photo,'VH-ABC',explicit=True)
        with patch.object(m,'access_status',return_value='blocked'),patch.object(m.requests,'post',side_effect=AssertionError('Blocked upload attempted')):m.process_outgoing()
        self.assertEqual(m.preferences()['access_status'],'blocked')
        with self.assertRaises(ValueError):m.enqueue_owned_photo(self.photo,'VH-DEF',explicit=True)
    def test_missing_only_download_preserves_existing_photo_and_credit(self):
        self.enable(auto_download='yes')
        static=self.folder/'static';images=static/'uploads/aircraft';images.mkdir(parents=True);(images/'own.jpg').write_bytes(b'keep my photo')
        engine=create_engine('sqlite://');self.addCleanup(engine.dispose)
        with engine.begin() as c:
            c.execute(text('CREATE TABLE aircraft (AircraftID INT,Registration TEXT,Aircraft_Image TEXT,MSN TEXT,Aircraft_Type TEXT,Aircraft_Updated TEXT)'))
            c.execute(text("INSERT INTO aircraft VALUES (1,'VH-ABC',NULL,'123','Model','keep timestamp'),(2,'VH-DEF','own.jpg','456','Other','keep timestamp')"))
            c.execute(text('ALTER TABLE aircraft ADD COLUMN ICAO_Address TEXT'))
        class Connection:
            def __init__(self,begin=False):self.context=engine.begin() if begin else engine.connect()
            def __enter__(self):self.c=self.context.__enter__();return self
            def __exit__(self,*args):return self.context.__exit__(*args)
            def execute(self,sql,*args):return self.c.execute(text(str(sql).replace(' FOR UPDATE','')),*args)
        fake=SimpleNamespace(connect=lambda:Connection(),begin=lambda:Connection(True));ext=ModuleType('extensions');ext.db=SimpleNamespace(engine=fake)
        photo=dict(access_grant='fixture-grant',id='a'*32,registration='VH-ABC',msn='123',aircraft_type='Model',license='CC BY 4.0',license_url=m.LICENSE_URL,photographer='Fixture',sha256=m.hashlib.sha256(self.data).hexdigest())
        api=MagicMock();api.json.return_value={'photos':[photo]};image=MagicMock();image.iter_content.return_value=[self.data]
        app=Flask(__name__,static_folder=str(static))
        with patch.dict('sys.modules',{'extensions':ext}),patch.object(m,'download_headers',return_value={'Authorization':'Bearer fixture-only'}),patch.object(m.requests,'get',side_effect=[api,image])as get:
            m.download_missing(app)
            self.assertTrue(all(c.kwargs['headers']['Authorization']=='Bearer fixture-only'for c in get.call_args_list))
            self.assertEqual(get.call_args_list[-1].kwargs['headers']['X-Photo-Grant'],'fixture-grant')
        self.assertEqual((images/'own.jpg').read_bytes(),b'keep my photo');self.assertEqual((images/('COMM_'+photo['id']+'.jpg')).read_bytes(),self.data)
        self.assertEqual(m.credits()['COMM_'+photo['id']+'.jpg']['photographer'],'Fixture')
        with engine.connect() as c:self.assertEqual(c.execute(text('SELECT Aircraft_Updated FROM aircraft WHERE AircraftID=1')).scalar(),'keep timestamp')

    def test_download_gate_fails_closed_and_optout_has_no_network(self):
        with patch.object(m.requests,'get',side_effect=AssertionError('Opt-out network')):
            self.assertIsNone(m.download_headers())
            m.download_missing(Flask(__name__))
        p=self.enable(auto_download='yes');p['token']='fixture-only'
        for allowed,expected in [(False,None),(True,{'Authorization':'Bearer fixture-only'})]:
            response=MagicMock();response.status_code=200;response.json.return_value={'status':'active','download_allowed':allowed}
            with patch.object(m.requests,'get',return_value=response):self.assertEqual(m.download_headers(p),expected)



    def test_aircraft_xmp_survives_sharing_queue(self):
        from utils.aircraft_photo_metadata import stamp_jpeg,identity,read_metadata
        stamp_jpeg(self.photo,identity('VH-ABC','00123','7c1234'))
        self.enable()
        self.assertTrue(m.enqueue_owned_photo(self.photo,'VH-ABC','Fixture Aircraft','00123',explicit=True))
        job=next((m.root()/'outgoing').glob('*.json'));receipt=json.loads(job.read_text())
        self.assertEqual(receipt['icao_hex'],'7C1234')
        self.assertEqual(read_metadata(job.with_suffix('.jpg')),identity('VH-ABC','00123','7C1234'))
