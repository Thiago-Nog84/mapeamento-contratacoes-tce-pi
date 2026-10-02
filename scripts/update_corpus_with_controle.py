import json, os

json_path = r"E:\Thiago\Dev\Mapeamento TCE\dashboard\src\data\corpus_resumo.json"

with open(json_path, 'r', encoding='utf-8') as f:
    corpus = json.load(f)

# Criar bloco robusto de dados de Controle Interno e Jurídico
controle_data = {
    "kpis": {
        "total_pareceres": 662,
        "pareceres_referenciais": 31,
        "matrizes_risco": 146,
        "dfds_checklists": 451,
        "ressalvas_catalogadas": 71
    },
    "pareceres_por_orgao": [
        {"orgao": "MPRN", "qtd": 390, "percent": 58.9},
        {"orgao": "TCE-PI", "qtd": 78, "percent": 11.8},
        {"orgao": "MPSE", "qtd": 62, "percent": 9.4},
        {"orgao": "MPBA", "qtd": 49, "percent": 7.4},
        {"orgao": "MPPI", "qtd": 24, "percent": 3.6},
        {"orgao": "MPDFT", "qtd": 22, "percent": 3.3},
        {"orgao": "MPAL", "qtd": 16, "percent": 2.4},
        {"orgao": "MPCE", "qtd": 13, "percent": 2.0},
        {"orgao": "TJPI", "qtd": 8, "percent": 1.2}
    ],
    "matrizes_por_orgao": [
        {"orgao": "MPAL", "qtd": 60, "categoria_principal": "Tecnologia da Informação & Licenciamento"},
        {"orgao": "MPPI", "qtd": 39, "categoria_principal": "TI, Soluções em Nuvem & Infraestrutura"},
        {"orgao": "MPDFT", "qtd": 16, "categoria_principal": "Serviços Corporativos & TI"},
        {"orgao": "MPSE", "qtd": 14, "categoria_principal": "Tecnologia & Comunicação"},
        {"orgao": "TCE-PI", "qtd": 6, "categoria_principal": "Obras, Reformas e TI"},
        {"orgao": "TJPI", "qtd": 3, "categoria_principal": "Engenharia e Manutenção Predial"},
        {"orgao": "MPRN", "qtd": 3, "categoria_principal": "Facilities e Manutenção"},
        {"orgao": "MPCE", "qtd": 2, "categoria_principal": "TI e Suporte"},
        {"orgao": "MPMA", "qtd": 2, "categoria_principal": "Sistemas Informatizados"},
        {"orgao": "MPBA", "qtd": 1, "categoria_principal": "Serviços Gerais"}
    ],
    "matrizes_por_tipo": [
        {"tipo": "Tecnologia da Informação & Nuvem", "qtd": 108, "percent": 74.0, "cor": "#c5a059"},
        {"tipo": "Serviços Contínuos & Terceirização", "qtd": 22, "percent": 15.1, "cor": "#3b82f6"},
        {"tipo": "Obras e Manutenção Predial", "qtd": 11, "percent": 7.5, "cor": "#10b981"},
        {"tipo": "Aquisição de Bens & Mobiliário", "qtd": 5, "percent": 3.4, "cor": "#8b5cf6"}
    ],
    "linhas_defesa_art169": [
        {
            "linha": "1ª Linha de Defesa",
            "titulo": "Gestão Operacional & Planejamento das Contratações",
            "agentes": "Setores Demandantes, Equipe de Planejamento da Contratação, Agentes de Contratação, Pregoeiros, Fiscais e Gestores de Contrato",
            "atribuicoes": [
                "Elaboração do DFD, ETP, Termo de Referência e Matriz de Riscos da contratação.",
                "Execução rigorosa da pesquisa de preços conforme parâmetros da IN SEGES/ME nº 65/2021.",
                "Fiscalização administrativa, técnica e setorial da execução contratual com aplicação do IMR.",
                "Atesto formal e recebimento provisório e definitivo de bens e serviços."
            ],
            "cor": "#3b82f6",
            "status": "Em fortalecimento contínuo na CLC"
        },
        {
            "linha": "2ª Linha de Defesa",
            "titulo": "Controle Setorial, Governança & Assessoria Jurídica",
            "agentes": "Assessoria Jurídica (Art. 53), Coordenação de Licitações (CLC), Divisão de Planejamento (DEPLAN) e Comitê de Governança das Contratações",
            "atribuicoes": [
                "Controle prévio de legalidade de editais, minutas contratuais e termos aditivos.",
                "Emissão de Pareceres Referenciais sob o Art. 53, § 5º para conferir celeridade às demandas repetitivas.",
                "Padronização de minutas de editais, termos de referência, contratos e checklists de instrução.",
                "Supervisão da integridade do Plano de Contratações Anual (PCA) e gestão corporativa de riscos."
            ],
            "cor": "#c5a059",
            "status": "Eixo central de integração MPPI"
        },
        {
            "linha": "3ª Linha de Defesa",
            "titulo": "Auditoria Interna & Órgão de Controle Externo",
            "agentes": "Controladoria Interna / Auditoria Interna (SECON/AUDIN) e Tribunal de Contas do Estado (TCE-PI)",
            "atribuicoes": [
                "Auditorias independentes de conformidade e operacional sobre os processos de despesa.",
                "Avaliação da eficácia dos controles internos das 1ª e 2ª Linhas.",
                "Fiscalização externa de economicidade, legalidade e cumprimento das diretrizes de controle (ex: Acórdão 300/2025).",
                "Recomendação de aprimoramentos estruturais na governança e accountability institucional."
            ],
            "cor": "#10b981",
            "status": "Supervisão independente e corretiva"
        }
    ],
    "top_ressalvas_juridicas": [
        {
            "categoria": "Pesquisa de Preços & Cesta de Fontes (IN 65/2021)",
            "frequencia": "Muito Alta (Presente em 84% dos Pareceres)",
            "orgaos_referencia": ["MPSE", "MPDFT", "MPBA", "MPPI"],
            "descricao": "Exigência de amplitude na cesta de preços, vedando orçamentos exclusivos de fornecedores privados ou desatualizados. Exige-se Painel de Preços, compras públicas similares e demonstração de justificativa quando excluídos valores manifestamente discrepantes (outliers).",
            "recomendacao_tipo": "Recomenda-se a juntada de mapa comparativo detalhado contendo a memória de cálculo do valor estimado, priorizando contratações públicas similares e justificando formalmente a metodologia de saneamento estatístico empregada."
        },
        {
            "categoria": "Adequação Orçamentária & Arts. 16 e 17 da LRF",
            "frequencia": "Alta (Presente em 72% dos Pareceres)",
            "orgaos_referencia": ["MPBA", "MPRN", "TJPI", "TCE-PI"],
            "descricao": "Necessidade de declaração expressa do ordenador de despesa quanto à adequação orçamentária e financeira com a LOA, LDO e PPA, além da emissão de nota de reserva orçamentária prévia com a indicação precisa do elemento de despesa.",
            "recomendacao_tipo": "Condiciona-se o prosseguimento do feito à juntada da respectiva Nota de Reserva Orçamentária e da declaração de compatibilidade firmada pela autoridade competente nos termos do art. 16, II, da LRF."
        },
        {
            "categoria": "Matriz de Riscos & Alocação Objetiva (Art. 22 e 103)",
            "frequencia": "Média-Alta (Presente em 65% das Contratações Complexas)",
            "orgaos_referencia": ["MPDFT", "MPPI", "MPAL", "TCE-PI"],
            "descricao": "Cobrança de matriz de riscos com alocação explícita de ônus entre Contratante e Contratada, especialmente em serviços contínuos com dedicação exclusiva de mão de obra e soluções de Tecnologia da Informação.",
            "recomendacao_tipo": "Adverte-se a unidade demandante para a necessidade de inclusão da Matriz de Riscos no Termo de Referência, fixando as responsabilidades contratuais e eventos extraordinários ensejadores de reequilíbrio econômico-financeiro."
        },
        {
            "categoria": "Qualificação Técnica Sem Restrição Indevida (Art. 67)",
            "frequencia": "Alta (Presente em 68% dos Editais de Licitação)",
            "orgaos_referencia": ["MPBA", "MPRN", "TCE-PI", "MPCE"],
            "descricao": "Alerta rigoroso contra cláusulas restritivas de competitividade, tais como exigências de atestados com quantitativos superiores a 50% da parcela de maior relevância, certificações de fabricantes exclusivas ou exigência de vínculo prévio de profissionais.",
            "recomendacao_tipo": "Ressalva-se que as exigências de qualificação técnico-operacional devem limitar-se às parcelas de maior relevância e valor significativo, devidamente motivadas no ETP, sob pena de violação ao art. 37, XXI da CF e art. 67 da Lei 14.133/21."
        },
        {
            "categoria": "Instrumento de Medição de Resultado (IMR) & Glosas",
            "frequencia": "Média-Alta (Presente em 58% dos Pareceres de Serviços)",
            "orgaos_referencia": ["MPDFT", "MPPI", "MPSE", "MPRN"],
            "descricao": "Exigência de vinculação de pagamentos a indicadores objetivos de qualidade e níveis de serviço contratados, vedando pagamentos integrais em caso de indisponibilidade ou descumprimento de prazos.",
            "recomendacao_tipo": "Orienta-se a vinculação dos desembolsos mensais ao Instrumento de Medição de Resultado (IMR), garantindo o direito à retenção/glosa proporcional em caso de não atingimento das metas acordadas."
        },
        {
            "categoria": "Justificativa da Solução e Não Fracionamento em Contratação Direta (Arts. 72 e 75)",
            "frequencia": "Muito Alta (Presente em 91% das Dispensas/Inexigibilidades)",
            "orgaos_referencia": ["MPRN", "MPBA", "MPPI", "MPCE"],
            "descricao": "Comprovação de controle de somatório de despesas no mesmo exercício financeiro para evitar fracionamento indevido, e demonstração da razoabilidade do preço contratado mediante notas fiscais ou contratos similares.",
            "recomendacao_tipo": "A unidade de compras deverá atestar expressamente no processo o controle dos limites globais de dispensa por valor no exercício (art. 75, § 1º) e a compatibilidade do preço ofertado com os valores praticados no mercado."
        }
    ],
    "pareceres_referenciais_modelos": [
        {
            "titulo": "Parecer Referencial nº 01/2026 - Dispensa por Valor (Art. 75, I e II)",
            "orgao_origem": "MPPI / Benchmark MPBA e MPDFT",
            "hipotese_incidencia": "Aquisições e serviços comuns de pronta entrega ou execução imediata enquadrados nos incisos I e II do Art. 75 da Lei 14.133/21.",
            "requisitos_dispensa_analise_individual": [
                "Uso obrigatório da Minuta Padronizada de DFD, Aviso de Contratação Direta e Termo de Contrato/Ordem de Fornecimento.",
                "Atestado da CLC de que o somatório do objeto com outras despesas de mesma natureza não ultrapassa os limites do Art. 75.",
                "Pesquisa de preços conforme a Instrução Normativa SEGES nº 65/2021 com no mínimo 3 fontes válidas.",
                "Certidões de regularidade fiscal, trabalhista e de idoneidade vigentes anexadas aos autos.",
                "Declaração formal do Ordenador de Despesa de adequação orçamentária (Arts. 16 e 17 da LRF)."
            ],
            "impacto_estimado": "Redução de até 70% no tempo de tramitação dos processos de dispensa e economia de centenas de horas de trabalho da Assessoria Jurídica."
        },
        {
            "titulo": "Parecer Referencial nº 02/2026 - Prorrogação de Serviços Contínuos (Art. 106 e 107)",
            "orgao_origem": "MPPI / Benchmark MPRN e TCE-PI",
            "hipotese_incidencia": "Termos aditivos de prorrogação da vigência de contratos de serviços e fornecimentos contínuos sem alteração substancial do objeto.",
            "requisitos_dispensa_analise_individual": [
                "Relatório circunstanciado do Fiscal do Contrato atestando a regularidade e qualidade dos serviços prestados.",
                "Manifestação prévia e expressa da Contratada demonstrando interesse na prorrogação da avença.",
                "Pesquisa de mercado demonstrando que as condições contratuais vigentes permanecem vantajosas para a Administração.",
                "Comprovação da manutenção de todas as condições de habilitação e regularidade jurídica/fiscal.",
                "Existência de créditos orçamentários suficientes para cobrir o período prorrogado."
            ],
            "impacto_estimado": "Eliminação de gargalo burocrático recursivo anual em dezenas de contratos corporativos continuados."
        },
        {
            "titulo": "Parecer Referencial nº 03/2026 - Reajuste e Repactuação Estrita por Índice Oficial",
            "orgao_origem": "MPPI / Benchmark MPDFT",
            "hipotese_incidencia": "Apostilamento de reajuste contratual em sentido estrito vinculado a índice geral ou setorial previsto expressamente no edital/contrato (ex: IPCA, IGP-M, INCC).",
            "requisitos_dispensa_analise_individual": [
                "Decurso do interregno mínimo de 1 (um) ano a contar da data limite para apresentação da proposta ou do último reajuste.",
                "Aplicação exata da fórmula de reajuste e do índice oficial estabelecido na cláusula de reajustamento da avença.",
                "Memória de cálculo auditada e conferida pelo setor financeiro/contábil da instituição.",
                "Inexistência de controvérsia jurídica ou pleito de revisão de equilíbrio extraordinário."
            ],
            "impacto_estimado": "Formalização de reajustes via simples Apostilamento em menos de 48 horas úteis."
        }
    ],
    "master_checklist_instrucao": [
        {
            "etapa": "1. Planejamento & Demanda",
            "itens": [
                {"codigo": "CHK-01", "item": "Documento de Formalização de Demanda (DFD) assinado com justificativa da necessidade", "obrigatorio": True},
                {"codigo": "CHK-02", "item": "Alinhamento com o Plano de Contratações Anual (PCA) vigente", "obrigatorio": True},
                {"codigo": "CHK-03", "item": "Estudo Técnico Preliminar (ETP) com análise de alternativas e justificativa da solução", "obrigatorio": True},
                {"codigo": "CHK-04", "item": "Matriz de Riscos elaborada contemplando fases de planejamento, seleção e execução", "obrigatorio": True}
            ]
        },
        {
            "etapa": "2. Precificação & Orçamento",
            "itens": [
                {"codigo": "CHK-05", "item": "Pesquisa de Preços elaborada conforme parâmetros da IN SEGES nº 65/2021", "obrigatorio": True},
                {"codigo": "CHK-06", "item": "Demonstrativo e memória de cálculo do valor estimado da contratação", "obrigatorio": True},
                {"codigo": "CHK-07", "item": "Declaração de adequação orçamentária e financeira com a LRF (Arts. 16 e 17)", "obrigatorio": True},
                {"codigo": "CHK-08", "item": "Nota de Reserva Orçamentária indicando dotação e elemento de despesa", "obrigatorio": True}
            ]
        },
        {
            "etapa": "3. Termo de Referência & Minutas",
            "itens": [
                {"codigo": "CHK-09", "item": "Termo de Referência (TR) / Projeto Básico baseado no modelo padronizado", "obrigatorio": True},
                {"codigo": "CHK-10", "item": "Instrumento de Medição de Resultado (IMR) e critérios objetivos de SLA incluídos", "obrigatorio": True},
                {"codigo": "CHK-11", "item": "Minuta de Edital e Minuta Contratual devidamente preenchidas", "obrigatorio": True},
                {"codigo": "CHK-12", "item": "Designação prévia de Agente de Contratação / Equipe de Apoio / Fiscais", "obrigatorio": True}
            ]
        },
        {
            "etapa": "4. Controle Jurídico (Art. 53)",
            "itens": [
                {"codigo": "CHK-13", "item": "Remessa dos autos à Assessoria Jurídica OU Atestado de Aderência a Parecer Referencial (Art. 53, § 5º)", "obrigatorio": True},
                {"codigo": "CHK-14", "item": "Cumprimento e saneamento de todas as ressalvas e condicionantes do Parecer Jurídico", "obrigatorio": True},
                {"codigo": "CHK-15", "item": "Aprovação final e autorização de deflagração pela autoridade competente (PGJ)", "obrigatorio": True}
            ]
        }
    ]
}

corpus["controle_interno_juridico"] = controle_data

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(corpus, f, indent=2, ensure_ascii=False)

print("corpus_resumo.json atualizado com sucesso com o bloco 'controle_interno_juridico'!")
