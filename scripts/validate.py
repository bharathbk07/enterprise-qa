#!/usr/bin/env python3
"""Dependency-free emitted-format integrity checks; not native client acceptance."""
import hashlib,json,re,tomllib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def header(path,name):
    text=path.read_text();assert text.startswith('---\n') and len(text.splitlines())<500
    front=text.split('---',2)[1];assert re.search(r'^name: '+re.escape(name)+r'$',front,re.M)
    desc=json.loads(re.search(r'^description: (.+)$',front,re.M)[1]);assert isinstance(desc,str) and 0<len(desc)<=1024 and '<' not in desc and '>' not in desc
    assert len(name)<=64 and re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',name)
    assert not re.search(r'^\[TODO:',text,re.M)
    return text
catalog=json.loads((ROOT/'skill-definition.json').read_text());manifest=json.loads((ROOT/'agent-manifest.json').read_text())
skills={s['id']:s for s in catalog['skills']};agents={a['id']:a for a in manifest['agents']}
assert len(skills)==len(catalog['skills']) and len(agents)==len(manifest['agents']) and len(skills)==len(agents)
assert catalog['entrypoint'] in skills and manifest['entrypoint'] in agents
contract=(ROOT/'contracts/CONTRACT.md').read_text()
for name,skill in skills.items():
    p=ROOT/skill['path'];text=header(p,name);assert (p.parent/'references/CONTRACT.md').read_text()==contract
    for link in re.findall(r'`(references/[^`]+)`',text):assert (p.parent/link).exists(),link
for name,agent in agents.items():
    assert agent['skill'] in skills;header(ROOT/agent['prompt'],name)
    for platform,location,extension in [('cursor','.cursor/skills','.md'),('claude-code','.claude/skills','.md'),('vscode-copilot','.agents/skills','.agent.md')]:
        path=ROOT/'adapters'/platform/'agents'/(name+extension);text=header(path,name);assert f'{location}/{agent["skill"]}/SKILL.md' in text
for path in ROOT.rglob('*.json'):
    if any(x in path.parts for x in ('node_modules','.npm-cache','dist','__pycache__')):continue
    json.loads(path.read_text())
for platform,key in [('cursor','mcpServers'),('claude-code','mcpServers'),('vscode-copilot','servers')]:
    document=json.loads((ROOT/f'integrations/templates/{platform}.mcp.example.json').read_text());assert set(document[key])=={'splunk','dynatrace','neoload','atlassian'}
    assert all(v['url'].startswith('https://') for v in document[key].values())
    assert 'NODE_TLS_REJECT_UNAUTHORIZED' not in json.dumps(document)
tomllib.loads((ROOT/'integrations/templates/codex.config.example.toml').read_text())
owned=json.loads((ROOT/'distribution.json').read_text())['files'];assert len({x['path'] for x in owned})==len(owned)
for entry in owned:
    path=ROOT/entry['path'];assert path.resolve().is_relative_to(ROOT) and path.is_file();assert hashlib.sha256(path.read_bytes()).hexdigest()==entry['sha256'],entry['path']
print(f'Validated {len(skills)} skills, {len(agents)} roles, native adapters, template formats and {len(owned)} owned source checksums. No live connection implied.')
