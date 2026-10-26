"""Read-only final-delivery checks; findings require contextual review.

Examples:
  python scripts/check_delivery.py --root submit --expect paper.pdf --expect support/result.xlsx
  python scripts/check_delivery.py --root submit --pdf paper.pdf --aux ../build/main.aux --body-limit 30
  python scripts/check_delivery.py --root submit --pdf paper.pdf --body-first 2 --body-last 31 --body-limit 30

PDF inspection requires pypdf. No deletion, model execution, or full-package hashing.
Aux files must belong to the same freshly compiled PDF; explicit pages are 1-based
physical PDF pages, never printed page numbers. The limit is supplied by the user.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re


def physical_pages(aux_text: str) -> dict[str, int]:
    result = {}
    for name in ('body-start', 'body-end', 'appendix-start'):
        match = re.search(r'\\zref@newlabel\{skill:' + name + r'\}\{([^\n]*)', aux_text)
        value = re.search(r'\\abspage\{(\d+)\}', match.group(1)) if match else None
        if value:
            result[name] = int(value.group(1))
    return result


def page_check(total: int, first: int | None, last: int | None,
               limit: int | None, appendix: int | None = None) -> dict:
    out = {'total_pages': total, 'body_first': first, 'body_last': last,
           'body_limit': limit, 'appendix_first': appendix}
    if first is None or last is None:
        return dict(out, status='not_checked', reason='Body boundaries were not established.')
    if not 1 <= first <= last <= total:
        return dict(out, status='error', reason='Physical page boundaries are outside this PDF or reversed.')
    if appendix is not None and not last < appendix <= total:
        return dict(out, status='error', reason='Appendix overlaps the body or lies outside this PDF.')
    count = last - first + 1
    return dict(out, body_pages=count,
                status='not_checked' if limit is None else 'over_limit' if count > limit else 'within_limit',
                reason='No applicable page limit supplied.' if limit is None else '')


def inspect_tree(root: Path, expected: list[str]) -> dict:
    missing = []
    for rel in expected:
        path = (root / rel).resolve()
        if not path.is_relative_to(root):
            raise ValueError(f'Expected deliverable must be inside root: {rel}')
        if not path.is_file():
            missing.append(rel)
    findings, skipped = [], []
    text_types = {'.md', '.txt', '.tex', '.py', '.m', '.json', '.yaml', '.yml', '.toml'}
    pattern = re.compile(r'〔待填|\\slot\{|作为(?:一个)?AI|你是ChatGPT|用户要求|Codex提示词|对话记录|系统提示词', re.I)
    count = 0
    for path in sorted(root.rglob('*')):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if not path.resolve().is_relative_to(root):
            skipped.append({'path': rel, 'reason': 'external symlink'})
            continue
        count += 1
        if path.suffix.lower() in {'.pyc', '.aux', '.log', '.synctex'} or '__pycache__' in path.parts:
            findings.append({'path': rel, 'kind': 'possible_build_cache'})
        if re.search(r'prompt|提示词|对话|任务书|交接|旧版|备份', path.name, re.I):
            findings.append({'path': rel, 'kind': 'possible_process_file'})
        if path.suffix.lower() not in text_types:
            continue
        if path.stat().st_size > 2_000_000:
            skipped.append({'path': rel, 'reason': 'text larger than 2 MB'})
            continue
        try:
            lines = path.read_text(encoding='utf-8-sig').splitlines()
        except UnicodeError:
            skipped.append({'path': rel, 'reason': 'non-UTF8 text'})
            continue
        for i, line in enumerate(lines, 1):
            if pattern.search(line):
                findings.append({'path': rel, 'line': i, 'kind': 'possible_placeholder_or_conversation',
                                 'excerpt': line.strip()[:160]})
    return {'file_count': count, 'missing': missing, 'review_candidates': findings,
            'skipped': skipped, 'note': 'Candidates may be legitimate documentation or disclosure. Review; do not delete blindly.'}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--root', required=True, type=Path)
    ap.add_argument('--expect', action='append', default=[], help='Required file relative to root; repeatable.')
    ap.add_argument('--pdf', type=Path, help='Relative to root, or absolute.')
    ap.add_argument('--aux', type=Path, help='Current template aux with skill physical-page markers.')
    ap.add_argument('--body-first', type=int)
    ap.add_argument('--body-last', type=int)
    ap.add_argument('--body-limit', type=int, help='Verified applicable body limit; no default.')
    args = ap.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        ap.error('--root must be an existing directory')
    if args.body_limit is not None and args.body_limit < 1:
        ap.error('--body-limit must be positive')
    if (args.body_first is None) != (args.body_last is None):
        ap.error('Provide both --body-first and --body-last')
    if args.aux and args.body_first is not None:
        ap.error('Use either --aux or explicit physical page boundaries, not both')
    report = {'scope': 'File inventory, UTF8 text candidates, PDF page bounds; not a full compliance or visual review.'}
    try:
        report['files'] = inspect_tree(root, args.expect)
        report['pages'] = {'status': 'not_checked', 'reason': 'No PDF supplied.'}
        if args.pdf:
            from pypdf import PdfReader
            path = args.pdf if args.pdf.is_absolute() else root / args.pdf
            doc = PdfReader(path)
            markers = physical_pages(args.aux.read_text(encoding='utf-8')) if args.aux else {}
            report['pages'] = page_check(len(doc.pages), markers.get('body-start', args.body_first),
                markers.get('body-end', args.body_last), args.body_limit, markers.get('appendix-start'))
            report['pages']['boundary_source'] = ('aux (must match this PDF)' if args.aux
                else 'explicit physical pages' if args.body_first is not None else 'not established')
        blocking = bool(report['files']['missing']) or report['pages']['status'] in {'error', 'over_limit'}
        report['status'] = 'blocking_findings' if blocking else 'checks_run_review_remaining'
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 2 if blocking else 0
    except (OSError, ValueError, ImportError) as exc:
        report.update(status='error', error=str(exc))
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
