#!/usr/bin/env python3
"""Dry-run by default. Install allowlisted owned files; optionally initialize official Playwright agents through a protected staging step."""
import argparse,hashlib,json,subprocess
from safe_install import snapshot, apply_checked
from pathlib import Path
PLATFORMS=('cursor','claude-code','vscode-copilot','codex','antigravity','chatgpt-portable')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def owned(source):
    manifest=json.loads((source/'distribution.json').read_text());files=[]
    for entry in manifest['files']:
        p=source/entry['path']
        if Path(entry['path']).is_absolute() or not p.resolve().is_relative_to(source):raise ValueError('Unsafe distribution source.')
        if not p.is_file() or sha(p)!=entry['sha256']:raise ValueError(f'Distribution file changed; review then run sync_package.py: {entry["path"]}')
        files.append(p)
    return files+[source/'distribution.json']
class InstallPlan(dict):
    pass

def plan(source,workspace,platforms,update_managed=False):
    source,workspace=Path(source).resolve(),Path(workspace).resolve()
    if workspace.is_relative_to(source):raise ValueError('Install workspace cannot be the source or nested inside it.')
    mapping=InstallPlan({workspace/'.qa-agent'/p.relative_to(source):p for p in owned(source)})
    roots={'cursor':'.cursor/skills','claude-code':'.claude/skills','vscode-copilot':'.agents/skills','codex':'.agents/skills','antigravity':'.agents/skills'}
    declared=set(owned(source))
    for platform in platforms:
        if platform in roots:
            for p in declared:
                if p.is_relative_to(source/'skills'):mapping[workspace/roots[platform]/p.relative_to(source/'skills')]=p
        if platform in ('cursor','claude-code','vscode-copilot'):
            target={'cursor':'.cursor/agents','claude-code':'.claude/agents','vscode-copilot':'.github/agents'}[platform]
            for p in declared:
                if p.is_relative_to(source/'adapters'/platform/'agents'):mapping[workspace/target/p.name]=p
    receipt=workspace/'.qa-agent/.install-state.json'
    if not receipt.resolve().is_relative_to(workspace):raise ValueError('Install receipt escapes workspace.')
    receipt_state=snapshot(workspace,receipt)
    receipt_document=json.loads(receipt.read_text()) if receipt.is_file() else {'files':{}}
    if not isinstance(receipt_document,dict) or not isinstance(receipt_document.get('files'),dict):raise ValueError('Invalid installation ownership receipt.')
    previous=receipt_document['files']
    conflicts=[];expected={}
    for dest,src in mapping.items():
        state=snapshot(workspace,dest)
        expected[dest]=state
        if state['kind']=='file':
            existing=state['sha256']
            if existing!=sha(src) and not (update_managed and previous.get(str(dest.relative_to(workspace)))==existing):conflicts.append(str(dest))
    mapping.expected=expected
    mapping.sources={src:sha(src) for src in set(mapping.values())}
    mapping.receipt=receipt
    mapping.receipt_state=receipt_state
    mapping.previous=dict(previous)
    mapping.conflicts=list(conflicts)
    return mapping,conflicts

def apply(mapping,workspace):
    workspace=Path(workspace).resolve()
    if not isinstance(mapping,InstallPlan):raise ValueError('Apply requires the original inspected install plan.')
    if mapping.conflicts:raise ValueError('Install conflicts require review before apply.')
    writes={};files=dict(mapping.previous)
    for dest,src in mapping.items():
        data=src.read_bytes()
        checksum=hashlib.sha256(data).hexdigest()
        if checksum!=mapping.sources.get(src):raise ValueError(f'Install source changed after preflight: {src}')
        writes[dest]=data
        files[str(dest.relative_to(workspace))]=checksum
    writes[mapping.receipt]=(json.dumps({'schema_version':'1.0','files':files},indent=2)+'\n').encode()
    expected={**mapping.expected,mapping.receipt:mapping.receipt_state}
    apply_checked(workspace,writes,expected)

def main():
    p=argparse.ArgumentParser();p.add_argument('--workspace',required=True);p.add_argument('--platforms',default='all');p.add_argument('--apply',action='store_true');p.add_argument('--update-managed',action='store_true');p.add_argument('--playwright-loop',choices=['vscode','claude','codex']);p.add_argument('--playwright-cli');p.add_argument('--playwright-reference-only',action='store_true');a=p.parse_args()
    platforms=list(PLATFORMS) if a.platforms=='all' else [s.strip() for s in a.platforms.split(',')]
    if any(x not in PLATFORMS for x in platforms):p.error('Unknown platform.')
    source=Path(__file__).resolve().parents[1];workspace=Path(a.workspace).resolve()
    try:mapping,conflicts=plan(source,workspace,platforms,a.update_managed)
    except (OSError,ValueError,TypeError,KeyError,subprocess.TimeoutExpired) as e:p.error(str(e))
    prepared=None
    if a.playwright_loop:
        try:
            from setup_playwright_agents import prepare
            prepared=prepare(workspace,a.playwright_loop,a.playwright_cli,a.playwright_reference_only,a.update_managed)
            conflicts.extend(prepared['summary']['conflicts'])
        except (OSError,ValueError,TypeError,KeyError,subprocess.TimeoutExpired) as e:p.error(str(e))
    official=prepared['summary'] if prepared else {'required_during_setup':True,'status':'pending','next_step':'Run setup_playwright_agents.py with the chosen loop, or supply --playwright-loop after approving its preview.'}
    print(json.dumps({'workspace':str(workspace),'platforms':platforms,'files':len(mapping),'conflicts':conflicts,'apply_requested':a.apply,'managed_update':a.update_managed,'dependency_installation':False,'active_mcp_settings_planned':bool(prepared and not a.playwright_reference_only),'official_playwright_agents':official,'destinations':[str(x.relative_to(workspace)) for x in mapping]},indent=2))
    if conflicts:return 2
    if a.apply:
        try:
            if prepared:
                from safe_install import verify_expected
                verify_expected(workspace,prepared['expected'])
            apply(mapping,workspace)
            if prepared:
                from setup_playwright_agents import apply_prepared
                apply_prepared(prepared)
        except (OSError,ValueError,TypeError,KeyError) as e:p.error(str(e))
    return 0
if __name__=='__main__':raise SystemExit(main())
