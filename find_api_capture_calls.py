# -*- coding: utf-8 -*-
import urllib.request, ssl, re

ctx = ssl._create_unverified_context()
url = "https://portal.tce.pi.gov.br/capture/main-es2015.2133e33da242ef436728.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
content = urllib.request.urlopen(req, context=ctx).read().decode("utf-8", "ignore")

# Find template strings or concatenations with apiUrl
endpoints = set(re.findall(r'apiUrl\s*\+\s*[`\'\"]([^\`\'\"]+)[`\'\"]', content))
print("Endpoints concatenados com apiUrl:")
for ep in sorted(endpoints):
    print("  ->", ep)

# Also check backtick template literals `${...apiUrl}...`
template_literals = set(re.findall(r'`\$\{.*?apiUrl\}([^`]+)`', content))
print("\nTemplate literals com apiUrl:")
for tl in sorted(template_literals):
    print("  ->", tl)
