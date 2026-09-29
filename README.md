# Mapeamento do Ecossistema de Contratacoes Publicas - TCE-PI

Este projeto implementa uma solucao completa e automatizada para mapear, extrair e catalogar os **procedimentos licitatorios**, os **artefatos documentais** (editais, projetos basicos, termos de referencia, minutas) e os **normativos** regulamentares do Tribunal de Contas do Estado do Piaui (TCE-PI).

**Objetivo estrategico:** Utilizar o TCE-PI como **orgao de referencia** (enquanto fiscalizador modelo) para subsidiar o aprimoramento dos processos de contratacao do **Ministerio Publico do Estado do Piaui (MPPI)**.

---

## 1. Arquitetura do Ecossistema TCE-PI

O fluxo de contratacoes publicas do Piaui e composto pela integracao entre os sistemas internos e murais publicos do Tribunal:

```
[Jurisdicionados / UGs]
         |
         +---> [Licitacoes Web (/licitacoesweb)] ---> [Muralic (/muralic)] ---> API /portaldacidadania
         |        (Fase Externa / Procedimento)         (Mural de Licitacoes)
         |
         +---> [Contratos Web (/contratosweb)]   ---> [Muralcon (/muralcon)] ---> Sagres / Despesas
                  (Contratos, Aditivos, Rescisoes)      (Mural de Contratos)
```

1. **Licitacoes Web (`/licitacoesweb`)**: Modulo de alimentacao obrigatoria onde os orgaos cadastram o procedimento, datas, lotes, responsaveis e enviam os arquivos.
2. **Mural de Licitacoes - Muralic (`/muralic`)**: Portal publico de transparencia das licitacoes e seus respectivos anexos e artefatos.
3. **Contratos Web / Muralcon**: Gestao de contratos, termos aditivos e contratacoes diretas (dispensas e inexigibilidades).
4. **API Portal da Cidadania**: Camada REST documentada em `/api/portaldacidadania/docs/`.

---

## 2. Mapeamento do Proprio TCE-PI (Orgao Contratante)

O Tribunal de Contas do Estado do Piaui atua como orgao contratante atraves de duas Unidades Gestoras:
* **UG `020101`**: Tribunal de Contas do Estado (TCE)
* **UG `020102`**: Fundo de Modernizacao do Tribunal de Contas (FMTC)

```bash
python mapear_tce_pi.py --limite 10
python mapear_tce_pi.py --download
```

---

## 3. Integracao com a API do PNCP

O TCE-PI (CNPJ `05.818.935/0001-01`) publica obrigatoriamente no PNCP todas as suas contratacoes sob a Lei n. 14.133/2021.

```bash
python mapear_pncp_tce.py --ano 2026 --download
python mapear_pncp_tce.py --ano 2025 --download
```

Arquivos gerados:
* `contratacoes_tce_pncp_2026.json` -- 91 contratacoes de 2026
* `contratacoes_tce_pncp_2025.json` -- 104 contratacoes de 2025

---

## 4. Corpus IA -- Extracao de Artefatos em Markdown

O script `analisar_pdfs.py` processa todos os PDFs baixados do PNCP, classifica automaticamente cada documento por tipo e gera arquivos `.md` estruturados para uso em **RAG** ou **fine-tuning** de modelos de IA.

```bash
python analisar_pdfs.py --pasta downloads/PNCP
python analisar_pdfs.py --pasta downloads/PNCP --incremental
```

### Resultados Alcancados (set/2026)

| Indicador | Valor |
| :--- | :--- |
| Contratacoes mapeadas (2025+2026) | **195** |
| PDFs baixados do PNCP | **596** (158,8 MB) |
| Documentos no corpus `.md` | **842** |
| Taxa de extracao com sucesso | **96%** |

### Distribuicao por Tipo de Artefato

