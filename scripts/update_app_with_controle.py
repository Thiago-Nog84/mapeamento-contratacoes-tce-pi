import sys, os

app_path = r"E:\Thiago\Dev\Mapeamento TCE\dashboard\src\App.jsx"

with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update imports
old_import = "import { \n  Shield, FileText, Search, Activity, Scale, \n  CheckCircle, Copy, TrendingDown\n} from 'lucide-react';"
new_import = """import { 
  Shield, FileText, Search, Activity, Scale, 
  CheckCircle, Copy, TrendingDown, ShieldCheck, AlertTriangle, Layers, BookOpen, CheckSquare
} from 'lucide-react';"""

if old_import in content:
    content = content.replace(old_import, new_import)
else:
    # Try more permissive replacement
    content = content.replace("TrendingDown\n} from 'lucide-react';", "TrendingDown, ShieldCheck, AlertTriangle, Layers, BookOpen, CheckSquare\n} from 'lucide-react';")

# 2. Add state for active control sub-view & checklist in App component
old_state = "  const [copiedId, setCopiedId] = useState(null);"
new_state = """  const [copiedId, setCopiedId] = useState(null);
  const [controleSubTab, setControleSubTab] = useState('ressalvas');
  const [checkedItems, setCheckedItems] = useState({});

  const toggleCheck = (codigo) => {
    setCheckedItems(prev => ({
      ...prev,
      [codigo]: !prev[codigo]
    }));
  };"""

if old_state in content:
    content = content.replace(old_state, new_state)

# 3. Add Nav Menu Item
old_nav_economicidade = """          <button 
            className={`nav-item ${activeTab === 'economicidade' ? 'active' : ''}`}
            onClick={() => setActiveTab('economicidade')}
          >
            <TrendingDown size={20} /> Economicidade & Deságio
          </button>"""

# Notice encoding in file might be Desgio or Deságio
nav_target = None
for candidate in [
    """<button \n            className={`nav-item ${activeTab === 'economicidade' ? 'active' : ''}`}\n            onClick={() => setActiveTab('economicidade')}\n          >\n            <TrendingDown size={20} /> Economicidade & Desgio\n          </button>""",
    """<button \n            className={`nav-item ${activeTab === 'economicidade' ? 'active' : ''}`}\n            onClick={() => setActiveTab('economicidade')}\n          >\n            <TrendingDown size={20} /> Economicidade & Deságio\n          </button>"""
]:
    if candidate in content:
        nav_target = candidate
        break

new_nav_item = """

          <button 
            className={`nav-item ${activeTab === 'controle' ? 'active' : ''}`}
            onClick={() => setActiveTab('controle')}
          >
            <ShieldCheck size={20} /> Controle Interno & Jurídico
          </button>"""

if nav_target:
    content = content.replace(nav_target, nav_target + new_nav_item)
else:
    print("WARNING: Could not find exact nav target, trying fallback insertion")
    content = content.replace("setActiveTab('economicidade')", "setActiveTab('economicidade')")

# 4. Topbar Title for Controle
old_topbar_title = "{activeTab === 'economicidade' && 'Estudo de Economicidade: Orçado vs. Homologado (R$ 341M Analisados)'}"
for candidate_title in [
    "{activeTab === 'economicidade' && 'Estudo de Economicidade: Orado vs. Homologado (R$ 341M Analisados)'}",
    "{activeTab === 'economicidade' && 'Estudo de Economicidade: Orçado vs. Homologado (R$ 341M Analisados)'}"
]:
    if candidate_title in content:
        content = content.replace(
            candidate_title,
            candidate_title + "\n              {activeTab === 'controle' && 'Controle Interno e Jurídico: Matrizes de Risco, Pareceres e Linhas de Defesa'}"
        )
        break

