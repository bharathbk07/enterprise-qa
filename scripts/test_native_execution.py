import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from native_run_checks import check_native, KINDS


class NativeExecutionTests(unittest.TestCase):
    def record(self):
        return {'schema_version': '1.0', 'application_id': 'fixture', 'environment': 'fixture',
                'run_id': 'NATIVE-fixture', 'revision': 'fixture-revision', 'runner': 'unittest',
                'working_directory': '.', 'command': [sys.executable, '-m', 'unittest', 'selected_test'],
                'execution_kind': 'automated-unit', 'started_at': '2026-10-17T00:00:00Z',
                'ended_at': '2026-10-17T00:00:01Z', 'runner_exit_code': 0, 'status': 'passed',
                'report_references': ['native-runs/assets/source.log'], 'limitations': [],
                'tests': [{'test_id': 'fixture.Test.test_selected', 'status': 'passed', 'attempts': [
                    {'status': 'passed', 'evidence_references': ['native-runs/assets/source.log']}]}]}

    def test_each_native_kind_works_without_manual_flow_identity(self):
        for kind in KINDS:
            record = self.record(); record['execution_kind'] = kind
            result = check_native(record)
            self.assertTrue(result['valid']); self.assertFalse(result['manual_gate_eligible'])

    def test_zero_exit_does_not_pass_empty_or_blocked_collection(self):
        record = self.record(); record['tests'] = []; record['limitations'] = ['No selected tests collected.']
        self.assertFalse(check_native(record)['valid'])
        record['status'] = 'not-executed'; self.assertTrue(check_native(record)['valid'])
        record = self.record(); record['tests'][0].update(status='blocked', attempts=[])
        self.assertFalse(check_native(record)['valid'])

    def test_failed_then_passed_retry_preserves_failure(self):
        record = self.record(); test = record['tests'][0]; test['status'] = 'failed'
        test['attempts'].insert(0, {'status': 'failed', 'evidence_references': ['native-runs/assets/first.log']})
        self.assertFalse(check_native(record)['valid'])
        record['status'] = 'failed'; self.assertTrue(check_native(record)['valid'])
        test['status'] = 'passed'; self.assertFalse(check_native(record)['valid'])

    def test_exit_code_duplicate_and_malformed_records(self):
        record = self.record(); record['runner_exit_code'] = 1; self.assertFalse(check_native(record)['valid'])
        record = self.record(); record['tests'].append(copy.deepcopy(record['tests'][0])); self.assertFalse(check_native(record)['valid'])
        for value in (None, [], 'output'):
            self.assertFalse(check_native(value)['valid'])
        record = self.record(); record['runner_exit_code'] = True; self.assertFalse(check_native(record)['valid'])

    def test_real_selected_unittest_command_without_flow_index_and_evidence_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / 'selected_test.py').write_text('import unittest\nclass Test(unittest.TestCase):\n def test_selected(self): self.assertEqual(2 + 2, 4)\n')
            result = subprocess.run([sys.executable, '-m', 'unittest', '-v', 'selected_test'], cwd=root, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0); self.assertIn('Ran 1 test', result.stderr)
            record = self.record(); record['runner_exit_code'] = result.returncode
            record['command'] = [sys.executable, '-m', 'unittest', '-v', 'selected_test']
            record['tests'][0]['test_id'] = 'selected_test.Test.test_selected'
            self.assertIn(record['tests'][0]['test_id'], result.stderr)
            evidence = root / record['report_references'][0]; evidence.parent.mkdir(parents=True); evidence.write_text(result.stdout + result.stderr)
            self.assertFalse((root / 'flows/index.json').exists())
            self.assertTrue(check_native(record, root)['valid'])
            record['report_references'] = ['../outside.log']; self.assertFalse(check_native(record, root)['valid'])
