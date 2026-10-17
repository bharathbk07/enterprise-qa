#!/usr/bin/env python3
"""Validate native-run result records without requiring manual flows or running commands."""
import argparse
import json
from pathlib import Path
from engineering_checks import instant

KINDS = {'automated-unit', 'automated-component', 'automated-contract', 'automated-integration', 'automated-e2e'}
OUTCOMES = ('passed', 'failed', 'blocked', 'not-executed')


def check_native(record, application_root=None):
    errors, counts = [], dict.fromkeys(OUTCOMES, 0)
    if not isinstance(record, dict):
        return {'valid': False, 'errors': ['Native run must be an object.'], 'counts': counts}
    root = Path(application_root).resolve() if application_root else None
    def refs(value):
        if not isinstance(value, list) or any(not isinstance(x, str) or not x.strip() for x in value):
            return False
        if root:
            for item in value:
                path = (root / item).resolve()
                if Path(item).is_absolute() or not path.is_relative_to(root) or not path.is_file() or path.stat().st_size == 0:
                    return False
        return True
    for key in ('application_id', 'environment', 'run_id', 'revision', 'working_directory', 'runner'):
        if not isinstance(record.get(key), str) or not record[key].strip(): errors.append(f'Missing {key}.')
    if record.get('schema_version') != '1.0': errors.append('Unsupported native run schema.')
    if not isinstance(record.get('execution_kind'), str) or record['execution_kind'] not in KINDS:
        errors.append('Native run requires an automated execution kind.')
    command = record.get('command')
    if not isinstance(command, list) or not command or any(not isinstance(x, str) or not x.strip() for x in command):
        errors.append('Record the selected runner command as nonempty argv, with no secret values.')
    begin, end = instant(record.get('started_at')), instant(record.get('ended_at'))
    if not begin or not end or end < begin: errors.append('Timezone-aware ordered run timestamps required.')
    status, exit_code = record.get('status'), record.get('runner_exit_code')
    if status not in OUTCOMES: errors.append('Invalid run status.')
    if exit_code is not None and type(exit_code) is not int: errors.append('runner_exit_code must be an integer or null.')
    if status in ('passed', 'failed') and type(exit_code) is not int: errors.append('Executed run needs the actual exit code.')
    if not refs(record.get('report_references')) or (status in ('passed', 'failed') and not record['report_references']):
        errors.append('Executed run needs usable source report references.')
    limitations = record.get('limitations')
    if not isinstance(limitations, list) or any(not isinstance(x, str) or not x.strip() for x in limitations):
        errors.append('limitations must be an array of strings.')
    tests = record.get('tests')
    if not isinstance(tests, list): errors.append('tests must be an array.'); tests = []
    seen = set()
    for test in tests:
        if not isinstance(test, dict) or not isinstance(test.get('test_id'), str) or not test['test_id'].strip():
            errors.append('Native test needs a stable runner test_id.'); continue
        ident = test['test_id']
        if ident in seen: errors.append('Duplicate native test ID.')
        seen.add(ident)
        outcome = test.get('status')
        if outcome not in OUTCOMES: errors.append(f'{ident}: invalid status.'); continue
        counts[outcome] += 1
        attempts = test.get('attempts')
        if not isinstance(attempts, list): errors.append(f'{ident}: attempts must be an array.'); continue
        if outcome in ('passed', 'failed'):
            if not attempts or not isinstance(attempts[0], dict) or attempts[0].get('status') != outcome:
                errors.append(f'{ident}: preserve the first attempt outcome.')
        for attempt in attempts:
            if not isinstance(attempt, dict) or attempt.get('status') not in OUTCOMES or not refs(attempt.get('evidence_references')):
                errors.append(f'{ident}: invalid attempt evidence.'); continue
            if attempt['status'] in ('passed', 'failed') and not attempt['evidence_references']:
                errors.append(f'{ident}: missing executed attempt evidence.')
    if status == 'passed' and (exit_code != 0 or not tests or counts['passed'] != len(tests)):
        errors.append('Passed native run requires selected tests, zero exit and every first outcome passed.')
    if counts['failed'] and status != 'failed': errors.append('Original failures cannot be converted to a passed or blocked run.')
    if not tests and not limitations: errors.append('Empty test collection needs an explicit limitation.')
    return {'valid': not errors, 'errors': errors, 'counts': counts, 'manual_gate_eligible': False,
            'scope': 'Native result structure only; no execution, approval grant, evidence attestation or manual-flow eligibility.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record', required=True)
    parser.add_argument('--application-root')
    args = parser.parse_args()
    try: result = check_native(json.loads(Path(args.record).read_text()), args.application_root)
    except (OSError, ValueError, TypeError): result = {'valid': False, 'errors': ['Cannot read a valid native run record.']}
    print(json.dumps(result, indent=2))
    return 0 if result['valid'] else 2


if __name__ == '__main__': raise SystemExit(main())
