import os

with open('src/pncp_client.py', 'r', encoding='utf-8') as f:
    code = f.read()

new_get = """
    import time
    def _get(self, url: str) -> Any:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Accept": "application/json"
            }
        )
        for t in range(5):
            try:
                with urllib.request.urlopen(req, context=self.ctx, timeout=self.timeout) as resp:
                    return json.loads(resp.read().decode('utf-8'))
            except urllib.error.HTTPError as e:
                if e.code == 429 or e.code == 403:
                    print(f"      [!] API PNCP bloqueou ({e.code}). Aguardando 10s...")
                    self.time.sleep(10)
                else:
                    return {}
            except Exception as e:
                print(f"      [!] Erro PNCP: {e}. Aguardando 5s...")
                self.time.sleep(5)
        return {}
"""

# Replace the original _get method
code = code.replace(
"""    def _get(self, url: str) -> Any:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Accept": "application/json"
            }
        )
        with urllib.request.urlopen(req, context=self.ctx, timeout=self.timeout) as resp:
            return json.loads(resp.read().decode('utf-8'))""", new_get.strip())

code = code.replace("import ssl\n", "import ssl\nimport time\n")
code = code.replace("self.time.sleep", "time.sleep")

with open('src/pncp_client.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("pncp_client.py atualizado com retry e sleep")
