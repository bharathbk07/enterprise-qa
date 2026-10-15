#!/usr/bin/env python3
"""Verify the current-version manual execution prerequisite; never grant overrides."""
import argparse, json
from pathlib import Path
from datetime import datetime

def load(path, default=None):
    if not path.exists() and default is not None: return default
    return json.loads(path.read_text())

def timestamp(value):
    try:
        result=datetime.fromisoformat(value.replace('Z','+00:00'))
        return result if result.tzinfo is not None else None
    except (ValueError, AttributeError, TypeError): return None

def evaluate(root, selectors):
    root=Path(root).resolve()
    def local(path,default=None):
        if not path.resolve().is_relative_to(root):raise ValueError('Evidence record escapes application root.')
        return load(path,default)
    app=local(root/'application.json')['application_id']
    flows=local(root/'flows/index.json')['flows']
    current={}
    for c in local(root/'cases/index.json')['cases']:
        if c.get('status')!='active':continue
        if any(type(c.get(k)) is not int or c[k]<=0 for k in ('flow_version','case_version')):raise ValueError('Invalid current case/flow version.')
        key=(c['flow_id'],c['flow_version'],c['case_id'])
        if key in current:raise ValueError('Duplicate current case index entry.')
        current[key]=c['case_version']
    chosen=[]
    for selector in selectors:
        matches=[f for f in flows if selector.casefold() in {str(f['id']).casefold(),str(f['number']).casefold(),f['name'].casefold()}]
        if len(matches)!=1: raise ValueError(f'Unknown or ambiguous flow selector: {selector}')
        if matches[0] not in chosen: chosen.append(matches[0])
    runs=[local(p) for p in (root/'runs').glob('*.json')]
    overrides=local(root/'overrides.json',{'overrides':[]})['overrides']
    results=[]
    for flow in chosen:
        executed=set();evidence=[]
        for run in runs:
            if run.get('application_id')!=app or run.get('schema_version')!='1.0': continue
            for case in run.get('cases',[]):
                if case.get('flow_id')!=flow['id'] or case.get('flow_version')!=flow['version'] or case.get('execution_kind') not in ('manual-browser','manual-api'): continue
                if any(type(case.get(k)) is not int or case[k]<=0 for k in ('flow_version','case_version')):continue
                key=(case['flow_id'],case['flow_version'],case.get('case_id'))
                if key not in current or current[key]!=case.get('case_version'): continue
                attempts=case.get('attempts',[])
                if not attempts: continue
                first=attempts[0]
                begin,end=timestamp(first.get('started_at')),timestamp(first.get('ended_at'))
                if first.get('status') not in ('passed','failed') or not begin or not end or end<begin: continue
                paths=[]
                for item in first.get('evidence',[]):
                    if not isinstance(item,str): continue
                    p=(root/item).resolve()
                    if p.is_relative_to(root) and p.is_file() and p.stat().st_size>0: paths.append(str(p.relative_to(root)))
                if not paths: continue
                executed.add(case['case_id']);evidence.extend(paths)
        approved=[o for o in overrides if o.get('flow_id')==flow['id'] and o.get('flow_version')==flow['version'] and o.get('scope')=='automation' and o.get('explicit') is True and o.get('authorized_by') and o.get('reason') and timestamp(o.get('authorized_at'))]
        results.append({'flow_id':flow['id'],'flow_version':flow['version'],'distinct_executed_cases':sorted(executed),'count':len(executed),'evidence':sorted(set(evidence)),'override':bool(approved),'eligible':len(executed)>=2 or bool(approved)})
    return {'application_id':app,'eligible':bool(results) and all(r['eligible'] for r in results),'flows':results,'attestation':'Local evidence checks; not a signed approval or enforcement hook.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--application-root',required=True);p.add_argument('--flows',required=True);a=p.parse_args()
    try: result=evaluate(a.application_root,[s.strip() for s in a.flows.split(',') if s.strip()]);print(json.dumps(result,indent=2));return 0 if result['eligible'] else 2
    except (ValueError,KeyError,OSError,TypeError) as e: print(json.dumps({'eligible':False,'error':str(e)}));return 2
if __name__=='__main__': raise SystemExit(main())
