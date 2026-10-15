#!/usr/bin/env python3
"""Local structural preflight. This cannot attest truth or grant user authorization."""
import argparse, hashlib, json, math
from datetime import datetime

def instant(value):
    if not isinstance(value,str):return None
    try:
        result=datetime.fromisoformat(value.replace('Z','+00:00'))
        return result if result.tzinfo is not None else None
    except ValueError:return None

def digest(proposal):
    return hashlib.sha256(json.dumps(proposal,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()

def positive(value):return type(value) in (int,float) and math.isfinite(value) and value>0

def check(kind,record,proposal=None):
    errors=[]
    if not isinstance(record,dict):return ['Record must be an object.']
    def require(keys):
        for key in keys:
            if record.get(key) in (None,'',[],{}):errors.append(f'Missing {key}.')
    if kind in ('context','profile'):
        require(['application_id','environment','investigation_id','start_utc','end_utc'])
        start,end=instant(record.get('start_utc')),instant(record.get('end_utc'))
        if not start or not end or end<=start:errors.append('A positive timezone-aware time window is required.')
    if kind=='context':
        budget=record.get('query_budget',{})
        for field in ('max_rows','max_pages','max_calls','timeout_seconds'):
            value=budget.get(field) if isinstance(budget,dict) else None
            if type(value) is not int or value<=0:errors.append(f'query_budget.{field} must be a positive integer.')
    elif kind=='profile':
        require(['tool','target_ids','workload_id','thresholds','abort_conditions','generator_limits','monitoring_plan'])
        if record.get('tool') not in ('k6','jmeter','neoload'):errors.append('Unsupported performance tool.')
        load=record.get('load',{})
        if not isinstance(load,dict) or load.get('model') not in ('open','closed') or not positive(load.get('value')):errors.append('Load model/value required.')
        elif load.get('unit') not in (('arrivals/s','requests/s','transactions/s') if load['model']=='open' else ('concurrent-users',)):errors.append('Load unit does not match the model.')
        if not positive(record.get('duration_seconds')):errors.append('Positive duration_seconds required.')
    elif kind=='rca':
        require(['investigation_id','application_id','environment','cause','classification','evidence_matrix','cause_scores'])
        if record.get('classification') not in ('suspected','probable','confirmed'):errors.append('Invalid cause classification.')
        if record.get('classification')=='confirmed':
            mechanism=record.get('mechanism_evidence')
            if not isinstance(mechanism,list) or not mechanism or any(not isinstance(x,str) or not x.strip() for x in mechanism):errors.append('Confirmed requires mechanism evidence references.')
            matrix=record.get('evidence_matrix',{})
            for source in ('logs','traces','metrics','code'):
                evidence=matrix.get(source) if isinstance(matrix,dict) else None
                if not isinstance(evidence,list) or not evidence or any(not isinstance(x,str) or not x.strip() for x in evidence):errors.append(f'Confirmed requires {source} evidence references.')
            if record.get('contradictions') or record.get('missing_sources'):errors.append('Confirmed cannot have unresolved contradictions/missing sources.')
        scores=record.get('cause_scores',{})
        for source in ('test-data','application-api-bug','automation-code','ui-locator-change','environment'):
            value=scores.get(source,'absent') if isinstance(scores,dict) else 'absent'
            if value is not None and (type(value) not in (int,float) or not math.isfinite(value) or not 0<=value<=100):errors.append(f'Invalid score for {source}.')
    elif kind=='approval':
        require(['explicit','authorized_by','authorization_reference','authorized_at','action','target','environment','proposal_digest'])
        if record.get('explicit') is not True:errors.append('Explicit approval required.')
        if not instant(record.get('authorized_at')):errors.append('Timezone-aware approval timestamp required.')
        if not isinstance(proposal,dict):errors.append('Original proposal required to bind approval.')
        else:
            if record.get('proposal_digest')!=digest(proposal):errors.append('Proposal changed or digest mismatch.')
            for key in ('action','target','environment'):
                if record.get(key)!=proposal.get(key):errors.append(f'Approval scope mismatch: {key}.')
    elif kind not in ('context','profile'):errors.append('Unknown check kind.')
    return errors

def verify_artifacts(proposal,artifact_root):
    from pathlib import Path
    errors=[]
    if not isinstance(proposal,dict):return ['Original proposal required.']
    patches=proposal.get('patches',[])
    if not patches:return errors
    if not artifact_root:return ['Proposal uses patch files: provide --artifact-root to verify their content.']
    root=Path(artifact_root).resolve()
    for patch in patches:
        if not isinstance(patch,dict) or not isinstance(patch.get('path'),str):errors.append('Invalid patch file reference.');continue
        path=(root/patch['path']).resolve()
        if Path(patch['path']).is_absolute() or not path.is_relative_to(root) or not path.is_file():errors.append('Patch path missing or outside artifact root.');continue
        actual=hashlib.sha256(path.read_bytes()).hexdigest()
        if actual!=patch.get('sha256'):errors.append(f'Patch content changed: {patch["path"]}.')
    return errors

def main():
    p=argparse.ArgumentParser();p.add_argument('--kind',choices=['context','profile','rca','approval'],required=True);p.add_argument('--record',required=True);p.add_argument('--proposal');p.add_argument('--artifact-root');a=p.parse_args()
    try:
        from pathlib import Path
        record=json.loads(Path(a.record).read_text());proposal=json.loads(Path(a.proposal).read_text()) if a.proposal else None
        errors=check(a.kind,record,proposal)
        if a.kind=='approval':errors.extend(verify_artifacts(proposal,a.artifact_root))
    except (OSError,ValueError,TypeError) as e:errors=[str(e)]
    print(json.dumps({'valid':not errors,'errors':errors,'scope':'Structural checks only; no causal attestation or authorization grant.'},indent=2));return 2 if errors else 0
if __name__=='__main__':raise SystemExit(main())
