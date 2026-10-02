import sys

sys.stdout.reconfigure(encoding='utf-8')

checkpoint_path = r"E:\Thiago\Dev\Mapeamento TCE\CHECKPOINT_PROJETO.md"

novo_checkpoint = """# 📌 CHECKPOINT EXECUTIVO — OBSERVATÓRIO DE CONTRATAÇÕES PÚBLICAS & GOVERNANÇA (MPPI)
**Data de Salvamento:** 02/10/2026 — 07:40  
**Repositório Físico:** [`E:\\Thiago\\Dev\\Mapeamento TCE`](file:///E:/Thiago/Dev/Mapeamento%20TCE)  
**Painel Web Interativo:** `http://localhost:5173/` (Vite + React em execução contínua com nova aba de Controle)

---

## 1. 📊 Status Atual do Acervo de Inteligência RAG (10.504 Documentos Indexados)

A meta histórica de cobertura regional foi atingida: **100% dos Ministérios Públicos dos 9 estados da Região Nordeste** estão agora integralmente mapeados, baixados, estruturados e indexados no arquivo mestre [`corpus_ia/indice.jsonl`](file:///E:/Thiago/Dev/Mapeamento%20TCE/corpus_ia/indice.jsonl):

| Instituição / Órgão | Docs Indexados | Âmbito de Mapeamento / UGs | Destaques Técnicos |
| :--- | :---: | :--- | :--- |
| **MPRN (Rio Grande do Norte)** | **2.743** | PGJ Sede e Fundo Especial FRMP | Maior acervo de TRs, pareceres e atas integradas do Nordeste |
| **TJ-PI (Poder Judiciário)** | **2.178** | Sede (`04101`), CGJ (`04103`), FERMOJUPI (`04105`) | Provimento 13/2025 indexado integralmente (Arts. 46 e 58-59) |
| **MPSE (Sergipe)** | **1.144** | PGJ Sergipe (`CNPJ 13.168.687/0001-10`) | 541 certames mapeados e rito sumário de dispensas por valor |
| **TCE-PI (Controle Externo)** | **1.120** | UO `02101` e `02102` (2023 a 2026) | Precedentes vinculantes, Acórdão 300/2025 e matriz de outliers |
| **MPPI (Órgão Piloto)** | **561** | PGJ e Fundo Especial (FPDC) | 153 certames com pacotes zip descompactados (peças SEI) |
| **MPAL (Alagoas)** | **538** | PGJ Alagoas (`CNPJ 12.472.734/0001-52`) | Mapeamento robusto de obras, engenharia e manutenção predial |
| **MPBA (Bahia)** | **472** | PGJ Bahia (`CNPJ 04.142.491/0001-66`) | Maior volume orçamentário do Nordeste em terceirização e pareceres |
| **MPDFT (Ramo MPU)** | **435** | `UASG 200009` (2024 a 2026) | Referência nacional em TIC, SLAs e governança ministerial |
| **MPMA (Maranhão)** | **431** | PGJ Maranhão (`CNPJ 05.483.912/0001-85`) | Similaridade logística direta e fronteira geográfica com o MPPI |
| **MPCE (Ceará)** | **322** | PGJ Ceará (`CNPJ 06.928.790/0001-56`) | 198 certames e 75 casos de inexigibilidade para capacitação |
| **MPPB (Paraíba)** | **293** | PGJ Paraíba (`CNPJ 09.284.001/0001-80`) | Referência em transparência de dados abertos e TIC |
| **MPPE (Pernambuco)** | **267** | PGJ Pernambuco (`CNPJ 24.417.065/0001-03`) | Base com dados comparativos de valores orçados vs homologados |
| **TOTAL CONSOLIDADO** | **10.504** | **12 Instituições (100% Nordeste + Judiciário/TCE/MPU)** | **Repositório Nacional de Inteligência** |

---

## 2. 🛡️ Estudo de Controle Interno e Jurídico Concluído (Art. 169 e Art. 53 da Lei 14.133/21)

Consolidado no artefato [`estudo_controle_interno_e_juridico.md`](file:///C:/Users/thiagonogueira/.gemini/antigravity-ide/brain/e5e204f7-b200-42db-83e5-73c4d996ed9e/estudo_controle_interno_e_juridico.md) e na nova aba **"Controle Interno & Jurídico"** do Dashboard:
* **Instrumentos Mapeados:**
  * **662 Pareceres Jurídicos** analisados (MPRN 390, TCE-PI 78, MPSE 62, MPBA 49, MPPI 24, MPDFT 22, MPAL 16, MPCE 13, TJPI 8);
  * **146 Matrizes e Mapas de Risco Estruturados** (74% em TIC e Soluções em Nuvem, 15,1% em Serviços Terceirizados Contínuos);
  * **451 DFDs / Instrumentos de Demanda** (1ª Linha);
  * **31 Pareceres Referenciais e Minutas Padronizadas**.
* **Arquitetura das 3 Linhas de Defesa (Art. 169):**
  * **1ª Linha (Operacional):** Setores demandantes, equipe de planejamento (DFD/ETP/TR), pregoeiros e fiscais de contrato com foco em IMR/SLA;
  * **2ª Linha (Supervisão & Legalidade):** CLC, Assessoria Jurídica (Art. 53), Governança e DEPLAN;
  * **3ª Linha (Auditoria Independente):** Auditoria Interna (SECON) e TCE-PI.
* **Top 6 Ressalvas Jurídicas Recorrentes:**
  1. *Pesquisa de Preços (IN 65/2021)* — Exigência de cesta de fontes e saneamento fundamentado de outliers (84% dos casos);
  2. *Adequação Orçamentária (Arts. 16 e 17 LRF)* — Declaração formal e reserva orçamentária prévia (72%);
  3. *Qualificação Técnica (Art. 67)* — Vedação a exigências restritivas e teto de 50% para parcelas relevantes (68%);
  4. *Justificativa de Preço e Não Fracionamento (Arts. 72 e 75)* — Controle de limites de dispensa por ramo (91%);
  5. *Matriz de Riscos (Art. 22 e 103)* — Alocação objetiva de encargos e riscos extraordinários (65%);
  6. *IMR & Glosas* — Vinculação de desembolsos a métricas de SLA com previsão expressa de retenções (58%).
* **Minutas de Pareceres Jurídicos Referenciais (Art. 53, § 5º):**
  * **PR 01/2026:** Dispensa por Valor (Art. 75, I e II);
  * **PR 02/2026:** Prorrogação Ordinária de Serviços Contínuos (Art. 106/107);
  * **PR 03/2026:** Apostilamento de Reajuste por Índice Oficial.
* **Master Checklist de Conformidade da Instrução Processual:** 15 itens essenciais com interatividade e barra de progresso no painel web.

---

## 3. 💰 Estudo de Economicidade & Deságio Concluído

Consolidado no artefato [`estudo_economicidade_mppe_mppi.md`](file:///C:/Users/thiagonogueira/.gemini/antigravity-ide/brain/e5e204f7-b200-42db-83e5-73c4d996ed9e/estudo_economicidade_mppe_mppi.md) e na aba dedicada do Dashboard:
* **Total Orçado Analisado:** R$ 341.262.169,56
* **Total Homologado Final:** R$ 272.403.233,78
* **Economia Gerada:** **R$ 68.858.935,79** aos cofres públicos
* **Deságio Médio Global:** **20,18%** (faixa de maturidade internacional)
* **Parâmetros Setoriais para a CLC/MPPI:**
  * **TIC / Licenças:** Deságio médio de **25,32%** (serve como parâmetro de vantajosidade na Carona);
  * **Mão de Obra Terceirizada:** Deságio de **13,14%** (alerta de risco: descontos acima de 20% exigem diligência de exequibilidade);
  * **Obras / Manutenção Predial:** Deságio de **10,58%**;
  * **Mobiliário:** Deságio de **28,05%**.

---

## 4. 📜 Peças Normativas e Minutas Prontas para o MPPI

O artefato [`caderno_normativo_e_proposicoes_mppi.md`](file:///C:/Users/thiagonogueira/.gemini/antigravity-ide/brain/e5e204f7-b200-42db-83e5-73c4d996ed9e/caderno_normativo_e_proposicoes_mppi.md) contém as três minutas regulamentares estruturadas:
1. **Minuta 1 (Ato PGJ):** Dispensa por Valor (Art. 75, I e II) com rito sumário, dispensa facultativa de ETP e parecer referencial da Assessoria Jurídica;
2. **Minuta 2 (Ato PGJ):** Inexigibilidade de Capacitação para o CEAF (Art. 74, III, "f") via prospecto público, respaldada pelos 75 precedentes empíricos do MPCE e dezenas do MPMA e MPSE;
3. **Minuta 3 (IN CLC):** Checklist de Governança para Adesão a Atas de Registro de Preços ("Carona"), blindando a instituição conforme o Acórdão 300/2025 - TCE-PI e Arts. 58-59 do Provimento 13/2025 - TJ-PI.

---

## 5. 💻 Estado das Ferramentas
* **Painel Web (Dashboard):** Operando em `http://localhost:5173/` com 6 abas integradas:
  1. *Visão Geral (12 Instituições & 10.504 Documentos)*;
  2. *Economicidade & Deságio (R$ 341M Analisados e Deságio por Setor)*;
  3. *Controle Interno & Jurídico (3 Linhas de Defesa, 662 Pareceres, 146 Riscos, Modelos Referenciais e Checklist)*;
  4. *Minutas & Proposições Normativas MPPI*;
  5. *Checklist Carona (Acórdão 300/2025 TCE-PI)*;
  6. *Explorador Semântico RAG*.
* **Integridade dos Dados:** Todos os arquivos físicos, bancos JSON e markdowns preservados na unidade `E:\\Thiago\\Dev\\Mapeamento TCE`.
"""

with open(checkpoint_path, 'w', encoding='utf-8') as f:
    f.write(novo_checkpoint)

print("CHECKPOINT_PROJETO.md atualizado com sucesso no drive E:!")
