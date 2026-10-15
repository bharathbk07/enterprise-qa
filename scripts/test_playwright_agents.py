import json,subprocess,sys,tempfile,tomllib,unittest
from pathlib import Path
from setup_playwright_agents import prepare,apply_prepared
ROOT=Path(__file__).resolve().parents[1]
CLI=ROOT/'recorder/node_modules/playwright/cli.js'

@unittest.skipUnless(CLI.is_file(),'Prepare recorder npm dependencies to test official CLI generation offline.')
class OfficialAgentTests(unittest.TestCase):
    def test_all_documented_local_loops_generate_parseable_agents_without_app_scaffold(self):
        for loop in ('vscode','claude','codex'):
            with self.subTest(loop=loop),tempfile.TemporaryDirectory() as directory:
                workspace=Path(directory).resolve();prepared=prepare(workspace,loop,CLI)
                self.assertFalse(any(workspace.iterdir()),'preview must not write target files')
                self.assertFalse(prepared['summary']['conflicts']);self.assertEqual(prepared['summary']['official_agents'],['planner','generator','healer'])
                apply_prepared(prepared)
                agents=[p for p in prepared['writes'] if p.suffix in ('.md','.toml')];self.assertEqual(len(agents),3)
                for agent in agents:
                    text=agent.read_text();self.assertIn('Enterprise QA execution boundary',text)
                    if loop=='codex':
                        spec=tomllib.loads(text);self.assertIn('two distinct current-version',spec['developer_instructions']);self.assertIn(str(CLI.resolve()),spec['mcp_servers']['playwright-test']['args'])
                self.assertTrue(any(p.name=='LICENSE.playwright-test-agents' and p.is_file() for p in prepared['writes']))
                self.assertFalse((workspace/'tests').exists());self.assertFalse((workspace/'specs').exists());self.assertFalse((workspace/'.github/workflows').exists())
    def test_existing_mcp_servers_and_unrelated_fields_are_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace=Path(directory).resolve();original={'mcpServers':{'company-service':{'url':'https://fixture.invalid/mcp'}},'other-setting':{'kept':True}}
            (workspace/'.mcp.json').write_text(json.dumps(original));prepared=prepare(workspace,'claude',CLI);apply_prepared(prepared)
            actual=json.loads((workspace/'.mcp.json').read_text());self.assertEqual(actual['mcpServers']['company-service'],original['mcpServers']['company-service']);self.assertEqual(actual['other-setting'],original['other-setting']);self.assertIn(str(CLI.resolve()),actual['mcpServers']['playwright-test']['args'])
    def test_existing_playwright_server_conflict_writes_nothing(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace=Path(directory).resolve();original={'mcpServers':{'playwright-test':{'command':'custom-runner'}}};path=workspace/'.mcp.json';path.write_text(json.dumps(original));prepared=prepare(workspace,'claude',CLI)
            self.assertTrue(prepared['summary']['conflicts'])
            with self.assertRaises(ValueError):apply_prepared(prepared)
            self.assertEqual(json.loads(path.read_text()),original);self.assertFalse((workspace/'.claude').exists())
    def test_user_edited_agents_are_not_overwritten_by_managed_refresh(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace=Path(directory).resolve();apply_prepared(prepare(workspace,'claude',CLI));agent=workspace/'.claude/agents/playwright-test-planner.md';agent.write_text(agent.read_text()+'\nuser customization\n');prepared=prepare(workspace,'claude',CLI,update_managed=True);self.assertIn(str(agent),prepared['summary']['conflicts'])
    def test_reference_only_does_not_activate_native_agents_or_mcp(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace=Path(directory).resolve();prepared=prepare(workspace,'claude',CLI,reference_only=True);apply_prepared(prepared)
            self.assertTrue((workspace/'.qa-agent/vendor/playwright/claude/.claude/agents/playwright-test-healer.md').is_file());self.assertFalse((workspace/'.claude').exists());self.assertFalse((workspace/'.mcp.json').exists())
    def test_settings_path_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory,tempfile.TemporaryDirectory() as outside:
            workspace=Path(directory).resolve();(workspace/'.qa-agent').symlink_to(outside,target_is_directory=True)
            with self.assertRaises(ValueError):prepare(workspace,'claude',CLI)
    def test_missing_local_cli_fails_without_npx_download(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError,'Local Playwright CLI missing'):prepare(directory,'claude')

    def test_combined_install_applies_toolkit_and_official_agents(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace=Path(directory).resolve()
            result=subprocess.run([sys.executable,str(ROOT/'scripts/install.py'),'--workspace',str(workspace),'--platforms','claude-code','--playwright-loop','claude','--playwright-cli',str(CLI),'--apply'],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertTrue((workspace/'.qa-agent/contracts/CONTRACT.md').is_file())
            self.assertTrue((workspace/'.claude/agents/qa-setup.md').is_file())
            self.assertTrue((workspace/'.claude/agents/playwright-test-planner.md').is_file())
            self.assertIn('playwright-test',json.loads((workspace/'.mcp.json').read_text())['mcpServers'])
            self.assertFalse((workspace/'.github/workflows').exists())
            self.assertFalse((workspace/'tests').exists())
    def test_combined_install_conflict_prevents_both_stages(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace=Path(directory).resolve()
            original={'mcpServers':{'playwright-test':{'command':'custom-runner'}}}
            (workspace/'.mcp.json').write_text(json.dumps(original))
            result=subprocess.run([sys.executable,str(ROOT/'scripts/install.py'),'--workspace',str(workspace),'--platforms','claude-code','--playwright-loop','claude','--playwright-cli',str(CLI),'--apply'],capture_output=True,text=True)
            self.assertEqual(result.returncode,2,result.stderr)
            self.assertFalse((workspace/'.qa-agent').exists())
            self.assertFalse((workspace/'.claude').exists())
            self.assertEqual(json.loads((workspace/'.mcp.json').read_text()),original)
