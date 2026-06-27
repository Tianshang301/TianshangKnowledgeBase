#!/usr/bin/env python3
"""Comprehensive broken wiki-link analysis."""
import os
import re
from collections import Counter
from path_utils import BASE, SKIP_DIRS, walk_markdown

# Build existing file index
existing_base = set()
for root, dirs, files in os.walk(BASE):
    if '.git' in root or '.obsidian' in root or '.ruff_cache' in root:
        continue
    for f in files:
        if f.endswith('.md'):
            existing_base.add(f[:-3])
            rel = os.path.relpath(os.path.join(root, f), BASE).replace('\\', '/')[:-3]
            existing_base.add(rel)

# Scan for broken links
broken_links = Counter()
source_map = {}

for root, dirs, files in os.walk(BASE):
    if '.git' in root or '.obsidian' in root or '.ruff_cache' in root:
        continue
    for f in files:
        if not f.endswith('.md'):
            continue
        fpath = os.path.join(root, f)
        rel_source = os.path.relpath(fpath, BASE).replace('\\', '/')
        try:
            with open(fpath, 'r', encoding='utf-8') as fh:
                content = fh.read()
        except:
            continue
        for m in re.finditer(r'\[\[([^\]]+?)\]\]', content):
            target = m.group(1).split('|')[0].split('#')[0].strip()
            if not target or target in ('INDEX', 'LearningPath', 'README', '404'):
                continue
            if target in existing_base or target + '.md' in existing_base:
                continue
            sd = os.path.dirname(rel_source)
            ft = sd + '/' + target
            if ft in existing_base or ft + '.md' in existing_base:
                continue
            broken_links[target] += 1
            source_map.setdefault(target, []).append(rel_source)

# Categorize
garbled, index_refs, topical, other = [], [], [], []
for target, count in broken_links.most_common():
    g = sum(1 for c in target if ord(c) < 32 or ord(c) == 65533)
    if g > 0 or '?' in target or target.count('_') > 4:
        garbled.append((target, count))
    elif target.endswith('/INDEX') or '/INDEX' in target:
        index_refs.append((target, count))
    elif count >= 3:
        topical.append((target, count))
    else:
        other.append((target, count))

print(f'Total broken: {len(broken_links)} unique, {sum(broken_links.values())} occurrences')
print(f'Garbled: {len(garbled)}')
print(f'INDEX refs: {len(index_refs)}')
print(f'Topical (>=3 refs): {len(topical)}')
print(f'Low (<3 refs): {len(other)}')

print('\n=== GARBLED (to REMOVE) ===')
for t, c in garbled:
    print(f'  [{c}] {repr(t)[:80]}')

print('\n=== TOPICAL (>=3, to CREATE) ===')
for t, c in topical:
    print(f'  [{c}] {t}')

# Save full list for batch processing
with open(os.path.join(BASE, '.opencode', 'fixes', 'broken_targets.txt'), 'w', encoding='utf-8') as f:
    for t, c in broken_links.most_common():
        f.write(f'{c}\t{t}\n')
