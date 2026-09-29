# Normativos Relacionados às Contratações Públicas - TCE-PI

Este documento consolida o arcabouço normativo que disciplina os procedimentos licitatórios, contratações diretas, contratos administrativos e o envio obrigatório de artefatos aos sistemas de fiscalização do Tribunal de Contas do Estado do Piauí (TCE-PI).

---

## 1. Instrução Normativa TCE-PI nº 02/2026 (Principal Norma Vigente)

* **Publicação / Vigência:** Fevereiro de 2026.
* **Revogação Expressa:** Revogou a Instrução Normativa TCE-PI nº 06/2017 e todas as alterações posteriores.
* **Âmbito de Aplicação:** 
  * Todos os Poderes (Executivo, Legislativo, Judiciário);
  * Ministério Público do Estado do Piauí (MPPI) e Tribunal de Contas (TCE-PI);
  * Autarquias, Fundações Públicas, Empresas Públicas e Sociedades de Economia Mista estaduais e municipais;
  * Consórcios Públicos e Entidades do Terceiro Setor (OS, OSCIPs e cooperativas) que gerenciem recursos públicos.

### 1.1 Sistemas Integrados Obrigatórios

1. **Licitações Web (`/licitacoesweb`):**
   * Destinado ao cadastro e alimentação da fase preparatória e externa de todos os procedimentos licitatórios, procedimentos auxiliares (credenciamento, pré-qualificação, PMI) e convênios/parcerias.
   * Alimentação obrigatória dos artefatos: Edital, Termo de Referência (TR), Estudo Técnico Preliminar (ETP), Projeto Básico (PB), Planilha Orçamentária e Parecer Jurídico.
   * Publicidade imediata no **Mural de Licitações (Muralic)**.

2. **Contratos Web (`/contratosweb`):**
   * Destinado ao registro de:
     * Contratos decorrentes de licitações;
     * Contratações Diretas (Dispensas e Inexigibilidades);
     * Atas de Registro de Preços e adesões ("caronas");
     * Termos aditivos, rescisões e incidentes contratuais.
   * Publicidade imediata no **Mural de Contratos (Muralcon)**.

3. **Obras Web (`/obrasweb`):**
   * Módulo específico para acompanhamento físico-financeiro de obras e serviços de engenharia.
   * Exigência de cronograma físico-financeiro, ART/RRT, medições periódicas e relatórios fotográficos.

### 1.2 Prazos Principais de Alimentação

| Procedimento / Evento | Prazo Limite no TCE-PI | Sistema |
| :--- | :--- | :--- |
| **Publicação do Edital de Licitação** | Até a data da publicação oficial / divulgação | Licitações Web |
| **Alteração de Edital / Data de Abertura** | Imediatamente após a decisão, respeitando reabertura de prazos | Licitações Web |
| **Resultado / Homologação** | Até 5 (cinco) dias úteis após o ato | Licitações Web |
| **Assinatura do Contrato / Termo Aditivo** | Até 10 (dez) dias úteis após a assinatura | Contratos Web |
| **Contratação Direta (Dispensa / Inexigibilidade)** | Até 5 (cinco) dias úteis após o ato de ratificação | Contratos Web |
| **Adesão à Ata de Registro de Preços** | Até 5 (cinco) dias úteis após autorização do órgão gerenciador | Contratos Web |

---

## 2. Lei Federal nº 14.133/2021 (Nova Lei de Licitações e Contratos)

* **Impacto no TCE-PI:**
  * O TCE-PI adaptou seus formulários no Licitações Web e Muralic para contemplar os novos modos de disputa (*Aberto*, *Aberto/Fechado*, *Fechado*), critérios de julgamento e os procedimentos auxiliares.
  * Integração com o **Portal Nacional de Contratações Públicas (PNCP)**: os dados enviados pelos jurisdicionados são validados quanto à conformidade de publicidade legal.

---

## 3. Resoluções e Instruções Normativas de Prestação de Contas (Sagres)

* **Sagres Folha e Sagres Contábil:**
  * Disciplinam a remessa mensal eletrônica da execução orçamentária e financeira dos órgãos estaduais e municipais.
  * Cruzamento de dados entre o empenho/pagamento e o contrato cadastrado no Contratos Web.
* **Documentos Digitais:**
  * Disponibilizados na API através dos endpoints `/documentos/estado` e `/documentos/:idUnidadeGestora/digitalizados`.
