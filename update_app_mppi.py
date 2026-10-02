# -*- coding: utf-8 -*-
import re

app_path = r"E:\Thiago\Dev\Mapeamento TCE\dashboard\src\App.jsx"

with open(app_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Import jurisprudência data
if "import jurisData from" not in content:
    content = content.replace(
        "import corpusData from './data/corpus_resumo.json';",
        "import corpusData from './data/corpus_resumo.json';\nimport jurisData from './data/jurisprudencia_resumo.json';"
    )

# 2. Update CustomTooltip colors
content = content.replace("border: '1px solid rgba(197,160,89,0.4)'", "border: '1px solid rgba(166,2,37,0.5)'")
content = content.replace("entry.color || '#c5a059'", "entry.color || '#a60225'")
content = content.replace("background: entry.color || '#c5a059'", "background: entry.color || '#a60225'")

# 3. Add jurisprudência filter state in App component
if "const [jurisSearch, setJurisSearch]" not in content:
    content = content.replace(
        "const [selectedCat, setSelectedCat] = useState('TODOS');",
        "const [selectedCat, setSelectedCat] = useState('TODOS');\n  const [jurisSearch, setJurisSearch] = useState('');\n  const [selectedJurisClasse, setSelectedJurisClasse] = useState('TODOS');"
    )

# 4. Replace gold colors with official MPPI red #a60225 or #ff4d6d or #e2e8f0
content = content.replace("color: '#c5a059'", "color: '#a60225'")
content = content.replace("color: \"#c5a059\"", "color: \"#a60225\"")
content = content.replace("'#c5a059'", "'#a60225'")
content = content.replace('"#c5a059"', '"#a60225"')
content = content.replace("rgba(197,160,89", "rgba(166,2,37")
content = content.replace("rgba(197, 160, 89", "rgba(166, 2, 37")
content = content.replace("#9b111e", "#a60225")

# 5. Update brand sidebar
old_brand = """            <div className="brand">
              <div className="brand-icon">
                <Shield size={26} color="#a60225" />
              </div>
              <div>
                <div className="brand-title">PROJETO Lic.IA</div>
                <div className="brand-sub">Governana & Compras Pǧblicas ? MPPI</div>
              </div>
            </div>"""

new_brand = """            <div className="brand-wrapper">
              <div className="brand-mppi-header">
                <img src="/logo_mppi.png" alt="Ministério Público do Estado do Piauí" className="mppi-logo-img" />
              </div>
              <div>
                <div className="brand-title-licia">PROJETO <span>Lic.IA</span></div>
                <div className="brand-sub">Observatório de Governança & Compras</div>
                <div className="brand-unit">CLC • Ministério Público do Piauí</div>
              </div>
            </div>"""

content = re.sub(r'<div className="brand">.*?</div>\s*</div>\s*</div>', new_brand, content, flags=re.DOTALL)

# 6. Add Jurisprudência nav item
old_nav_item = """              <button 
                className={`nav-item ${activeTab === 'controle' ? 'active' : ''}`}
                onClick={() => setActiveTab('controle')}
              >
                <ShieldCheck size={18} /> Controle Interno & Jurdico
              </button>"""

new_nav_items = """              <button 
                className={`nav-item ${activeTab === 'jurisprudencia' ? 'active' : ''}`}
                onClick={() => setActiveTab('jurisprudencia')}
              >
                <Scale size={18} /> Jurisprudência TCE-PI (1.766 Julgados)
              </button>

              <button 
                className={`nav-item ${activeTab === 'controle' ? 'active' : ''}`}
                onClick={() => setActiveTab('controle')}
              >
                <ShieldCheck size={18} /> Controle Interno & Jurídico
              </button>"""

if "activeTab === 'jurisprudencia'" not in content:
    # Look for controle button
    content = re.sub(
        r'<button\s+className=\{`nav-item \$\{activeTab === \'controle\'.*?Controle Interno & Jur.*?<\/button>',
        new_nav_items,
        content,
        flags=re.DOTALL
    )

# 7. Add Jurisprudência View section
juris_view = """
          {/* TAB 7: JURISPRUDÊNCIA TCE-PI (1.766 JULGADOS) */}
          {activeTab === 'jurisprudencia' && (
            <div>
              {/* BANNER INSTITUCIONAL DE JURISPRUDÊNCIA */}
              <div className="hero-portal" style={{ marginBottom: '28px' }}>
                <div className="card-tarja"></div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '20px' }}>
                  <div style={{ maxWidth: '800px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
                      <span className="tag tag-mppi">
                        <Scale size={13} /> AUDITORIA JURISPRUDENCIAL PREVENTIVA
                      </span>
                      <span className="tag tag-silver">
                        118 INFORMATIVOS PROCESSADOS
                      </span>
                    </div>
                    <h2 style={{ fontSize: '1.75rem', fontWeight: 800, color: '#ffffff', lineHeight: '1.25' }}>
                      Jurisprudência Consolidada do TCE-PI: 1.766 Julgados Estruturados
                    </h2>
                    <p style={{ color: '#cbd5e1', fontSize: '0.94rem', marginTop: '8px', lineHeight: '1.5' }}>
                      Módulo semântico da <strong>Lic.IA</strong> que cruza minutas, termos de referência e editais do MPPI com as teses fixadas pelo Plenário e pelas Câmaras do Tribunal de Contas, prevenindo apontamentos, sobrepreço e anulação de certames.
                    </p>
                  </div>
                  <div style={{ textAlign: 'right', background: 'rgba(10,14,23,0.85)', padding: '18px 24px', borderRadius: '12px', border: '1px solid rgba(166,2,37,0.3)' }}>
                    <div style={{ fontSize: '0.78rem', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Precedentes de Licitações</div>
                    <div style={{ fontSize: '2.4rem', fontWeight: 800, color: '#ffffff' }}>224</div>
                    <div style={{ fontSize: '0.76rem', color: '#ff4d6d' }}>Compras & Contratos</div>
                  </div>
                </div>
              </div>

              {/* STATS DE JURISPRUDÊNCIA */}
              <div className="stats-grid" style={{ gridTemplateColumns: 'repeat(4, 1fr)', marginBottom: '28px' }}>
                <div className="stat-card">
                  <div className="stat-label">Informativos Baixados</div>
                  <div className="stat-val">{jurisData.total_informativos}</div>
                  <div className="stat-sub">Pleno e Câmaras (PDFs íntegros)</div>
                </div>
                <div className="stat-card">
                  <div className="stat-label">Total de Julgados</div>
                  <div className="stat-val">{jurisData.total_julgados.toLocaleString()}</div>
                  <div className="stat-sub">Decisões, acórdãos e votos</div>
                </div>
                <div className="stat-card">
                  <div className="stat-label">Denúncias & Fraudes</div>
                  <div className="stat-val">278</div>
                  <div className="stat-sub">Apurações de irregularidades</div>
                </div>
                <div className="stat-card">
                  <div className="stat-label">Tomadas de Contas</div>
                  <div className="stat-val">210</div>
                  <div className="stat-sub">Dano ao erário e sobrepreço</div>
                </div>
              </div>

              {/* FILTROS & BUSCA EM TEMPO REAL */}
              <div className="card" style={{ marginBottom: '24px' }}>
                <div className="card-tarja"></div>
                <div style={{ display: 'flex', gap: '14px', flexWrap: 'wrap', alignItems: 'center' }}>
                  <div style={{ flex: 1, minWidth: '280px', position: 'relative' }}>
                    <Search size={18} style={{ position: 'absolute', left: '14px', top: '13px', color: '#94a3b8' }} />
                    <input 
                      type="text" 
                      placeholder="Pesquisar por processo, relator, município ou tema (ex: pregão, sobrepreço, resíduos)..."
                      value={jurisSearch}
                      onChange={e => setJurisSearch(e.target.value)}
                      style={{
                        width: '100%',
                        padding: '11px 16px 11px 42px',
                        background: 'rgba(10, 14, 23, 0.8)',
                        border: '1px solid rgba(226, 232, 240, 0.2)',
                        borderRadius: '8px',
                        color: '#fff',
                        fontSize: '0.88rem'
                      }}
                    />
                  </div>
                  <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                    {['TODOS', 'TOMADA DE CONTAS', 'DENÚNCIA', 'REPRESENTAÇÃO', 'RECURSO'].map(cls => (
                      <button 
                        key={cls}
                        className={`btn ${selectedJurisClasse === cls ? 'btn-vinho' : 'btn-outline'}`}
                        style={{ padding: '8px 14px', fontSize: '0.78rem' }}
                        onClick={() => setSelectedJurisClasse(cls)}
                      >
                        {cls}
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              {/* LISTAGEM DOS CASOS */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                {(jurisData.casos_destaque || [])
                  .filter(c => {
                    const matchSearch = jurisSearch === '' || 
                      (c.numero_processo && c.numero_processo.toLowerCase().includes(jurisSearch.toLowerCase())) ||
                      (c.objeto && c.objeto.toLowerCase().includes(jurisSearch.toLowerCase())) ||
                      (c.unidade_gestora && c.unidade_gestora.toLowerCase().includes(jurisSearch.toLowerCase())) ||
                      (c.resumo_julgamento && c.resumo_julgamento.toLowerCase().includes(jurisSearch.toLowerCase()));
                    const matchClasse = selectedJurisClasse === 'TODOS' || c.tipo_processo === selectedJurisClasse;
                    return matchSearch && matchClasse;
                  })
                  .slice(0, 25)
                  .map((item, idx) => (
                    <div key={item.id || idx} className="card" style={{ padding: '20px 24px' }}>
                      <div className="card-tarja"></div>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '10px', flexWrap: 'wrap', gap: '10px' }}>
                        <div>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                            <span className="tag tag-mppi">{item.tipo_processo}</span>
                            <span style={{ fontSize: '0.88rem', fontWeight: 800, color: '#ffffff' }}>
                              Processo {item.numero_processo}
                            </span>
                            <span style={{ color: '#64748b' }}>•</span>
                            <span style={{ fontSize: '0.8rem', color: '#cbd5e1' }}>{item.colegiado}</span>
                          </div>
                          <div style={{ fontSize: '0.78rem', color: '#94a3b8' }}>
                            Sessão: <strong>{item.data_sessao}</strong> | Relator: <strong>{item.relator}</strong> | UG: <strong style={{ color: '#f8fafc' }}>{item.unidade_gestora}</strong>
                          </div>
                        </div>
                        <button 
                          className="btn btn-outline" 
                          style={{ padding: '4px 10px', fontSize: '0.74rem' }}
                          onClick={() => handleCopy(item.resumo_julgamento, item.id)}
                        >
                          {copiedId === item.id ? <Check size={12} color="#10b981" /> : <Copy size={12} />} Copiar
                        </button>
                      </div>

                      {item.objeto && (
                        <div style={{ fontSize: '0.84rem', color: '#e2e8f0', marginBottom: '8px', lineHeight: '1.45', background: 'rgba(255,255,255,0.03)', padding: '8px 12px', borderRadius: '6px' }}>
                          <strong>Objeto:</strong> {item.objeto}
                        </div>
                      )}

                      <div style={{ fontSize: '0.82rem', color: '#cbd5e1', lineHeight: '1.45', borderLeft: '3px solid #a60225', paddingLeft: '12px' }}>
                        <strong>Decisão / Síntese:</strong> {item.resumo_julgamento}
                      </div>
                    </div>
                  ))}
              </div>
            </div>
          )}
"""

if "{activeTab === 'jurisprudencia' &&" not in content:
    # Insert right before </main>
    content = content.replace("        </main>", juris_view + "\n        </main>")

with open(app_path, "w", encoding="utf-8") as f:
    f.write(content)

print("App.jsx atualizado com sucesso no padrão do Manual do MPPI!")
