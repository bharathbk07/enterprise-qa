"""Synthetic quality-plan consistency cases, not application quality assessments."""
import copy
import unittest
from architecture_checks import check_plan, DOMAINS


class ArchitectureTests(unittest.TestCase):
    def plan(self):
        return {'application_id': 'fixture', 'environment': 'fixture', 'assessment_id': 'SYNTHETIC',
                'revision': 'fixture-revision', 'requested_outcome': 'fixture:verify-behavior',
                'strategy': 'compatible', 'strategy_reference': 'fixture:user-choice',
                'domains': {d: {'status': 'selected' if d == 'functional-correctness' else 'excluded',
                                'rationale': 'Synthetic selected scope.'} for d in DOMAINS},
                'requirements': [{'id': 'REQ-1', 'domain': 'functional-correctness', 'source_reference': 'fixture:rule',
                                  'acceptance': 'Fixture request preserves the test invariant.', 'components': ['fixture:api'],
                                  'verification_method': 'fixture:assertion', 'outcome': 'passed', 'evidence_references': ['fixture:result']}],
                'findings': [], 'solutions': []}

    def with_solution(self):
        plan = self.plan()
        plan['findings'] = [{'id': 'BUG-1', 'requirement_ids': ['REQ-1'], 'domain': 'functional-correctness',
                             'status': 'resolved', 'evidence_references': ['fixture:repro', 'fixture:regression']}]
        plan['solutions'] = [{'id': 'SOL-1', 'finding_ids': ['BUG-1'], 'status': 'validated',
                              'rationale': 'Addresses fixture mechanism.', 'tradeoffs': 'Fixture local compatibility change.',
                              'acceptance': 'Fixture invariant holds.', 'validation_requirement_ids': ['REQ-1'],
                              'evidence_references': ['fixture:validation'], 'rollback_reference': 'fixture:rollback'}]
        return plan

    def test_complete_record_is_not_a_certification(self):
        result = check_plan(self.plan())
        self.assertTrue(result['valid']); self.assertEqual(result['recorded_summary'], 'recorded-checks-complete')
        self.assertEqual(result['recorded_counts']['executed'], 1)

    def test_unexecuted_or_unknown_acceptance_cannot_be_passed(self):
        for key, value in [('acceptance', ''), ('evidence_references', [])]:
            plan = self.plan(); plan['requirements'][0][key] = value
            self.assertFalse(check_plan(plan)['valid'])
        plan = self.plan(); plan['requirements'][0].update(outcome='not-executed', acceptance='', evidence_references=[])
        result = check_plan(plan); self.assertTrue(result['valid']); self.assertEqual(result['recorded_summary'], 'incomplete')

    def test_all_domains_need_explicit_disposition(self):
        plan = self.plan(); del plan['domains']['security']; self.assertFalse(check_plan(plan)['valid'])
        plan = self.plan(); plan['domains']['security']['status'] = 'selected'
        result = check_plan(plan); self.assertTrue(result['valid']); self.assertEqual(result['recorded_summary'], 'incomplete')

    def test_duplicate_ids_and_wrong_scope_are_rejected(self):
        plan = self.plan(); plan['requirements'].append(copy.deepcopy(plan['requirements'][0]))
        self.assertFalse(check_plan(plan)['valid'])
        plan = self.plan(); plan['requirements'][0]['domain'] = 'security'; self.assertFalse(check_plan(plan)['valid'])

    def test_solution_validation_requires_passed_checks_and_evidence(self):
        plan = self.with_solution(); self.assertTrue(check_plan(plan)['valid'])
        for outcome in ('failed', 'blocked', 'not-executed'):
            changed = copy.deepcopy(plan); changed['requirements'][0]['outcome'] = outcome
            self.assertFalse(check_plan(changed)['valid'])
        plan['solutions'][0]['evidence_references'] = []; self.assertFalse(check_plan(plan)['valid'])

    def test_solution_linkage_and_recovery_remain_explicit(self):
        plan = self.with_solution(); plan['solutions'][0]['finding_ids'] = ['UNKNOWN']; self.assertFalse(check_plan(plan)['valid'])
        plan = self.with_solution(); plan['solutions'][0]['rollback_reference'] = ''; self.assertFalse(check_plan(plan)['valid'])
        plan = self.with_solution(); plan['solutions'][0]['status'] = 'proposed'
        result = check_plan(plan); self.assertTrue(result['valid']); self.assertEqual(result['recorded_summary'], 'incomplete')

    def test_requirements_gaps_and_undecided_strategy_remain_visible(self):
        plan = self.plan(); plan.update(strategy='undecided', strategy_reference='')
        plan['findings'] = [{'id': 'GAP-1', 'requirement_ids': [], 'requirements_gap': True,
                             'domain': 'functional-correctness', 'status': 'suspected', 'evidence_references': []}]
        result = check_plan(plan); self.assertTrue(result['valid']); self.assertEqual(result['recorded_summary'], 'incomplete')
        plan['findings'][0]['status'] = 'resolved'; self.assertFalse(check_plan(plan)['valid'])

    def test_malformed_records_fail_cleanly(self):
        for value in (None, [], True, 'raw text'):
            self.assertFalse(check_plan(value)['valid'])
        for key, value in [('requirements', [None]), ('domains', []), ('findings', 'raw'), ('solutions', [True])]:
            plan = self.plan(); plan[key] = value; self.assertFalse(check_plan(plan)['valid'])
        plan = self.plan(); plan['requirements'][0]['domain'] = []; self.assertFalse(check_plan(plan)['valid'])

    def test_failed_requirement_does_not_become_a_complete_clean_assessment(self):
        plan = self.plan(); plan['requirements'][0]['outcome'] = 'failed'
        result = check_plan(plan); self.assertTrue(result['valid']); self.assertEqual(result['recorded_summary'], 'open-findings')

    def test_unrelated_passing_requirement_cannot_validate_an_unfixed_source(self):
        plan = self.with_solution()
        original = plan['requirements'][0]; original['outcome'] = 'failed'
        unrelated = copy.deepcopy(original); unrelated.update(id='REQ-UNRELATED', outcome='passed')
        plan['requirements'].append(unrelated); plan['findings'][0]['status'] = 'reproduced'
        plan['solutions'][0]['validation_requirement_ids'] = ['REQ-UNRELATED']
        self.assertFalse(check_plan(plan)['valid'])
        original['outcome'] = 'passed'
        self.assertFalse(check_plan(plan)['valid'], 'Passing the source check does not remove the missing linkage.')
        plan['solutions'][0]['validation_requirement_ids'].append('REQ-1')
        self.assertTrue(check_plan(plan)['valid'])

    def test_validated_solution_must_cover_all_linked_findings(self):
        plan = self.with_solution()
        second = copy.deepcopy(plan['requirements'][0]); second['id'] = 'REQ-2'
        plan['requirements'].append(second)
        plan['findings'][0]['requirement_ids'].append('REQ-2')
        self.assertFalse(check_plan(plan)['valid'])
        plan['solutions'][0]['validation_requirement_ids'].append('REQ-2')
        self.assertTrue(check_plan(plan)['valid'])
