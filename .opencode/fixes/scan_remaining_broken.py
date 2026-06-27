#!/usr/bin/env python3
"""Scan and fix ALL remaining broken wiki-links."""
import os
import re
from path_utils import BASE, SKIP_DIRS, walk_markdown

# Build complete file index
files_index = {}
path_index = set()
for root, dirs, files in os.walk(BASE):
    if '.git' in root or '.obsidian' in root or '.ruff_cache' in root or '.opencode' in root:
        continue
    for f in files:
        if f.endswith('.md'):
            base = f[:-3]
            files_index[base.lower()] = base
            rel = os.path.relpath(os.path.join(root, f), BASE).replace('\\', '/')
            path_index.add(rel)
            path_index.add(rel[:-3])

# Scan for broken links
remaining = Counter()
source_map = {}

for root, dirs, files in os.walk(BASE):
    if '.git' in root or '.obsidian' in root or '.ruff_cache' in root or '.opencode' in root:
        continue
    for f in files:
        if not f.endswith('.md'):
            continue
        fpath = os.path.join(root, f)
        rel_src = os.path.relpath(fpath, BASE).replace('\\', '/')
        try:
            with open(fpath, 'r', encoding='utf-8') as fh:
                content = fh.read()
        except:
            continue
        for m in re.finditer(r'\[\[([^\]]+?)\]\]', content):
            raw = m.group(1).strip()
            target = raw.split('|')[0].split('#')[0].strip()
            if not target or target in ('INDEX', 'LearningPath', 'README', '404'):
                continue
            if target in files_index.values():
                continue
            if target.lower() in files_index:
                continue
            if target + '.md' in path_index:
                continue
            sd = os.path.dirname(rel_src)
            rt = sd + '/' + target
            if rt in path_index or rt + '.md' in path_index:
                continue
            remaining[target] += 1
            source_map.setdefault(target, []).append(rel_src)

# Categorize
path_based = []
simple = []
for t, c in remaining.most_common():
    if '/' in t or '\\' in t:
        path_based.append((t, c))
    else:
        simple.append((t, c))

print(f'Total remaining broken: {len(remaining)} unique, {sum(remaining.values())} occurrences')
print(f'  Path-based: {len(path_based)}')
print(f'  Simple name: {len(simple)}')

if simple:
    print('\n=== SIMPLE NAME (fixing these) ===')
    for t, c in simple:
        srcs = source_map.get(t, [])[:2]
        print(f'  [{c}] {t}')

if path_based:
    print(f'\n=== PATH-BASED (verifying in Obsidian) ===')
    for t, c in path_based[:10]:
        srcs = source_map.get(t, [])[:2]
        print(f'  [{c}] {t}')

# FIX: Create stub files for ALL simple-name broken links
print('\n=== Creating stub files ===')
created = 0
for t, c in simple:
    # Find or create a directory
    dest_dir = None
    
    # Look for existing file with similar name pattern
    for root, dirs, files in os.walk(BASE):
        if '.git' in root or '.obsidian' in root or '.ruff_cache' in root or '.opencode' in root:
            continue
        for f in files:
            if f.endswith('.md') and f[:-3].lower() == t.lower():
                dest_dir = root
                break
        if dest_dir:
            break
    
    if not dest_dir:
        # Find first source file that references this link, and place stub nearby
        srcs = source_map.get(t, [])
        if srcs:
            src_path = os.path.join(BASE, srcs[0].replace('/', '\\'))
            dest_dir = os.path.dirname(src_path)
        else:
            dest_dir = os.path.join(BASE, '_Stubs')
    
    os.makedirs(dest_dir, exist_ok=True)
    fpath = os.path.join(dest_dir, t + '.md')
    
    if os.path.exists(fpath):
        continue
    
    # Derive tags from directory
    rel_dir = os.path.relpath(dest_dir, BASE).replace('\\', '/')
    tag_parts = [p for p in rel_dir.split('/') if p and p != '_Stubs']
    tag_str = ', '.join(["'" + p + "'" for p in tag_parts]) if tag_parts else "'_Stubs'"
    
    content = '---\n'
    content += f'aliases: [{t}]\n'
    content += f'tags: [{tag_str}]\n'
    content += '---\n\n'
    content += f'# {t}\n\n'
    content += '> 此页面内容待完善。\n\n'
    content += '## 相关条目\n'
    content += '- [[INDEX|当前目录索引]]\n'
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    created += 1
    print(f'  [CREATE] {os.path.relpath(fpath, BASE)} (refs: {c})')

print(f'\nCreated {created} new stub files')
