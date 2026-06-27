#!/usr/bin/env python3
"""Update INDEX.md files and create missing ones."""
import os
from path_utils import BASE, SKIP_DIRS, walk_markdown

# 1. Create INDEX for NLP directory
nlp_dir = os.path.join(BASE, '05_ComputerScience', 'ArtificialIntelligence', 'NLP')
os.makedirs(nlp_dir, exist_ok=True)
nlp_files = sorted([f[:-3] for f in os.listdir(nlp_dir) if f.endswith('.md') and f != 'INDEX.md'])
idx = os.path.join(nlp_dir, 'INDEX.md')
with open(idx, 'w', encoding='utf-8') as f:
    f.write('---\n')
    f.write('aliases: [NLP]\n')
    f.write("tags: ['05_ComputerScience', 'ArtificialIntelligence', 'NLP']\n")
    f.write('---\n\n')
    f.write('# 自然语言处理 (NLP)\n\n')
    f.write('> 自然语言处理索引\n\n')
    f.write('## 文件\n\n')
    for name in nlp_files:
        f.write(f'- [[{name}]]\n')
    f.write('\n## 相关条目\n')
    f.write('- [[../INDEX|AI 索引]]\n')
    f.write('- [[../../INDEX|ComputerScience 索引]]\n')
print(f'[INDEX] NLP: {len(nlp_files)} files')

# 2. Update SportsMedicine INDEX to include all content files
sm_dir = os.path.join(BASE, '12_SportsScience', 'SportsMedicine')
sm_files = sorted([f[:-3] for f in os.listdir(sm_dir) if f.endswith('.md') and f not in ('INDEX.md', 'LearningPath.md')])
idx = os.path.join(sm_dir, 'INDEX.md')
with open(idx, 'w', encoding='utf-8') as f:
    f.write('---\n')
    f.write('aliases: [SportsMedicine]\n')
    f.write("tags: ['12_SportsScience', 'SportsMedicine']\n")
    f.write('---\n\n')
    f.write('# SportsMedicine\n\n')
    f.write('运动医学索引，涵盖运动损伤、康复、营养、生物力学等主题。\n\n')
    f.write('## 文件\n\n')
    for name in sm_files:
        desc = name.replace('And', ' & ').replace('In', ' in ')
        f.write(f'- [[{name}]] — {desc}\n')
    f.write('\n## 相关条目\n')
    f.write('- [[../ExercisePhysiology/INDEX|ExercisePhysiology]]\n')
    f.write('- [[../SportsTraining/INDEX|SportsTraining]]\n')
    f.write('- [[../INDEX|SportsScience 索引]]\n')
print(f'[INDEX] SportsMedicine: {len(sm_files)} files')

# 3. Update SportsTraining INDEX
st_dir = os.path.join(BASE, '12_SportsScience', 'SportsTraining')
st_files = sorted([f[:-3] for f in os.listdir(st_dir) if f.endswith('.md') and f not in ('INDEX.md', 'LearningPath.md')])
idx = os.path.join(st_dir, 'INDEX.md')
with open(idx, 'w', encoding='utf-8') as f:
    f.write('---\n')
    f.write('aliases: [SportsTraining]\n')
    f.write("tags: ['12_SportsScience', 'SportsTraining']\n")
    f.write('---\n\n')
    f.write('# SportsTraining\n\n')
    f.write('运动训练索引，涵盖训练理论、方法、周期化和专项训练。\n\n')
    f.write('## 文件\n\n')
    for name in st_files:
        f.write(f'- [[{name}]]\n')
    f.write('\n## 相关条目\n')
    f.write('- [[../ExercisePhysiology/INDEX|ExercisePhysiology]]\n')
    f.write('- [[../SportsMedicine/INDEX|SportsMedicine]]\n')
    f.write('- [[../INDEX|SportsScience 索引]]\n')
print(f'[INDEX] SportsTraining: {len(st_files)} files')

# 4. Update ManagementScienceAndEngineering INDEX
ms_dir = os.path.join(BASE, '11_ManagementSciences', 'ManagementScienceAndEngineering')
ms_files = sorted([f[:-3] for f in os.listdir(ms_dir) if f.endswith('.md') and f not in ('INDEX.md', 'LearningPath.md')])
idx = os.path.join(ms_dir, 'INDEX.md')
with open(idx, 'w', encoding='utf-8') as f:
    f.write('---\n')
    f.write('aliases: [ManagementScienceAndEngineering]\n')
    f.write("tags: ['11_ManagementSciences', 'ManagementScienceAndEngineering']\n")
    f.write('---\n\n')
    f.write('# 管理科学与工程\n\n')
    f.write('管理科学与工程索引。\n\n')
    f.write('## 文件\n\n')
    for name in ms_files:
        f.write(f'- [[{name}]]\n')
    f.write('\n## 相关条目\n')
    f.write('- [[../INDEX|Management 索引]]\n')
print(f'[INDEX] ManagementScienceAndEngineering: {len(ms_files)} files')

print('\nDone!')
