#!/usr/bin/env python3
"""Fix remaining frontmatter issues: 1 missing + remove .md from tags."""
import os
import re
from path_utils import BASE, SKIP_DIRS, walk_markdown

# Fix 1: Kotlin/Basics.md missing frontmatter
fpath = os.path.join(BASE, '05_ComputerScience', 'ProgrammingLanguages', 'Kotlin', 'Basics.md')
with open(fpath, 'r', encoding='utf-8') as fh:
    c = fh.read()
if not c.startswith('---'):
    tag_str = "'05_ComputerScience', 'ProgrammingLanguages', 'Kotlin'"
    fm = '---\n' + f'aliases: [Basics]\ntags: [{tag_str}]\n' + '---\n\n'
    with open(fpath, 'w', encoding='utf-8') as fh:
        fh.write(fm + c.lstrip('\ufeff'))
    print('Fixed Kotlin/Basics.md')

# Fix 2: Remove .md from tags across all files
fixed = 0
for root, dirs, files in os.walk(BASE):
    if '.git' in root or '.obsidian' in root or '.ruff_cache' in root or '.opencode' in root:
        continue
    for f in files:
        if not f.endswith('.md'):
            continue
        fpath = os.path.join(root, f)
        with open(fpath, 'r', encoding='utf-8') as fh:
            c = fh.read()
        if '.md' not in c[:300]:
            continue
        lines = c.split('\n')
        changed = False
        for i, line in enumerate(lines):
            if line.startswith('tags:') and '.md' in line:
                lines[i] = line.replace('.md', '')
                changed = True
        if changed:
            with open(fpath, 'w', encoding='utf-8') as fh:
                fh.write('\n'.join(lines))
            fixed += 1

print(f'Fixed .md in tags for {fixed} files')
print('Done!')
