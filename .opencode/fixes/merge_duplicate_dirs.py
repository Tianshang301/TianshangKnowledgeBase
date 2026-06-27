#!/usr/bin/env python3
"""
Merge duplicate directories in the knowledge base.
Detects and merges: CloudComputing/ -> CloudComputingAndDistributedSystems/
                      NLP/ -> NaturalLanguageProcessing/
Usage:
    python merge_duplicate_dirs.py          # preview
    python merge_duplicate_dirs.py --apply  # execute merge
"""
import os
import re
import sys
import shutil
import subprocess
from path_utils import BASE, walk_markdown

# Merge map: { old_dir_rel: new_dir_rel }
MERGE_MAP = {
    '05_ComputerScience/CloudComputing': '05_ComputerScience/CloudComputingAndDistributedSystems',
    '05_ComputerScience/ArtificialIntelligence/NLP': '05_ComputerScience/ArtificialIntelligence/NaturalLanguageProcessing',
}

DRY_RUN = '--apply' not in sys.argv


def update_wikilinks_for_path(filepath, old_prefix, new_prefix):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    pattern = re.compile(r'\[\[([^\]]+?)\]\]')
    changed = False

    def replace(m):
        nonlocal changed
        link = m.group(1)
        parts = link.split('|', 1)
        target = parts[0].strip()
        display = parts[1] if len(parts) > 1 else None
        if target.startswith(old_prefix):
            new_target = new_prefix + target[len(old_prefix):]
            new_link = f'[[{new_target}|{display}]]' if display else f'[[{new_target}]]'
            changed = True
            return new_link
        # Also handle bare name reference [[Topic]] where topic is a file being moved
        return m.group(0)

    content = pattern.sub(replace, content)
    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    return changed


def main():
    print(f'{"DRY RUN" if DRY_RUN else "APPLY"} mode\n')

    for old_rel, new_rel in MERGE_MAP.items():
        old_abs = os.path.join(BASE, old_rel.replace('/', '\\'))
        new_abs = os.path.join(BASE, new_rel.replace('/', '\\'))

        print(f'Merging:  {old_rel}/')
        print(f'     into {new_rel}/')

        if not os.path.isdir(old_abs):
            print(f'  [SKIP] source does not exist')
            continue
        if not os.path.isdir(new_abs):
            print(f'  [SKIP] target does not exist')
            continue

        # List files in old dir
        old_files = set()
        for f in os.listdir(old_abs):
            if f.endswith('.md'):
                old_files.add(f)
        new_files = set()
        for f in os.listdir(new_abs):
            if f.endswith('.md'):
                new_files.add(f)

        conflicts = old_files & new_files
        unique_old = old_files - new_files

        print(f'  Files in source: {len(old_files)}')
        print(f'  Files in target: {len(new_files)}')
        print(f'  Conflicts (same name): {len(conflicts)}')
        print(f'  Unique files to move: {len(unique_old)}')

        if conflicts:
            for c in sorted(conflicts):
                old_path = os.path.join(old_abs, c)
                new_path = os.path.join(new_abs, c)
                old_size = os.path.getsize(old_path)
                new_size = os.path.getsize(new_path)
                print(f'    Conflict: {c} (source={old_size}B, target={new_size}B)')

        # Phase 1: Update all wiki-links to point to new paths
        print(f'  Phase 1: Updating wiki-links...')
        link_changes = 0
        for root, dirs, files in walk_markdown():
            for fname in files:
                fpath = os.path.join(root, fname)
                if fpath.startswith(old_abs) or fpath.startswith(new_abs):
                    continue
                if update_wikilinks_for_path(fpath, old_rel + '/', new_rel + '/'):
                    link_changes += 1
        print(f'    Files with updated links: {link_changes}')

        if DRY_RUN:
            print(f'  Phase 2: [DRY-RUN] Would move files and git rm old dir')
            for f in sorted(unique_old):
                print(f'    Would move: {old_rel}/{f} -> {new_rel}/{f}')
            for c in sorted(conflicts):
                old_path = os.path.join(old_abs, c)
                new_path = os.path.join(new_abs, c)
                old_size = os.path.getsize(old_path)
                new_size = os.path.getsize(new_path)
                if old_size > new_size:
                    print(f'    Conflict {c}: would KEEP source (larger)')
                else:
                    print(f'    Conflict {c}: would KEEP target (larger or equal)')
            print(f'    Would create redirect: {old_rel}/INDEX.md -> {new_rel}/INDEX.md')
            print(f'    Would git rm -rf {old_rel}/')
        else:
            print(f'  Phase 2: Moving unique files...')
            for f in sorted(unique_old):
                src = os.path.join(old_abs, f)
                dst = os.path.join(new_abs, f)
                shutil.copy2(src, dst)
                print(f'    Moved: {f}')
            print(f'  Phase 3: Handling conflicts (keeping larger file)...')
            for c in sorted(conflicts):
                old_path = os.path.join(old_abs, c)
                new_path = os.path.join(new_abs, c)
                old_size = os.path.getsize(old_path)
                new_size = os.path.getsize(new_path)
                if old_size > new_size:
                    shutil.copy2(old_path, new_path)
                    print(f'    Replaced: {c} (source larger)')
                else:
                    print(f'    Kept existing: {c} (target larger or equal)')
            print(f'  Phase 4: Creating redirect INDEX.md in old location...')
            new_index_rel = f'{new_rel}/INDEX'
            redirect_content = f'''---
aliases: [INDEX]
tags: ['{old_rel.split("/")[0]}', 'INDEX']
---

# {old_rel.split("/")[-1]}

> This directory has been merged into [[{new_index_rel}|{new_rel.split("/")[-1]}]].

Please update your links to point to the new location.
'''
            with open(os.path.join(old_abs, 'INDEX.md'), 'w', encoding='utf-8') as f:
                f.write(redirect_content)
            print(f'    Created redirect INDEX.md')
            print(f'  Phase 5: Removing old directory via git...')
            try:
                # Remove all files except INDEX.md redirect
                for f in os.listdir(old_abs):
                    if f != 'INDEX.md':
                        fp = os.path.join(old_abs, f)
                        if os.path.isfile(fp):
                            subprocess.run(['git', 'rm', fp], cwd=BASE, check=True, capture_output=True)
                subprocess.run(['git', 'add', os.path.join(old_abs, 'INDEX.md')], cwd=BASE, check=False)
                print(f'    Old directory cleaned. Only redirect INDEX.md remains.')
            except subprocess.CalledProcessError as e:
                print(f'    [WARN] git rm issue: {e.stderr.strip()}')
        print()

    print('Done!')


if __name__ == '__main__':
    main()
