import os

root = r"F:\TianshangKnowledgeBase"

# (garbled, correct) pairs - garbled text produced by encoding chain errors
REPLACEMENTS = [
    ("鐩稿叧鏉＄洰", "相关条目"),  # 相关条目 (UTF-8 bytes read as GBK)
    ("鐩稿叧", "相关"),              # 相关
    ("鏉＄洰", "条目"),              # 条目
    ("绱㈠紩", "索引"),              # 索引 (GBK bytes read as UTF-8)
    # Euro sign in place of Chinese punctuation
    ("€€", "——"),                    # em dash pairs
    ("€", "、"),                      # Chinese enumeration comma
]

count = 0
for dirpath, dirnames, filenames in os.walk(root):
    for f in filenames:
        if not f.endswith(".md"):
            continue
        path = os.path.join(dirpath, f)
        try:
            with open(path, "r", encoding="utf-8") as fh:
                content = fh.read()
        except Exception:
            continue
        changed = False
        for garbled, correct in REPLACEMENTS:
            if garbled in content:
                content = content.replace(garbled, correct)
                changed = True
        if changed:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(content)
            count += 1
print(f"Fixed {count} files")
