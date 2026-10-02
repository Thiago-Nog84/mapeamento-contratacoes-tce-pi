import React, { useState, useMemo } from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, Cell
} from 'recharts';
import { 
  Shield, FileText, Search, Activity, Scale, 
  CheckCircle, Copy, TrendingDown, ShieldCheck, AlertTriangle, 
  Layers, BookOpen, CheckSquare, Award, ExternalLink, Calculator,
  ChevronRight, Building, Sparkles, Filter, Database, Check, Clock, UserCheck
} from 'lucide-react';
import corpusData from './data/corpus_resumo.json';
import './index.css';

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div style={{ background: 'rgba(15, 23, 42, 0.95)', border: '1px solid rgba(197,160,89,0.4)', padding: '14px', borderRadius: '10px', boxShadow: '0 8px 30px rgba(0,0,0,0.5)', zIndex: 100 }}>
        <p style={{ color: '#fff', marginBottom: '8px', fontWeight: 700, fontSize: '0.95rem' }}>{label}</p>
        {payload.map((entry, index) => (
          <p key={index} style={{ color: entry.color || '#c5a059', fontSize: '0.88rem', margin: '4px 0', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: entry.color || '#c5a059', display: 'inline-block' }}></span>
            {entry.name}: <strong>{entry.value.toLocaleString()}</strong> {entry.unit || 'docs/processos'}
          </p>
        ))}
      </div>
    );
  }
  return null;
};

