import os, sys, json, re
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

indice_path = r"E:\Thiago\Dev\Mapeamento TCE\corpus_ia\indice.jsonl"

pareceres = []
matrizes = []
dfds = []

# Categorias temáticas de ressalvas com regex
categorias_ressalvas = {
    "Pesquisa de Preços & Cotação": [
        r"pesquisa\s+de\s+preço", r"mapa\s+comparativo", r"painel\s+de\s+preço", r"in\s+65",
        r"cesta\s+de\s+preço", r"justificativa\s+do\s+preço", r"sobrepreço", r"inexequí", r"inexequi"
    ],
    "Adequação Orçamentária & LRF": [
        r"art\.?\s*16", r"lrf", r"disponibilidade\s+orçament", r"dotação\s+orçament",
        r"declaração\s+de\s+adequação", r"nota\s+de\s+reserva", r"empenho"
    ],
    "Qualificação Técnica & Habilitação": [
        r"qualificação\s+técnica", r"atestado", r"capacidade\s+técnico-operacional",
        r"vedação\s+à\s+restrição", r"certidão", r"regularidade\s+fiscal", r"regularidade\s+trabalhista"
    ],
    "Gestão Contratual, IMR & SLA": [
        r"instrumento\s+de\s+medição", r"imr", r"nível\s+de\s+serviço", r"sla", r"fiscal\s+do\s+contrato",
        r"glosa", r"sanções", r"penalidades", r"recebimento\s+provisório"
    ],
    "Matriz de Riscos & Alocação": [
        r"matriz\s+de\s+risco", r"alocação\s+de\s+risco", r"riscos\s+contratuais", r"equilíbrio\s+econômico"
    ],
    "Direta (Dispensa / Inexigibilidade)": [
        r"art\.?\s*72", r"art\.?\s*74", r"art\.?\s*75", r"inviabilidade\s+de\s+competição",
        r"singularidade", r"notória\s+especialização", r"fracionamento"
    ],
    "Pareceres Referenciais (Art. 53 §5º)": [
        r"art\.?\s*53,?\s*§\s*5", r"parecer\s+referencial", r"manifestação\s+referencial",
        r"minuta\s+padronizada", r"modelo\s+padronizado"
    ]
}

ressalvas_por_categoria = {k: [] for k in categorias_ressalvas}
pareceres_referenciais_detalhes = []

riscos_por_fase = {
    "Planejamento": [],
    "Seleção do Fornecedor": [],
    "Execução e Gestão Contratual": []
}

