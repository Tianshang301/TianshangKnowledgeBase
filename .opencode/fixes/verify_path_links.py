#!/usr/bin/env python3
"""Verify that path-based wiki-links actually resolve to existing files."""
import os
import re
from path_utils import BASE, SKIP_DIRS, walk_markdown

# Build all existing files set
existing = set()
for root, dirs, files in os.walk(BASE):
    if '.git' in root or '.obsidian' in root or '.ruff_cache' in root or '.opencode' in root:
        continue
    for f in files:
        if f.endswith('.md'):
            existing.add(os.path.join(root, f))

# Scan all path-based links and verify they resolve
failures = []
for root, dirs, files in os.walk(BASE):
    if '.git' in root or '.obsidian' in root or '.ruff_cache' in root or '.opencode' in root:
        continue
    for f in files:
        if not f.endswith('.md'):
            continue
        fpath = os.path.join(root, f)
        try:
            with open(fpath, 'r', encoding='utf-8') as fh:
                content = fh.read()
        except:
            continue
        
        for m in re.finditer(r'\[\[([^\]]+?)\]\]', content):
            raw = m.group(1).strip()
            target = raw.split('|')[0].split('#')[0].strip()
            
            # Only check path-based links
            if '/' not in target and '\\' not in target:
                continue
            if target in ('INDEX', 'LearningPath', 'README', '404'):
                continue
            
            # Resolve relative to source file
            src_dir = os.path.dirname(fpath)
            resolved = os.path.normpath(os.path.join(src_dir, target))
            if not resolved.endswith('.md'):
                resolved += '.md'
            
            if resolved not in existing:
                failures.append((fpath, target, resolved))

# Remove duplicates
seen = set()
unique_failures = []
for fpath, target, resolved in failures:
    key = (fpath, target)
    if key not in seen:
        seen.add(key)
        unique_failures.append((fpath, target, resolved))

print(f'Truly broken path-based links: {len(unique_failures)}')
if unique_failures:
    print()
    for fpath, target, resolved in unique_failures[:30]:
        rel_src = os.path.relpath(fpath, BASE).replace('\\', '/')
        rel_tgt = os.path.relpath(resolved, BASE).replace('\\', '/')
        print(f'  {target:40s}  in {rel_src}')
        print(f'  -> would resolve to: {rel_tgt}')
        print()
    if len(unique_failures) > 30:
        print(f'... and {len(unique_failures) - 30} more')

if not unique_failures:
    print('ALL path-based links resolve correctly!')
