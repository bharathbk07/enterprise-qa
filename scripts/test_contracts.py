import json,tempfile,unittest
from pathlib import Path
from check_gate import evaluate
from install import plan

class ContractTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.write('application.json',{'application_id':'demo'})
        self.write('flows/index.json',{'flows':[{'id':'FLOW-001','number':1,'name':'Login','version':2}]})
        self.write('cases/index.json',{'cases':[{'case_id':n,'case_version':1,'flow_id':'FLOW-001','flow_version':2,'status':'active'} for n in ['CASE-001','CASE-002']]})
        (self.root/'evidence.txt').write_text('observed result')
    def tearDown(self):self.temp.cleanup()
    def write(self,name,data):
        p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data))
    def case(self,id='CASE-001',version=2,status='passed',kind='manual-browser',evidence='evidence.txt'):
        return {'case_id':id,'case_version':1,'flow_id':'FLOW-001','flow_version':version,'execution_kind':kind,'attempts':[{'status':status,'started_at':'2026-10-14T12:00:00Z','ended_at':'2026-10-14T12:01:00Z','evidence':[evidence]}]}
    def write_run(self,cases,name='one'):
        self.write('runs/'+name+'.json',{'schema_version':'1.0','application_id':'demo','run_id':name,'environment':'test','cases':cases})
    def test_duplicate_case_and_old_flow_do_not_satisfy_gate(self):
        self.write_run([self.case(),self.case(),self.case('CASE-002',version=1)])
        out=evaluate(self.root,['Login']);self.assertFalse(out['eligible']);self.assertEqual(out['flows'][0]['count'],1)
    def test_two_distinct_cases_include_failed_manual_case(self):
        self.write_run([self.case(),self.case('CASE-002',status='failed')]);self.assertTrue(evaluate(self.root,['1'])['eligible'])
    def test_blocked_automated_and_missing_evidence_do_not_count(self):
        self.write_run([self.case(status='blocked'),self.case('CASE-002',kind='automated'),self.case(evidence='missing.txt')]);self.assertEqual(evaluate(self.root,['FLOW-001'])['flows'][0]['count'],0)
    def test_all_native_runner_kinds_are_excluded_from_manual_gate(self):
        for kind in ('automated-unit','automated-component','automated-contract','automated-integration','automated-e2e'):
            self.write_run([self.case(kind=kind),self.case('CASE-002',kind=kind)])
            result=evaluate(self.root,['Login']);self.assertFalse(result['eligible']);self.assertEqual(result['flows'][0]['count'],0)

    def test_version_scoped_explicit_override(self):
        self.write('overrides.json',{'overrides':[{'flow_id':'FLOW-001','flow_version':1,'scope':'automation','explicit':True,'authorized_by':'user','reason':'requested','authorized_at':'2026-10-14T12:00:00Z'}]});self.assertFalse(evaluate(self.root,['Login'])['eligible'])
        data=json.loads((self.root/'overrides.json').read_text());data['overrides'][0]['flow_version']=2;self.write('overrides.json',data);self.assertTrue(evaluate(self.root,['Login'])['eligible'])
    def test_ambiguous_and_unknown_flow_stop_selection(self):
        with self.assertRaises(ValueError):evaluate(self.root,['missing'])
        self.write('flows/index.json',{'flows':[{'id':'FLOW-001','number':1,'name':'Login','version':2},{'id':'FLOW-002','number':2,'name':'Login','version':1}]})
        with self.assertRaises(ValueError):evaluate(self.root,['Login'])
    def test_updated_case_version_invalidates_execution(self):
        self.write_run([self.case(),self.case('CASE-002')]);data=json.loads((self.root/'cases/index.json').read_text());data['cases'][1]['case_version']=2;self.write('cases/index.json',data);self.assertFalse(evaluate(self.root,['Login'])['eligible'])

class InstallTests(unittest.TestCase):
    def test_install_plan_detects_overwrites_without_mutating(self):
        source=Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as d:
            ws=Path(d);mapping,conflicts=plan(source,ws,['cursor']);self.assertFalse(conflicts);self.assertFalse((ws/'.cursor').exists());self.assertTrue(any(p.name=='qa-browser.md' for p in mapping))
            p=ws/'.cursor/agents/qa-browser.md';p.parent.mkdir(parents=True);p.write_text('user customizations');_,conflicts=plan(source,ws,['cursor']);self.assertIn(str(p.resolve()),conflicts);self.assertEqual(p.read_text(),'user customizations')
    def test_workspace_escape_symlink_rejected(self):
        source=Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as d,tempfile.TemporaryDirectory() as outside:
            ws=Path(d);(ws/'.qa-agent').symlink_to(outside,target_is_directory=True)
            with self.assertRaises(ValueError):plan(source,ws,['cursor'])

