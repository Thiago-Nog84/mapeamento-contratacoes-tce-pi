# 📌 CHECKPOINT EXECUTIVO — OBSERVATÓRIO DE CONTRATAÇÕES PÚBLICAS & GOVERNANÇA (MPPI)
**Data de Salvamento:** 01/10/2026 — 21:50  
**Repositório Físico:** [`E:\Thiago\Dev\Mapeamento TCE`](file:///E:/Thiago/Dev/Mapeamento%20TCE)  
**Painel Web Interativo:** `http://localhost:5173/` (Vite + React em execução contínua)

---

## 1. 📊 Status Atual do Acervo de Inteligência RAG (10.504 Documentos Indexados)

A meta histórica de cobertura regional foi atingida: **100% dos Ministérios Públicos dos 9 estados da Região Nordeste** estão agora integralmente mapeados, baixados, estruturados e indexados no arquivo mestre [`corpus_ia/indice.jsonl`](file:///E:/Thiago/Dev/Mapeamento%20TCE/corpus_ia/indice.jsonl):

| Instituição / Órgão | Docs Indexados | Âmbito de Mapeamento / UGs | Destaques Técnicos |
| :--- | :---: | :--- | :--- |
| **MPRN (Rio Grande do Norte)** | **2.743** | PGJ Sede e Fundo Especial FRMP | Maior acervo de TRs e atas integradas do Nordeste |
| **TJ-PI (Poder Judiciário)** | **2.178** | Sede (`04101`), CGJ (`04103`), FERMOJUPI (`04105`) | Provimento 13/2025 indexado integralmente (Arts. 46 e 58-59) |
| **MPSE (Sergipe)** | **1.144** | PGJ Sergipe (`CNPJ 13.168.687/0001-10`) | 541 certames mapeados e rito sumário de dispensas por valor |
| **TCE-PI (Controle Externo)** | **1.120** | UO `02101` e `02102` (2023 a 2026) | Precedentes vinculantes, Acórdão 300/2025 e matriz de outliers |
| **MPPI (Órgão Piloto)** | **561** | PGJ e Fundo Especial (FPDC) | 153 certames com pacotes zip descompactados (peças SEI) |
| **MPAL (Alagoas)** | **538** | PGJ Alagoas (`CNPJ 12.472.734/0001-52`) | Mapeamento robusto de obras, engenharia e manutenção predial |
| **MPBA (Bahia)** | **472** | PGJ Bahia (`CNPJ 04.142.491/0001-66`) | Maior volume orçamentário do Nordeste em terceirização |
| **MPDFT (Ramo MPU)** | **435** | `UASG 200009` (2024 a 2026) | Referência nacional em TIC, SLAs e governança ministerial |
| **MPMA (Maranhão)** | **431** | PGJ Maranhão (`CNPJ 05.483.912/0001-85`) | Similaridade logística direta e fronteira geográfica com o MPPI |
| **MPCE (Ceará)** | **322** | PGJ Ceará (`CNPJ 06.928.790/0001-56`) | 198 certames e 75 casos de inexigibilidade para capacitação |
| **MPPB (Paraíba)** | **293** | PGJ Paraíba (`CNPJ 09.284.001/0001-80`) | Referência em transparência de dados abertos e TIC |
| **MPPE (Pernambuco)** | **267** | PGJ Pernambuco (`CNPJ 24.417.065/0001-03`) | Base com dados comparativos de valores orçados vs homologados |
| **TOTAL CONSOLIDADO** | **10.504** | **12 Instituições (100% Nordeste + Judiciário/TCE/MPU)** | **Repositório Nacional de Inteligência** |

---

## 2. 💰 Estudo de Economicidade & Deságio Concluído

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

## 3. 📜 Peças Normativas e Minutas Prontas para o MPPI

O artefato [`caderno_normativo_e_proposicoes_mppi.md`](file:///C:/Users/thiagonogueira/.gemini/antigravity-ide/brain/e5e204f7-b200-42db-83e5-73c4d996ed9e/caderno_normativo_e_proposicoes_mppi.md) contém as três minutas regulamentares estruturadas:
1. **Minuta 1 (Ato PGJ):** Dispensa por Valor (Art. 75, I e II) com rito sumário, dispensa facultativa de ETP e parecer referencial da Assessoria Jurídica (confirmada pelo Art. 46 do Provimento 13/2025 TJ-PI);
2. **Minuta 2 (Ato PGJ):** Inexigibilidade de Capacitação para o CEAF (Art. 74, III, "f") via prospecto público, respaldada pelos 75 precedentes empíricos do MPCE e dezenas do MPMA e MPSE;
3. **Minuta 3 (IN CLC):** Checklist de Governança para Adesão a Atas de Registro de Preços ("Carona"), blindando a instituição conforme o Acórdão 300/2025 - TCE-PI e Arts. 58-59 do Provimento 13/2025 - TJ-PI.

---

## 4. 💻 Estado das Ferramentas
* **Painel Web (Dashboard):** Operando em `http://localhost:5173/` com os 12 órgãos monitorados, ranking de documentos, filtros avançados e aba de economicidade.
* **Integridade dos Dados:** Todos os arquivos físicos, bancos JSON e markdowns preservados na unidade `E:\Thiago\Dev\Mapeamento TCE`.