export default function App() {
  const [activeTab, setActiveTab] = useState('visao-geral');
  const [search, setSearch] = useState('');
  const [selectedOrgao, setSelectedOrgao] = useState('TODOS');
  const [selectedCat, setSelectedCat] = useState('TODOS');
  const [copiedId, setCopiedId] = useState(null);
  
  // Controle Sub-tabs
  const [controleSubTab, setControleSubTab] = useState('ressalvas');
  const [checkedItems, setCheckedItems] = useState({});

  // Boas Práticas Sub-tabs
  const [boasPraticasTab, setBoasPraticasTab] = useState('criterios');

  // Normativos Sub-tabs
  const [selectedMinuta, setSelectedMinuta] = useState('minuta1');

  // Simulador de Deságio
  const [simValor, setSimValor] = useState(500000);
  const [simCategoria, setSimCategoria] = useState('tic');

  const handleCopy = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2500);
  };

  const toggleCheck = (codigo) => {
    setCheckedItems(prev => ({
      ...prev,
      [codigo]: !prev[codigo]
    }));
  };

  // Cálculo do Simulador
  const simuladorResultado = useMemo(() => {
    const taxas = {
      tic: { nome: 'Tecnologia da Informação & Nuvem', taxa: 25.32, riscoLimite: 38 },
      mobiliario: { nome: 'Mobiliário e Equipamentos', taxa: 28.05, riscoLimite: 42 },
      terceirizacao: { nome: 'Mão de Obra Terceirizada (Serviços Contínuos)', taxa: 13.14, riscoLimite: 22 },
      obras: { nome: 'Obras & Manutenção Predial', taxa: 10.58, riscoLimite: 20 },
      geral: { nome: 'Compras e Serviços Comuns Gerais', taxa: 20.18, riscoLimite: 35 }
    };
    const sel = taxas[simCategoria] || taxas.geral;
    const economia = simValor * (sel.taxa / 100);
    const homologado = simValor - economia;
    return {
      categoriaNome: sel.nome,
      taxaDesagio: sel.taxa,
      riscoLimite: sel.riscoLimite,
      economiaProjetada: economia,
      valorHomologado: homologado
    };
  }, [simValor, simCategoria]);

  // Documentos filtrados do RAG
  const filteredDocs = useMemo(() => {
    return (corpusData.recent_docs || []).filter(doc => {
      const matchSearch = search === '' || 
        (doc.titulo && doc.titulo.toLowerCase().includes(search.toLowerCase())) ||
        (doc.objeto && doc.objeto.toLowerCase().includes(search.toLowerCase())) ||
        (doc.modalidade && doc.modalidade.toLowerCase().includes(search.toLowerCase()));
      const matchOrgao = selectedOrgao === 'TODOS' || doc.orgao === selectedOrgao;
      const matchCat = selectedCat === 'TODOS' || doc.categoria === selectedCat;
      return matchSearch && matchOrgao && matchCat;
    });
  }, [search, selectedOrgao, selectedCat]);

  return (
    <div>
      {/* LIVE TOP TICKER BAR */}
      <div className="live-bar">
        <div style={{ display: 'flex', alignItems: 'center', gap: '18px' }}>
          <span className="live-badge">
            <span className="live-dot"></span>
            PROJETO Lic.IA ATIVO: 10.504 DOCUMENTOS INDEXADOS
          </span>
          <span style={{ color: '#475569' }}>|</span>
          <span style={{ color: '#cbd5e1', fontSize: '0.76rem' }}>
            100% do Nordeste Monitorado (9 MPs Estaduais + TJ-PI + TCE-PI + MPDFT)
          </span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <span style={{ color: '#c5a059', fontWeight: 600, fontSize: '0.78rem' }}>
            Lei Federal nº 14.133/2021 & Acórdão nº 300/2025 TCE-PI
          </span>
          <button 
            className="btn btn-outline" 
            style={{ padding: '3px 10px', fontSize: '0.72rem', borderRadius: '4px' }}
            onClick={() => setActiveTab('boas-praticas')}
          >
            🏆 Candidatura Prêmio CNMP
          </button>
        </div>
      </div>

      <div className="layout">
        {/* SIDEBAR NAVIGATION */}
        <aside className="sidebar">
          <div>
            <div className="brand">
              <div className="brand-icon">
                <Shield size={26} color="#c5a059" />
              </div>
              <div>
                <div className="brand-title">PROJETO Lic.IA</div>
                <div className="brand-sub">Governança & Compras Públicas • MPPI</div>
              </div>
            </div>

            <nav className="nav-menu">
              <button 
                className={`nav-item ${activeTab === 'visao-geral' ? 'active' : ''}`}
                onClick={() => setActiveTab('visao-geral')}
              >
                <Activity size={18} /> Panorama Regional (12 Órgãos)
              </button>

              <button 
                className={`nav-item ${activeTab === 'economicidade' ? 'active' : ''}`}
                onClick={() => setActiveTab('economicidade')}
              >
                <TrendingDown size={18} /> Economicidade & Simulador
              </button>

              <button 
                className={`nav-item ${activeTab === 'controle' ? 'active' : ''}`}
                onClick={() => setActiveTab('controle')}
              >
                <ShieldCheck size={18} /> Controle Interno & Jurídico
              </button>

              <button 
                className={`nav-item ${activeTab === 'normativos' ? 'active' : ''}`}
                onClick={() => setActiveTab('normativos')}
              >
                <Scale size={18} /> Caderno Normativo MPPI
              </button>

              <button 
                className={`nav-item ${activeTab === 'boas-praticas' ? 'active' : ''}`}
                onClick={() => setActiveTab('boas-praticas')}
              >
                <Award size={18} /> Projeto Boas Práticas (CNMP)
              </button>

              <button 
                className={`nav-item ${activeTab === 'rag' ? 'active' : ''}`}
                onClick={() => setActiveTab('rag')}
              >
                <Search size={18} /> Explorador Semântico RAG
              </button>
            </nav>
          </div>

          <div className="sidebar-footer">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
              <span style={{ fontSize: '0.78rem', color: '#94a3b8' }}>Repositório Unificado:</span>
              <span className="tag" style={{ background: 'rgba(16, 185, 129, 0.15)', color: '#34d399', fontSize: '0.68rem' }}>100% NE</span>
            </div>
            <div style={{ fontSize: '1.25rem', fontWeight: 800, color: '#c5a059', letterSpacing: '-0.02em' }}>
              {corpusData.total_docs.toLocaleString()} docs
            </div>
            <div style={{ fontSize: '0.72rem', color: '#64748b', marginTop: '4px', lineHeight: '1.3' }}>
              MPPI • MPCE • MPPE • MPMA • MPBA • MPRN • MPPB • MPAL • MPSE • TJPI • TCE-PI • MPDFT
            </div>
          </div>
        </aside>

        {/* MAIN CONTENT AREA */}
        <main className="main-content">
          {/* HEADER TOPBAR */}
          <header className="topbar">
            <div>
              <h1 className="topbar-title">
                {activeTab === 'visao-geral' && 'Panorama Geral: Todos os 9 Ministérios Públicos do Nordeste + Tribunais'}
                {activeTab === 'economicidade' && 'Estudo de Economicidade & Simulador de Deságio (R$ 341M Analisados)'}
                {activeTab === 'controle' && 'Controle Interno e Jurídico: Matrizes de Risco, Pareceres e Linhas de Defesa'}
                {activeTab === 'normativos' && 'Caderno de Proposições Normativas para o MPPI'}
                {activeTab === 'boas-praticas' && 'Candidatura ao Prêmio CNMP 2026 & Prêmio Melhores Práticas MPPI'}
                {activeTab === 'rag' && 'Explorador Semântico de Inteligência (10.504 Peças Indexadas)'}
              </h1>
              <p className="topbar-desc">
                Coordenação de Licitações e Contratos (CLC/MPPI) • PROJETO Lic.IA: A Inteligência Artificial em Licitações do MPPI de Dados
              </p>
            </div>
            <div style={{ display: 'flex', gap: '10px' }}>
              <span className="tag" style={{ background: 'rgba(197, 160, 89, 0.15)', color: '#c5a059', border: '1px solid rgba(197, 160, 89, 0.3)' }}>
                12 Instituições Integradas
              </span>
              <span className="tag" style={{ background: 'rgba(16, 185, 129, 0.15)', color: '#34d399', border: '1px solid rgba(16, 185, 129, 0.3)' }}>
                R$ 68,8M Economizados
              </span>
            </div>
          </header>

          {/* TAB 1: VISÃO GERAL */}
          {activeTab === 'visao-geral' && (
            <div className="tab-pane">
              {/* HERO BANNER INSTITUCIONAL */}
              <div className="hero-portal">
                <div style={{ maxWidth: '85%' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
                    <span className="tag" style={{ background: 'rgba(155, 17, 30, 0.3)', color: '#ff6b7a', border: '1px solid rgba(155, 17, 30, 0.6)' }}>
                      Ecossistema de IA do MPPI • Atividade-Meio & Governança de Contratações
                    </span>
                    <span className="tag" style={{ background: 'rgba(197, 160, 89, 0.2)', color: '#e6c883' }}>
                      Prêmio CNMP 2026 • Governança e Gestão
                    </span>
                  </div>
                  <h2 style={{ fontSize: '1.75rem', fontWeight: 800, color: '#fff', lineHeight: '1.25', marginBottom: '10px' }}>
                    PROJETO Lic.IA — Inteligência e Governança em Compras do Nordeste
                  </h2>
                  <p style={{ color: '#cbd5e1', fontSize: '0.98rem', lineHeight: '1.6' }}>
                    O Observatório da CLC/MPPI centraliza, estrutura e analisa dados de <strong>100% dos Ministérios Públicos dos 9 estados do Nordeste</strong>, 
                    além do TJ-PI, TCE-PI e MPDFT. Uma infraestrutura de dados moderna que fundamenta tomadas de decisão, orienta pesquisas de mercado, 
                    padroniza instrumentos convocatórios e protege a instituição com governança antecipada.
                  </p>
                </div>
              </div>

              {/* STATS PRINCIPAIS */}
              <div className="stats-grid" style={{ gridTemplateColumns: 'repeat(4, 1fr)' }}>
                <div className="stat-card" style={{ borderLeft: '4px solid #c5a059' }}>
                  <div className="stat-label">Total de Documentos</div>
                  <div className="stat-val">{corpusData.total_docs.toLocaleString()}</div>
                  <div className="stat-sub">100% em formato Markdown/JSON</div>
                </div>
                <div className="stat-card" style={{ borderLeft: '4px solid #3b82f6' }}>
                  <div className="stat-label">Instituições Monitoradas</div>
                  <div className="stat-val">12 Órgãos</div>
                  <div className="stat-sub">9 MPs do Nordeste + Tribunais</div>
                </div>
                <div className="stat-card" style={{ borderLeft: '4px solid #10b981' }}>
                  <div className="stat-label">Economia Mapeada (Deságio)</div>
                  <div className="stat-val" style={{ color: '#34d399' }}>R$ 68,8 Mi</div>
                  <div className="stat-sub">20,18% de deságio médio global</div>
                </div>
                <div className="stat-card" style={{ borderLeft: '4px solid #8b5cf6' }}>
                  <div className="stat-label">Controle & Riscos Mapeados</div>
                  <div className="stat-val">{corpusData.controle_interno_juridico?.kpis.total_pareceres + corpusData.controle_interno_juridico?.kpis.matrizes_risco || 808} peças</div>
                  <div className="stat-sub">662 Pareceres e 146 Riscos</div>
                </div>
              </div>

              {/* GRÁFICOS DO PANORAMA */}
              <div style={{ display: 'grid', gridTemplateColumns: '1.3fr 0.7fr', gap: '20px', marginTop: '10px' }}>
                <div className="card">
                  <h3 className="card-title">Ranking de Documentos por Instituição Monitorada (12 Órgãos)</h3>
                  <p className="card-desc">Volume total de peças contratuais, editais, termos de referência e pareceres indexados</p>
                  <div style={{ height: '340px', width: '100%', marginTop: '15px' }}>
                    <ResponsiveContainer>
                      <BarChart data={corpusData.orgaos_chart} margin={{ top: 20, right: 30, left: 10, bottom: 25 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                        <XAxis dataKey="name" stroke="#94a3b8" />
                        <YAxis stroke="#94a3b8" />
                        <RechartsTooltip content={<CustomTooltip />} />
                        <Bar dataKey="docs" name="Documentos Indexados" radius={[6, 6, 0, 0]}>
                          {corpusData.orgaos_chart.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.fill} />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                <div className="card">
                  <h3 className="card-title">Distribuição por Tipologia de Peça</h3>
                  <p className="card-desc">Estrutura das 10.504 peças processuais indexadas</p>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginTop: '12px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', padding: '9px 14px', background: 'rgba(255,255,255,0.02)', borderRadius: '6px' }}>
                      <span style={{ fontSize: '0.86rem', color: '#cbd5e1' }}>Termos de Referência (TR/PB)</span>
                      <strong style={{ color: '#c5a059' }}>{corpusData.by_cat['tr'] || 1250}</strong>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', padding: '9px 14px', background: 'rgba(255,255,255,0.02)', borderRadius: '6px' }}>
                      <span style={{ fontSize: '0.86rem', color: '#cbd5e1' }}>Editais & Avisos Convocatórios</span>
                      <strong style={{ color: '#3b82f6' }}>{corpusData.by_cat['edital'] || 1480}</strong>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', padding: '9px 14px', background: 'rgba(255,255,255,0.02)', borderRadius: '6px' }}>
                      <span style={{ fontSize: '0.86rem', color: '#cbd5e1' }}>Atos de Ratificação / Decisões</span>
                      <strong style={{ color: '#34d399' }}>{corpusData.by_cat['ratificacao'] || 1350}</strong>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', padding: '9px 14px', background: 'rgba(255,255,255,0.02)', borderRadius: '6px' }}>
                      <span style={{ fontSize: '0.86rem', color: '#cbd5e1' }}>Pareceres Jurídicos (Art. 53)</span>
                      <strong style={{ color: '#f59e0b' }}>{corpusData.controle_interno_juridico?.kpis.total_pareceres || 662}</strong>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', padding: '9px 14px', background: 'rgba(255,255,255,0.02)', borderRadius: '6px' }}>
                      <span style={{ fontSize: '0.86rem', color: '#cbd5e1' }}>DFD / Documentos de Demanda</span>
                      <strong style={{ color: '#8b5cf6' }}>{corpusData.by_cat['dfd'] || 451}</strong>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', padding: '9px 14px', background: 'rgba(255,255,255,0.02)', borderRadius: '6px' }}>
                      <span style={{ fontSize: '0.86rem', color: '#cbd5e1' }}>Matrizes de Risco (Art. 22/103)</span>
                      <strong style={{ color: '#ec4899' }}>{corpusData.controle_interno_juridico?.kpis.matrizes_risco || 146}</strong>
                    </div>
                  </div>
                </div>
              </div>

              {/* GRID DOS 12 ÓRGÃOS DO NORDESTE */}
              <div style={{ marginTop: '28px' }}>
                <h3 style={{ fontSize: '1.2rem', color: '#f8fafc', fontWeight: 700, marginBottom: '16px' }}>
                  As 12 Instituições Monitoradas pelo Observatório
                </h3>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px' }}>
                  {[
                    { nome: 'MPRN', estado: 'Rio Grande do Norte', docs: 2743, cnpj: '08.539.467/0001-63', cor: '#3b82f6', destaque: 'Maior acervo de TRs e atas do NE' },
                    { nome: 'TJ-PI', estado: 'Piauí (Judiciário)', docs: 2178, cnpj: '04.054.499/0001-72', cor: '#8b5cf6', destaque: 'Provimento 13/2025 e Sede/FERMOJUPI' },
                    { nome: 'MPSE', estado: 'Sergipe', docs: 1144, cnpj: '13.168.687/0001-10', cor: '#10b981', destaque: '541 certames e rito sumário de valor' },
                    { nome: 'TCE-PI', estado: 'Piauí (Controle Externo)', docs: 1120, cnpj: '05.818.935/0001-30', cor: '#c5a059', destaque: 'Acórdão 300/2025 e precedentes vinculantes' },
                    { nome: 'MPPI', estado: 'Piauí (Órgão Piloto)', docs: 561, cnpj: '04.145.419/0001-44', cor: '#9b111e', destaque: '153 certames e peças descompactadas SEI' },
                    { nome: 'MPAL', estado: 'Alagoas', docs: 538, cnpj: '12.472.734/0001-52', cor: '#f59e0b', destaque: 'Líder em matrizes de risco (60 peças)' },
                    { nome: 'MPBA', estado: 'Bahia', docs: 472, cnpj: '04.142.491/0001-66', cor: '#ec4899', destaque: 'Maior volume orçamentário terceirizado' },
                    { nome: 'MPDFT', estado: 'Distrito Federal (MPU)', docs: 435, cnpj: '26.989.715/0002-93', cor: '#06b6d4', destaque: 'Referência em TIC, SLAs e IMR ministerial' },
                    { nome: 'MPMA', estado: 'Maranhão', docs: 431, cnpj: '05.483.912/0001-85', cor: '#14b8a6', destaque: 'Fronteira e similaridade logística com PI' },
                    { nome: 'MPCE', estado: 'Ceará', docs: 322, cnpj: '06.928.790/0001-56', cor: '#6366f1', destaque: '75 precedentes de inexigibilidade CEAF' },
                    { nome: 'MPPB', estado: 'Paraíba', docs: 293, cnpj: '09.284.001/0001-80', cor: '#84cc16', destaque: 'Transparência em dados abertos e TIC' },
                    { nome: 'MPPE', estado: 'Pernambuco', docs: 267, cnpj: '24.417.065/0001-03', cor: '#f97316', destaque: 'Dados comparativos de deságio e orçado' }
                  ].map((org, i) => (
                    <div key={i} className="card" style={{ padding: '16px', borderTop: `3px solid ${org.cor}` }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                        <span style={{ fontWeight: 800, fontSize: '1.1rem', color: '#fff' }}>{org.nome}</span>
                        <span className="tag" style={{ background: `${org.cor}22`, color: org.cor, fontSize: '0.72rem' }}>
                          {org.docs.toLocaleString()} docs
                        </span>
                      </div>
                      <div style={{ fontSize: '0.8rem', color: '#94a3b8', marginBottom: '4px' }}>{org.estado}</div>
                      <div style={{ fontSize: '0.75rem', color: '#64748b', fontFamily: 'JetBrains Mono, monospace', marginBottom: '8px' }}>
                        CNPJ: {org.cnpj}
                      </div>
                      <div style={{ fontSize: '0.78rem', color: '#cbd5e1', borderTop: '1px solid #1e293b', paddingTop: '6px' }}>
                        {org.destaque}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* TAB 2: ECONOMICIDADE & SIMULADOR */}
          {activeTab === 'economicidade' && (
            <div className="tab-pane">
              {/* STATS DE ECONOMICIDADE */}
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
                  <div className="stat-val" style={{ color: '#c5a059' }}>20,18%</div>
                  <div className="stat-sub">Faixa saudável de competitividade</div>
                </div>
              </div>

              {/* SIMULADOR INTERATIVO DE DESÁGIO E RISCO */}
              <div className="simulador-box" style={{ marginBottom: '24px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
                  <Calculator size={22} color="#c5a059" />
                  <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#fff' }}>
                    Simulador Interativo de Deságio e Risco Lic.IA (CLC/MPPI)
                  </h3>
                </div>
                <p style={{ color: '#94a3b8', fontSize: '0.88rem', marginBottom: '20px' }}>
                  Estime o valor final homologado e a economia projetada para novas contratações do MPPI, com base na curva empírica dos Ministérios Públicos do Nordeste.
                </p>

                <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1.8fr', gap: '24px', alignItems: 'center' }}>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    <div>
                      <label style={{ display: 'block', fontSize: '0.85rem', color: '#cbd5e1', fontWeight: 600, marginBottom: '6px' }}>
                        Valor Estimado Orçado no ETP / TR:
                      </label>
                      <div style={{ display: 'flex', alignItems: 'center', background: '#0f172a', border: '1px solid #334155', borderRadius: '8px', padding: '10px 14px' }}>
                        <span style={{ color: '#c5a059', fontWeight: 700, marginRight: '8px' }}>R$</span>
                        <input 
                          type="number" 
                          value={simValor} 
                          onChange={(e) => setSimValor(Number(e.target.value) || 0)}
                          style={{ background: 'transparent', border: 'none', color: '#fff', fontSize: '1.1rem', fontWeight: 700, width: '100%', outline: 'none' }}
                        />
                      </div>
                    </div>

                    <div>
                      <label style={{ display: 'block', fontSize: '0.85rem', color: '#cbd5e1', fontWeight: 600, marginBottom: '6px' }}>
                        Categoria do Objeto Contratual:
                      </label>
                      <select 
                        value={simCategoria} 
                        onChange={(e) => setSimCategoria(e.target.value)}
                        style={{ width: '100%', padding: '12px 14px', background: '#0f172a', border: '1px solid #334155', borderRadius: '8px', color: '#fff', fontSize: '0.9rem' }}
                      >
                        <option value="tic">Tecnologia da Informação & Nuvem (Deságio Médio: 25,32%)</option>
                        <option value="mobiliario">Mobiliário e Equipamentos (Deságio Médio: 28,05%)</option>
                        <option value="terceirizacao">Mão de Obra Terceirizada Continuada (Deságio Médio: 13,14%)</option>
                        <option value="obras">Obras & Manutenção Predial (Deságio Médio: 10,58%)</option>
                        <option value="geral">Compras e Serviços Comuns Gerais (Deságio Médio: 20,18%)</option>
                      </select>
                    </div>
                  </div>

                  {/* RESULTADO DO SIMULADOR */}
                  <div style={{ background: 'rgba(15, 23, 42, 0.7)', border: '1px solid rgba(197, 160, 89, 0.3)', borderRadius: '12px', padding: '20px' }}>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '14px', marginBottom: '14px' }}>
                      <div style={{ padding: '10px', background: 'rgba(255,255,255,0.02)', borderRadius: '8px', borderLeft: '3px solid #10b981' }}>
                        <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Economia Projetada</div>
                        <div style={{ fontSize: '1.25rem', fontWeight: 800, color: '#34d399', marginTop: '4px' }}>
                          R$ {simuladorResultado.economiaProjetada.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                        </div>
                        <div style={{ fontSize: '0.72rem', color: '#10b981' }}>{simuladorResultado.taxaDesagio}% do valor orçado</div>
                      </div>

                      <div style={{ padding: '10px', background: 'rgba(255,255,255,0.02)', borderRadius: '8px', borderLeft: '3px solid #3b82f6' }}>
                        <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Homologação Esperada</div>
                        <div style={{ fontSize: '1.25rem', fontWeight: 800, color: '#60a5fa', marginTop: '4px' }}>
                          R$ {simuladorResultado.valorHomologado.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                        </div>
                        <div style={{ fontSize: '0.72rem', color: '#64748b' }}>Valor final previsto</div>
                      </div>

                      <div style={{ padding: '10px', background: 'rgba(255,255,255,0.02)', borderRadius: '8px', borderLeft: '3px solid #ef4444' }}>
                        <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Alerta de Inexequibilidade</div>
                        <div style={{ fontSize: '1.25rem', fontWeight: 800, color: '#f87171', marginTop: '4px' }}>
                          &gt; {simuladorResultado.riscoLimite}%
                        </div>
                        <div style={{ fontSize: '0.72rem', color: '#ef4444' }}>Exigir diligência formal</div>
                      </div>
                    </div>

                    <div style={{ fontSize: '0.8rem', color: '#cbd5e1', lineHeight: '1.4' }}>
                      <strong style={{ color: '#c5a059' }}>Parâmetro de Governança para o MPPI:</strong> Propostas que apresentem desconto superior a {simuladorResultado.riscoLimite}% para {simuladorResultado.categoriaNome} devem acionar diligência formal de exequibilidade (Art. 59, § 2º da Lei 14.133/21).
                    </div>
                  </div>
                </div>
              </div>

              {/* GRÁFICO E DIRETRIZES */}
              <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 0.8fr', gap: '20px' }}>
                <div className="card">
                  <h3 className="card-title">Deságio Médio (%) por Categoria de Objeto</h3>
                  <p className="card-desc">Percentual de desconto obtido entre o valor de referência e a proposta homologada</p>
                  <div style={{ height: '320px', width: '100%', marginTop: '15px' }}>
                    <ResponsiveContainer>
                      <BarChart data={corpusData.economicidade.chart_categorias} margin={{ top: 20, right: 30, left: 10, bottom: 25 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                        <XAxis dataKey="categoria" stroke="#94a3b8" angle={-15} textAnchor="end" interval={0} height={50} />
                        <YAxis stroke="#94a3b8" unit="%" />
                        <RechartsTooltip content={<CustomTooltip />} />
                        <Bar dataKey="desagio" name="Deságio Médio (%)" fill="#10b981" radius={[6, 6, 0, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                <div className="card">
                  <h3 className="card-title">Diretrizes Setoriais para a CLC / MPPI</h3>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginTop: '12px' }}>
                    <div style={{ padding: '12px', background: 'rgba(239, 68, 68, 0.1)', borderLeft: '4px solid #ef4444', borderRadius: '4px' }}>
                      <strong style={{ color: '#f87171', fontSize: '0.85rem' }}>Mão de Obra Terceirizada (Deságio Médio: 13,14%)</strong>
                      <p style={{ color: '#cbd5e1', fontSize: '0.8rem', marginTop: '4px' }}>
                        Descontos acima de 20% representam risco gravíssimo de inadimplemento salarial e previdenciário. Exigir conta vinculada (fato gerador).
                      </p>
                    </div>

                    <div style={{ padding: '12px', background: 'rgba(16, 185, 129, 0.1)', borderLeft: '4px solid #10b981', borderRadius: '4px' }}>
                      <strong style={{ color: '#34d399', fontSize: '0.85rem' }}>Soluções de TIC e Licenças (Deságio Médio: 25,32%)</strong>
                      <p style={{ color: '#cbd5e1', fontSize: '0.8rem', marginTop: '4px' }}>
                        Alta margem comercial dos distribuidores permite negociações expressivas. Serve como balizador em pedidos de carona.
                      </p>
                    </div>

                    <div style={{ padding: '12px', background: 'rgba(197, 160, 89, 0.1)', borderLeft: '4px solid #c5a059', borderRadius: '4px' }}>
                      <strong style={{ color: '#e6c883', fontSize: '0.85rem' }}>Obras e Reformas Prediais (Deságio Médio: 10,58%)</strong>
                      <p style={{ color: '#cbd5e1', fontSize: '0.8rem', marginTop: '4px' }}>
                        Margem estreita regulada pelo SINAPI. Descontos elevados costumam acarretar paralisação e pedidos intempestivos de aditivos.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* TAB 3: CONTROLE INTERNO & JURÍDICO */}
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
                  <div className="stat-sub">Mapas estruturados nos 9 MPs</div>
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
              <div style={{ display: 'flex', gap: '10px', marginBottom: '20px', borderBottom: '1px solid #1e293b', paddingBottom: '12px' }}>
                <button 
                  className={`btn ${controleSubTab === 'ressalvas' ? 'btn-primary' : 'btn-outline'}`}
                  style={{ fontSize: '0.85rem', padding: '8px 16px' }}
                  onClick={() => setControleSubTab('ressalvas')}
                >
                  <AlertTriangle size={16} /> Top Ressalvas Jurídicas Recorrentes
                </button>
                <button 
                  className={`btn ${controleSubTab === 'linhas' ? 'btn-primary' : 'btn-outline'}`}
                  style={{ fontSize: '0.85rem', padding: '8px 16px' }}
                  onClick={() => setControleSubTab('linhas')}
                >
                  <Layers size={16} /> As 3 Linhas de Defesa (Art. 169)
                </button>
                <button 
                  className={`btn ${controleSubTab === 'matrizes' ? 'btn-primary' : 'btn-outline'}`}
                  style={{ fontSize: '0.85rem', padding: '8px 16px' }}
                  onClick={() => setControleSubTab('matrizes')}
                >
                  <Activity size={16} /> Matrizes de Risco & Alocação
                </button>
                <button 
                  className={`btn ${controleSubTab === 'referenciais' ? 'btn-primary' : 'btn-outline'}`}
                  style={{ fontSize: '0.85rem', padding: '8px 16px' }}
                  onClick={() => setControleSubTab('referenciais')}
                >
                  <BookOpen size={16} /> Pareceres Referenciais (Art. 53, § 5º)
                </button>
                <button 
                  className={`btn ${controleSubTab === 'checklist' ? 'btn-primary' : 'btn-outline'}`}
                  style={{ fontSize: '0.85rem', padding: '8px 16px' }}
                  onClick={() => setControleSubTab('checklist')}
                >
                  <CheckSquare size={16} /> Master Checklist CLC/MPPI
                </button>
              </div>

              {/* CONTEÚDO 1: TOP RESSALVAS */}
              {controleSubTab === 'ressalvas' && (
                <div>
                  <div style={{ marginBottom: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                      <h3 style={{ fontSize: '1.15rem', color: '#f8fafc', fontWeight: 600 }}>
                        Catálogo das 6 Ressalvas Mais Frequentes nos 662 Pareceres Jurídicos
                      </h3>
                      <p style={{ color: '#94a3b8', fontSize: '0.85rem' }}>
                        Diretrizes preventivas extraídas das manifestações das Assessorias Jurídicas
                      </p>
                    </div>
                    <span className="tag" style={{ background: 'rgba(239, 68, 68, 0.15)', color: '#f87171' }}>
                      88% das Devoluções de Processos
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
                            <strong style={{ color: '#c5a059', fontStyle: 'normal' }}>Cláusula Padrão:</strong> "{res.recomendacao_tipo}"
                          </div>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid #1e293b', paddingTop: '8px' }}>
                          <span style={{ fontSize: '0.75rem', color: '#64748b' }}>
                            Órgãos: {res.orgaos_referencia.join(', ')}
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

              {/* CONTEÚDO 2: 3 LINHAS DE DEFESA */}
              {controleSubTab === 'linhas' && (
                <div>
                  <div style={{ marginBottom: '16px' }}>
                    <h3 style={{ fontSize: '1.15rem', color: '#f8fafc', fontWeight: 600 }}>
                      Arquitetura das 3 Linhas de Defesa no MPPI (Art. 169 da Lei nº 14.133/2021)
                    </h3>
                    <p style={{ color: '#94a3b8', fontSize: '0.85rem' }}>
                      Segregação de funções para blindar contratações e mitigar responsabilidades
                    </p>
                  </div>

                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '18px' }}>
                    {(corpusData.controle_interno_juridico?.linhas_defesa_art169 || []).map((linha, idx) => (
                      <div key={idx} className="card" style={{ borderTop: `4px solid ${linha.cor}` }}>
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
                    ))}
                  </div>
                </div>
              )}

              {/* CONTEÚDO 3: MATRIZES DE RISCO */}
              {controleSubTab === 'matrizes' && (
                <div>
                  <div style={{ display: 'grid', gridTemplateColumns: '1.1fr 0.9fr', gap: '20px' }}>
                    <div className="card">
                      <h3 className="card-title">Distribuição das 146 Matrizes por Categoria</h3>
                      <p className="card-desc">Predominância em tecnologia da informação e serviços continuados</p>
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

              {/* CONTEÚDO 4: PARECERES REFERENCIAIS */}
              {controleSubTab === 'referenciais' && (
                <div>
                  <div style={{ marginBottom: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                      <h3 style={{ fontSize: '1.15rem', color: '#f8fafc', fontWeight: 600 }}>
                        Modelos de Pareceres Jurídicos Referenciais para Adoção Imediata na CLC/MPPI
                      </h3>
                      <p style={{ color: '#94a3b8', fontSize: '0.85rem' }}>
                        Fundamentação no Art. 53, § 5º para conferir celeridade e dispensar remessa individualizada
                      </p>
                    </div>
                    <span className="tag" style={{ background: 'rgba(16, 185, 129, 0.15)', color: '#34d399' }}>
                      ~70% de Redução no Tempo de Tramitação
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

              {/* CONTEÚDO 5: MASTER CHECKLIST */}
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

          {/* TAB 4: CADERNO NORMATIVO MPPI */}
          {activeTab === 'normativos' && (
            <div className="tab-pane">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <div>
                  <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#fff' }}>
                    Caderno de Proposições Normativas para o MPPI
                  </h3>
                  <p style={{ color: '#94a3b8', fontSize: '0.88rem' }}>
                    Minutas regulamentares prontas para deliberação da PGJ e fortalecimento da CLC
                  </p>
                </div>
                <div style={{ display: 'flex', gap: '8px' }}>
                  <button 
                    className={`btn ${selectedMinuta === 'minuta1' ? 'btn-primary' : 'btn-outline'}`}
                    onClick={() => setSelectedMinuta('minuta1')}
                    style={{ fontSize: '0.82rem', padding: '8px 14px' }}
                  >
                    1. Dispensa por Valor (Ato PGJ)
                  </button>
                  <button 
                    className={`btn ${selectedMinuta === 'minuta2' ? 'btn-primary' : 'btn-outline'}`}
                    onClick={() => setSelectedMinuta('minuta2')}
                    style={{ fontSize: '0.82rem', padding: '8px 14px' }}
                  >
                    2. Capacitação CEAF (Ato PGJ)
                  </button>
                  <button 
                    className={`btn ${selectedMinuta === 'minuta3' ? 'btn-primary' : 'btn-outline'}`}
                    onClick={() => setSelectedMinuta('minuta3')}
                    style={{ fontSize: '0.82rem', padding: '8px 14px' }}
                  >
                    3. Governança Carona (IN CLC)
                  </button>
                </div>
              </div>

              {selectedMinuta === 'minuta1' && (
                <div className="card" style={{ borderLeft: '4px solid #c5a059' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                    <span className="tag" style={{ background: 'rgba(197, 160, 89, 0.15)', color: '#c5a059' }}>
                      Minuta de Ato da Procuradoria-Geral de Justiça
                    </span>
                    <button 
                      className="btn btn-outline" 
                      style={{ fontSize: '0.75rem', padding: '6px 12px' }}
                      onClick={() => handleCopy("MINUTA DE ATO PGJ - DISPENSA POR VALOR (ART. 75, I e II)...", "min1")}
                    >
                      {copiedId === "min1" ? "Copiado!" : "Copiar Minuta Completa"}
                    </button>
                  </div>
                  <h4 style={{ fontSize: '1.15rem', color: '#fff', fontWeight: 700, marginBottom: '8px' }}>
                    Regulamentação do Procedimento Sumário de Contratação Direta por Dispensa de Licitação em Razão do Valor
                  </h4>
                  <p style={{ color: '#cbd5e1', fontSize: '0.88rem', lineHeight: '1.6', marginBottom: '14px' }}>
                    Institui o rito sumário eletrônico com aviso de contratação de 3 dias úteis, estabelece a facultatividade de elaboração de ETP e matriz de riscos para bens comuns de pronta entrega, e formaliza o Parecer Jurídico Referencial da Assessoria Jurídica, respaldado pelo Art. 46 do Provimento nº 13/2025 do TJ-PI.
                  </p>
                  <div style={{ background: 'rgba(15, 23, 42, 0.5)', padding: '14px', borderRadius: '8px', border: '1px solid #1e293b', fontSize: '0.85rem', color: '#cbd5e1' }}>
                    <strong style={{ color: '#c5a059' }}>Principais Dispositivos:</strong>
                    <ul style={{ marginTop: '8px', paddingLeft: '20px', display: 'flex', flexDirection: 'column', gap: '6px' }}>
                      <li>Art. 3º: Rito sumário com instrução simplificada via DFD e mapa de preços IN 65/2021.</li>
                      <li>Art. 7º: Dispensa fundamentada de ETP e Matriz de Riscos em compras de entrega imediata.</li>
                      <li>Art. 12: Atestado de conformidade a Parecer Referencial com envio direto para autorização e empenho.</li>
                    </ul>
                  </div>
                </div>
              )}

              {selectedMinuta === 'minuta2' && (
                <div className="card" style={{ borderLeft: '4px solid #3b82f6' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                    <span className="tag" style={{ background: 'rgba(59, 130, 246, 0.15)', color: '#60a5fa' }}>
                      Minuta de Ato da Procuradoria-Geral de Justiça
                    </span>
                    <button 
                      className="btn btn-outline" 
                      style={{ fontSize: '0.75rem', padding: '6px 12px' }}
                      onClick={() => handleCopy("MINUTA DE ATO PGJ - INEXIGIBILIDADE DE CAPACITAÇÃO CEAF...", "min2")}
                    >
                      {copiedId === "min2" ? "Copiado!" : "Copiar Minuta Completa"}
                    </button>
                  </div>
                  <h4 style={{ fontSize: '1.15rem', color: '#fff', fontWeight: 700, marginBottom: '8px' }}>
                    Regulamentação das Contratações Diretas por Inexigibilidade de Capacitação e Treinamento para o CEAF (Art. 74, III, "f")
                  </h4>
                  <p style={{ color: '#cbd5e1', fontSize: '0.88rem', lineHeight: '1.6', marginBottom: '14px' }}>
                    Padroniza o rito de contratação de cursos, congressos e treinamentos abertos ao público pelo Centro de Estudos e Aperfeiçoamento Funcional (CEAF), baseado na singularidade do corpo docente e prospecto público oficial, respaldado por 75 precedentes empíricos mapeados no MPCE.
                  </p>
                  <div style={{ background: 'rgba(15, 23, 42, 0.5)', padding: '14px', borderRadius: '8px', border: '1px solid #1e293b', fontSize: '0.85rem', color: '#cbd5e1' }}>
                    <strong style={{ color: '#3b82f6' }}>Principais Dispositivos:</strong>
                    <ul style={{ marginTop: '8px', paddingLeft: '20px', display: 'flex', flexDirection: 'column', gap: '6px' }}>
                      <li>Art. 4º: Inscrição individual em cursos e seminários abertos mediante prospecto público como prova de preço.</li>
                      <li>Art. 6º: Dispensa de certidões que não constem no SICAF para pagamentos de pequeno valor de inscrição.</li>
                      <li>Art. 9º: Parecer referencial padronizado para capacitação continuada de membros e servidores.</li>
                    </ul>
                  </div>
                </div>
              )}

              {selectedMinuta === 'minuta3' && (
                <div className="card" style={{ borderLeft: '4px solid #10b981' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                    <span className="tag" style={{ background: 'rgba(16, 185, 129, 0.15)', color: '#34d399' }}>
                      Instrução Normativa da CLC / MPPI
                    </span>
                    <button 
                      className="btn btn-outline" 
                      style={{ fontSize: '0.75rem', padding: '6px 12px' }}
                      onClick={() => handleCopy("MINUTA DE INSTRUÇÃO NORMATIVA CLC - GOVERNANÇA DE CARONA...", "min3")}
                    >
                      {copiedId === "min3" ? "Copiado!" : "Copiar Minuta Completa"}
                    </button>
                  </div>
                  <h4 style={{ fontSize: '1.15rem', color: '#fff', fontWeight: 700, marginBottom: '8px' }}>
                    Instrução Normativa de Governança para Adesão a Atas de Registro de Preços ("Carona")
                  </h4>
                  <p style={{ color: '#cbd5e1', fontSize: '0.88rem', lineHeight: '1.6', marginBottom: '14px' }}>
                    Blinda a instituição contra o paradigmático <strong>Acórdão nº 300/2025-Plenário do TCE-PI</strong> e internaliza as diretrizes dos Arts. 58-59 do Provimento nº 13/2025 do TJ-PI, estabelecendo matriz de demonstração de vantajosidade e limite temporal de 1 ano de vigência.
                  </p>
                  <div style={{ background: 'rgba(15, 23, 42, 0.5)', padding: '14px', borderRadius: '8px', border: '1px solid #1e293b', fontSize: '0.85rem', color: '#cbd5e1' }}>
                    <strong style={{ color: '#10b981' }}>Dispositivos de Blindagem (Acórdão 300/2025):</strong>
                    <ul style={{ marginTop: '8px', paddingLeft: '20px', display: 'flex', flexDirection: 'column', gap: '6px' }}>
                      <li>Art. 3º: Vedação à adesão a atas licitadas sob a Lei 8.666/93; obrigatoriedade de regime estrito da Lei 14.133/21.</li>
                      <li>Art. 5º: Pesquisa contemporânea demonstrando que o preço registrado permanece vantajoso frente ao mercado.</li>
                      <li>Art. 8º: Anuência expressa do órgão gerenciador e do fornecedor, respeitados os limites de 50% e o dobro global.</li>
                    </ul>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* TAB 5: PROJETO BOAS PRÁTICAS (PRÊMIO CNMP & MPPI) */}
          {activeTab === 'boas-praticas' && (
            <div className="tab-pane">
              {/* HERO DO PROJETO */}
              <div className="hero-portal" style={{ borderColor: '#c5a059' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <div style={{ maxWidth: '80%' }}>
                    <div style={{ display: 'flex', gap: '10px', alignItems: 'center', marginBottom: '10px' }}>
                      <span className="tag" style={{ background: 'rgba(197, 160, 89, 0.2)', color: '#e6c883', border: '1px solid rgba(197, 160, 89, 0.5)' }}>
                        🏆 Candidatura Oficial • Prêmio CNMP 2026
                      </span>
                      <span className="tag" style={{ background: 'rgba(155, 17, 30, 0.25)', color: '#ff6b7a' }}>
                        Prêmio Melhores Práticas MPPI (Ato PGJ 1.025/2020)
                      </span>
                    </div>
                    <h2 style={{ fontSize: '1.75rem', fontWeight: 800, color: '#fff', marginBottom: '8px' }}>
                      {corpusData.premio_boas_praticas?.titulo}
                    </h2>
                    <p style={{ color: '#cbd5e1', fontSize: '0.92rem', lineHeight: '1.5' }}>
                      {corpusData.premio_boas_praticas?.subtitulo}
                    </p>
                    <div style={{ display: 'flex', gap: '20px', marginTop: '14px', fontSize: '0.82rem', color: '#94a3b8' }}>
                      <div><strong style={{ color: '#fff' }}>Unidade:</strong> {corpusData.premio_boas_praticas?.proponente}</div>
                      <div><strong style={{ color: '#fff' }}>Gerente:</strong> {corpusData.premio_boas_praticas?.gerente_projeto}</div>
                    </div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '0.78rem', color: '#94a3b8', textTransform: 'uppercase' }}>Categoria CNMP:</div>
                    <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#c5a059', marginTop: '2px' }}>
                      Governança e Gestão
                    </div>
                    <div style={{ fontSize: '0.75rem', color: '#34d399', marginTop: '4px' }}>
                      Alinhado ao ODS 16 da ONU
                    </div>
                  </div>
                </div>
              </div>

              {/* SELETOR SUB-MODO BOAS PRATICAS */}
              <div style={{ display: 'flex', gap: '10px', marginBottom: '20px', borderBottom: '1px solid #1e293b', paddingBottom: '12px' }}>
                <button 
                  className={`btn ${boasPraticasTab === 'criterios' ? 'btn-primary' : 'btn-outline'}`}
                  style={{ fontSize: '0.86rem', padding: '8px 18px' }}
                  onClick={() => setBoasPraticasTab('criterios')}
                >
                  <Award size={16} /> Defesa dos 5 Critérios Oficiais do CNMP (Art. 40 e 46)
                </button>
                <button 
                  className={`btn ${boasPraticasTab === 'tap' ? 'btn-primary' : 'btn-outline'}`}
                  style={{ fontSize: '0.86rem', padding: '8px 18px' }}
                  onClick={() => setBoasPraticasTab('tap')}
                >
                  <FileText size={16} /> Termo de Abertura de Projeto (TAP Oficial MPPI)
                </button>
              </div>

              {/* SUB-MODO 1: CRITÉRIOS DE JULGAMENTO DO CNMP */}
              {boasPraticasTab === 'criterios' && (
                <div>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '18px' }}>
                    {(corpusData.premio_boas_praticas?.criterios_cnmp || []).map((crit, idx) => (
                      <div key={idx} className="card" style={{ borderLeft: '4px solid #c5a059', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                        <div>
                          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                              <span style={{ fontSize: '1.1rem', fontWeight: 800, color: '#fff' }}>{crit.criterio}</span>
                              <span className="tag" style={{ background: 'rgba(197, 160, 89, 0.15)', color: '#c5a059' }}>
                                Peso {crit.peso}
                              </span>
                            </div>
                            <span className="tag" style={{ background: 'rgba(16, 185, 129, 0.15)', color: '#34d399', fontWeight: 700 }}>
                              Nota Estimada: {crit.pontuacao_estimada}
                            </span>
                          </div>
                          <h4 style={{ color: '#e2e8f0', fontSize: '0.98rem', fontWeight: 600, marginBottom: '10px' }}>
                            {crit.titulo_impacto}
                          </h4>
                          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                            {crit.evidencias.map((ev, eIdx) => (
                              <div key={eIdx} style={{ display: 'flex', gap: '8px', fontSize: '0.84rem', color: '#cbd5e1', lineHeight: '1.45' }}>
                                <CheckCircle size={15} color="#10b981" style={{ flexShrink: 0, marginTop: '2px' }} />
                                <span>{ev}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* ALINHAMENTO ESTRATÉGICO */}
                  <div className="card" style={{ marginTop: '20px', borderTop: '3px solid #3b82f6' }}>
                    <h3 className="card-title">Alinhamento Estratégico Institucional & ODS da ONU</h3>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px', marginTop: '12px' }}>
                      <div style={{ background: 'rgba(15, 23, 42, 0.6)', padding: '14px', borderRadius: '8px', border: '1px solid #1e293b' }}>
                        <strong style={{ color: '#3b82f6', fontSize: '0.85rem' }}>PEI MPPI 2022-2029</strong>
                        <p style={{ color: '#cbd5e1', fontSize: '0.8rem', marginTop: '6px' }}>
                          {corpusData.premio_boas_praticas?.alinhamento_estrategico.pei_mppi}
                        </p>
                      </div>
                      <div style={{ background: 'rgba(15, 23, 42, 0.6)', padding: '14px', borderRadius: '8px', border: '1px solid #1e293b' }}>
                        <strong style={{ color: '#c5a059', fontSize: '0.85rem' }}>PEN-MP (Conselho Nacional do MP)</strong>
                        <p style={{ color: '#cbd5e1', fontSize: '0.8rem', marginTop: '6px' }}>
                          {corpusData.premio_boas_praticas?.alinhamento_estrategico.pen_mp}
                        </p>
                      </div>
                      <div style={{ background: 'rgba(15, 23, 42, 0.6)', padding: '14px', borderRadius: '8px', border: '1px solid #1e293b' }}>
                        <strong style={{ color: '#10b981', fontSize: '0.85rem' }}>ODS 16 - Meta 16.6 (ONU)</strong>
                        <p style={{ color: '#cbd5e1', fontSize: '0.8rem', marginTop: '6px' }}>
                          {corpusData.premio_boas_praticas?.alinhamento_estrategico.ods_onu}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* SUB-MODO 2: TAP OFICIAL DO MPPI */}
              {boasPraticasTab === 'tap' && (
                <div>
                  <div className="card">
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
                      <div>
                        <h3 className="card-title">Termo de Abertura de Projeto (TAP Oficial) — Ato PGJ nº 1.254/2022</h3>
                        <p className="card-desc">Estruturado em conformidade com o Manual de Projetos da Assessoria de Planejamento e Gestão (APG)</p>
                      </div>
                      <span className="tag" style={{ background: 'rgba(16, 185, 129, 0.15)', color: '#34d399' }}>
                        Custo de Desenvolvimento: R$ 0,00 (Próprio)
                      </span>
                    </div>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                      <div style={{ background: 'rgba(15, 23, 42, 0.6)', padding: '14px', borderRadius: '8px', border: '1px solid #1e293b' }}>
                        <strong style={{ color: '#f8fafc', fontSize: '0.9rem' }}>1. Diagnóstico do Problema Fático:</strong>
                        <p style={{ color: '#cbd5e1', fontSize: '0.85rem', marginTop: '4px', lineHeight: '1.5' }}>
                          {corpusData.premio_boas_praticas?.tap_oficial.problema_diagnosticado}
                        </p>
                      </div>

                      <div style={{ background: 'rgba(15, 23, 42, 0.6)', padding: '14px', borderRadius: '8px', border: '1px solid #1e293b' }}>
                        <strong style={{ color: '#f8fafc', fontSize: '0.9rem' }}>2. Solução Institucional Entregue:</strong>
                        <p style={{ color: '#cbd5e1', fontSize: '0.85rem', marginTop: '4px', lineHeight: '1.5' }}>
                          {corpusData.premio_boas_praticas?.tap_oficial.solucao_entregue}
                        </p>
                      </div>

                      <div>
                        <strong style={{ color: '#c5a059', fontSize: '0.9rem', display: 'block', marginBottom: '8px' }}>
                          3. Os 5 Produtos Estratégicos Entregues:
                        </strong>
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '10px' }}>
                          {(corpusData.premio_boas_praticas?.tap_oficial.produtos_entregues || []).map((p, idx) => (
                            <div key={idx} style={{ background: 'rgba(255,255,255,0.02)', padding: '10px', borderRadius: '6px', border: '1px solid #1e293b' }}>
                              <div style={{ color: '#c5a059', fontWeight: 800, fontSize: '0.85rem' }}>Produto {p.num}</div>
                              <div style={{ fontWeight: 600, color: '#fff', fontSize: '0.82rem', marginTop: '2px' }}>{p.nome}</div>
                              <div style={{ color: '#94a3b8', fontSize: '0.74rem', marginTop: '4px' }}>{p.desc}</div>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* TAB 6: EXPLORADOR RAG */}
          {activeTab === 'rag' && (
            <div className="tab-pane">
              <div className="card" style={{ marginBottom: '20px' }}>
                <h3 className="card-title">Explorador Semântico RAG ({corpusData.total_docs.toLocaleString()} Peças Indexadas)</h3>
                <p className="card-desc">Consulte instantaneamente termos de referência, editais, atas, pareceres e matrizes de risco dos 12 órgãos</p>
                
                <div style={{ display: 'grid', gridTemplateColumns: '1.5fr 1fr 1fr', gap: '14px', marginTop: '16px' }}>
                  <div style={{ position: 'relative' }}>
                    <Search size={18} style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: '#c5a059' }} />
                    <input 
                      type="text" 
                      placeholder="Pesquisar por objeto, termo, tecnologia ou número..." 
                      value={search}
                      onChange={(e) => setSearch(e.target.value)}
                      style={{ width: '100%', padding: '12px 14px 12px 38px', background: '#0f172a', border: '1px solid #334155', borderRadius: '8px', color: '#fff', fontSize: '0.9rem', outline: 'none' }}
                    />
                  </div>

                  <select 
                    value={selectedOrgao} 
                    onChange={(e) => setSelectedOrgao(e.target.value)}
                    style={{ padding: '12px 14px', background: '#0f172a', border: '1px solid #334155', borderRadius: '8px', color: '#fff', fontSize: '0.9rem' }}
                  >
                    <option value="TODOS">Todos os Órgãos (12 Instituições)</option>
                    <option value="MPRN">MPRN (2.743 docs)</option>
                    <option value="TJ-PI">TJ-PI (2.178 docs)</option>
                    <option value="MPSE">MPSE (1.144 docs)</option>
                    <option value="TCE-PI">TCE-PI (1.120 docs)</option>
                    <option value="MPPI">MPPI (561 docs)</option>
                    <option value="MPAL">MPAL (538 docs)</option>
                    <option value="MPBA">MPBA (472 docs)</option>
                    <option value="MPDFT">MPDFT (435 docs)</option>
                    <option value="MPMA">MPMA (431 docs)</option>
                    <option value="MPCE">MPCE (322 docs)</option>
                    <option value="MPPB">MPPB (293 docs)</option>
                    <option value="MPPE">MPPE (267 docs)</option>
                  </select>

                  <select 
                    value={selectedCat} 
                    onChange={(e) => setSelectedCat(e.target.value)}
                    style={{ padding: '12px 14px', background: '#0f172a', border: '1px solid #334155', borderRadius: '8px', color: '#fff', fontSize: '0.9rem' }}
                  >
                    <option value="TODOS">Todas as Tipologias</option>
                    <option value="tr">Termo de Referência (TR/PB)</option>
                    <option value="edital">Edital / Aviso Convocatório</option>
                    <option value="parecer">Parecer Jurídico</option>
                    <option value="mapa_riscos">Matriz / Mapa de Riscos</option>
                    <option value="dfd">Documento de Demanda (DFD)</option>
                    <option value="contrato">Contrato / Termo Aditivo</option>
                    <option value="ratificacao">Ato de Ratificação / Decisão</option>
                  </select>
                </div>

                <div style={{ fontSize: '0.85rem', color: '#94a3b8', marginTop: '16px' }}>
                  Mostrando <strong>{filteredDocs.length}</strong> documentos representativos com metadados estruturados:
                </div>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                {filteredDocs.map((doc, idx) => (
                  <div key={idx} style={{ padding: '16px', background: 'rgba(18, 24, 38, 0.65)', border: '1px solid #1e293b', borderRadius: '8px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div style={{ maxWidth: '85%' }}>
                      <div style={{ display: 'flex', gap: '8px', alignItems: 'center', marginBottom: '6px' }}>
                        <span className="tag" style={{ background: 'rgba(197, 160, 89, 0.15)', color: '#c5a059', fontSize: '0.74rem' }}>
                          {doc.orgao}
                        </span>
                        <span className="tag" style={{ background: 'rgba(59, 130, 246, 0.15)', color: '#60a5fa', fontSize: '0.74rem' }}>
                          {doc.categoria.toUpperCase()}
                        </span>
                        <span style={{ fontSize: '0.8rem', color: '#64748b' }}>Ano {doc.ano} • {doc.modalidade}</span>
                      </div>
                      <div style={{ fontWeight: 600, fontSize: '0.95rem', color: '#f1f5f9' }}>{doc.titulo}</div>
                      <div style={{ fontSize: '0.85rem', color: '#94a3b8', marginTop: '4px' }}>{doc.objeto}</div>
                    </div>
                    <button 
                      className="btn btn-outline" 
                      style={{ fontSize: '0.8rem', padding: '6px 14px' }}
                      onClick={() => handleCopy(doc.objeto, doc.id)}
                    >
                      {copiedId === doc.id ? 'Copiado!' : 'Copiar Trecho'}
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
