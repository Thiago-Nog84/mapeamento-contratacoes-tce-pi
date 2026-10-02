# ROADMAP ESTRATÉGICO: PROJETO Lic.IA (2026 - 2027)
## Da Blindagem Local no MPPI ao Observatório Nacional de Compras do Ministério Público Brasileiro

---

### 🎯 Visão Geral do Roadmap
O **PROJETO Lic.IA** foi desenhado com uma arquitetura modular e progressiva, dividida em **4 Fases Estratégicas**. A iniciativa parte da blindagem imediata das contratações do MPPI em Teresina até alcançar a unificação de inteligência de compras de todos os **26 Ministérios Públicos Estaduais** e dos **ramos federais do Ministério Público da União (MPF, MPT, MPM e MPDFT)**, além do **CNMP**.

---

### 🗺️ FASES DE IMPLEMENTAÇÃO E ESCALA

```
[FASE 1: 1º Trim/2026] ──▶ [FASE 2: 2º Trim/2026] ──▶ [FASE 3: 3º-4º Trim/2026] ──▶ [FASE 4: 2027]
 Núcleo Local (Piauí)       Benchmarking Regional       Expansão Nacional             Integração CNPG/CNMP
 MPPI + TJ-PI + TCE-PI      9 MPs Nordeste + MPDFT      26 MPs Estaduais +            Observatório Nacional
 Blindagem Acórdão 300      10.504 Atos / R$ 341M       MPF, MPT, MPM, MPU            Banco Unificado do MP
 (STATUS: 100% PRONTO)      (STATUS: 100% PRONTO)       (STATUS: EM IMPLANTAÇÃO)      (META PRÊMIO CNMP)
```

---

### 🏛️ DETALHAMENTO DAS ETAPAS E ESTRATÉGIA DE EXPANSÃO

#### FASE 1: O Núcleo de Blindagem Local (Teresina / Piauí) — [CONCLUÍDA]
* **Escopo:** MPPI, TJ-PI e TCE-PI.
* **Foco Estratégico:** 
  * Mapeamento do mercado geográfico comum de fornecedores de Teresina (serviços terceirizados, vigilância, obras e compras corporativas).
  * Blindagem técnica e jurídica contra o **Acórdão 300/2025 do TCE-PI** para adesões a atas de registro de preços (caronas).
  * Redução do tempo de instrução na CLC de 35 para 10 dias.
* **Entregável:** Simulador de Deságio, Checklist das MJRs da PGJ e Caderno Normativo com minutas blindadas.

---

#### FASE 2: O Benchmarking Regional (Nordeste + MPDFT) — [CONCLUÍDA]
* **Escopo:** Todos os 9 MPs do Nordeste (MPPI, MPMA, MPCE, MPRN, MPPB, MPPE, MPAL, MPSE, MPBA) + MPDFT.
* **Foco Estratégico:**
  * Ingestão de **10.504 atos de compra** e **R$ 341 milhões** em contratações homologadas.
  * Identificação da régua empírica de **20,18% de deságio médio regional** para orientar as negociações em pregões eletrônicos.
  * R$ 68,8 milhões em economia potencial mapeada na região.
* **Entregável:** Painel Panorama Regional e Explorador Semântico com RAG funcional.

---

#### FASE 3: Expansão Nacional Federada (Todos os MPs do Brasil + Ramos Federais) — [EM IMPLANTAÇÃO]
* **Escopo Completo dos Órgãos Alvo:**
  1. **26 Ministérios Públicos Estaduais:** 
     * *Norte:* MPAC, MPAM, MPAP, MPPA, MPRO, MPRR, MPTO.
     * *Centro-Oeste:* MPGO, MPMT, MPMS.
     * *Sudeste:* MPMG, MPES, MPRJ, MPSP.
     * *Sul:* MPPR, MPSC, MPRS.
     * *Nordeste:* Já 100% integrados na Fase 2.
  2. **Ministério Público da União (MPU) e Ramos Federais:**
     * **MPF** (Ministério Público Federal / Procuradoria-Geral da República)
     * **MPT** (Ministério Público do Trabalho / PGT)
     * **MPM** (Ministério Público Militar / PGJM)
     * **MPDFT** (Ministério Público do Distrito Federal e Territórios)
     * **Secretaria-Geral do MPU** e **ESMPU** (Escola Superior do MPU)
  3. **Órgão Central:**
     * **CNMP** (Conselho Nacional do Ministério Público)

---

