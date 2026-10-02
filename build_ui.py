import os

css_content = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
  /* Cores MPPI - Baseadas em identidades de MPEs (Vinho/Vermelho Escuro, Dourado e Cinza Chumbo) */
  --bg-dark: #0f1115;
  --bg-card: rgba(26, 29, 36, 0.75);
  --bg-card-hover: rgba(32, 36, 45, 0.95);
  
  --mppi-primary: #9b111e; /* Vermelho/Vinho MPPI */
  --mppi-primary-light: #c21827;
  --mppi-gold: #c5a059; /* Dourado */
  --mppi-gold-light: #e6c883;
  --mppi-dark: #1f2229;
  
  --text-main: #f8fafc;
  --text-muted: #94a3b8;
  
  --accent-tce: #3b82f6; /* Azul para diferenciar o TCE-PI */
  
  --border-color: rgba(197, 160, 89, 0.15); /* Borda com toque dourado */
  --glass-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
  --glass-backdrop: blur(16px);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Inter', -apple-system, sans-serif;
  background-color: var(--bg-dark);
  background-image: 
    radial-gradient(circle at 10% 20%, rgba(155, 17, 30, 0.15) 0%, transparent 40%),
    radial-gradient(circle at 90% 80%, rgba(197, 160, 89, 0.1) 0%, transparent 40%);
  background-attachment: fixed;
  color: var(--text-main);
  min-height: 100vh;
  line-height: 1.6;
}

/* Glassmorphism Premium */
.glass-card {
  background: var(--bg-card);
  backdrop-filter: var(--glass-backdrop);
  -webkit-backdrop-filter: var(--glass-backdrop);
  border: 1px solid var(--border-color);
  border-radius: 20px;
  padding: 32px;
  box-shadow: var(--glass-shadow);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.glass-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--mppi-primary), var(--mppi-gold));
  opacity: 0;
  transition: opacity 0.4s ease;
}

.glass-card:hover {
  background: var(--bg-card-hover);
  transform: translateY(-4px);
  border-color: rgba(197, 160, 89, 0.3);
  box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.6);
}

.glass-card:hover::before {
  opacity: 1;
}

.dashboard-container {
  display: grid;
  grid-template-columns: 280px 1fr;
  min-height: 100vh;
}

/* Sidebar */
.sidebar {
  background: rgba(15, 17, 21, 0.8);
  backdrop-filter: blur(20px);
  border-right: 1px solid var(--border-color);
  padding: 32px 24px;
  display: flex;
  flex-direction: column;
}

.brand {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 48px;
}
.brand-icon {
  width: 48px; height: 48px;
  background: linear-gradient(135deg, var(--mppi-primary), #600711);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(155, 17, 30, 0.4);
}
.brand h2 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-main);
  line-height: 1.2;
}
.brand h2 span {
  color: var(--mppi-gold);
  font-size: 0.85rem;
  font-weight: 500;
  display: block;
}

.nav-menu { list-style: none; display: flex; flex-direction: column; gap: 8px; }
.nav-item {
  display: flex; align-items: center; gap: 12px;
  padding: 12px 16px;
  border-radius: 12px;
  color: var(--text-muted);
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  cursor: pointer;
}
.nav-item:hover, .nav-item.active {
  background: rgba(197, 160, 89, 0.1);
  color: var(--mppi-gold);
}
.nav-item.active {
  border-left: 3px solid var(--mppi-gold);
}

/* Main Content */
.main-content {
  padding: 40px;
  overflow-y: auto;
}

.header {
  margin-bottom: 40px;
}
.header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 8px;
}
.header p { color: var(--text-muted); font-size: 1.1rem; }

.grid-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-bottom: 32px;
}

.stat-val {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 16px 0 8px;
  color: #fff;
}
.stat-label {
  color: var(--text-muted);
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
}

.grid-charts {
  display: grid;
  grid-template-columns: 3fr 2fr;
  gap: 24px;
  margin-bottom: 32px;
}

.chart-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 12px;
  color: #fff;
}
.chart-title svg { color: var(--mppi-gold); }

