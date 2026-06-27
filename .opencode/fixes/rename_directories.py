#!/usr/bin/env python3
"""
Rename non-conforming directories to UpperCamelCase and update all wiki-links.
Usage:
    python rename_directories.py          # preview mode (dry run)
    python rename_directories.py --apply   # actually rename
"""
import os
import re
import sys
import subprocess
from path_utils import BASE, SKIP_DIRS, walk_markdown

RENAME_MAP = {
    '01_K12/Arts_and_Sports': '01_K12/ArtsAndSports',
    '01_K12/SeniorHigh/Chinese/AncientPoems_72': '01_K12/SeniorHigh/Chinese/AncientPoems72',
    '05_ComputerScience/HardwareAndEmbeddedSystems/PCB_Design': '05_ComputerScience/HardwareAndEmbeddedSystems/PCBDesign',
    '05_ComputerScience/ProgrammingLanguages/C_Cpp': '05_ComputerScience/ProgrammingLanguages/CCpp',
    '05_ComputerScience/SoftwareEngineering/DevOpsAndCI_CD': '05_ComputerScience/SoftwareEngineering/DevOpsAndCICD',
}

DRY_RUN = '--apply' not in sys.argv

def update_links_in_file(filepath, old_prefix, new_prefix):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    pattern = re.compile(r'\[\[([^\]]+?)\]\]')
    changed = False
    def replace_link(match):
        nonlocal changed
        link = match.group(1)
        parts = link.split('|', 1)
        target = parts[0].strip()
        display = parts[1] if len(parts) > 1 else None
        if target.startswith(old_prefix):
            new_target = new_prefix + target[len(old_prefix):]
            new_link = f'[[{new_target}|{display}]]' if display else f'[[{new_target}]]'
            changed = True
            return new_link
        return match.group(0)
    content = pattern.sub(replace_link, content)
    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    return changed

def main():
    print(f'{"DRY RUN" if DRY_RUN else "APPLY"} mode')
    print(f'Renaming {len(RENAME_MAP)} directories:')
    for old_rel, new_rel in RENAME_MAP.items():
        old_abs = os.path.join(BASE, old_rel.replace('/', '\\'))
        new_abs = os.path.join(BASE, new_rel.replace('/', '\\'))
        print(f'  {old_rel}/  ->  {new_rel}/')
        if not os.path.isdir(old_abs):
            print(f'    [SKIP] directory does not exist')
            continue
        if os.path.exists(new_abs):
            print(f'    [SKIP] target already exists')
            continue
        print(f'    Phase 1: Updating wiki-links...')
        link_changes = 0
        for root, dirs, files in walk_markdown():
            for fname in files:
                fpath = os.path.join(root, fname)
                if fpath.startswith(old_abs):
                    continue
                if update_links_in_file(fpath, old_rel + '/', new_rel + '/'):
                    link_changes += 1
        print(f'      Files with updated links: {link_changes}')
        for root, dirs, files in os.walk(old_abs):
            for fname in files:
                if not fname.endswith('.md'):
                    continue
                fpath = os.path.join(root, fname)
                for o, n in RENAME_MAP.items():
                    update_links_in_file(fpath, o + '/', n + '/')
        if DRY_RUN:
            print(f'    Phase 2: [DRY-RUN] git mv skipped')
        else:
            print(f'    Phase 2: Renaming directory via git mv...')
            try:
                subprocess.run(
                    ['git', 'mv', old_abs, new_abs],
                    cwd=BASE, check=True, capture_output=True, text=True
                )
                print(f'    [OK] git mv succeeded')
            except subprocess.CalledProcessError as e:
                print(f'    [FAIL] git mv: {e.stderr.strip()}')
        print()
    print('Phase 3: Updating frontmatter tags in moved files...')
    for old_rel, new_rel in RENAME_MAP.items():
        new_abs = os.path.join(BASE, new_rel.replace('/', '\\'))
        if not os.path.isdir(new_abs):
            continue
        for root, dirs, files in os.walk(new_abs):
            for fname in files:
                if not fname.endswith('.md'):
                    continue
                fpath = os.path.join(root, fname)
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                old_name = old_rel.rsplit('/', 1)[-1]
                new_name = new_rel.rsplit('/', 1)[-1]
                if old_name in content:
                    content = content.replace(old_name, new_name)
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write(content)
    print('Done!')

if __name__ == '__main__':
    main()