| Tipo | Docs | % |
| :--- | :--- | :--- |
| Ratificacao / Autorizacao de Empenho | 320 | 38,0% |
| Contrato / Minuta / Nota de Empenho | 178 | 21,1% |
| Termo de Referencia (TR) | 145 | 17,2% |
| Documento de Formalizacao de Demanda (DFD) | 88 | 10,4% |
| Estudo Tecnico Preliminar (ETP) | 46 | 5,5% |
| Edital de Licitacao | 10 | 1,2% |
| Parecer Juridico / Nota Tecnica | 8 | 0,9% |
| Pesquisa de Precos | 6 | 0,7% |
| Mapa / Analise de Riscos | 5 | 0,6% |
| Outros | 36 | 4,3% |

---

## 5. Estrutura do Projeto

```
Mapeamento TCE/
|-- main.py                       # CLI principal
|-- mapear_pncp_tce.py            # Mapeamento e download via PNCP
|-- analisar_pdfs.py              # Extracao de PDFs -> Markdown (corpus IA)
|-- rebuild_index.py              # Reconstroi o indice.jsonl
|-- src/
|   |-- api_client.py             # Cliente API TCE-PI
|   |-- pncp_client.py            # Cliente API PNCP
|   |-- muralic_scraper.py        # Extrator de artefatos do Muralic
|   |-- models.py                 # Modelos de dados
|   +-- storage.py                # Persistencia SQLite e JSON
|-- normativos/
|   |-- normativos_tce_pi.md      # IN TCE-PI 02/2026
|   +-- arcabouco_normativo_contratacoes.md  # Arcabouco normativo completo
|-- corpus_ia/                    # Corpus Markdown para IA (842 docs)
|   |-- etp/          (46 docs)
|   |-- tr/          (145 docs)
|   |-- dfd/          (88 docs)
|   |-- pesquisa_precos/ (6 docs)
|   |-- mapa_riscos/   (5 docs)
|   |-- edital/       (10 docs)
|   |-- parecer/       (8 docs)
|   |-- contrato/    (178 docs)
|   |-- ratificacao/ (320 docs)
|   |-- outros/       (36 docs)
|   |-- indice.jsonl  # Indice estruturado (842 registros)
|   +-- dataset.md    # Visao geral do corpus
|-- downloads/PNCP/   # PDFs baixados (596 arquivos / 158,8 MB)
|-- contratacoes_tce_pncp_2026.json
|-- contratacoes_tce_pncp_2025.json
+-- dados_tce.db
```

---

## 6. Normativos Mapeados

Consulte `normativos/arcabouco_normativo_contratacoes.md`.

* **Lei Federal n. 14.133/2021**: Nova Lei de Licitacoes -- artefatos obrigatorios (DFD, ETP, TR, Pesquisa de Precos, Mapa de Riscos).
* **IN TCE-PI n. 02/2026**: Obrigacoes de publicidade no Muralic e Contratos Web, prazos e sancoes.
* **Portaria CNMP-SG n. 151/2023**: Fase preparatoria e Equipe de Planejamento no MP.
* **Resolucao CNMP n. 283/2024 (MOTec)**: Contratacoes de TI no Ministerio Publico.
* **IN SEGES n. 65/2021**: Metodologia de pesquisa de precos.

---

## 7. Como Executar

### Pre-requisitos
```bash
pip install beautifulsoup4 pdfplumber requests
```

### Pipeline completo
```bash
# 1. Mapear e baixar contratacoes:
python mapear_pncp_tce.py --ano 2026 --download
python mapear_pncp_tce.py --ano 2025 --download

# 2. Extrair PDFs -> corpus Markdown:
python analisar_pdfs.py --pasta downloads/PNCP

# 3. Processar apenas arquivos novos:
python analisar_pdfs.py --pasta downloads/PNCP --incremental

# 4. Reconstruir indice:
python rebuild_index.py
```

---

## 8. Roadmap -- Proximos Passos

### Concluido
- [x] Mapeamento da API TCE-PI (Portal da Cidadania)
- [x] Integracao com API PNCP -- 195 contratacoes (2025 e 2026)
- [x] Download de 596 PDFs (158,8 MB)
- [x] Extracao e classificacao de 842 documentos em Markdown
- [x] Mapeamento do arcabouco normativo
- [x] Geracao do corpus IA com indice JSONL
- [x] Validacao de integridade do corpus (29/09/2026) -- Resultado: BOM | Relatorio: corpus_ia/relatorio_qualidade.md
- [x] Repositorio criado no GitHub (29/09/2026) -- https://github.com/Thiago-Nog84/mapeamento-contratacoes-tce-pi

