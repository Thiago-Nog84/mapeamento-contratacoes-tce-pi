import json

json_path = r"E:\Thiago\Dev\Mapeamento TCE\dashboard\src\data\corpus_resumo.json"

with open(json_path, 'r', encoding='utf-8') as f:
    corpus = json.load(f)

premio_data = {
    "titulo": "OBSERVATÓRIO INTEGRADO DE CONTRATAÇÕES PÚBLICAS E GOVERNANÇA MINISTERIAL",
    "subtitulo": "Inteligência Artificial, Gestão Preventiva de Riscos e Padronização Regional sob a Lei Federal nº 14.133/2021",
    "proponente": "Coordenação de Licitações e Contratos (CLC) — Ministério Público do Estado do Piauí (MPPI)",
    "gerente_projeto": "Thiago Nogueira de Sousa Martins Almeida (Coordenador da CLC/MPPI)",
    "patrocinador": "Procurador-Geral de Justiça do Estado do Piauí",
    "categoria_cnmp": "Governança e Gestão (Prêmio CNMP - Edição 2026)",
    "categoria_mppi": "Prêmio Melhores Práticas MPPI (Ato PGJ nº 1.025/2020 c/c Ato PGJ nº 1.254/2022)",
    "alinhamento_estrategico": {
        "pei_mppi": "Objetivo Estratégico: Aprimorar a governança, a gestão de recursos e a transparência institucional (PEI MPPI 2022-2029)",
        "pen_mp": "Macrodesafio: Governança e Gestão Estratégica orientada a resultados (CNMP)",
        "ods_onu": "ODS 16 - Paz, Justiça e Instituições Eficazes (Meta 16.6: Instituições eficazes e transparentes)"
    },
    "criterios_cnmp": [
        {
            "criterio": "Resolutividade",
            "peso": 2,
            "icone": "CheckCircle",
            "pontuacao_estimada": "10.0 / 10",
            "titulo_impacto": "Economia de R$ 68,8 Mi e Redução de 70% de Tempo em Compras Diretas",
            "evidencias": [
                "Análise empírica de 219 certames concluídos com dupla medição (R$ 341M orçado vs R$ 272M homologado, deságio de 20,18%).",
                "Instituição de Pareceres Referenciais (Art. 53, § 5º), eliminando remessas desnecessárias à Assessoria Jurídica em dispensas por valor.",
                "Blindagem jurídica preventiva de 100% dos processos de adesão a atas ('carona') em consonância com o Acórdão nº 300/2025 do TCE-PI."
            ]
        },
        {
            "criterio": "Inovação",
            "peso": 2,
            "icone": "Cpu",
            "pontuacao_estimada": "10.0 / 10",
            "titulo_impacto": "Pioneira Plataforma RAG / AI Cobrindo 100% dos MPs do Nordeste a Custo Zero",
            "evidencias": [
                "Primeiro repositório unificado do Brasil a integrar 10.504 documentos contratuais de todos os 9 estados da região Nordeste.",
                "Mineração automatizada de 662 pareceres jurídicos e 146 matrizes de risco para identificação proativa de padrões decisórios.",
                "Arquitetura de dados desenvolvida 100% com recursos internos e software livre, sem dispêndio de recursos públicos em consultorias."
            ]
        },
        {
            "criterio": "Proatividade",
            "peso": 1,
            "icone": "Shield",
            "pontuacao_estimada": "9.9 / 10",
            "titulo_impacto": "Arquitetura das 3 Linhas de Defesa (Art. 169) e Governança Antecipada",
            "evidencias": [
                "Master Checklist de Conformidade da Instrução Processual com 15 barreiras preventivas antes do envio à PGJ.",
                "Mapeamento de riscos críticos em TIC, terceirização e obras com alocação contratual explícita e regras de IMR/glosa.",
                "Elaboração proativa de 3 minutas normativas antes da ocorrência de apontamentos por órgãos de controle externo."
            ]
        },
        {
            "criterio": "Cooperação",
            "peso": 1,
            "icone": "Users",
            "pontuacao_estimada": "9.9 / 10",
            "titulo_impacto": "Integração Interinstitucional de 12 Entidades Públicas de Alto Nível",
            "evidencias": [
                "Compartilhamento de inteligência entre os 9 Ministérios Públicos Estaduais do Nordeste, TJ-PI, TCE-PI e MPDFT.",
                "Intercâmbio de editais, termos de referência e pesquisas de preço para viabilizar compras públicas compartilhadas na região.",
                "Harmonização da aplicação prática da Lei 14.133/2021 no âmbito dos órgãos ministeriais brasileiros."
            ]
        },
        {
            "criterio": "Transparência",
            "peso": 1,
            "icone": "Eye",
            "pontuacao_estimada": "10.0 / 10",
            "titulo_impacto": "Portal Público Aberto com Visualização Intuitiva e Rastreabilidade Total",
            "evidencias": [
                "Plataforma web interativa de livre acesso, permitindo a qualquer cidadão ou gestor consultar métricas de deságio e normativos.",
                "Auditabilidade total de cada processo mapeado com links e referências diretas ao PNCP e aos diários oficiais.",
                "Design moderno baseado nas melhores práticas de UI/UX, gráficos responsivos e visualização executiva para a tomada de decisão."
            ]
        }
    ],
    "tap_oficial": {
        "problema_diagnosticado": "Insegurança jurídica e morosidade na transição para a Lei 14.133/2021, sobrecarga na Assessoria Jurídica em processos repetitivos de dispensa por valor e riscos de nulidade em adesões a atas conforme o Acórdão 300/2025 do TCE-PI.",
        "solucao_entregue": "Ecossistema integrado de governança compreendendo repositório RAG de 10.504 peças, compêndio das 3 linhas de defesa, 3 pareceres referenciais e portal web de transparência ativa.",
        "produtos_entregues": [
            {"num": "1", "nome": "Base RAG Regional", "desc": "10.504 documentos dos 9 MPs do Nordeste, TJ-PI, TCE-PI e MPDFT indexados."},
            {"num": "2", "nome": "Estudo de Economicidade", "desc": "R$ 341M analisados com calibragem de 20,18% de deságio em 219 certames."},
            {"num": "3", "nome": "Compêndio de Controle", "desc": "662 pareceres jurídicos, 146 matrizes de risco e 451 DFDs catalogados."},
            {"num": "4", "nome": "Caderno de Proposições", "desc": "3 Atos da PGJ, 3 Pareceres Referenciais (Art. 53 §5º) e Checklist da CLC."},
            {"num": "5", "nome": "Portal Web Interativo", "desc": "Site completo com UX moderna, simulador de deságio e busca semântica."}
        ],
        "metodologia_gestao": "Manual de Projetos do MPPI (Ato PGJ nº 1.254/2022) alinhado ao Guia PMBOK 6ª Edição e PEN-MP.",
        "custo_financeiro": "R$ 0,00 (Desenvolvido exclusivamente com força de trabalho própria da CLC/MPPI)."
    }
}

corpus["premio_boas_praticas"] = premio_data

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(corpus, f, indent=2, ensure_ascii=False)

print("corpus_resumo.json atualizado com dados oficiais do Prêmio e TAP!")
