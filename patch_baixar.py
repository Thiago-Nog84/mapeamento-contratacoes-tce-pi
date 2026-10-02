import os
import re

with open('src/pncp_client.py', 'r', encoding='utf-8') as f:
    code = f.read()

new_baixar = """
    def baixar_arquivo(self, cnpj: str, ano: int, sequencial: int, sequencial_documento: int, destino: str) -> str:
        url = f"{self.BASE_PNCP}/orgaos/{cnpj}/compras/{ano}/{sequencial}/arquivos/{sequencial_documento}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        for t in range(5):
            try:
                import time
                with urllib.request.urlopen(req, context=self.ctx, timeout=self.timeout) as resp:
                    conteudo = resp.read()
                    os.makedirs(os.path.dirname(destino), exist_ok=True)
                    with open(destino, "wb") as f:
                        f.write(conteudo)
                    return destino
            except urllib.error.HTTPError as e:
                if e.code == 429 or e.code == 403:
                    print(f"      [!] API PNCP bloqueou o download ({e.code}). Aguardando 10s...")
                    time.sleep(10)
                else:
                    raise e
            except Exception as e:
                print(f"      [!] Erro no download PNCP: {e}. Aguardando 5s...")
                time.sleep(5)
        raise Exception(f"Falha ao baixar {url} apois 5 tentativas")
"""

code = re.sub(
    r'    def baixar_arquivo\(self, cnpj: str, ano: int, sequencial: int, sequencial_documento: int, destino: str\) -> str:.*?return destino',
    new_baixar.strip('\n'),
    code,
    flags=re.DOTALL
)

with open('src/pncp_client.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("baixar_arquivo atualizado com retries!")