/* RAG Search Area */
.search-container {
  position: relative;
  margin-bottom: 32px;
}
.search-input {
  width: 100%;
  padding: 20px 24px 20px 64px;
  border-radius: 16px;
  background: rgba(26, 29, 36, 0.8);
  border: 1px solid rgba(197, 160, 89, 0.3);
  color: #fff;
  font-size: 1.1rem;
  outline: none;
  box-shadow: 0 4px 24px rgba(0,0,0,0.2);
  transition: all 0.3s ease;
}
.search-input:focus {
  border-color: var(--mppi-gold);
  box-shadow: 0 4px 24px rgba(197, 160, 89, 0.2);
  background: rgba(26, 29, 36, 1);
}
.search-icon {
  position: absolute;
  left: 24px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--mppi-gold);
}

/* Insight Cards */
.insight-card {
  background: rgba(15, 17, 21, 0.5);
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 16px;
}
.insight-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.insight-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #fff;
}
.tags { display: flex; gap: 8px; }
.tag {
  padding: 4px 12px;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
}
.tag.mppi { background: rgba(155, 17, 30, 0.2); color: #ff6b7a; border: 1px solid rgba(155, 17, 30, 0.5); }
.tag.tce { background: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.5); }

.insight-body {
  color: var(--text-muted);
  font-size: 0.95rem;
  line-height: 1.6;
}
"""

jsx_content = """
import React, { useState } from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer,
  RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar
} from 'recharts';
import { Shield, FileText, Search, Activity, BookOpen, Layers, Target, Scale } from 'lucide-react';
import './index.css';

const barData = [
  { name: 'Dispensa', TCE: 339, MPPI: 14 },
  { name: 'Inexigibilidade', TCE: 490, MPPI: 9 },
  { name: 'Pregão', TCE: 13, MPPI: 17 }
];

const radarData = [
  { subject: 'Atestados Téc.', TCE: 90, MPPI: 55, fullMark: 100 },
  { subject: 'Penalidades', TCE: 85, MPPI: 60, fullMark: 100 },
  { subject: 'SLA Flexível', TCE: 40, MPPI: 85, fullMark: 100 },
  { subject: 'Sustentabilidade', TCE: 80, MPPI: 40, fullMark: 100 },
  { subject: 'Exigência de Capital', TCE: 95, MPPI: 50, fullMark: 100 },
  { subject: 'Garantias', TCE: 85, MPPI: 90, fullMark: 100 },
];

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div style={{ background: 'rgba(26, 29, 36, 0.95)', border: '1px solid rgba(197,160,89,0.3)', padding: '12px', borderRadius: '8px' }}>
        <p style={{ color: '#fff', marginBottom: '8px', fontWeight: 600 }}>{label}</p>
        {payload.map((entry, index) => (
          <p key={index} style={{ color: entry.color, fontSize: '0.9rem' }}>
            {entry.name}: {entry.value} processos
          </p>
        ))}
      </div>
    );
  }
  return null;
};

