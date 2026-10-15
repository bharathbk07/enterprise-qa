#!/usr/bin/env python3
"""Dry-run by default. Install allowlisted owned files; never merge active MCP settings."""
import argparse,hashlib,json,shutil
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
def plan(source,workspace,platforms,update_managed=False):
    source,workspace=Path(source).resolve(),Path(workspace).resolve()
    if workspace.is_relative_to(source):raise ValueError('Install workspace cannot be the source or nested inside it.')
    mapping={workspace/'.qa-agent'/p.relative_to(source):p for p in owned(source)}
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
    previous=json.loads(receipt.read_text()).get('files',{}) if receipt.is_file() else {}
    conflicts=[]
    for dest,src in mapping.items():
        if not dest.resolve().is_relative_to(workspace):raise ValueError(f'Symlink/path escapes workspace: {dest}')
        if dest.exists():
            if not dest.is_file():conflicts.append(str(dest));continue
            existing=sha(dest)
            if existing!=sha(src) and not (update_managed and previous.get(str(dest.relative_to(workspace)))==existing):conflicts.append(str(dest))
    return mapping,conflicts

def apply(mapping,workspace):
    workspace=Path(workspace).resolve();files={}
    for dest,src in mapping.items():
        if not dest.resolve().is_relative_to(workspace):raise ValueError('Destination changed during installation.')
        dest.parent.mkdir(parents=True,exist_ok=True)
        if src.resolve()!=dest.resolve():shutil.copy2(src,dest)
        files[str(dest.relative_to(workspace))]=sha(dest)
    receipt=workspace/'.qa-agent/.install-state.json'
    previous=json.loads(receipt.read_text()).get('files',{}) if receipt.exists() else {}
    previous.update(files);receipt.write_text(json.dumps({'schema_version':'1.0','files':previous},indent=2)+'\n')
    # Deliberately no stale-file deletion, global installation or active settings edits.
def main():
    p=argparse.ArgumentParser();p.add_argument('--workspace',required=True);p.add_argument('--platforms',default='all');p.add_argument('--apply',action='store_true');p.add_argument('--update-managed',action='store_true');a=p.parse_args()
    platforms=list(PLATFORMS) if a.platforms=='all' else [s.strip() for s in a.platforms.split(',')]
    if any(x not in PLATFORMS for x in platforms):p.error('Unknown platform.')
    source=Path(__file__).resolve().parents[1];workspace=Path(a.workspace).resolve()
    try:mapping,conflicts=plan(source,workspace,platforms,a.update_managed)
    except (OSError,ValueError,TypeError,KeyError) as e:p.error(str(e))
    print(json.dumps({'workspace':str(workspace),'platforms':platforms,'files':len(mapping),'conflicts':conflicts,'apply_requested':a.apply,'managed_update':a.update_managed,'dependency_installation':False,'active_mcp_settings_changed':False,'destinations':[str(x.relative_to(workspace)) for x in mapping]},indent=2))
    if conflicts:return 2
    if a.apply:apply(mapping,workspace)
    return 0
if __name__=='__main__':raise SystemExit(main())
