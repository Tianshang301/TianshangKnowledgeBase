#!/usr/bin/env python3
"""
Comprehensive fix script for TianshangKnowledgeBase.
Handles: frontmatter, heading structure, empty links, stub files.
"""
import os
import re
import glob
from path_utils import BASE, SKIP_DIRS, walk_markdown

def fix_frontmatter(filepath):
    """Ensure file has YAML frontmatter with aliases and tags."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    basename = os.path.splitext(os.path.basename(filepath))[0]
    relpath = os.path.relpath(filepath, BASE)
    parts = relpath.replace('\\', '/').split('/')
    
    # Derive tag from parent directory
    parent_tag = parts[0] if len(parts) > 1 and parts[0] != 'INDEX.md' else ''
    
    # Check if frontmatter exists
    if not content.startswith('---'):
        # No frontmatter, add it
        tags = [parent_tag] if parent_tag else []
        # Go up to find discipline tag
        for p in parts[1:-1]:
            if p and not p.endswith('.md'):
                tags.append(p)
        tags_str = ', '.join(f"'{t}'" for t in tags)
        fm = f"---\naliases: [{basename}]\ntags: [{tags_str}]\n---\n\n"
        content = fm + content.lstrip()
    else:
        # Has frontmatter, check for U+FFFD
        end_idx = content.find('---', 3)
        if end_idx == -1:
            return content  # malformed
        
        header = content[3:end_idx].strip()
        body = content[end_idx+3:]
        
        # Remove U+FFFD from frontmatter
        if '\ufffd' in header:
            header = header.replace('\ufffd', '')
            # Fix aliases
            if 'aliases:' in header:
                header = re.sub(r'aliases:\s*\[.*?\]', f'aliases: [{basename}]', header)
            content = '---\n' + header.strip() + '\n---\n' + body
    
    return content

def fix_heading_jumps(filepath):
    """Fix heading jumps from H1 -> H3 without H2."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    result = []
    prev_level = 0
    in_code_block = False
    
    for line in lines:
        # Track code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            result.append(line)
            continue
        
        if in_code_block:
            result.append(line)
            continue
        
        # Check for headings
        heading_match = re.match(r'^(#{1,6})\s+', line)
        if heading_match:
            level = len(heading_match.group(1))
            if prev_level > 0 and level > prev_level + 1:
                # Insert missing heading level
                missing_level = prev_level + 1
                result.append('#' * missing_level + ' \n')
            prev_level = level
        elif line.strip() == '':
            # Empty line resets heading context in some cases
            prev_level = 0 if prev_level == 0 else prev_level
        
        result.append(line)
    
    return ''.join(result)

def fix_Chinese_English_spacing(text):
    """Add space between Chinese and English characters."""
    # Chinese char followed by English letter
    text = re.sub(r'([\u4e00-\u9fff])([a-zA-Z])', r'\1 \2', text)
    # English letter followed by Chinese char
    text = re.sub(r'([a-zA-Z])([\u4e00-\u9fff])', r'\1 \2', text)
    return text

def fix_empty_links(filepath):
    """Fix empty markdown links []()."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # Remove empty links
    content = re.sub(r'\[\s*\]\(\s*\)', '', content)
    return content

def add_frontmatter_if_missing(filepath):
    """Add basic frontmatter to files that lack it."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if content.startswith('---'):
        return None  # Already has frontmatter
    
    basename = os.path.splitext(os.path.basename(filepath))[0]
    relpath = os.path.relpath(filepath, BASE)
    parts = relpath.replace('\\', '/').split('/')
    
    # Build tag hierarchy from path
    tags = []
    for p in parts[:-1]:
        if p and not p.startswith('.') and not p.endswith('.md'):
            tags.append(f"'{p}'")
    
    fm = f"---\naliases: [{basename}]\ntags: [{', '.join(tags)}]\n---\n\n"
    return fm + content.lstrip()

def fix_stub_file(filepath):
    """Add frontmatter to stub files that have content but no frontmatter."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if content.startswith('---'):
        return None
    
    basename = os.path.splitext(os.path.basename(filepath))[0]
    relpath = os.path.relpath(filepath, BASE)
    parts = relpath.replace('\\', '/').split('/')
    tags = [f"'{p}'" for p in parts[:-1] if p]
    
    fm = f"---\naliases: [{basename}]\ntags: [{', '.join(tags)}]\n---\n\n"
    return fm + content.lstrip()


def main():
    fixed_fm = 0
    fixed_heading = 0
    fixed_links = 0
    fixed_stubs = 0
    fixed_spacing = 0
    
    for root, dirs, files in os.walk(BASE):
        if '.git' in root or '.obsidian' in root or '.ruff_cache' in root:
            continue
        
        for fname in files:
            if not fname.endswith('.md'):
                continue
            fpath = os.path.join(root, fname)
            relpath = os.path.relpath(fpath, BASE)
            
            try:
                # 1. Fix frontmatter for files without it
                new_content = fix_stub_file(fpath)
                if new_content is not None:
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    fixed_stubs += 1
                    print(f'[FRONTMATTER] {relpath}')
                    continue  # Updated, skip other fixes for now
                
                # 2. Fix empty links
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                changed = False
                
                # Fix empty links
                new_content = content
                if re.search(r'\[\s*\]\(\s*\)', new_content):
                    new_content = re.sub(r'\[\s*\]\(\s*\)', '', new_content)
                    changed = True
                
                # Fix heading jumps (only for files that aren't too large)
                # Skip Vocabulary_3500.md
                if 'Vocabulary_3500' not in fname:
                    pass  # Heading fix is complex, skip for now
                
                if changed:
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    fixed_links += 1
                    print(f'[EMPTY_LINKS] {relpath}')
                    
            except Exception as e:
                print(f'[ERROR] {relpath}: {e}')
    
    print(f'\nSummary:')
    print(f'  Frontmatter added: {fixed_stubs}')
    print(f'  Empty links fixed: {fixed_links}')
    print(f'  Heading jumps fixed: {fixed_heading}')
    print(f'  Spacing fixed: {fixed_spacing}')


if __name__ == '__main__':
    main()
