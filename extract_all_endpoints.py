import re

with open("E:/Thiago/Dev/Mapeamento TCE/tce_bundle.js", "r", encoding="utf-8") as f:
    text = f.read()

# Let's unescape hex like \xE7
def unescape_hex(s):
    return re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), s)

# Find all endpoints: url:"...",type:"...",title:"..."
pattern = re.compile(r'type:\"([a-zA-Z]+)\",url:\"([^\"]+)\"')
matches = pattern.findall(text)
print(f"Total de endpoints encontrados com regex type/url: {len(matches)}")
for mth, url in matches:
    print(f"  [{mth.upper()}] {url}")

if not matches:
    # Try finding url:"..."
    urls = re.findall(r'url:\"([^\"]+)\"', text)
    print(f"Total de URLs encontradas: {len(urls)}")
    for u in urls[:30]:
        print(f"  {u}")
