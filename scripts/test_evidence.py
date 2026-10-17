"""Synthetic normalized connector responses; not live server integration tests."""
import copy
import unittest
from evidence_checks import assess, PROVIDERS
from engineering_checks import check, digest


class EvidenceTests(unittest.TestCase):
    def record(self):
        return {'provider': 'splunk', 'channel': 'mcp', 'operation': 'read', 'status': 'ok',
                'application_id': 'synthetic-app', 'environment': 'fixture', 'source_reference': 'fixture:source',
                'query_reference': 'fixture:query', 'start_utc': '2026-10-17T00:00:00Z',
                'end_utc': '2026-10-17T00:05:00Z', 'collected_at': '2026-10-17T00:06:00Z',
                'redaction_reviewed': True, 'complete': True, 'row_count': 3,
                'truncated': False, 'next_page': None, 'limitations': []}

    def failure(self, status):
        record = self.record()
        record.update(status=status, complete=False, row_count=0, limitations=['Synthetic connector response unavailable.'])
        return record

    def test_scoped_observations_for_all_six_products(self):
        for provider in PROVIDERS:
            record = self.record(); record['provider'] = provider
            result = assess(record)
            self.assertTrue(result['valid']); self.assertEqual(result['evidence_use'], 'scoped-observations-only')

    def test_pasted_data_never_claims_direct_tool_execution(self):
        record = self.record(); record['channel'] = 'user-paste'
        self.assertEqual(assess(record)['provenance'], 'user-supplied')

    def test_denial_and_expiry_do_not_retry(self):
        for status in ('denied', 'auth-expired'):
            record = self.failure(status); record.update(remaining_calls=10, remaining_seconds=60)
            result = assess(record)
            self.assertTrue(result['valid']); self.assertFalse(result['retry_candidate'])
            self.assertEqual(result['evidence_use'], 'insufficient')

    def test_throttle_honors_retry_after_and_remaining_budget(self):
        record = self.failure('rate-limited'); record.update(retry_after_seconds=10, remaining_calls=2, remaining_seconds=11)
        self.assertTrue(assess(record)['retry_candidate'])
        record['remaining_seconds'] = 10; self.assertFalse(assess(record)['retry_candidate'])
        record['remaining_seconds'] = 60; record['remaining_calls'] = 0; self.assertFalse(assess(record)['retry_candidate'])
        record['remaining_calls'] = 2; del record['retry_after_seconds']; self.assertFalse(assess(record)['retry_candidate'])

    def test_uncertain_launch_and_write_require_reconciliation(self):
        for operation in ('launch', 'write'):
            for status in ('timeout', 'unknown-outcome', 'rate-limited'):
                record = self.failure(status); record.update(operation=operation, remaining_calls=5, remaining_seconds=60, retry_after_seconds=1)
                result = assess(record)
                self.assertFalse(result['retry_candidate']); self.assertEqual(result['next_step'], 'reconcile-existing-operation-before-any-retry')

    def test_partial_and_page_limited_results_preserve_uncertainty(self):
        record = self.record(); record.update(complete=False, truncated=True, next_page='fixture:continuation', limitations=['Row budget reached.'])
        result = assess(record); self.assertTrue(result['valid']); self.assertEqual(result['evidence_use'], 'partial-observations-only')
        record['complete'] = True; self.assertFalse(assess(record)['valid'])

    def test_zero_rows_are_no_matches_not_healthy_result(self):
        record = self.record(); record['row_count'] = 0
        self.assertEqual(assess(record)['evidence_use'], 'no-matches-for-query-only')

    def test_failed_connection_and_missing_provenance_are_not_success(self):
        result = assess(self.failure('unavailable'))
        self.assertEqual(result['next_step'], 'offer-permitted-api-export-then-user-query')
        record = self.record(); del record['query_reference']; self.assertFalse(assess(record)['valid'])
        record = self.record(); record['redaction_reviewed'] = False; self.assertFalse(assess(record)['valid'])

    def test_malformed_values_fail_cleanly(self):
        for value in (None, [], True, 'raw output'):
            self.assertFalse(assess(value)['valid'])
        for key, value in [('status', []), ('row_count', True), ('remaining_calls', True), ('remaining_seconds', float('inf')), ('retry_after_seconds', -1), ('limitations', 'unknown'), ('collected_at', 'unknown'), ('next_page', 1)]:
            record = self.record(); record[key] = value; self.assertFalse(assess(record)['valid'], key)


class ReadinessTests(unittest.TestCase):
    def profile(self):
        return {'application_id': 'fixture', 'environment': 'fixture', 'investigation_id': 'SYNTHETIC',
                'start_utc': '2026-10-17T00:00:00Z', 'end_utc': '2026-10-17T00:05:00Z',
                'tool': 'jmeter', 'target_ids': ['fixture:plan'], 'workload_id': 'fixture:workload',
                'thresholds': [{'metric': 'p95', 'unit': 'ms', 'operator': '<', 'value': 500, 'source': 'fixture:slo'}],
                'abort_conditions': ['fixture:error-budget'], 'generator_limits': ['fixture:cpu'], 'monitoring_plan': ['fixture:metrics'],
                'load': {'model': 'closed', 'value': 1, 'unit': 'concurrent-users'}, 'duration_seconds': 300}

    def readiness(self, profile):
        return {'profile_digest': digest(profile), 'controls': [
            {'criterion': key, 'mechanism': 'external', 'implementation_reference': 'fixture:config',
             'verification_reference': 'fixture:verification', 'verified_at': '2026-10-17T00:00:00Z'}
            for key in ('thresholds:0', 'abort_conditions:0')]}

    def test_profile_binding_and_missing_or_duplicate_controls(self):
        profile = self.profile(); record = self.readiness(profile)
        self.assertEqual(check('readiness', record, profile), [])
        changed = copy.deepcopy(profile); changed['duration_seconds'] = 600
        self.assertTrue(check('readiness', record, changed))
        record['controls'].pop(); self.assertTrue(check('readiness', record, profile))
        record = self.readiness(profile); record['controls'].append(record['controls'][0]); self.assertTrue(check('readiness', record, profile))

    def test_manual_controls_require_owner_cadence_and_actual_approval_reference(self):
        profile = self.profile(); record = self.readiness(profile); control = record['controls'][1]; control['mechanism'] = 'manual'
        self.assertTrue(check('readiness', record, profile))
        control.update(owner='fixture-operator', observation_interval_seconds=5, explicit_manual_approval_reference='fixture:user-approval')
        self.assertEqual(check('readiness', record, profile), [])
        control['observation_interval_seconds'] = True; self.assertTrue(check('readiness', record, profile))

    def test_unverified_or_malformed_controls_fail_without_execution(self):
        profile = self.profile(); record = self.readiness(profile)
        record['controls'][0]['verification_reference'] = ''; self.assertTrue(check('readiness', record, profile))
        record = self.readiness(profile); record['controls'] = [None]; self.assertTrue(check('readiness', record, profile))
        self.assertTrue(check('readiness', record, None))
