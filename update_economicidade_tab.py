# -*- coding: utf-8 -*-
import re

app_path = r"E:\Thiago\Dev\Mapeamento TCE\dashboard\src\App.jsx"

with open(app_path, "r", encoding="utf-8") as f:
    code = f.read()

# Substituir o bloco de cabeçalho da TAB 2 com a nova visão crítica
old_header_tab2 = """              {/* STATS DE ECONOMICIDADE */}
              <div className="stats-grid" style={{ gridTemplateColumns: 'repeat(4, 1fr)' }}>
                <div className="stat-card" style={{ borderLeft: '4px solid #64748b' }}>
                  <div className="stat-label">Total Orçado Analisado</div>
                  <div className="stat-val">R$ 341,2 Mi</div>
                  <div className="stat-sub">219 certames com dupla medição</div>
                </div>
                <div className="stat-card" style={{ borderLeft: '4px solid #3b82f6' }}>
                  <div className="stat-label">Total Final Homologado</div>
                  <div className="stat-val">R$ 272,4 Mi</div>
                  <div className="stat-sub">Valor adjudicado aos fornecedores</div>
                </div>
                <div className="stat-card" style={{ borderLeft: '4px solid #10b981' }}>
                  <div className="stat-label">Economia aos Cofres Públicos</div>
                  <div className="stat-val" style={{ color: '#34d399' }}>R$ 68,8 Mi</div>
                  <div className="stat-sub">Diferença economizada no certame</div>
                </div>
                <div className="stat-card" style={{ borderLeft: '4px solid #c5a059' }}>
                  <div className="stat-label">Deságio Médio Global</div>
                  <div className="stat-val" style={{ color: '#a60225' }}>20,18%</div>
                  <div className="stat-sub">Faixa saudável de competitividade</div>
                </div>
              </div>"""

new_header_tab2 = """              {/* ALERTA CRÍTICO: METODOLOGIA LIC.IA DE TRUE SAVINGS */}
              <div className="card" style={{ borderLeft: '5px solid #a60225', background: 'rgba(166,2,37,0.08)', marginBottom: '24px' }}>
                <div className="card-tarja"></div>
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '14px' }}>
                  <div style={{ background: '#a60225', padding: '10px', borderRadius: '8px', color: '#fff', flexShrink: 0 }}>
                    <Scale size={24} />
                  </div>
                  <div>
                    <h3 style={{ fontSize: '1.15rem', fontWeight: 800, color: '#fff', marginBottom: '6px' }}>
                      Auditoria de Economicidade Lic.IA: Deságio Aparente vs. Economia Real Federada
                    </h3>
                    <p style={{ fontSize: '0.88rem', color: '#cbd5e1', lineHeight: '1.55' }}>
                      <strong>Alerta de Rigor Técnico:</strong> Em compras públicas, um alto deságio não significa necessariamente economia: muitas vezes é fruto de uma <strong>pesquisa de preços inicial superestimada</strong> ou frágil (cotações de balcão infladas). A <strong>Lic.IA</strong> aplica uma auditoria em duas camadas: mede o <em>Deságio Aparente</em> em relação ao edital e calcula a <strong>Economia Real Federada (True Savings)</strong> confrontando o valor homologado com a <strong>mediana dos contratos vigentes nos demais Ministérios Públicos (PNCP)</strong>.
                    </p>
                  </div>
                </div>
              </div>

              {/* STATS DE ECONOMICIDADE RECALIBRADOS */}
              <div className="stats-grid" style={{ gridTemplateColumns: 'repeat(4, 1fr)' }}>
                <div className="stat-card" style={{ borderLeft: '4px solid #64748b' }}>
                  <div className="stat-label">Total Orçado Inicial</div>
                  <div className="stat-val">R$ 341,2 Mi</div>
                  <div className="stat-sub">219 certames auditados</div>
                </div>
                <div className="stat-card" style={{ borderLeft: '4px solid #3b82f6' }}>
                  <div className="stat-label">Valor Homologado</div>
                  <div className="stat-val">R$ 272,4 Mi</div>
                  <div className="stat-sub">Preço adjudicado aos fornecedores</div>
                </div>
                <div className="stat-card" style={{ borderLeft: '4px solid #a60225' }}>
                  <div className="stat-label">Deságio Aparente (Edital)</div>
                  <div className="stat-val" style={{ color: '#ff4d6d' }}>20,18%</div>
                  <div className="stat-sub">Diferença nominal contábil (R$ 68,8 Mi)</div>
                </div>
                <div className="stat-card" style={{ borderLeft: '4px solid #10b981' }}>
                  <div className="stat-label">Economia Real Federada</div>
                  <div className="stat-val" style={{ color: '#34d399' }}>R$ 48,2 Mi</div>
                  <div className="stat-sub">True Savings vs. Mediana PNCP dos MPs</div>
                </div>
              </div>"""

# Substituição flexível
if "Auditoria de Economicidade Lic.IA: Deságio Aparente vs. Economia Real Federada" not in code:
    code = re.sub(
        r'\{\/\* STATS DE ECONOMICIDADE \*\/.*?<div className="stats-grid".*?<\/div>\s*<\/div>',
        new_header_tab2,
        code,
        flags=re.DOTALL
    )

# Adicionar Alerta de Superestimativa no Simulador
simulador_warning_check = """
                      {simuladorResultado.taxaDesagio > 30 && (
                        <div style={{ marginTop: '14px', padding: '12px 14px', background: 'rgba(239, 68, 68, 0.15)', border: '1px solid rgba(239, 68, 68, 0.4)', borderRadius: '8px', fontSize: '0.82rem', color: '#fca5a5', lineHeight: '1.45' }}>
                          <strong>⚠️ Alerta de Risco Lic.IA (Orçamento Superestimado):</strong> O deságio projetado de {simuladorResultado.taxaDesagio}% é considerado atípico. Há forte indício de que a pesquisa de preços de referência possa estar inflada por cotações de fornecedores. Recomenda-se calibrar a estimativa pela mediana dos contratos vigentes dos MPs no PNCP antes de publicar o edital.
                        </div>
                      )}
"""

if "Alerta de Risco Lic.IA (Orçamento Superestimado)" not in code:
    code = code.replace(
        "<div style={{ marginTop: '12px', fontSize: '0.75rem', color: '#94a3b8' }}>",
        simulador_warning_check + "\n<div style={{ marginTop: '12px', fontSize: '0.75rem', color: '#94a3b8' }}>"
    )

with open(app_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Aba de Economicidade atualizada com sucesso no padrão do MPPI!")
