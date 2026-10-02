# Corpus de Artefatos de Contratacoes Publicas - TCE-PI
## Gerado em: 29/09/2026 11:18

> **Fonte:** PNCP | **Orgao:** TCE-PI | **Total:** 842 documentos
> **Anos cobertos:** 2025 e 2026 | **Contratacoes mapeadas:** 195
> **Finalidade:** Corpus de referencia para estudo e treinamento de IA
> **Base legal:** Lei 14.133/2021 | IN TCE-PI 02/2026 | Portaria CNMP-SG 151/2023

---

## Por Tipo de Artefato

| Tipo de Artefato | Quantidade | % do Corpus |
| :--- | :--- | :--- |
| Ratificacao/Autorizacao | 447 | 36.6% |
| Termo de Referencia | 232 | 19.0% |
| Contrato/Minuta | 217 | 17.8% |
| DFD | 120 | 9.8% |
| ETP | 81 | 6.6% |
| Outros | 55 | 4.5% |
| Pesquisa de Precos | 23 | 1.9% |
| Parecer Juridico | 17 | 1.4% |
| Edital | 14 | 1.1% |
| Mapa de Riscos | 14 | 1.1% |

## Por Modalidade

| Modalidade | Quantidade | % |
| :--- | :--- | :--- |
| Inexigibilidade de Licitação | 490 | 40.2% |
| None | 378 | 31.0% |
| Dispensa de Licitação | 339 | 27.8% |
| Pregão Eletrônico | 13 | 1.1% |

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
  ratificacao/  (447 docs)  <- Ratificacao/Autorizacao
  tr/  (232 docs)  <- Termo de Referencia
  contrato/  (217 docs)  <- Contrato/Minuta
  dfd/  (120 docs)  <- DFD
  etp/  ( 81 docs)  <- ETP
  outros/  ( 55 docs)  <- Outros
  pesquisa_precos/  ( 23 docs)  <- Pesquisa de Precos
  parecer/  ( 17 docs)  <- Parecer Juridico
  edital/  ( 14 docs)  <- Edital
  mapa_riscos/  ( 14 docs)  <- Mapa de Riscos
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