function App() {
  const [search, setSearch] = useState('');

  return (
    <div className="dashboard-container">
      {/* Sidebar com Identidade MPPI */}
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">
            <Shield color="#e6c883" size={28} />
          </div>
          <h2>
            MPPI
            <span>Observatório de Compras</span>
          </h2>
        </div>

        <nav>
          <ul className="nav-menu">
            <li className="nav-item active"><Activity size={20} /> Visão Geral</li>
            <li className="nav-item"><BookOpen size={20} /> Base Normativa</li>
            <li className="nav-item"><Scale size={20} /> Análise RAG</li>
            <li className="nav-item"><Layers size={20} /> Relatórios</li>
          </ul>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <header className="header">
          <h1>Análise Comparativa de Editais</h1>
          <p>Motor RAG treinado com 1.241 documentos do TCE-PI e MPPI</p>
        </header>

        {/* Top Stats */}
        <section className="grid-stats">
          <div className="glass-card" style={{ borderTop: '4px solid var(--mppi-gold)' }}>
            <FileText color="var(--mppi-gold)" size={32} />
            <div className="stat-val">1.120</div>
            <div className="stat-label">Documentos TCE-PI (Modelo)</div>
          </div>
          <div className="glass-card" style={{ borderTop: '4px solid var(--mppi-primary)' }}>
            <FileText color="#ff6b7a" size={32} />
            <div className="stat-val">121</div>
            <div className="stat-label">Documentos MPPI (Análise)</div>
          </div>
          <div className="glass-card" style={{ borderTop: '4px solid #34d399' }}>
            <Target color="#34d399" size={32} />
            <div className="stat-val">84%</div>
            <div className="stat-label">Grau de Alinhamento Global</div>
          </div>
        </section>

        {/* Charts */}
        <section className="grid-charts">
          <div className="glass-card">
            <div className="chart-title">
              <Layers size={24} />
              Distribuição por Modalidade (2024-2026)
            </div>
            <div style={{ height: '350px' }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={barData} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                  <XAxis dataKey="name" stroke="#94a3b8" tick={{ fill: '#94a3b8' }} axisLine={false} />
                  <YAxis stroke="#94a3b8" tick={{ fill: '#94a3b8' }} axisLine={false} />
                  <RechartsTooltip content={<CustomTooltip />} />
                  <Legend wrapperStyle={{ paddingTop: '20px' }} />
                  <Bar dataKey="TCE" name="TCE-PI" fill="#3b82f6" radius={[6, 6, 0, 0]} barSize={40} />
                  <Bar dataKey="MPPI" name="MPPI" fill="#9b111e" radius={[6, 6, 0, 0]} barSize={40} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="glass-card">
            <div className="chart-title">
              <Activity size={24} />
              Radar de Rigidez Institucional
            </div>
            <div style={{ height: '350px' }}>
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="65%" data={radarData}>
                  <PolarGrid stroke="rgba(255,255,255,0.1)" />
                  <PolarAngleAxis dataKey="subject" tick={{ fill: '#94a3b8', fontSize: 12, fontWeight: 500 }} />
                  <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                  <Radar name="TCE-PI" dataKey="TCE" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.3} strokeWidth={2} />
                  <Radar name="MPPI" dataKey="MPPI" stroke="#9b111e" fill="#9b111e" fillOpacity={0.5} strokeWidth={2} />
                  <Legend wrapperStyle={{ paddingTop: '20px' }} />
                  <RechartsTooltip contentStyle={{ background: 'rgba(26,29,36,0.95)', border: '1px solid rgba(197,160,89,0.3)', borderRadius: '8px' }} />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </section>

        {/* RAG Search Engine */}
        <section className="glass-card">
          <div className="chart-title" style={{ marginBottom: '16px' }}>
            <Search size={24} />
            Motor RAG: Extração de Lacunas & Compliance
          </div>
          
          <div className="search-container">
            <Search className="search-icon" size={24} />
            <input 
              type="text" 
              className="search-input"
              placeholder="Pesquise o objeto (ex: Serviços de Limpeza, Licenças de Software, Vigilância)..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>

          <div className="insights-container">
            <div className="insight-card">
              <div className="insight-header">
                <div className="insight-title">Comparativo Normativo: Terceirização</div>
                <div className="tags">
                  <span className="tag tce">TCE-PI: Rígido</span>
                  <span className="tag mppi">MPPI: Flexível</span>
                </div>
              </div>
              <div className="insight-body">
                O <strong>MPPI</strong> utiliza a Resolução CNMP nº 150/2016 como base primária para serviços continuados, mantendo SLAs baseados em relatórios mensais amplos. Já o <strong>TCE-PI</strong> adotou integralmente a IN SEGES/MPDG nº 05/2017 e a Lei 14.133/21, aplicando IMR (Instrumento de Medição de Resultado) com descontos diretos na fatura atrelados a checklists diários.
                <br/><br/>
                <strong style={{color: 'var(--mppi-gold)'}}>Recomendação RAG:</strong> Atualizar as minutas do MPPI para prever o IMR (Instrumento de Medição de Resultado) detalhado, reduzindo a subjetividade da fiscalização.
              </div>
            </div>

            <div className="insight-card">
              <div className="insight-header">
                <div className="insight-title">Critérios ESG e Sustentabilidade</div>
                <div className="tags">
                  <span className="tag tce">TCE-PI: 80/100</span>
                  <span className="tag mppi">MPPI: 40/100</span>
                </div>
              </div>
              <div className="insight-body">
                Os Editais do <strong>TCE-PI</strong> exigem que a contratada reserve 5% das vagas de terceirização para mulheres vítimas de violência doméstica (Decreto Estadual). Essa exigência está ausente nos 14 editais de dispensa analisados do <strong>MPPI</strong>.
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
"""

with open('dashboard/src/index.css', 'w', encoding='utf-8') as f:
    f.write(css_content)

with open('dashboard/src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(jsx_content)

print("UI Reconstruída com as cores do MPPI!")