# 5. Build the entire Controle Tab Pane JSX
controle_tab_jsx = '''
        {/* TAB: CONTROLE INTERNO & JURÍDICO */}
        {activeTab === 'controle' && (
          <div className="tab-pane">
            {/* STATS DE CONTROLE */}
            <div className="stats-grid" style={{ gridTemplateColumns: 'repeat(4, 1fr)' }}>
              <div className="stat-card" style={{ borderLeft: '4px solid #3b82f6' }}>
                <div className="stat-label">Pareceres Jurídicos</div>
                <div className="stat-val">{corpusData.controle_interno_juridico?.kpis.total_pareceres || 662}</div>
                <div className="stat-sub">Análises de legalidade mapeadas</div>
              </div>
              <div className="stat-card" style={{ borderLeft: '4px solid #c5a059' }}>
                <div className="stat-label">Matrizes de Risco</div>
                <div className="stat-val">{corpusData.controle_interno_juridico?.kpis.matrizes_risco || 146}</div>
                <div className="stat-sub">Mapas de risco estruturados</div>
              </div>
              <div className="stat-card" style={{ borderLeft: '4px solid #10b981' }}>
                <div className="stat-label">DFDs / Demanda (1ª Linha)</div>
                <div className="stat-val">{corpusData.controle_interno_juridico?.kpis.dfds_checklists || 451}</div>
                <div className="stat-sub">Instrumentos de formalização</div>
              </div>
              <div className="stat-card" style={{ borderLeft: '4px solid #8b5cf6' }}>
                <div className="stat-label">Pareceres Referenciais</div>
                <div className="stat-val">{corpusData.controle_interno_juridico?.kpis.pareceres_referenciais || 31}</div>
                <div className="stat-sub">Sob o Art. 53, § 5º da Lei 14.133</div>
              </div>
            </div>

            {/* SUB-MENU DE CONTROLE */}
            <div style={{ display: 'flex', gap: '10px', marginTop: '24px', marginBottom: '20px', borderBottom: '1px solid #1e293b', paddingBottom: '12px' }}>
              <button 
                className={`btn ${controleSubTab === 'ressalvas' ? 'btn-primary' : 'btn-outline'}`}
                style={{ fontSize: '0.88rem', padding: '8px 16px' }}
                onClick={() => setControleSubTab('ressalvas')}
              >
                <AlertTriangle size={16} style={{ marginRight: '6px', verticalAlign: 'text-bottom' }} />
                Top Ressalvas Jurídicas Recorrentes
              </button>
              <button 
                className={`btn ${controleSubTab === 'linhas' ? 'btn-primary' : 'btn-outline'}`}
                style={{ fontSize: '0.88rem', padding: '8px 16px' }}
                onClick={() => setControleSubTab('linhas')}
              >
                <Layers size={16} style={{ marginRight: '6px', verticalAlign: 'text-bottom' }} />
                As 3 Linhas de Defesa (Art. 169)
              </button>
              <button 
                className={`btn ${controleSubTab === 'matrizes' ? 'btn-primary' : 'btn-outline'}`}
                style={{ fontSize: '0.88rem', padding: '8px 16px' }}
                onClick={() => setControleSubTab('matrizes')}
              >
                <Activity size={16} style={{ marginRight: '6px', verticalAlign: 'text-bottom' }} />
                Matrizes de Risco & Alocação
              </button>
              <button 
                className={`btn ${controleSubTab === 'referenciais' ? 'btn-primary' : 'btn-outline'}`}
                style={{ fontSize: '0.88rem', padding: '8px 16px' }}
                onClick={() => setControleSubTab('referenciais')}
              >
                <BookOpen size={16} style={{ marginRight: '6px', verticalAlign: 'text-bottom' }} />
                Pareceres Referenciais (Art. 53, § 5º)
              </button>
              <button 
                className={`btn ${controleSubTab === 'checklist' ? 'btn-primary' : 'btn-outline'}`}
                style={{ fontSize: '0.88rem', padding: '8px 16px' }}
                onClick={() => setControleSubTab('checklist')}
              >
                <CheckSquare size={16} style={{ marginRight: '6px', verticalAlign: 'text-bottom' }} />
                Master Checklist CLC/MPPI
              </button>
            </div>

            {/* CONTEÚDO 1: TOP RESSALVAS JURÍDICAS RECORRENTES */}
            {controleSubTab === 'ressalvas' && (
              <div>
                <div style={{ marginBottom: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <h3 style={{ fontSize: '1.15rem', color: '#f8fafc', fontWeight: 600 }}>
                      Catálogo das 6 Ressalvas Mais Frequentes nos 662 Pareceres Jurídicos
                    </h3>
                    <p style={{ color: '#94a3b8', fontSize: '0.85rem', marginTop: '2px' }}>
                      Diretrizes preventivas extraídas das manifestações jurídicas para blindar os certames do MPPI
                    </p>
                  </div>
                  <span className="tag" style={{ background: 'rgba(239, 68, 68, 0.15)', color: '#f87171', border: '1px solid rgba(239, 68, 68, 0.3)' }}>
                    Concentram 88% das Devoluções de Processos
                  </span>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '16px' }}>
                  {(corpusData.controle_interno_juridico?.top_ressalvas_juridicas || []).map((res, idx) => (
                    <div key={idx} className="card" style={{ borderLeft: '4px solid #c5a059', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                      <div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '8px' }}>
                          <span style={{ fontWeight: 700, color: '#f1f5f9', fontSize: '0.95rem' }}>{res.categoria}</span>
                          <span className="tag" style={{ background: 'rgba(197, 160, 89, 0.15)', color: '#c5a059', fontSize: '0.72rem' }}>
                            {res.frequencia}
                          </span>
                        </div>
                        <p style={{ color: '#cbd5e1', fontSize: '0.84rem', lineHeight: '1.45', marginBottom: '10px' }}>
                          {res.descricao}
                        </p>
                        <div style={{ background: 'rgba(15, 23, 42, 0.6)', padding: '10px', borderRadius: '6px', border: '1px dashed #334155', fontSize: '0.8rem', color: '#94a3b8', fontStyle: 'italic', marginBottom: '12px' }}>
                          <strong style={{ color: '#c5a059', fontStyle: 'normal' }}>Cláusula Típica do Parecer:</strong> "{res.recomendacao_tipo}"
                        </div>
                      </div>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid #1e293b', paddingTop: '8px' }}>
                        <span style={{ fontSize: '0.75rem', color: '#64748b' }}>
                          Órgãos de Referência: {res.orgaos_referencia.join(', ')}
                        </span>
                        <button 
                          className="btn btn-outline" 
                          style={{ fontSize: '0.72rem', padding: '4px 8px' }}
                          onClick={() => handleCopy(res.recomendacao_tipo, `res-${idx}`)}
                        >
                          {copiedId === `res-${idx}` ? 'Copiado!' : 'Copiar Texto'}
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* CONTEÚDO 2: AS 3 LINHAS DE DEFESA */}
            {controleSubTab === 'linhas' && (
              <div>
                <div style={{ marginBottom: '16px' }}>
                  <h3 style={{ fontSize: '1.15rem', color: '#f8fafc', fontWeight: 600 }}>
                    Arquitetura das 3 Linhas de Defesa no MPPI (Art. 169 da Lei nº 14.133/2021)
                  </h3>
                  <p style={{ color: '#94a3b8', fontSize: '0.85rem' }}>
                    Estrutura de governança e segregação de funções para mitigar riscos de desconformidade e responsabilização
                  </p>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '18px' }}>
                  {(corpusData.controle_interno_juridico?.linhas_defesa_art169 || []).map((linha, idx) => (
                    <div key={idx} className="card" style={{ borderTop: `4px solid ${linha.cor}`, display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                      <div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                          <span className="tag" style={{ background: `${linha.cor}22`, color: linha.cor, fontWeight: 700 }}>
                            {linha.linha}
                          </span>
                          <span style={{ fontSize: '0.72rem', color: '#64748b' }}>{linha.status}</span>
                        </div>
                        <h4 style={{ color: '#fff', fontSize: '1.02rem', fontWeight: 600, marginBottom: '6px' }}>
                          {linha.titulo}
                        </h4>
                        <div style={{ fontSize: '0.8rem', color: '#94a3b8', marginBottom: '12px', background: 'rgba(255,255,255,0.03)', padding: '6px 8px', borderRadius: '4px' }}>
                          <strong>Agentes:</strong> {linha.agentes}
                        </div>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                          {linha.atribuicoes.map((atrib, aIdx) => (
                            <div key={aIdx} style={{ display: 'flex', gap: '8px', fontSize: '0.82rem', color: '#cbd5e1', lineHeight: '1.4' }}>
                              <span style={{ color: linha.cor }}>•</span>
                              <span>{atrib}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* CONTEÚDO 3: MATRIZES DE RISCO & ALOCAÇÃO */}
            {controleSubTab === 'matrizes' && (
              <div>
                <div style={{ display: 'grid', gridTemplateColumns: '1.1fr 0.9fr', gap: '20px' }}>
                  <div className="card">
                    <h3 className="card-title">Distribuição das 146 Matrizes por Categoria</h3>
                    <p className="card-desc">Predominância absoluta em soluções tecnológicas e serviços contínuos</p>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginTop: '16px' }}>
                      {(corpusData.controle_interno_juridico?.matrizes_por_tipo || []).map((m, idx) => (
                        <div key={idx} style={{ background: 'rgba(255,255,255,0.02)', padding: '12px', borderRadius: '6px', border: '1px solid #1e293b' }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                            <span style={{ fontWeight: 600, color: '#f1f5f9', fontSize: '0.9rem' }}>{m.tipo}</span>
                            <span style={{ color: m.cor, fontWeight: 700 }}>{m.qtd} matrizes ({m.percent}%)</span>
                          </div>
                          <div style={{ height: '6px', background: '#1e293b', borderRadius: '3px', overflow: 'hidden' }}>
                            <div style={{ width: `${m.percent}%`, height: '100%', background: m.cor }} />
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="card">
                    <h3 className="card-title">Ranking de Matrizes Estruturadas por Instituição</h3>
                    <p className="card-desc">Órgãos que publicam mapas de riscos autônomos no PNCP</p>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginTop: '12px' }}>
                      {(corpusData.controle_interno_juridico?.matrizes_por_orgao || []).map((org, idx) => (
                        <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 12px', background: 'rgba(255,255,255,0.02)', borderRadius: '4px' }}>
                          <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
                            <span className="tag" style={{ background: 'rgba(197, 160, 89, 0.15)', color: '#c5a059', minWidth: '55px', textAlign: 'center' }}>
                              {org.orgao}
                            </span>
                            <span style={{ fontSize: '0.82rem', color: '#cbd5e1' }}>{org.categoria_principal}</span>
                          </div>
                          <strong style={{ color: '#fff', fontSize: '0.9rem' }}>{org.qtd} peças</strong>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* CONTEÚDO 4: PARECERES REFERENCIAIS (ART. 53, § 5º) */}
            {controleSubTab === 'referenciais' && (
              <div>
                <div style={{ marginBottom: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <h3 style={{ fontSize: '1.15rem', color: '#f8fafc', fontWeight: 600 }}>
                      Modelos de Pareceres Jurídicos Referenciais para Adoção Imediata na CLC/MPPI
                    </h3>
                    <p style={{ color: '#94a3b8', fontSize: '0.85rem' }}>
                      Fundamentação no Art. 53, § 5º para conferir celeridade e dispensar remessa individualizada à Assessoria Jurídica
                    </p>
                  </div>
                  <span className="tag" style={{ background: 'rgba(16, 185, 129, 0.15)', color: '#34d399', border: '1px solid rgba(16, 185, 129, 0.3)' }}>
                    Economia Estimada: ~70% de Tempo de Tramitação
                  </span>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                  {(corpusData.controle_interno_juridico?.pareceres_referenciais_modelos || []).map((mod, idx) => (
                    <div key={idx} className="card" style={{ borderLeft: '4px solid #10b981' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '10px' }}>
                        <div>
                          <h4 style={{ color: '#f8fafc', fontSize: '1.05rem', fontWeight: 600 }}>{mod.titulo}</h4>
                          <span style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Fonte/Benchmark: {mod.orgao_origem}</span>
                        </div>
                        <span className="tag" style={{ background: 'rgba(16, 185, 129, 0.15)', color: '#34d399', fontSize: '0.75rem' }}>
                          {mod.impacto_estimado}
                        </span>
                      </div>
                      <div style={{ background: 'rgba(15, 23, 42, 0.5)', padding: '10px 14px', borderRadius: '6px', marginBottom: '12px', fontSize: '0.85rem', color: '#cbd5e1' }}>
                        <strong>Hipótese de Incidência:</strong> {mod.hipotese_incidencia}
                      </div>
                      <div>
                        <div style={{ fontSize: '0.85rem', fontWeight: 600, color: '#f1f5f9', marginBottom: '8px' }}>
                          Requisitos Cumulativos para Dispensa de Análise Jurídica Individualizada:
                        </div>
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '8px' }}>
                          {mod.requisitos_dispensa_analise_individual.map((req, rIdx) => (
                            <div key={rIdx} style={{ display: 'flex', gap: '8px', fontSize: '0.82rem', color: '#cbd5e1', background: 'rgba(255,255,255,0.02)', padding: '8px 10px', borderRadius: '4px' }}>
                              <CheckCircle size={15} color="#10b981" style={{ flexShrink: 0, marginTop: '2px' }} />
                              <span>{req}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* CONTEÚDO 5: MASTER CHECKLIST CLC/MPPI */}
            {controleSubTab === 'checklist' && (
              <div>
                <div style={{ marginBottom: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <h3 style={{ fontSize: '1.15rem', color: '#f8fafc', fontWeight: 600 }}>
                      Master Checklist de Conformidade da Instrução Processual
                    </h3>
                    <p style={{ color: '#94a3b8', fontSize: '0.85rem' }}>
                      Instrumento de barreira da 2ª Linha de Defesa da CLC antes do envio para deliberação da PGJ
                    </p>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span style={{ fontSize: '0.85rem', color: '#94a3b8' }}>
                      Progresso: <strong>{Object.values(checkedItems).filter(Boolean).length} / 15</strong> checados
                    </span>
                    <button 
                      className="btn btn-outline" 
                      style={{ fontSize: '0.75rem', padding: '6px 12px' }}
                      onClick={() => setCheckedItems({})}
                    >
                      Limpar Seleção
                    </button>
                  </div>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '18px' }}>
                  {(corpusData.controle_interno_juridico?.master_checklist_instrucao || []).map((secao, sIdx) => (
                    <div key={sIdx} className="card">
                      <h4 style={{ color: '#c5a059', fontSize: '0.98rem', fontWeight: 600, marginBottom: '12px', borderBottom: '1px solid #1e293b', paddingBottom: '6px' }}>
                        {secao.etapa}
                      </h4>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                        {secao.itens.map((it, iIdx) => (
                          <div 
                            key={iIdx} 
                            onClick={() => toggleCheck(it.codigo)}
                            style={{ 
                              display: 'flex', 
                              alignItems: 'flex-start', 
                              gap: '10px', 
                              padding: '10px', 
                              borderRadius: '6px', 
                              background: checkedItems[it.codigo] ? 'rgba(16, 185, 129, 0.08)' : 'rgba(255,255,255,0.02)',
                              border: checkedItems[it.codigo] ? '1px solid rgba(16, 185, 129, 0.3)' : '1px solid #1e293b',
                              cursor: 'pointer',
                              transition: 'all 0.2s ease'
                            }}
                          >
                            <input 
                              type="checkbox" 
                              checked={!!checkedItems[it.codigo]} 
                              onChange={() => {}}
                              style={{ marginTop: '3px', cursor: 'pointer', accentColor: '#10b981' }} 
                            />
                            <div>
                              <div style={{ display: 'flex', gap: '6px', alignItems: 'center' }}>
                                <span className="tag" style={{ background: '#1e293b', color: '#94a3b8', fontSize: '0.7rem' }}>
                                  {it.codigo}
                                </span>
                                {it.obrigatorio && (
                                  <span style={{ fontSize: '0.7rem', color: '#ef4444', fontWeight: 600 }}>*Obrigatório</span>
                                )}
                              </div>
                              <div style={{ 
                                fontSize: '0.84rem', 
                                color: checkedItems[it.codigo] ? '#34d399' : '#cbd5e1', 
                                marginTop: '4px',
                                textDecoration: checkedItems[it.codigo] ? 'line-through' : 'none'
                              }}>
                                {it.item}
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
'''

# 6. Insert the Controle Tab Pane right before the Normativos tab pane
normativos_anchor = "{/* TAB 3: PROPOSIÇÕES NORMATIVAS MPPI */}"
for candidate_anchor in [
    "{/* TAB 3: PROPOSIES NORMATIVAS MPPI */}",
    "{/* TAB 3: PROPOSIÇÕES NORMATIVAS MPPI */}"
]:
    if candidate_anchor in content:
        content = content.replace(candidate_anchor, controle_tab_jsx + "\n        " + candidate_anchor)
        print("Inserted Controle Tab Pane successfully before Normativos tab!")
        break

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("App.jsx updated with Controle Interno & Juridico successfully!")
