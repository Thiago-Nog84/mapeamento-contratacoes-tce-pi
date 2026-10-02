# -*- coding: utf-8 -*-
import re

with open("E:/Thiago/Dev/Mapeamento TCE/tce_bundle.js", "r", encoding="utf-8") as f:
    text = f.read()

def unescape_hex(s):
    return re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), s)

# Find all blocks matching {type:"...",url:"...",title:"...",group:"..."
pattern = re.compile(r'\{type:\"([^\"]+)\",url:\"([^\"]+)\",title:\"([^\"]+)\",group:\"([^\"]+)\"', re.IGNORECASE)
matches = pattern.findall(text)

print(f"Total de endpoints identificados: {len(matches)}")
groups = {}
for mth, url, title, group in matches:
    title_clean = unescape_hex(title)
    group_clean = unescape_hex(group)
    groups.setdefault(group_clean, []).append((mth.upper(), url, title_clean))

for g, items in sorted(groups.items()):
    print(f"\n### Grupo: {g} ({len(items)} endpoints)")
    for mth, url, title in items:
        print(f"  * `[{mth}] {url}`: {title}")
