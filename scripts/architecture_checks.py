#!/usr/bin/env python3
"""Check local quality-plan consistency; not runtime evidence or enterprise certification."""
import argparse
import json
from pathlib import Path

DOMAINS = {
    'functional-correctness', 'performance', 'security', 'accessibility',
    'data-integrity', 'resilience-recoverability', 'maintainability-operability',
}


def check_plan(record):
    errors, warnings = [], []

    def text(value):
        return isinstance(value, str) and bool(value.strip())

    def references(value):
        return isinstance(value, list) and all(text(item) for item in value)

    if not isinstance(record, dict):
        return {'valid': False, 'errors': ['Quality plan must be an object.'], 'warnings': [], 'recorded_summary': 'incomplete'}
    for key in ('application_id', 'environment', 'assessment_id', 'revision', 'requested_outcome'):
        if not text(record.get(key)):
            errors.append(f'Missing {key}.')
    strategy = record.get('strategy')
    if strategy not in ('compatible', 'structural', 'modernization', 'undecided'):
        errors.append('Invalid strategy.')
    if strategy != 'undecided' and not text(record.get('strategy_reference')):
        errors.append('Selected strategy needs a source/confirmation reference.')
    if strategy == 'undecided':
        warnings.append('Assessment strategy is undecided; no implementation path is selected.')
    domains = record.get('domains')
    selected = set()
    if not isinstance(domains, dict) or set(domains) != DOMAINS:
        errors.append('Classify every quality domain as selected, excluded or deferred.')
        domains = domains if isinstance(domains, dict) else {}
    for domain, item in domains.items():
        if not isinstance(item, dict) or item.get('status') not in ('selected', 'excluded', 'deferred') or not text(item.get('rationale')):
            errors.append(f'Invalid domain disposition: {domain}.')
            continue
        if item['status'] == 'selected':
            selected.add(domain)
        elif item['status'] == 'deferred':
            warnings.append(f'Deferred domain: {domain}.')
    if not selected:
        warnings.append('No quality domain selected.')

    def rows(key):
        values = record.get(key)
        if not isinstance(values, list):
            errors.append(f'{key} must be an array.')
            return {}
        result = {}
        for item in values:
            if not isinstance(item, dict) or not text(item.get('id')):
                errors.append(f'Invalid {key} entry.')
                continue
            ident = item['id']
            if ident in result:
                errors.append(f'Duplicate {key} ID: {ident}.')
            result[ident] = item
        return result

    requirements, findings, solutions = rows('requirements'), rows('findings'), rows('solutions')
    covered = set()
    executed = 0
    for ident, requirement in requirements.items():
        domain = requirement.get('domain')
        if not isinstance(domain, str) or domain not in selected:
            errors.append(f'{ident}: requirement must belong to a selected domain.')
        else:
            covered.add(domain)
        for key in ('source_reference', 'verification_method'):
            if not text(requirement.get(key)):
                errors.append(f'{ident}: missing {key}.')
        if not references(requirement.get('components')) or not requirement['components']:
            errors.append(f'{ident}: affected components required.')
        outcome = requirement.get('outcome')
        if outcome not in ('passed', 'failed', 'blocked', 'not-executed'):
            errors.append(f'{ident}: invalid outcome.')
        evidence = requirement.get('evidence_references')
        if not references(evidence):
            errors.append(f'{ident}: invalid evidence references.')
        if outcome in ('passed', 'failed'):
            executed += 1
            if not text(requirement.get('acceptance')):
                errors.append(f'{ident}: executed result requires known acceptance criteria.')
            if not evidence:
                errors.append(f'{ident}: executed result requires evidence.')
        else:
            warnings.append(f'{ident}: not executed or blocked.')
        if not text(requirement.get('acceptance')):
            warnings.append(f'{ident}: unresolved acceptance criteria.')
    for domain in selected - covered:
        warnings.append(f'Selected domain has no mapped requirements: {domain}.')

    for ident, finding in findings.items():
        links = finding.get('requirement_ids')
        if not references(links) or any(link not in requirements for link in links):
            errors.append(f'{ident}: invalid requirement linkage.')
            links = []
        if not links and finding.get('requirements_gap') is not True:
            errors.append(f'{ident}: link a requirement or explicitly identify a requirements gap.')
        domain = finding.get('domain')
        if not isinstance(domain, str) or domain not in selected:
            errors.append(f'{ident}: finding must belong to a selected domain.')
        if any(requirements[link].get('domain') != domain for link in links):
            errors.append(f'{ident}: finding domain differs from linked requirement.')
        status, evidence = finding.get('status'), finding.get('evidence_references')
        if status not in ('suspected', 'reproduced', 'resolved'):
            errors.append(f'{ident}: invalid finding status.')
        if not references(evidence) or (status in ('reproduced', 'resolved') and not evidence):
            errors.append(f'{ident}: invalid or missing finding evidence.')
        if status == 'resolved' and (not links or any(requirements[link].get('outcome') != 'passed' for link in links)):
            errors.append(f'{ident}: resolved finding requires all linked verification results passed.')

    for ident, solution in solutions.items():
        links = solution.get('finding_ids')
        if not references(links) or not links or any(link not in findings for link in links):
            errors.append(f'{ident}: source findings required.')
        for key in ('rationale', 'tradeoffs'):
            if not text(solution.get(key)):
                errors.append(f'{ident}: missing {key}.')
        status = solution.get('status')
        if status not in ('proposed', 'accepted', 'implemented', 'validated', 'deferred'):
            errors.append(f'{ident}: invalid solution status.')
        validations = solution.get('validation_requirement_ids')
        if not references(validations) or any(link not in requirements for link in validations):
            errors.append(f'{ident}: invalid solution validation linkage.')
            validations = []
        evidence = solution.get('evidence_references')
        if not references(evidence):
            errors.append(f'{ident}: invalid solution evidence.')
        if status in ('implemented', 'validated') and not text(solution.get('rollback_reference')):
            errors.append(f'{ident}: implementation needs rollback/recovery reference.')
        if status == 'validated':
            if not text(solution.get('acceptance')) or not evidence or not validations:
                errors.append(f'{ident}: validated solution needs acceptance, evidence and verification requirements.')
            if any(requirements[link].get('outcome') != 'passed' for link in validations):
                errors.append(f'{ident}: validated solution has failed/untested verification.')
            affected = set()
            if references(links):
                for finding_id in links:
                    finding = findings.get(finding_id, {})
                    original = finding.get('requirement_ids')
                    if not references(original) or not original:
                        errors.append(f'{ident}: resolve source finding requirements before validating the solution.')
                        continue
                    affected.update(original)
            if not affected.issubset(set(validations)):
                errors.append(f'{ident}: validation must cover every requirement of its source findings.')
            if any(requirements.get(link, {}).get('outcome') != 'passed' for link in affected):
                errors.append(f'{ident}: source finding requirements remain failed or untested.')
        elif status != 'deferred':
            warnings.append(f'{ident}: solution is not validated.')
    summary = 'incomplete'
    if not errors and not warnings:
        summary = 'open-findings' if (any(f.get('status') != 'resolved' for f in findings.values()) or any(r.get('outcome') == 'failed' for r in requirements.values())) else 'recorded-checks-complete'
    return {'valid': not errors, 'errors': errors, 'warnings': warnings, 'recorded_summary': summary,
            'recorded_counts': {'selected_domains': len(selected), 'requirements': len(requirements), 'executed': executed,
                                'findings': len(findings), 'solutions': len(solutions)},
            'scope': 'Local consistency only; no test execution, evidence attestation, approval grant, release authorization or certification.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record', required=True)
    args = parser.parse_args()
    try:
        result = check_plan(json.loads(Path(args.record).read_text()))
    except (OSError, ValueError, TypeError):
        result = {'valid': False, 'errors': ['Cannot read a valid quality-plan JSON record.']}
    print(json.dumps(result, indent=2))
    return 0 if result['valid'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