class CleanupTests(unittest.TestCase):
    def test_cleanup_preview_and_confirm_preserve_other_records(self):
        import subprocess
        source=Path(__file__).resolve().parents[1];cli=source/'recorder/dist/src/cli.js'
        if not cli.exists(): self.skipTest('Build recorder before CLI integration checks.')
        with tempfile.TemporaryDirectory() as d:
            ws=Path(d);app=ws/'qa/demo';record=app/'recordings/REC-fixture';record.mkdir(parents=True)
            (record/'session.json').write_text(json.dumps({'application_id':'demo','recording_id':'REC-fixture','ended_at':'2026-10-15T00:00:00Z'}))
            (app/'knowledge.md').write_text('canonical knowledge')
            cmd=['node',str(cli),'cleanup','--workspace',str(ws),'--app','demo','--recordings','REC-fixture']
            preview=subprocess.run(cmd,capture_output=True,text=True);self.assertEqual(preview.returncode,0,preview.stderr);self.assertTrue(record.exists())
            deleted=subprocess.run(cmd+['--confirm'],capture_output=True,text=True);self.assertEqual(deleted.returncode,0,deleted.stderr);self.assertFalse(record.exists());self.assertTrue((app/'knowledge.md').exists())
    def test_cleanup_rejects_profile_owner_with_retained_dependent(self):
        import subprocess
        source=Path(__file__).resolve().parents[1];cli=source/'recorder/dist/src/cli.js'
        if not cli.exists(): self.skipTest('Build recorder before CLI integration checks.')
        with tempfile.TemporaryDirectory() as d:
            ws=Path(d);root=ws/'qa/demo/recordings'
            for id,owner in [('REC-owner','REC-owner'),('REC-dependent','REC-owner')]:
                record=root/id;record.mkdir(parents=True);(record/'session.json').write_text(json.dumps({'application_id':'demo','recording_id':id,'profile_owner_recording':owner,'ended_at':'2026-10-15T00:00:00Z'}))
            cmd=['node',str(cli),'cleanup','--workspace',str(ws),'--app','demo','--recordings','REC-owner','--confirm']
            result=subprocess.run(cmd,capture_output=True,text=True);self.assertNotEqual(result.returncode,0);self.assertTrue((root/'REC-owner').exists())

class StrictGateTests(unittest.TestCase):
    setUp=ContractTests.setUp
    tearDown=ContractTests.tearDown
    write=ContractTests.write
    case=ContractTests.case
    write_run=ContractTests.write_run
    def test_duplicate_index_fails_closed(self):
        p=self.root/'cases/index.json';data=json.loads(p.read_text());data['cases'].append(data['cases'][0]);self.write('cases/index.json',data)
        with self.assertRaises(ValueError):evaluate(self.root,['Login'])
    def test_boolean_version_does_not_count(self):
        case=self.case();case['case_version']=True;self.write_run([case,self.case('CASE-002')]);self.assertFalse(evaluate(self.root,['Login'])['eligible'])
    def test_run_symlink_escape_rejected(self):
        with tempfile.TemporaryDirectory() as outside:
            file=Path(outside)/'run.json';file.write_text('{}');(self.root/'runs').mkdir();(self.root/'runs/escape.json').symlink_to(file)
            with self.assertRaises(ValueError):evaluate(self.root,['Login'])

class ActiveCleanupTests(unittest.TestCase):
    def test_confirmed_cleanup_refuses_live_recorder_process(self):
        import os,subprocess
        cli=Path(__file__).resolve().parents[1]/'recorder/dist/src/cli.js'
        if not cli.exists():self.skipTest('Build recorder first.')
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=root/'qa/demo/recordings/REC-active';p.mkdir(parents=True);(p/'session.json').write_text(json.dumps({'application_id':'demo','recording_id':'REC-active','process_id':os.getpid()}))
            result=subprocess.run(['node',str(cli),'cleanup','--workspace',str(root),'--app','demo','--recordings','REC-active','--confirm'],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0);self.assertTrue(p.exists());self.assertIn('active recording',result.stderr)
