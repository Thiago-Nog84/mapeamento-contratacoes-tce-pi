# -*- coding: utf-8 -*-
import json
import sqlite3
import os

DB_PATH = r"E:\Thiago\Dev\Mapeamento TCE\dados_jurisprudencia_tce.db"
DEST_JSON = r"E:\Thiago\Dev\Mapeamento TCE\dashboard\src\data\jurisprudencia_resumo.json"

con = sqlite3.connect(DB_PATH)
con.row_factory = sqlite3.Row
cur = con.cursor()

# Get summary stats
total_julgados = cur.execute("SELECT COUNT(*) FROM julgados_tce").fetchone()[0]
total_info = cur.execute("SELECT COUNT(*) FROM informativos_tce").fetchone()[0]

classes = cur.execute("""
    SELECT tipo_processo, COUNT(*) as qtd 
    FROM julgados_tce 
    GROUP BY tipo_processo 
    ORDER BY qtd DESC
""").fetchall()

# Procurement specific cases (sample top 50)
lic_cases = cur.execute("""
    SELECT id, numero_processo, colegiado, data_sessao, relator, tipo_processo, unidade_gestora, objeto, resumo_julgamento
    FROM julgados_tce 
    WHERE objeto LIKE '%licita%' OR objeto LIKE '%preg%' OR objeto LIKE '%contrat%' 
       OR objeto LIKE '%edital%' OR objeto LIKE '%dispensa%' OR objeto LIKE '%inexig%'
       OR texto_bruto LIKE '%licita%' OR texto_bruto LIKE '%preg%' OR texto_bruto LIKE '%contrat%'
    ORDER BY id DESC
    LIMIT 60
""").fetchall()

output = {
    "total_julgados": total_julgados,
    "total_informativos": total_info,
    "total_licitacoes": len(cur.execute("""
        SELECT id FROM julgados_tce 
        WHERE objeto LIKE '%licita%' OR objeto LIKE '%preg%' OR objeto LIKE '%contrat%' 
           OR objeto LIKE '%edital%' OR objeto LIKE '%dispensa%' OR objeto LIKE '%inexig%'
           OR texto_bruto LIKE '%licita%' OR texto_bruto LIKE '%preg%' OR texto_bruto LIKE '%contrat%'
    """).fetchall()),
    "classes": [{"nome": r["tipo_processo"], "qtd": r["qtd"]} for r in classes],
    "casos_destaque": [dict(r) for r in lic_cases]
}

with open(DEST_JSON, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Salvo {DEST_JSON} com sucesso ({len(output['casos_destaque'])} casos amostrados).")
