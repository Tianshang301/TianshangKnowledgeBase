#!/usr/bin/env python3
"""Final verification: check for ANY remaining broken wiki-links."""
import os
import re
from path_utils import BASE, SKIP_DIRS, walk_markdown

# Build complete file index
all_files = set()
all_basenames = set()
for root, dirs, files in os.walk(BASE):
    if '.git' in root or '.obsidian' in root or '.ruff_cache' in root or '.opencode' in root:
        continue
    for f in files:
        if f.endswith('.md'):
            full = os.path.normpath(os.path.join(root, f))
            all_files.add(full)
            all_basenames.add(f[:-3].lower())

broken_simple = []
broken_relative = []
broken_root = []

for root, dirs, files in os.walk(BASE):
    if '.git' in root or '.obsidian' in root or '.ruff_cache' in root or '.opencode' in root:
        continue
    for f in files:
        if not f.endswith('.md'):
            continue
        fpath = os.path.normpath(os.path.join(root, f))
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
            
            # SIMPLE name resolution
            if '/' not in target and '\\' not in target:
                # Check source dir first, then vault root
                in_src_dir = os.path.normpath(os.path.join(os.path.dirname(fpath), target + '.md'))
                in_vault_root = os.path.normpath(os.path.join(BASE, target + '.md'))
                if in_src_dir not in all_files and in_vault_root not in all_files and target.lower() not in all_basenames:
                    broken_simple.append((target, fpath))
            
            # RELATIVE path resolution (starts with .)
            elif target.startswith('.'):
                resolved = os.path.normpath(os.path.join(os.path.dirname(fpath), target))
                if not resolved.endswith('.md'):
                    resolved += '.md'
                if resolved not in all_files:
                    broken_relative.append((target, fpath, resolved))
            
            # VAULT-ROOT path resolution 
            else:
                resolved = os.path.normpath(os.path.join(BASE, target))
                if not resolved.endswith('.md'):
                    resolved += '.md'
                if resolved not in all_files:
                    broken_root.append((target, fpath, resolved))

print(f'=== FINAL VERIFICATION ===')
print()

# Deduplicate
simple_unique = list(set(t for t, _ in broken_simple))
relative_unique = list(set((t,) for t, _, _ in broken_relative))
root_unique = list(set(t for t, _, _ in broken_root))

print(f'Truly broken simple-name links: {len(simple_unique)}')
if simple_unique:
    for t in sorted(simple_unique)[:20]:
        srcs = [s for tt, s in broken_simple if tt == t][:2]
        for s in srcs:
            print(f'  "{t}"  in {os.path.relpath(s, BASE)}')

print()
print(f'Truly broken relative-path links (starting with .): {len(broken_relative)}')
if broken_relative:
    for t, s, r in broken_relative[:10]:
        print(f'  {t}')
        print(f'    from: {os.path.relpath(s, BASE)}')
        print(f'    wants: {os.path.relpath(r, BASE)}')

print()
print(f'Unresolved vault-root links: {len(broken_root)}')
if broken_root:
    # Group by target to show unique ones
    root_by_target = {}
    for t, s, r in broken_root:
        root_by_target.setdefault(t, []).append(s)
    
    # Only print unique targets with count
    unique_root = [(t, len(sources)) for t, sources in root_by_target.items()]
    unique_root.sort(key=lambda x: -x[1])
    for t, c in unique_root[:20]:
        print(f'  [{c}] {t}')
    if len(unique_root) > 20:
        print(f'  ... and {len(unique_root)-20} more')

if not simple_unique and not broken_relative and not broken_root:
    print('ALL WIKI-LINKS RESOLVE CORRECTLY!')