### 💡 A MELHOR ESTRATÉGIA PARA A EXPANSÃO NACIONAL

A expansão para todos os MPs e ramos federais não deve depender de burocracias lentas de convênios prévios. Adotaremos uma **estratégia tripartite inteligente**:

#### 1. Estratégia Tecnológica (Ingestão Federada via API do PNCP)
* **Sem Necessidade de Convênio Prévio:** Todos os 30 MPs brasileiros são obrigados pelo art. 174 da Lei 14.133/2021 a publicar 100% de seus editais, atas e contratos no **Portal Nacional de Contratações Públicas (PNCP)**.
* **Rotina Automatizada por CNPJ Raiz:** Criamos um catálogo dos CNPJs de todos os ramos federais e MPs estaduais. Um script Python em segundo plano consulta a API oficial do PNCP (`https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao`), baixando editais, termos de referência e valores homologados automaticamente.
* **Custo Marginal Zero:** A infraestrutura atual do MPPI já suporta o processamento dos dados sem custos adicionais de servidores.

#### 2. Estratégia de Clusterização Temática por Famílias de Compra
Para não sobrecarregar a base com dados dispersos, a Lic.IA agrupa as compras nacionais nas **6 Famílias Críticas Ministeriais**:
* 💻 **Tecnologia & Softwares Especializados:** Licenças periciais (Cellebrite, Oxygen), ferramentas de big data, storage forense, nuvem e data centers.
* 🚗 **Frotas & Segurança Institucional:** Veículos operacionais, viaturas blindadas, coletes balísticos, armamento e rastreamento para membros sob ameaça.
* 🏢 **Infraestrutura & Obras das Sedes:** Reformas de Promotorias de Justiça, módulos de energia solar, ar-condicionado e acessibilidade.
* 👥 **Serviços Terceirizados Contínuos:** Apoio administrativo, recepcionistas, motoristas, copeiragem e limpeza predial.
* 🛡️ **Segurança Armada & Vigilância:** Monitoramento eletrônico CFTV e postos de vigilância armada.
* 📚 **Capacitação & Eventos (CEAF / ESMPU):** Cursos de formação, plataformas de EAD e consultorias pedagógicas.

#### 3. Estratégia Institucional e Política (O "Cavalo de Tróia" do CNMP)
* **O MPPI como Provedor, não como Pedinte:** O MPPI chega ao Conselho Nacional de Procuradores-Gerais (CNPG) e à Comissão de Planejamento Estratégico (CPE/CNMP) com o sistema **já funcionando e com os dados de todos os MPs minerados**.
* **Discurso Oficial do PGJ:**
  > *"O Ministério Público do Estado do Piauí desenvolveu a Lic.IA e está franqueando o acesso de sua inteligência de contratações a todos os colegas de outros estados e aos ramos federais do MPU, sem custos."*
* **Impacto no Prêmio CNMP 2026:** Atendimento com **nota máxima (100%)** nos critérios de *Cooperação Interinstitucional* e *Replicabilidade Nacional*.

---

### 📅 CRONOGRAMA DE EXPANSÃO (MILESTONES)

| Marco | Prazo | Ação Estratégica | Responsável |
|---|---|---|---|
| **M1** | Abr/2026 | Mapeamento dos CNPJs e Unidades Gestoras do MPF, MPT, MPM, MPU e CNMP | Equipe Técnica CLC |
| **M2** | Mai/2026 | Ingestão piloto dos dados de contratações federais e testes de deságio de TI | Equipe Técnica CLC |
| **M3** | Jul/2026 | Ingestão dos 17 MPs Estaduais restantes (Norte, Sul, Sudeste, Centro-Oeste) | Equipe Técnica CLC |
| **M4** | Ago/2026 | Apresentação executiva do Painel Nacional ao Procurador-Geral de Justiça (PGJ) | Coordenador CLC |
| **M5** | Set/2026 | Inscrição oficial do Projeto Lic.IA no Banco Nacional de Projetos do CNMP | APG / PGJ / CLC |
| **M6** | 2027 | Proposta de celebração de Acordo de Cooperação Técnica com o CNMP para adoção nacional | PGJ / CNMP |

---

### 🏆 Conclusão Estratégica
Com este roadmap, a **Lic.IA** deixa de ser apenas uma ferramenta interna de Teresina para se tornar a **maior base de inteligência analítica em contratações públicas de todo o Ministério Público brasileiro**, conferindo ao MPPI uma liderança tecnológica e de governança sem precedentes.
