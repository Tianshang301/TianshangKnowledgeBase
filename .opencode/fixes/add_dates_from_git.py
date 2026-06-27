#!/usr/bin/env python3
"""
Batch-add `created` and `updated` frontmatter fields from git history.
Uses a single pass of `git log` for performance (O(1) git call).
"""
import os
import re
import subprocess
from collections import defaultdict
from path_utils import BASE, SKIP_DIRS, walk_markdown

DATE_FM_RE = re.compile(r'^created:\s*\S+\s*$', re.MULTILINE)


def get_git_dates(base_path):
    """Single-pass: build {rel_path: (created_date, updated_date)} from git log."""
    dates = {}
    try:
        result = subprocess.run(
            ['git', 'log', '--all', '--format=%H %ai', '--name-only'],
            cwd=base_path, capture_output=True, text=True, timeout=120
        )
    except subprocess.TimeoutExpired:
        print('[WARN] git log timed out, falling back to per-file mode')
        return None

    current_date = None
    file_dates = defaultdict(list)

    for line in result.stdout.split('\n'):
        line = line.strip()
        if not line:
            continue
        # Commit hash + date line
        if re.match(r'^[0-9a-f]{40} \d{4}-\d{2}-\d{2}', line):
            current_date = line.split()[1]
        elif current_date and line.endswith('.md'):
            file_dates[line].append(current_date)

    for fpath, dlist in file_dates.items():
        if dlist:
            dates[fpath] = (dlist[0], dlist[-1])

    return dates


def add_dates_to_file(filepath, created, updated):
    """Add or update created/updated in frontmatter."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if not content.startswith('---'):
        return False

    end_idx = content.find('---', 3)
    if end_idx == -1:
        return False

    header = content[3:end_idx]
    body = content[end_idx + 3:]

    # Already has created field
    if DATE_FM_RE.search(header):
        return False

    # Add created/updated after tags line
    if 'tags:' in header:
        # Find the tags line and add after it
        lines = header.split('\n')
        new_lines = []
        for line in lines:
            new_lines.append(line)
            if line.strip().startswith('tags:'):
                new_lines.append(f'created: {created}')
                new_lines.append(f'updated: {updated}')
        new_header = '\n'.join(new_lines)
    else:
        # Append at end of frontmatter
        new_header = header.rstrip() + f'\ncreated: {created}\nupdated: {updated}'

    new_content = '---' + new_header + '---' + body

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True


def main():
    print('Phase 1: Building date map from git history (single pass)...')
    dates = get_git_dates(BASE)
    if dates is None:
        print('[ERROR] Failed to get git dates. Is this a git repository?')
        return

    print(f'Found dates for {len(dates)} files in git history')

    print('Phase 2: Scanning files and adding dates...')
    updated = 0
    skipped_has_dates = 0
    skipped_no_git = 0
    total = 0

    for root, dirs, files in walk_markdown():
        for fname in files:
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, BASE).replace('\\', '/')
            total += 1

            if rel in dates:
                cr_date, upd_date = dates[rel]
                if add_dates_to_file(fpath, cr_date, upd_date):
                    updated += 1
                    print(f'  [ADDED] {rel}  ({cr_date} → {upd_date})')
                else:
                    skipped_has_dates += 1
            else:
                skipped_no_git += 1

            if total % 300 == 0:
                print(f'  Progress: {total} files scanned...')

    print(f'\n=== Results ===')
    print(f'Total .md files scanned: {total}')
    print(f'Dates ADDED: {updated}')
    print(f'Already had dates: {skipped_has_dates}')
    print(f'No git history: {skipped_no_git}')


if __name__ == '__main__':
    main()
