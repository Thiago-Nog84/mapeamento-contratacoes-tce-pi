# -*- coding: utf-8 -*-
import os
import sqlite3
import json

DB_PATH = r"E:\Thiago\Dev\Mapeamento TCE\dados_jurisprudencia_tce.db"
DEST_DIR = r"C:\Users\thiagonogueira\OneDrive - mppi.mp.br\CLC\01_Processos_e_Aquisicoes\Base de Conhecimento - Thiago\02_Jurisprudencia_e_Orientacoes\Informativos_Julgamentos_TCE_PI"

os.makedirs(DEST_DIR, exist_ok=True)

con = sqlite3.connect(DB_PATH)
con.row_factory = sqlite3.Row
cur = con.cursor()

def format_julgados_md(titulo, subtitulo, rows, is_licitacao=False):
    md = []
    md.append(f"# ⚖️ {titulo}")
    md.append(f"### {subtitulo}")
    md.append("")
    md.append(f"**Fonte Oficial:** Tribunal de Contas do Estado do Piauí (TCE-PI) • Informativos de Julgamentos das Sessões")
    md.append(f"**Total de Processos Mapeados:** {len(rows)}")
    md.append(f"**Integração:** Projeto Lic.IA • Observatório de Governança & Compras Públicas (MPPI / CLC)")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 📋 Índice Rápido de Processos")
    md.append("")
    md.append("| Processo | Colegiado | Data Sessão | Relator | Unidade Gestora | Tipo |")
    md.append("| :--- | :--- | :---: | :--- | :--- | :--- |")
    for r in rows:
        proc = r["numero_processo"]
        col = r["colegiado"]
        dt = r["data_sessao"]
        rel = r["relator"].replace("\n", " ").strip()
        ug = (r["unidade_gestora"] or "Não informada").strip()
        tp = r["tipo_processo"]
        anchor = proc.replace("/", "").replace("-", "").lower()
        md.append(f"| [{proc}](#{anchor}) | {col} | {dt} | {rel} | {ug} | {tp} |")
    
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 🔍 Detalhamento dos Julgados")
    md.append("")
    
    for i, r in enumerate(rows):
        proc = r["numero_processo"]
        anchor = proc.replace("/", "").replace("-", "").lower()
        col = r["colegiado"]
        dt = r["data_sessao"]
        rel = r["relator"].replace("\n", " ").strip()
        ug = (r["unidade_gestora"] or "Não informada").strip()
        tp = r["tipo_processo"]
        obj = (r["objeto"] or "Objeto não detalhado formalmente na pauta.").strip()
        dec = (r["resumo_julgamento"] or "Consulte o acórdão na íntegra.").strip()
        raw = (r["texto_bruto"] or "").strip()
        
        md.append(f"### <a id=\"{anchor}\"></a>{i+1}. Processo {proc} • {tp}")
        md.append(f"* **Colegiado:** {col}")
        md.append(f"* **Data da Sessão:** {dt}")
        md.append(f"* **Relator:** {rel}")
        md.append(f"* **Unidade Gestora:** {ug}")
        if obj:
            md.append(f"* **Objeto / Fato Apurado:** {obj}")
        md.append("")
        md.append(f"> **Síntese / Decisão Registrada:**")
        md.append(f"> {dec}")
        md.append("")
        if len(raw) > len(dec) + 50:
            md.append("<details>")
            md.append("<summary>📄 Ver extrato completo da pauta / informativo</summary>")
            md.append("")
            md.append("```text")
            md.append(raw[:1500])
            md.append("```")
            md.append("</details>")
            md.append("")
        md.append("---")
        md.append("")
        
    return "\n".join(md)

# 1. Especial Licitações e Contratos (224 julgados)
print("Gerando: 01_Licitacoes_e_Contratos_Julgados_TCE_PI.md...")
lic_rows = cur.execute("""
    SELECT * FROM julgados_tce 
    WHERE objeto LIKE '%licita%' OR objeto LIKE '%preg%' OR objeto LIKE '%contrat%' 
       OR objeto LIKE '%edital%' OR objeto LIKE '%dispensa%' OR objeto LIKE '%inexig%'
       OR texto_bruto LIKE '%licita%' OR texto_bruto LIKE '%preg%' OR texto_bruto LIKE '%contrat%'
    ORDER BY id DESC
""").fetchall()

with open(os.path.join(DEST_DIR, "01_Licitacoes_e_Contratos_Julgados_TCE_PI.md"), "w", encoding="utf-8") as f:
    f.write(format_julgados_md(
        "TCE-PI • Jurisprudência Especializada em Licitações e Contratos",
        "Coletânea de 224 Julgados sobre Editais, Pregões, Contratos, Sobrepreço e Sanções",
        lic_rows,
        is_licitacao=True
    ))

