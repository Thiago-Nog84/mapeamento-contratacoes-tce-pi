# -*- coding: utf-8 -*-
import sqlite3
import json

con = sqlite3.connect("E:/Thiago/Dev/Mapeamento TCE/dados_jurisprudencia_tce.db")
con.row_factory = sqlite3.Row
cur = con.cursor()

print("--- AMOSTRA DE JULGADOS EXTRAÍDOS DO TCE-PI ---")
rows = cur.execute("""
    SELECT colegiado, data_sessao, relator, numero_processo, tipo_processo, unidade_gestora, objeto, resumo_julgamento 
    FROM julgados_tce 
    WHERE tipo_processo != 'Outros' OR objeto != ''
    LIMIT 4
""").fetchall()

for i, r in enumerate(rows):
    print(f"\n[{i+1}] Processo: {r['numero_processo']} | Colegiado: {r['colegiado']}")
    print(f"    Sessão: {r['data_sessao']} | Relator: {r['relator']}")
    print(f"    Classe: {r['tipo_processo']} | UG: {r['unidade_gestora']}")
    print(f"    Objeto: {r['objeto']}")
    print(f"    Decisão/Resumo: {r['resumo_julgamento']}")
