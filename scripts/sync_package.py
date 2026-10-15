#!/usr/bin/env python3
"""Synchronize generated references/adapters and an explicit distribution allowlist."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sync():
    catalog=json.loads((ROOT/'skill-definition.json').read_text());manifest=json.loads((ROOT/'agent-manifest.json').read_text())
    contract=(ROOT/'contracts/CONTRACT.md').read_text();engineering=(ROOT/'contracts/ENGINEERING.md').read_text()
    license_text=(ROOT/'LICENSE').read_text()
    (ROOT/'agents/LICENSE').write_text(license_text)
    for entry in catalog['skills']:
        base=(ROOT/entry['path']).parent
        (base/'references/CONTRACT.md').write_text(contract)
        (base/'LICENSE').write_text(license_text)
        if (base/'references/ENGINEERING.md').exists():(base/'references/ENGINEERING.md').write_text(engineering)
    for name in ('qa-rca','qa-fix-proposal','qa-fix-implementation'):
        (ROOT/f'skills/{name}/references/RECORDS.md').write_text((ROOT/'contracts/ENGINEERING-RECORDS.md').read_text())
    (ROOT/'skills/qa-recording/references/RECORDER.md').write_text((ROOT/'docs/RECORDER.md').read_text())
    (ROOT/'skills/qa-knowledge/references/FLOW-DOCUMENT.md').write_text((ROOT/'docs/FLOW-DOCUMENT.md').read_text())
    for name in ('qa-knowledge','qa-orchestrate'):
        (ROOT/f'skills/{name}/references/INTERACTION.md').write_text((ROOT/'docs/INTERACTION.md').read_text())
    (ROOT/'skills/qa-setup/references/INTEGRATIONS.md').write_text((ROOT/'integrations/SETUP.md').read_text())
    for platform,skillroot in [('cursor','.cursor/skills'),('claude-code','.claude/skills'),('vscode-copilot','.agents/skills')]:
        dest=ROOT/'adapters'/platform/'agents';dest.mkdir(parents=True,exist_ok=True)
        (dest/'LICENSE.enterprise-qa').write_text(license_text)
        for agent in manifest['agents']:
            extension='.agent.md' if platform=='vscode-copilot' else '.md'
            source=(ROOT/agent['prompt']).read_text()
            (dest/(agent['id']+extension)).write_text(source+f'\nWorkspace skill path: `{skillroot}/{agent["skill"]}/SKILL.md`. Package resources: `.qa-agent/`.\n')
    files={ROOT/p for p in ['README.md','LICENSE','CONTRIBUTING.md','SECURITY.md','SUPPORT.md','CODE_OF_CONDUCT.md','THIRD_PARTY_NOTICES.md','CHANGELOG.md','skill-definition.json','agent-manifest.json','verification.md','.gitignore']}
    for skill in catalog['skills']:
        base=(ROOT/skill['path']).parent;files.add(base/'SKILL.md');files.add(base/'LICENSE');files.update((base/'references').glob('*.md'))
    files.update(ROOT/a['prompt'] for a in manifest['agents'])
    files.add(ROOT/'agents/LICENSE')
    files.update((ROOT/'.github').glob('*.md'));files.update((ROOT/'.github/ISSUE_TEMPLATE').glob('*.yml'))
    for directory,patterns in [('contracts',['*.md','*.json']),('docs',['*.md','*.json','*.html','*.canvas.tsx']),('integrations',['*.md','*.json']),('integrations/templates',['*.json','*.toml'])]:
        for pattern in patterns:files.update((ROOT/directory).glob(pattern))
    for p in ['check_gate.py','engineering_checks.py','install.py','sync_package.py','validate.py','test_contracts.py','test_engineering.py']:
        path=ROOT/'scripts'/p
        if path.exists():files.add(path)
    for platform in ('codex','antigravity','chatgpt-portable'):files.add(ROOT/'adapters'/platform/'instructions.md')
    for platform in ('cursor','claude-code','vscode-copilot'):
        files.update((ROOT/'adapters'/platform/'agents').glob('*.md'));files.add(ROOT/'adapters'/platform/'agents/LICENSE.enterprise-qa')
    files.update(ROOT/'recorder'/p for p in ['package.json','package-lock.json','tsconfig.json'])
    files.update((ROOT/'recorder/src').glob('*.ts'));files.update((ROOT/'recorder/test').glob('*.ts'))
    records=[]
    for path in sorted(files):
        if not path.is_file() or not path.resolve().is_relative_to(ROOT):raise ValueError(f'Missing/escaping distribution file: {path}')
        records.append({'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    (ROOT/'distribution.json').write_text(json.dumps({'schema_version':'1.0','package_version':catalog['package_version'],'files':records},indent=2)+'\n')
    return len(records)
if __name__=='__main__':print(f'Synchronized {sync()} owned source/configuration files.')
