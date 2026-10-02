# -*- coding: utf-8 -*-
import re

with open("E:/Thiago/Dev/Mapeamento TCE/main-capture.js", "w", encoding="utf-8") as f:
    pass # placeholder

import urllib.request, ssl
ctx = ssl._create_unverified_context()
url = "https://portal.tce.pi.gov.br/capture/main-es2015.2133e33da242ef436728.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
content = urllib.request.urlopen(req, context=ctx).read().decode("utf-8", "ignore")

# Find occurrences of api-capture
for match in re.finditer(r'api-capture', content):
    start = max(0, match.start() - 100)
    end = min(len(content), match.end() + 200)
    print("--- SNIPPET ---")
    print(content[start:end])