# 2. Denúncias (278 julgados)
print("Gerando: 02_Denuncias_Licitacoes_e_Fraudes_TCE_PI.md...")
den_rows = cur.execute("SELECT * FROM julgados_tce WHERE tipo_processo = 'DENÚNCIA' ORDER BY id DESC").fetchall()
with open(os.path.join(DEST_DIR, "02_Denuncias_Licitacoes_e_Fraudes_TCE_PI.md"), "w", encoding="utf-8") as f:
    f.write(format_julgados_md(
        "TCE-PI • Julgados em Denúncias",
        "Apuração de Fraudes, Direcionamento de Certames e Irregularidades na Gestão Pública",
        den_rows
    ))

# 3. Recursos, Agravos e Embargos (327 julgados)
print("Gerando: 03_Recursos_Agravos_Embargos_TCE_PI.md...")
rec_rows = cur.execute("SELECT * FROM julgados_tce WHERE tipo_processo IN ('RECURSO', 'AGRAVO', 'EMBARGOS') ORDER BY id DESC").fetchall()
with open(os.path.join(DEST_DIR, "03_Recursos_Agravos_Embargos_TCE_PI.md"), "w", encoding="utf-8") as f:
    f.write(format_julgados_md(
        "TCE-PI • Julgados em Recursos, Agravos e Embargos",
        "Teses Recursais e Fixação de Entendimentos pelo Pleno e pelas Câmaras",
        rec_rows
    ))

# 4. Tomadas de Contas Especiais (210 julgados)
print("Gerando: 04_Tomadas_de_Contas_Especiais_TCE_PI.md...")
tce_rows = cur.execute("SELECT * FROM julgados_tce WHERE tipo_processo = 'TOMADA DE CONTAS' ORDER BY id DESC").fetchall()
with open(os.path.join(DEST_DIR, "04_Tomadas_de_Contas_Especiais_TCE_PI.md"), "w", encoding="utf-8") as f:
    f.write(format_julgados_md(
        "TCE-PI • Julgados em Tomadas de Contas Especiais (TCE)",
        "Apuração de Dano ao Erário, Desvio de Finalidade, Superfaturamento e Imputação de Débito",
        tce_rows
    ))

# 5. Representações (176 julgados)
print("Gerando: 05_Representacoes_Licitantes_TCE_PI.md...")
rep_rows = cur.execute("SELECT * FROM julgados_tce WHERE tipo_processo = 'REPRESENTAÇÃO' ORDER BY id DESC").fetchall()
with open(os.path.join(DEST_DIR, "05_Representacoes_Licitantes_TCE_PI.md"), "w", encoding="utf-8") as f:
    f.write(format_julgados_md(
        "TCE-PI • Julgados em Representações",
        "Impugnações a Editais formuladas por Empresas Licitantes e Órgãos Ministeriais",
        rep_rows
    ))

# 6. Prestações de Contas (61 julgados)
print("Gerando: 06_Prestacoes_de_Contas_TCE_PI.md...")
pc_rows = cur.execute("SELECT * FROM julgados_tce WHERE tipo_processo = 'PRESTAÇÃO DE CONTAS' ORDER BY id DESC").fetchall()
with open(os.path.join(DEST_DIR, "06_Prestacoes_de_Contas_TCE_PI.md"), "w", encoding="utf-8") as f:
    f.write(format_julgados_md(
        "TCE-PI • Julgados em Prestações de Contas",
        "Regularidade e Aprovação com Ressalvas de Contas de Gestão e Governo",
        pc_rows
    ))

# 7. Auditorias & Medidas Cautelares (26 julgados)
print("Gerando: 07_Auditorias_e_Medidas_Cautelares_TCE_PI.md...")
aud_rows = cur.execute("SELECT * FROM julgados_tce WHERE tipo_processo IN ('AUDITORIA', 'MEDIDA CAUTELAR') ORDER BY id DESC").fetchall()
with open(os.path.join(DEST_DIR, "07_Auditorias_e_Medidas_Cautelares_TCE_PI.md"), "w", encoding="utf-8") as f:
    f.write(format_julgados_md(
        "TCE-PI • Auditorias e Medidas Cautelares",
        "Suspensão Cautelar de Licitações e Fiscalizações Temáticas",
        aud_rows
    ))

