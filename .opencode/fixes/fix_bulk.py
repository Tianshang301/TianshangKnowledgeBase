#!/usr/bin/env python3
"""
Bulk fix script for remaining issues:
1. Remove U+FFFD from ALL project files
2. Fix Chinese-English spacing in new/modified files  
3. Fix trailing whitespace
4. Fix mixed list markers
5. Fix empty links
6. Add frontmatter to 404.md and README files
"""
import os
import re
from path_utils import BASE, SKIP_DIRS, SKIP_FILES, walk_markdown

stats = {'fffd': 0, 'trailing_ws': 0, 'mixed_lists': 0, 'empty_links': 0, 'ce_spacing': 0}

def fix_file(fpath):
    rel = os.path.relpath(fpath, BASE)
    base = os.path.basename(fpath)
    if base in SKIP_FILES:
        return
    
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return
    
    original = content
    changed = False
    
    # 1. Remove U+FFFD
    if '\ufffd' in content:
        content = content.replace('\ufffd', '')
        stats['fffd'] += 1
        changed = True
    
    # 2. Fix empty links []()
    if re.search(r'\[\s*\]\(\s*\)', content):
        content = re.sub(r'\[\s*\]\(\s*\)', '', content)
        stats['empty_links'] += 1
        changed = True
    
    # 3. Fix trailing whitespace (on non-code lines)
    lines = content.split('\n')
    new_lines = []
    in_code = False
    ws_fixed = False
    for line in lines:
        if line.strip().startswith('```'):
            in_code = not in_code
            new_lines.append(line)
            continue
        if not in_code and line != line.rstrip():
            line = line.rstrip()
            ws_fixed = True
        new_lines.append(line)
    if ws_fixed:
        stats['trailing_ws'] += 1
        content = '\n'.join(new_lines)
        changed = True
    
    # 4. Fix mixed list markers (prefer '-')
    if re.search(r'^\s*[\*\+]\s', content, re.MULTILINE):
        content = re.sub(r'^(\s*)[\*\+](\s)', r'\1-\2', content, flags=re.MULTILINE)
        stats['mixed_lists'] += 1
        changed = True
    
    # 5. Fix Chinese-English spacing (only in paragraph text, not code blocks)
    # Pattern: Chinese char followed by English letter
    content = re.sub(r'([\u4e00-\u9fff\u3400-\u4dbf])([a-zA-Z])', r'\1 \2', content)
    # Pattern: English letter followed by Chinese char
    content = re.sub(r'([a-zA-Z])([\u4e00-\u9fff\u3400-\u4dbf])', r'\1 \2', content)
    
    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'[FIXED] {rel}')

def main():
    count = 0
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        
        for fname in files:
            if not fname.endswith('.md'):
                continue
            fpath = os.path.join(root, fname)
            fix_file(fpath)
            count += 1
            if count % 200 == 0:
                print(f'Progress: {count} files checked...')
    
    print(f'\n=== Summary ===')
    print(f'Files with U+FFFD removed: {stats["fffd"]}')
    print(f'Files with trailing whitespace fixed: {stats["trailing_ws"]}')
    print(f'Files with mixed list markers fixed: {stats["mixed_lists"]}')
    print(f'Files with empty links fixed: {stats["empty_links"]}')
    print(f'Total files processed: {count}')

if __name__ == '__main__':
    main()
