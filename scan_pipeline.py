#!/usr/bin/env python3
"""
Full-text regex scanning pipeline for paratext analysis of Shuenjoyu Vol. I.
Usage: python scan_pipeline.py --input <text_file> --output <results.json>
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from regex_patterns import PATTERN_REGISTRY, SUBCLASS_REGISTRY, FNOTE_EXPLICIT, FNOTE_IMPLICIT


def load_text(filepath: str) -> tuple[str, list[str]]:
    """Load OCR-cleaned text. Returns (full_text, lines)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    lines = text.split('\n')
    return text, lines


def run_scan(text: str) -> dict:
    """
    Run all registered regex patterns against the full text.
    Returns dict with raw matches per pattern, keyed by pattern_id.
    """
    results = {}
    for pattern_id, (label, pattern, is_paratext) in PATTERN_REGISTRY.items():
        matches = pattern.findall(text)
        # Deduplicate exact matches within same category
        unique_matches = list(dict.fromkeys(matches))
        results[pattern_id] = {
            'label': label,
            'count_raw': len(matches),
            'count_unique': len(unique_matches),
            'is_paratext': is_paratext,
            'matches': unique_matches[:500],  # Truncate for output size
        }
    return results


def classify_subcategory(pattern_id: str, match_text: str) -> str:
    """Apply sub-classification rules to a single match."""
    if pattern_id not in SUBCLASS_REGISTRY:
        return 'other'

    subclass_rules = SUBCLASS_REGISTRY[pattern_id]
    for sub_label, sub_pattern in subclass_rules.items():
        if sub_pattern.search(match_text):
            return sub_label
    return 'other'


def run_classification(scan_results: dict) -> dict:
    """Sub-classify matches and produce categorized counts."""
    classified = defaultdict(lambda: defaultdict(int))

    for pattern_id, data in scan_results.items():
        if not data['is_paratext']:
            continue
        for match in data['matches']:
            subcat = classify_subcategory(pattern_id, match)
            classified[pattern_id][subcat] += 1

    return dict(classified)


def count_fnote_explicit(text: str) -> int:
    """Count explicit 訳注 vs implicit 注 markers."""
    explicit = len(FNOTE_EXPLICIT.findall(text))
    implicit = len(FNOTE_IMPLICIT.findall(text))
    return {'explicit_訳注': explicit, 'implicit_注': implicit}


def compute_summary(scan_results: dict, classified: dict, fnote_breakdown: dict) -> dict:
    """Produce the final summary table."""
    summary = {
        'input_stats': {},
        'paratextual_categories': {},
        'excluded_categories': {},
        'totals': {},
    }

    # Paratextual
    paratext_total = 0
    for pid, data in scan_results.items():
        entry = {
            'label': data['label'],
            'count_unique': data['count_unique'],
        }
        if pid in classified:
            entry['subcategories'] = dict(classified[pid])

        if data['is_paratext']:
            summary['paratextual_categories'][pid] = entry
            paratext_total += data['count_unique']
        else:
            summary['excluded_categories'][pid] = entry

    summary['totals'] = {
        'paratext_total': paratext_total,
        'fnote_breakdown': fnote_breakdown,
    }

    return summary


def main():
    parser = argparse.ArgumentParser(
        description='Paratext Regex Scan Pipeline — Shuenjoyu Vol. I'
    )
    parser.add_argument('--input', '-i', required=True,
                        help='Path to OCR-cleaned text file (UTF-8)')
    parser.add_argument('--output', '-o', default='results.json',
                        help='Output JSON file path (default: results.json)')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Print per-category breakdown to stdout')
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f'Error: Input file not found: {args.input}', file=sys.stderr)
        sys.exit(1)

    # Load
    text, lines = load_text(str(input_path))
    total_chars = len(text)

    # Scan
    scan_results = run_scan(text)

    # Sub-classify
    classified = run_classification(scan_results)

    # Fnote breakdown
    fnote_breakdown = count_fnote_explicit(text)

    # Summarize
    summary = compute_summary(scan_results, classified, fnote_breakdown)
    summary['input_stats'] = {
        'filename': input_path.name,
        'total_lines': len(lines),
        'total_chars': total_chars,
    }

    # Output
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    if args.verbose:
        print(f'Lines scanned:  {len(lines):,}')
        print(f'Chars scanned:  {total_chars:,}')
        print(f'Paratext total: {summary["totals"]["paratext_total"]}')
        print(f'Fnote explicit: {fnote_breakdown["explicit_訳注"]}')
        print(f'Fnote implicit: {fnote_breakdown["implicit_注"]}')
        print()
        for pid, data in scan_results.items():
            status = '✓' if data['is_paratext'] else '✗'
            print(f'  [{status}] {data["label"]}: {data["count_unique"]}')

    print(f'Results written to: {args.output}')


if __name__ == '__main__':
    main()