# 8. Outros Procedimentos e Consultas (688 julgados)
print("Gerando: 08_Outros_Procedimentos_e_Consultas_TCE_PI.md...")
out_rows = cur.execute("SELECT * FROM julgados_tce WHERE tipo_processo IN ('Outros', 'CONSULTA') ORDER BY id DESC").fetchall()
with open(os.path.join(DEST_DIR, "08_Outros_Procedimentos_e_Consultas_TCE_PI.md"), "w", encoding="utf-8") as f:
    f.write(format_julgados_md(
        "TCE-PI • Outros Procedimentos, Incidentes e Consultas",
        "Consultas Formais, Despachos e Incidentes Julgados pelos Colegiados",
        out_rows
    ))

# 9. Painel Consolidado de Governança
print("Gerando: 00_PAINEL_CONSOLIDADO_JURISPRUDENCIA_TCE_PI.md...")
painel_md = f"""# 🏛️ Base de Conhecimento • Jurisprudência Consolidada do TCE-PI
### Módulo de Governança Jurisprudencial do PROJETO Lic.IA (MPPI / CLC)

Este diretório reúne a extração sistemática e semântica de **1.766 julgados e processos** a partir de **118 Informativos de Julgamentos Oficiais** do Tribunal de Contas do Estado do Piauí (TCE-PI), abrangendo sessões plenárias e de câmaras.

---

## 📊 Matriz de Distribuição Processual

| Arquivo de Conhecimento | Classe Processual | Qtd. Processos | Foco Temático / Aplicação na CLC |
| :--- | :--- | :---: | :--- |
| [`01_Licitacoes_e_Contratos_Julgados_TCE_PI.md`](01_Licitacoes_e_Contratos_Julgados_TCE_PI.md) | **Especial Compras Públicas** | **224** | **Editais, pregões, termos de referência, sobrepreço e sanções a licitantes.** |
| [`02_Denuncias_Licitacoes_e_Fraudes_TCE_PI.md`](02_Denuncias_Licitacoes_e_Fraudes_TCE_PI.md) | Denúncias | **278** | Direcionamento de licitações, sobrepreço e irregularidades denunciadas. |
| [`03_Recursos_Agravos_Embargos_TCE_PI.md`](03_Recursos_Agravos_Embargos_TCE_PI.md) | Recursos, Agravos e Embargos | **327** | Teses consolidadas em grau de recurso e deliberações do Tribunal Pleno. |
| [`04_Tomadas_de_Contas_Especiais_TCE_PI.md`](04_Tomadas_de_Contas_Especiais_TCE_PI.md) | Tomadas de Contas Especiais | **210** | Dano ao erário, superfaturamento contratual e imputação de débito. |
| [`05_Representacoes_Licitantes_TCE_PI.md`](05_Representacoes_Licitantes_TCE_PI.md) | Representações | **176** | Impugnações a cláusulas restritivas de competitividade feitas por licitantes. |
| [`06_Prestacoes_de_Contas_TCE_PI.md`](06_Prestacoes_de_Contas_TCE_PI.md) | Prestações de Contas | **61** | Regularidade formal de despesas governamentais e compras de gestão. |
| [`07_Auditorias_e_Medidas_Cautelares_TCE_PI.md`](07_Auditorias_e_Medidas_Cautelares_TCE_PI.md) | Auditorias e Cautelares | **26** | Suspensão cautelar de certames com risco de dano irreparável. |
| [`08_Outros_Procedimentos_e_Consultas_TCE_PI.md`](08_Outros_Procedimentos_e_Consultas_TCE_PI.md) | Consultas e Outros | **688** | Interpretação normativa formal e incidentes colegiados. |
| **TOTAL GERAL** | **Colegiados do TCE-PI** | **1.766** | **Base de Inteligência Preventiva para a CLC / MPPI** |

---

## 🎯 Aplicação Prática no Trabalho da CLC / MPPI

1. **Auditoria de Minutas**: Confronto prévio das exigências de habilitação com as cláusulas que já foram derrubadas em Representações e Denúncias no TCE-PI.
2. **Mitigação de Riscos**: Evitar redações em Termos de Referência que geraram Tomadas de Contas Especiais por sobrepreço ou fiscalização deficiente.
3. **Alimentação do RAG da Lic.IA**: Toda esta base está catalogada em formato Markdown e JSON para suporte imediato a consultas semânticas por modelos de Inteligência Artificial.
"""

with open(os.path.join(DEST_DIR, "00_PAINEL_CONSOLIDADO_JURISPRUDENCIA_TCE_PI.md"), "w", encoding="utf-8") as f:
    f.write(painel_md)

print("Exportação concluída com sucesso para:", DEST_DIR)