total_lido = 0
with open(indice_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        total_lido += 1
        try:
            d = json.loads(line)
        except:
            continue
            
        cat = d.get("categoria", "")
        org = d.get("orgao", "")
        lbl = (d.get("label", "") + " " + d.get("objeto", "")).lower()
        resumo = (d.get("texto_resumo", "") or "").lower()
        md_path = d.get("arquivo_md", "")
        
        texto_completo = ""
        if md_path and os.path.exists(md_path):
            try:
                with open(md_path, "r", encoding="utf-8", errors="ignore") as mdf:
                    texto_completo = mdf.read()
            except:
                texto_completo = resumo
        else:
            texto_completo = resumo
            
        txt_l = texto_completo.lower()

        # 1. PROCESSAR PARECERES JURÍDICOS
        if cat == "parecer" or "parecer" in lbl or "juridico" in lbl or "parecer" in resumo:
            pareceres.append(d)
            
            # Verificar se é referencial
            is_ref = False
            for p in categorias_ressalvas["Pareceres Referenciais (Art. 53 §5º)"]:
                if re.search(p, txt_l):
                    is_ref = True
                    break
            if is_ref:
                pareceres_referenciais_detalhes.append({
                    "id": d.get("id"),
                    "orgao": org,
                    "ano": d.get("ano"),
                    "titulo": d.get("label"),
                    "objeto": d.get("objeto")
                })
                
            # Classificar trechos de ressalva
            frases = re.split(r'[\.\n;]', texto_completo)
            for f_text in frases:
                f_clean = " ".join(f_text.split()).strip()
                if len(f_clean) < 35 or len(f_clean) > 280:
                    continue
                f_lower = f_clean.lower()
                
                # Deve conter termo indicativo de orientação/ressalva/alerta
                if not any(k in f_lower for k in [
                    "recomenda", "ressalva", "condiciona", "deverá", "necessário", "atentar", 
                    "orienta-se", "alerta", "sob pena", "providenciar", "exigir", "juntar"
                ]):
                    continue
                    
                # Classificar nas categorias
                for cat_nome, padroes in categorias_ressalvas.items():
                    if any(re.search(p, f_lower) for p in padroes):
                        if len(ressalvas_por_categoria[cat_nome]) < 30:
                            ressalvas_por_categoria[cat_nome].append({
                                "orgao": org,
                                "ano": d.get("ano"),
                                "texto": f_clean
                            })
                            
        # 2. PROCESSAR MATRIZES DE RISCO
        if cat == "mapa_riscos" or "risco" in lbl or "matriz" in lbl:
            matrizes.append(d)
            
            # Identificar eventos de risco e fase
            frases = re.split(r'[\.\n;]', texto_completo)
            for f_text in frases:
                f_clean = " ".join(f_text.split()).strip()
                if len(f_clean) < 30 or len(f_clean) > 250:
                    continue
                f_low = f_clean.lower()
                
                if any(k in f_low for k in ["risco", "falha", "atraso", "inadimplemento", "descumprimento", "prejuízo", "defeito"]):
                    if any(p in f_low for p in ["especificação", "projeto", "estimativa", "edital", "tr", "etp", "demanda"]):
                        if len(riscos_por_fase["Planejamento"]) < 25:
                            riscos_por_fase["Planejamento"].append({"orgao": org, "evento": f_clean})
                    elif any(p in f_low for p in ["proposta", "deserção", "recurso", "conluio", "habilitação", "lance"]):
                        if len(riscos_por_fase["Seleção do Fornecedor"]) < 25:
                            riscos_por_fase["Seleção do Fornecedor"].append({"orgao": org, "evento": f_clean})
                    elif any(p in f_low for p in ["entrega", "execução", "trabalhista", "sla", "fiscalização", "reajuste", "pagamento"]):
                        if len(riscos_por_fase["Execução e Gestão Contratual"]) < 25:
                            riscos_por_fase["Execução e Gestão Contratual"].append({"orgao": org, "evento": f_clean})

        # 3. DFDs
        if cat == "dfd" or "dfd" in lbl or "formalização da demanda" in lbl:
            dfds.append(d)

print(f"Total Pareceres Analisados: {len(pareceres)}")
print(f"Pareceres Referenciais / Modelos Padronizados: {len(pareceres_referenciais_detalhes)}")
print(f"Total Matrizes de Risco: {len(matrizes)}")
print(f"Total DFDs: {len(dfds)}")

stats_por_cat_ressalva = {k: len(v) for k, v in ressalvas_por_categoria.items()}
print("Ressalvas por categoria extraídas:", stats_por_cat_ressalva)

output_data = {
    "metricas_gerais": {
        "total_pareceres": len(pareceres),
        "total_pareceres_referenciais": len(pareceres_referenciais_detalhes),
        "total_matrizes_risco": len(matrizes),
        "total_dfds_checklists": len(dfds)
    },
    "pareceres_referenciais_amostra": pareceres_referenciais_detalhes[:15],
    "ressalvas_tematicas": ressalvas_por_categoria,
    "matriz_riscos_fases": riscos_por_fase
}

out_file = r"E:\Thiago\Dev\Mapeamento TCE\validacao\estudo_detalhado_controle_interno_juridico.json"
with open(out_file, "w", encoding="utf-8") as fp:
    json.dump(output_data, fp, indent=2, ensure_ascii=False)

print(f"Estudo detalhado gravado com sucesso em: {out_file}")
