import copy,json,tempfile,unittest,hashlib
from pathlib import Path
from engineering_checks import check,digest,verify_artifacts
from install import plan,apply
from check_gate import evaluate

class EngineeringTests(unittest.TestCase):
    def rca(self):return {'investigation_id':'INC-1','application_id':'demo','environment':'prod','cause':'connection pool saturation','classification':'confirmed','mechanism_evidence':['experiment/1'],'evidence_matrix':{k:[k+'/1'] for k in ['logs','traces','metrics','code']},'cause_scores':{k:None for k in ['test-data','application-api-bug','automation-code','ui-locator-change','environment']},'missing_sources':[],'contradictions':[]}
    def test_confirmed_requires_all_four_sources_and_mechanism(self):
        record=self.rca();self.assertEqual(check('rca',record),[])
        for source in ['logs','traces','metrics','code']:
            partial=copy.deepcopy(record);partial['evidence_matrix'][source]=[];self.assertTrue(check('rca',partial))
        record['mechanism_evidence']=[];self.assertTrue(check('rca',record))
    def test_probable_can_preserve_missing_sources(self):
        record=self.rca();record['classification']='probable';record['evidence_matrix']['code']=[];record['missing_sources']=['code'];self.assertEqual(check('rca',record),[])
    def test_contradictions_and_invalid_scores_block_confirmation(self):
        record=self.rca();record['contradictions']=['counterexample'];self.assertTrue(check('rca',record));record=self.rca();record['cause_scores']['environment']=101;self.assertTrue(check('rca',record));record['cause_scores']['environment']=True;self.assertTrue(check('rca',record))
    def test_context_needs_environment_window_and_positive_budgets(self):
        record={'application_id':'demo','environment':'test','investigation_id':'RUN-1','start_utc':'2026-10-15T00:00:00Z','end_utc':'2026-10-15T00:05:00Z','query_budget':{'max_rows':100,'max_pages':2,'max_calls':4,'timeout_seconds':20}};self.assertEqual(check('context',record),[]);record['query_budget']['max_pages']=0;self.assertTrue(check('context',record));record['environment']='';self.assertTrue(check('context',record))
    def test_approval_binds_content_and_scope(self):
        proposal={'action':'apply-local-fix','target':'src/service.ts','environment':'test','patches':[{'path':'patch.diff','sha256':'placeholder-for-unit-test'}]}
        approval={'explicit':True,'authorized_by':'human','authorization_reference':'trusted-user-message-1','authorized_at':'2026-10-15T00:00:00Z','action':proposal['action'],'target':proposal['target'],'environment':'test','proposal_digest':digest(proposal)}
        self.assertEqual(check('approval',approval,proposal),[]);changed=copy.deepcopy(proposal);changed['target']='other.ts';self.assertTrue(check('approval',approval,changed));approval['explicit']=False;self.assertTrue(check('approval',approval,proposal))
    def test_profile_rejects_mismatched_load_units_and_missing_abort(self):
        p={'application_id':'demo','environment':'test','investigation_id':'RUN-1','start_utc':'2026-10-15T00:00:00Z','end_utc':'2026-10-15T00:05:00Z','tool':'neoload','target_ids':['scenario-1'],'workload_id':'WL-1','thresholds':[{'source':'SLO-1'}],'abort_conditions':['error budget exceeded'],'generator_limits':['CPU bound'],'monitoring_plan':['bounded queries'],'load':{'model':'open','value':10,'unit':'arrivals/s'},'duration_seconds':300}
        self.assertEqual(check('profile',p),[]);p['load']['unit']='concurrent-users';self.assertTrue(check('profile',p));p['abort_conditions']=[];self.assertTrue(check('profile',p))

class OwnedDistributionTests(unittest.TestCase):
    def manifest(self,source):
        p=source/'README.md';(source/'distribution.json').write_text(json.dumps({'files':[{'path':'README.md','sha256':hashlib.sha256(p.read_bytes()).hexdigest()}]}))
    def test_undeclared_secret_not_installed_and_nested_target_rejected(self):
        with tempfile.TemporaryDirectory() as d,tempfile.TemporaryDirectory() as w:
            source=Path(d);(source/'README.md').write_text('owned');(source/'.env').write_text('DUMMY_SECRET=not-real');self.manifest(source)
            mapping,_=plan(source,Path(w),['cursor']);self.assertFalse(any(p.name=='.env' for p in mapping));
            with self.assertRaises(ValueError):plan(source,source/'nested-target',['cursor'])
    def test_managed_update_preserves_user_edits(self):
        with tempfile.TemporaryDirectory() as d,tempfile.TemporaryDirectory() as w:
            source=Path(d);ws=Path(w);(source/'README.md').write_text('v1');self.manifest(source);mapping,_=plan(source,ws,['cursor']);apply(mapping,ws)
            (source/'README.md').write_text('v2');self.manifest(source);_,conflicts=plan(source,ws,['cursor']);self.assertTrue(conflicts);mapping,conflicts=plan(source,ws,['cursor'],True);self.assertFalse(conflicts);apply(mapping,ws);self.assertEqual((ws/'.qa-agent/README.md').read_text(),'v2')
            (ws/'.qa-agent/README.md').write_text('user edit');(source/'README.md').write_text('v3');self.manifest(source);_,conflicts=plan(source,ws,['cursor'],True);self.assertTrue(conflicts)
    def test_declared_source_escape_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            source=Path(d);(source/'distribution.json').write_text(json.dumps({'files':[{'path':'../outside.json','sha256':'invalid'}]}))
            with self.assertRaises(ValueError):plan(source,source.parent/'target',['cursor'])

class PatchBindingTests(unittest.TestCase):
    def test_changed_patch_bytes_invalidate_preflight(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=root/'fix.diff';p.write_text('approved patch');proposal={'patches':[{'path':'fix.diff','sha256':hashlib.sha256(p.read_bytes()).hexdigest()}]}
            self.assertEqual(verify_artifacts(proposal,root),[]);self.assertTrue(verify_artifacts(proposal,None));p.write_text('changed patch');self.assertTrue(verify_artifacts(proposal,root));proposal['patches'][0]['path']='../other';self.assertTrue(verify_artifacts(proposal,root))
