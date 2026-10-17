#!/usr/bin/env python3
"""Validate local evidence envelopes and suggest bounded next steps; no product calls."""
import argparse
import json
import math
from pathlib import Path
from engineering_checks import instant

PROVIDERS = {'splunk', 'dynatrace', 'appdynamics', 'datadog', 'neoload', 'jmeter'}
STATUSES = {'ok', 'denied', 'auth-expired', 'rate-limited', 'timeout', 'unavailable', 'unknown-outcome'}


def assess(record):
    errors = []
    if not isinstance(record, dict):
        return {'valid': False, 'errors': ['Evidence must be an object.'], 'next_step': 'repair-envelope', 'retry_candidate': False, 'evidence_use': 'insufficient'}
    for key in ('application_id', 'environment', 'source_reference', 'query_reference'):
        if not isinstance(record.get(key), str) or not record[key].strip():
            errors.append(f'Missing {key}.')
    for key, choices in (
        ('provider', PROVIDERS), ('channel', {'mcp', 'api', 'export', 'user-paste'}),
        ('operation', {'read', 'launch', 'write'}), ('status', STATUSES),
    ):
        if not isinstance(record.get(key), str) or record[key] not in choices:
            errors.append(f'Invalid {key}.')
    start, end = instant(record.get('start_utc')), instant(record.get('end_utc'))
    if not start or not end or end <= start:
        errors.append('Positive timezone-aware event window required.')
    if not instant(record.get('collected_at')):
        errors.append('Timezone-aware collected_at required.')
    for key in ('redaction_reviewed', 'complete', 'truncated'):
        if type(record.get(key)) is not bool:
            errors.append(f'{key} must be boolean.')
    if record.get('redaction_reviewed') is not True:
        errors.append('Review redaction before accepting saved evidence.')
    count = record.get('row_count')
    if type(count) is not int or count < 0:
        errors.append('row_count must be a nonnegative integer.')
    next_page = record.get('next_page')
    if next_page is not None and (not isinstance(next_page, str) or not next_page.strip()):
        errors.append('next_page must be a nonempty string or null.')
    limitations = record.get('limitations')
    if not isinstance(limitations, list) or any(not isinstance(x, str) or not x.strip() for x in limitations):
        errors.append('limitations must be an array of nonempty strings.')
    partial = record.get('truncated') is True or next_page is not None or record.get('complete') is not True
    if record.get('complete') is True and (record.get('truncated') is True or next_page is not None or record.get('status') != 'ok'):
        errors.append('Complete evidence conflicts with failure/truncation/pagination.')
    if partial and not limitations:
        errors.append('Incomplete evidence needs explicit limitations.')
    for key in ('remaining_calls',):
        if key in record and (type(record[key]) is not int or record[key] < 0):
            errors.append(f'{key} must be a nonnegative integer.')
    for key in ('retry_after_seconds', 'remaining_seconds'):
        value = record.get(key)
        if key in record and (type(value) not in (int, float) or not math.isfinite(value) or value < 0):
            errors.append(f'{key} must be finite and nonnegative.')
    step, use, retry = 'repair-envelope', 'insufficient', False
    if not errors:
        status, operation = record['status'], record['operation']
        if status != 'ok' and operation != 'read':
            step = 'reconcile-existing-operation-before-any-retry'
        elif status == 'denied':
            step = 'stop-denied-path-no-permission-bypass'
        elif status == 'auth-expired':
            step = 'repair-approved-auth-or-use-permitted-export'
        elif status in ('rate-limited', 'timeout'):
            delay = record.get('retry_after_seconds') if status == 'rate-limited' else record.get('retry_after_seconds', 0)
            retry = (delay is not None and record.get('remaining_calls', 0) > 0
                     and record.get('remaining_seconds', 0) > delay)
            step = 'bounded-read-retry-within-existing-scope' if retry else 'report-limit-and-offer-permitted-fallback'
        elif status in ('unavailable', 'unknown-outcome'):
            step = 'offer-permitted-api-export-then-user-query'
        elif partial:
            step, use = 'retain-partial-request-only-missing-critical-slice', 'partial-observations-only'
        elif count == 0:
            step, use = 'report-no-matches-check-scope-without-expansion', 'no-matches-for-query-only'
        else:
            step, use = 'analyze-with-source-limitations', 'scoped-observations-only'
    return {'valid': not errors, 'errors': errors, 'next_step': step, 'retry_candidate': retry,
            'evidence_use': use, 'provenance': 'user-supplied' if record.get('channel') == 'user-paste' else record.get('channel'),
            'scope': 'Structural checks and suggestions only; no access grant, product calls, redaction guarantee or causal attestation.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record', required=True)
    args = parser.parse_args()
    try:
        result = assess(json.loads(Path(args.record).read_text()))
    except (OSError, ValueError, TypeError):
        result = {'valid': False, 'errors': ['Cannot read a valid evidence JSON record.']}
    print(json.dumps(result, indent=2))
    return 0 if result['valid'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
