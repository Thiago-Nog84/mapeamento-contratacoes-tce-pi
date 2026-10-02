# -*- coding: utf-8 -*-
import urllib.request, ssl, re

ctx = ssl._create_unverified_context()
url = "https://portal.tce.pi.gov.br/capture/main-es2015.2133e33da242ef436728.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
content = urllib.request.urlopen(req, context=ctx).read().decode("utf-8", "ignore")

# Find occurrences of 'get(' or 'post('
calls = re.findall(r'\.(get|post)\s*<[^>]+>\s*\(\s*[`\'\"]([^\`\'\"]+)[`\'\"]', content)
print(f"Chamadas HTTP encontradas: {len(calls)}")
for mth, endpoint in sorted(set(calls))[:30]:
    print(f"  [{mth.upper()}] {endpoint}")
