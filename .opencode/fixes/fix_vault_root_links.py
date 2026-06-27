#!/usr/bin/env python3
"""
Fix vault-root-relative wiki-links that are missing the top-level directory prefix.
e.g. [[BibTeX/INDEX]] -> [[00_KnowledgeFramework/BibTeX/INDEX]]
"""
import os
import re
from path_utils import BASE, SKIP_DIRS, walk_markdown

# Build a reverse index: for each possible path suffix, find the actual full path
# e.g., 'BibTeX/INDEX' -> '00_KnowledgeFramework/BibTeX/INDEX'
suffix_to_full = {}
for root, dirs, files in os.walk(BASE):
    if '.git' in root or '.obsidian' in root or '.ruff_cache' in root or '.opencode' in root:
        continue
    for f in files:
        if f.endswith('.md'):
            full_rel = os.path.relpath(os.path.join(root, f), BASE).replace('\\', '/')[:-3]
            # Register the full path
            parts = full_rel.split('/')
            for i in range(len(parts)):
                suffix = '/'.join(parts[i:])
                if suffix not in suffix_to_full:
                    suffix_to_full[suffix] = full_rel

# Now find and fix all vault-root-relative links
fixes = []  # (filepath, old_link, new_link)

for root, dirs, files in os.walk(BASE):
    if '.git' in root or '.obsidian' in root or '.ruff_cache' in root or '.opencode' in root:
        continue
    for f in files:
        if not f.endswith('.md'):
            continue
        fpath = os.path.join(root, f)
        rel_src = os.path.relpath(fpath, BASE).replace('\\', '/')[:-3]
        
        try:
            with open(fpath, 'r', encoding='utf-8') as fh:
                content = fh.read()
        except:
            continue
        
        new_content = content
        modified = False
        
        for m in re.finditer(r'\[\[([^\]]+?)\]\]', content):
            raw = m.group(1).strip()
            target = raw.split('|')[0].split('#')[0].strip()
            display = raw.split('|')[1] if '|' in raw else None
            
            # Skip: simple names (already handled), dot-prefixed (handled separately)
            if '/' not in target or target.startswith('.'):
                continue
            if target in ('INDEX', 'LearningPath', 'README', '404'):
                continue
            
            # Check if this link as vault-root-relative resolves to a real file
            resolved = target + '.md'
            resolved_path = os.path.normpath(os.path.join(BASE, resolved))
            
            if os.path.exists(resolved_path):
                continue  # Already correct
            
            # The link doesn't resolve from vault root.
            # Try to find the actual file via suffix matching
            if target in suffix_to_full:
                correct_full = suffix_to_full[target]
                
                # Build the replacement
                if display:
                    new_link = f'[[{correct_full}|{display}]]'
                else:
                    new_link = f'[[{correct_full}]]'
                
                old_link = m.group(0)
                
                if old_link in new_content:
                    new_content = new_content.replace(old_link, new_link, 1)
                    modified = True
                    fixes.append((rel_src, target, correct_full))

        if modified:
            # Safety: only write if we have the file
            with open(fpath, 'w', encoding='utf-8') as fh:
                fh.write(new_content)

# Report
if fixes:
    # Deduplicate
    seen = set()
    unique_fixes = []
    for src, old, new in fixes:
        key = (old, new)
        if key not in seen:
            seen.add(key)
            unique_fixes.append((old, new, src))
    
    print(f'Total link fixes applied: {len(fixes)}')
    print(f'Unique link corrections: {len(unique_fixes)}')
    print()
    print('=== Fixes (ordered by path) ===')
    for old, new, src in sorted(unique_fixes, key=lambda x: x[2]):
        print(f'  {old:40s} -> {new}')
        print(f'                         (in {src})')
else:
    print('No fixes needed.')

print(f'\nDone!')
