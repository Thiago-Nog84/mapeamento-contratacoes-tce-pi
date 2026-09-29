# Corpus de Artefatos de Contratacoes Publicas - TCE-PI
## Gerado em: 28/09/2026 15:38

> **Fonte:** PNCP | **Orgao:** TCE-PI | **Total:** 842 documentos
> **Anos cobertos:** 2025 e 2026 | **Contratacoes mapeadas:** 195
> **Finalidade:** Corpus de referencia para estudo e treinamento de IA
> **Base legal:** Lei 14.133/2021 | IN TCE-PI 02/2026 | Portaria CNMP-SG 151/2023

---

## Por Tipo de Artefato

| Tipo de Artefato | Quantidade | % do Corpus |
| :--- | :--- | :--- |
| Ratificacao/Autorizacao | 320 | 38.0% |
| Contrato/Minuta | 178 | 21.1% |
| Termo de Referencia | 145 | 17.2% |
| DFD | 88 | 10.5% |
| ETP | 46 | 5.5% |
| Outros | 36 | 4.3% |
| Edital | 10 | 1.2% |
| Parecer Juridico | 8 | 1.0% |
| Pesquisa de Precos | 6 | 0.7% |
| Mapa de Riscos | 5 | 0.6% |

## Por Modalidade

| Modalidade | Quantidade | % |
| :--- | :--- | :--- |
| Inexigibilidade de Licitação | 490 | 58.2% |
| Dispensa de Licitação | 339 | 40.3% |
| Pregão Eletrônico | 13 | 1.5% |

## Por Ano

| Ano | Documentos | Contratacoes |
| :--- | :--- | :--- |
| 2025 | 269 | 104 |
| 2026 | 573 | 91 |
| **Total** | **842** | **195** |

---

## Estrutura do Corpus

`
corpus_ia/
  ratificacao/  (320 docs)  <- Ratificacao/Autorizacao
  contrato/  (178 docs)  <- Contrato/Minuta
  tr/  (145 docs)  <- Termo de Referencia
  dfd/  ( 88 docs)  <- DFD
  etp/  ( 46 docs)  <- ETP
  outros/  ( 36 docs)  <- Outros
  edital/  ( 10 docs)  <- Edital
  parecer/  (  8 docs)  <- Parecer Juridico
  pesquisa_precos/  (  6 docs)  <- Pesquisa de Precos
  mapa_riscos/  (  5 docs)  <- Mapa de Riscos
  indice.jsonl      <- Indice estruturado JSONL (842 registros)
  dataset.md        <- Este arquivo
`

---

## Como Usar para IA

### RAG (LangChain / LlamaIndex)
`python
from langchain.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
loader = DirectoryLoader('corpus_ia/etp/', glob='*.md', loader_cls=UnstructuredMarkdownLoader)
docs = loader.load()  # Metadados: tipo, modalidade, ano, orgao
`

### Fine-tuning / JSONL
`python
import json
with open('corpus_ia/indice.jsonl') as f:
    dataset = [json.loads(l) for l in f]
# 842 registros com: id, tipo, modalidade, ano, resumo, caminho .md
`

---
*Corpus para uso interno do MPPI. Referencia: TCE-PI.*
