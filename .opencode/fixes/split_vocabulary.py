#!/usr/bin/env python3
"""
Split Vocabulary_3500.md into 1 alphabetical file + 4 thematic files.
Original file is NOT modified.
"""
import os
from path_utils import BASE, SKIP_DIRS, walk_markdown
SRC = os.path.join(BASE, r'01_K12\SeniorHigh\English\Vocabulary_3500.md')
DST_DIR = os.path.dirname(SRC)

with open(SRC, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Section boundary line numbers (0-indexed) from the original:
# L15: 人与自我, L1757: 人与社会, L3929: 人与自然, L5069: 功能词汇
SECTION_DEFS = [
    (15, 1756, 'Vocabulary_PersonalLife', '人与自我 (Personal Life)',
     ['01_K12', 'SeniorHigh', 'English', 'Vocabulary_PersonalLife'],
     '人与自我的核心词汇，涵盖个人身份、情感态度、学习工作、日常生活、身心健康等主题。'),
    (1757, 3928, 'Vocabulary_Society', '人与社会 (Society & Communication)',
     ['01_K12', 'SeniorHigh', 'English', 'Vocabulary_Society'],
     '人与社会的核心词汇，涵盖人际关系、职业文化、科技历史、语言文学等主题。'),
    (3929, 5068, 'Vocabulary_Nature', '人与自然 (Nature & Environment)',
     ['01_K12', 'SeniorHigh', 'English', 'Vocabulary_Nature'],
     '人与自然的核心词汇，涵盖自然环保、健康医疗、动植物、宇宙太空等主题。'),
    (5069, 5964, 'Vocabulary_FunctionWords', '功能词汇 (Function Words)',
     ['01_K12', 'SeniorHigh', 'English', 'Vocabulary_FunctionWords'],
     '功能词汇，涵盖动词短语、连接词、介词冠词、高频副词、情态动词等。'),
]

def extract_rows(lines):
    """Extract table rows from a list of lines."""
    rows = []
    for line in lines:
        s = line.strip()
        if s.startswith('| ') and '---' not in s and len(s) > 5:
            first_cell = s.split('|')[1].strip()
            if first_cell and first_cell[0].isalpha():
                rows.append((first_cell.lower(), s))
    return rows

def write_thematic_file(short_name, title, tags, desc, rows):
    fname = short_name + '.md'
    fpath = os.path.join(DST_DIR, fname)
    out = []
    out.append('---')
    out.append(f'aliases: [{short_name}]')
    tag_str = ', '.join(["'" + t + "'" for t in tags])
    out.append(f'tags: [{tag_str}]')
    out.append('---')
    out.append('')
    out.append(f'# {title}')
    out.append('')
    out.append(f'> {desc}')
    out.append('')
    out.append('| 单词 | 音标 | 词性 | 释义 | 搭配 |')
    out.append('|------|------|------|------|------|')
    for _, row in rows:
        out.append(row)
    out.append('')
    out.append('## 相关条目')
    out.append('- [[Vocabulary_3500_Alphabetical|词汇完整表（字母序）]]')
    for other in ['Vocabulary_PersonalLife', 'Vocabulary_Society', 'Vocabulary_Nature', 'Vocabulary_FunctionWords']:
        if other != short_name:
            out.append(f'- [[{other}]]')
    out.append('- [[../INDEX|SeniorHigh 索引]]')
    out.append('- [[../../INDEX|01_K12 索引]]')
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out) + '\n')
    print(f'[CREATED] {fname} ({len(rows)} entries)')

# Extract ALL rows from entire file
print('Extracting all vocabulary rows...')
all_rows = []
for start, end, short_name, _, _, _ in SECTION_DEFS:
    section_rows = extract_rows(lines[start+1:end])
    all_rows.extend(section_rows)

# Remove duplicates (keep first occurrence)
seen = set()
unique_rows = []
for key, row in all_rows:
    if key not in seen:
        seen.add(key)
        unique_rows.append((key, row))

# Sort alphabetically
unique_rows.sort(key=lambda x: x[0])
print(f'Total unique entries: {len(unique_rows)}')

# --- Create alphabetical master file ---
print('\n=== Creating alphabetical master: Vocabulary_3500_Alphabetical.md ===')
out = []
out.append('---')
out.append('aliases: [Vocabulary_3500_Alphabetical]')
out.append("tags: ['01_K12', 'SeniorHigh', 'English']")
out.append('---')
out.append('')
out.append('# 高中英语 · 新课标 3500 词汇（字母序全表）')
out.append('')
out.append('> 按字母顺序排列的完整高考词汇表。按主题分类请参见各主题分册。')
out.append('')
out.append('| 单词 | 音标 | 词性 | 释义 | 搭配 |')
out.append('|------|------|------|------|------|')
for _, row in unique_rows:
    out.append(row)
out.append('')
out.append('## 相关条目')
for _, _, short_name, title, _, _ in SECTION_DEFS:
    out.append(f'- [[{short_name}|{title.split()[0]}]]')
out.append('- [[Vocabulary_3500|原始主题分组表]]')
out.append('- [[../INDEX|SeniorHigh 索引]]')
out.append('- [[../../INDEX|01_K12 索引]]')

alf_path = os.path.join(DST_DIR, 'Vocabulary_3500_Alphabetical.md')
with open(alf_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(out) + '\n')
print(f'[CREATED] Vocabulary_3500_Alphabetical.md ({len(unique_rows)} entries)')

# --- Create 4 thematic files ---
print('\n=== Creating 4 thematic files ===')
for start, end, short_name, title, tags, desc in SECTION_DEFS:
    section_rows = extract_rows(lines[start+1:end])
    write_thematic_file(short_name, title, tags, desc, section_rows)

print('\nDone! Original Vocabulary_3500.md unchanged.')