### 1. Extracao das Contratacoes Internas do MPPI
> Fazer o mesmo mapeamento realizado para o TCE-PI aplicado as contratacoes do proprio **Ministerio Publico do Estado do Piaui**, gerando corpus equivalente para comparacao.
- [ ] Identificar CNPJ e UASG do MPPI no PNCP
- [ ] Adaptar e executar `mapear_pncp_tce.py` para o MPPI
- [ ] Baixar e extrair os PDFs dos artefatos do MPPI
- [ ] Gerar corpus Markdown equivalente em `corpus_ia_mppi/`

### 2. Conciliacao e Analise Comparativa TCE-PI x MPPI
> Realizar conciliacao entre os documentos das duas instituicoes para **verificar o alinhamento** dos processos, identificar gaps e mapear oportunidades de melhoria no MPPI.
- [ ] Comparar estrutura e qualidade dos ETPs (TCE-PI vs. MPPI)
- [ ] Comparar Termos de Referencia por categoria de objeto
- [ ] Verificar presenca e qualidade das Pesquisas de Precos
- [ ] Verificar presenca dos Mapas de Risco
- [ ] Gerar relatorio de conformidade com checklist da Lei 14.133/2021

### 3. Expansao para TJ-PI e Defensoria Publica do Estado
> Avaliar a viabilidade de coleta dos dados publicos das contratacoes do **Tribunal de Justica do Piaui (TJ-PI)** e da **Defensoria Publica do Estado do Piaui (DPE-PI)**, ampliando o corpus de referencia do sistema de justica estadual.
- [ ] Pesquisar CNPJ/UASG do TJ-PI e DPE-PI no PNCP
- [ ] Verificar disponibilidade de APIs ou portais publicos de licitacoes
- [ ] Avaliar volume e relevancia dos dados disponíveis
- [ ] Definir priorizacao: TJ-PI e/ou DPE-PI

### 4. Validacao da Integridade do Corpus para Treinamento de IA
> Avaliar se a extracao e transformacao dos arquivos `.pdf` e demais formatos em `.md` ocorreu de **forma integra e com qualidade suficiente** para suportar o treinamento de IAs.
- [ ] Auditar amostra representativa dos `.md` gerados (fidelidade ao PDF original)
- [ ] Tratar PDFs digitalizados (imagens sem OCR) com `pytesseract` ou `easyocr`
- [ ] Verificar e corrigir problemas de encoding (caracteres especiais corrompidos)
- [ ] Validar qualidade da classificacao automatica (ETP, TR, DFD, etc.)
- [ ] Gerar metricas do corpus: % de texto extraido, % por categoria, cobertura por modalidade
- [ ] Testar o corpus em aplicacao RAG (ex: perguntas sobre contratacoes)

### 5. Criar Repositorio no GitHub
> Publicar o projeto em repositorio no GitHub para versionamento, colaboracao e documentacao formal.
- [ ] Criar repositorio `mapeamento-contratacoes-tce-pi`
- [ ] Configurar `.gitignore` (excluir PDFs, banco de dados e corpus grande)
- [ ] Publicar codigo-fonte: `src/`, `mapear_pncp_tce.py`, `analisar_pdfs.py`
- [ ] Publicar normativos: `normativos/`
- [ ] Publicar documentacao: `README.md`, `corpus_ia/dataset.md`
- [ ] Adicionar licenca (MIT para o codigo / Creative Commons para os dados)
- [ ] Configurar GitHub Actions para execucao automatizada do pipeline anual

---

## Contexto Institucional

**Instituicao produtora:** Ministerio Publico do Estado do Piaui (MPPI)
**Setor responsavel:** CLC -- Coordenadoria de Licitacoes e Contratos
**Base normativa:** Lei 14.133/2021 | IN TCE-PI 02/2026 | Portaria CNMP-SG 151/2023


