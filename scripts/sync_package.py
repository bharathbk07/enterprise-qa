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
    mode_refs={'qa-recording':['RECORDING.md','BROWSER.md'],'qa-playwright':['BROWSER.md'],'qa-knowledge':['FLOWS.md'],'qa-test-design':['FLOWS.md'],'qa-test-execution':['FLOWS.md','BROWSER.md','AUTOMATION.md','NATIVE-EXECUTION.md'],'qa-automation':['AUTOMATION.md'],'qa-fix-implementation':['AUTOMATION.md'],'qa-setup':['SETUP.md'],'qa-analysis':['NATIVE-EXECUTION.md'],'qa-architect':['ARCHITECTURE-RECORDS.md'],'qa-reporting':['ARCHITECTURE-RECORDS.md']}
    for name,refs in mode_refs.items():
        for reference in refs:(ROOT/f'skills/{name}/references/{reference}').write_text((ROOT/'contracts'/reference).read_text())
    for name in ('qa-knowledge','qa-architect','qa-engineering','qa-orchestrate'):
        (ROOT/f'skills/{name}/references/KNOWLEDGE.md').write_text((ROOT/'contracts/KNOWLEDGE.md').read_text())
    for name in ('qa-rca','qa-fix-proposal','qa-fix-implementation','qa-jmeter','qa-performance','qa-performance-engineering'):
        (ROOT/f'skills/{name}/references/RECORDS.md').write_text((ROOT/'contracts/ENGINEERING-RECORDS.md').read_text())
    architecture=(ROOT/'contracts/ARCHITECTURE.md').read_text()
    for name in ('qa-architect','qa-stack-discovery','qa-functional-architecture','qa-security','qa-accessibility','qa-resilience','qa-data-quality','qa-solution-architecture','qa-reporting'):
        (ROOT/f'skills/{name}/references/ARCHITECTURE.md').write_text(architecture)
    for name,doc in [('qa-security','SECURITY-QUALITY.md'),('qa-accessibility','ACCESSIBILITY-QUALITY.md'),('qa-resilience','RESILIENCE-QUALITY.md'),('qa-data-quality','DATA-QUALITY.md')]:
        target={'qa-security':'SECURITY.md','qa-accessibility':'ACCESSIBILITY.md','qa-resilience':'RESILIENCE.md','qa-data-quality':'DATA.md'}[name]
        (ROOT/f'skills/{name}/references/{target}').write_text((ROOT/'docs'/doc).read_text())
    evidence=(ROOT/'contracts/EVIDENCE.md').read_text()
    for name in ('qa-mcp-splunk','qa-mcp-dynatrace','qa-mcp-appdynamics','qa-mcp-datadog','qa-mcp-neoload','qa-jmeter','qa-setup','qa-engineering','qa-performance','qa-performance-engineering','qa-telemetry-correlation','qa-analysis'):
        (ROOT/f'skills/{name}/references/EVIDENCE.md').write_text(evidence)
    for product in ('splunk','dynatrace','appdynamics','datadog','neoload'):
        (ROOT/f'skills/qa-mcp-{product}/references/CONNECTOR.md').write_text((ROOT/f'integrations/{product.upper()}.md').read_text())
    (ROOT/'skills/qa-jmeter/references/JMETER.md').write_text((ROOT/'docs/JMETER.md').read_text())
    (ROOT/'skills/qa-recording/references/RECORDER.md').write_text((ROOT/'docs/RECORDER.md').read_text())
    (ROOT/'skills/qa-knowledge/references/FLOW-DOCUMENT.md').write_text((ROOT/'docs/FLOW-DOCUMENT.md').read_text())
    for name in ('qa-knowledge','qa-orchestrate'):
        (ROOT/f'skills/{name}/references/INTERACTION.md').write_text((ROOT/'docs/INTERACTION.md').read_text())
    setup=(ROOT/'integrations/SETUP.md').read_text().replace('../docs/JMETER.md','JMETER.md').replace('../contracts/EVIDENCE.md','EVIDENCE.md')
    (ROOT/'skills/qa-setup/references/INTEGRATIONS.md').write_text(setup)
    for product in ('SPLUNK','DYNATRACE','APPDYNAMICS','DATADOG','NEOLOAD'):
        (ROOT/f'skills/qa-setup/references/{product}.md').write_text((ROOT/f'integrations/{product}.md').read_text())
    (ROOT/'skills/qa-setup/references/JMETER.md').write_text((ROOT/'docs/JMETER.md').read_text())
    for name in ('qa-setup','qa-playwright','qa-automation'):
        (ROOT/f'skills/{name}/references/PLAYWRIGHT-AGENTS.md').write_text((ROOT/'docs/PLAYWRIGHT-AGENTS.md').read_text())
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
    for p in ['check_gate.py','engineering_checks.py','install.py','sync_package.py','validate.py','test_contracts.py','test_engineering.py','setup_playwright_agents.py','test_playwright_agents.py','evidence_checks.py','test_evidence.py','architecture_checks.py','test_architecture.py','safe_install.py','test_install_safety.py','native_run_checks.py','test_native_execution.py']:
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
