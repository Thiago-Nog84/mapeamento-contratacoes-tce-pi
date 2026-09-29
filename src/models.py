"""
Modelos de dados para o Ecossistema de Contratações do TCE-PI.
Representa procedimentos licitatórios, artefatos, responsáveis e normativos.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Optional
from datetime import datetime

@dataclass
class ArtefatoLicitacao:
    id_licitacao_web: int
    numero_ordem: int
    tipo: str  # ex: Edital, Projeto básico, Termo de Referência, Planilha
    descricao: str
    nome_arquivo: str
    data_cadastro: str
    tamanho_bytes: Optional[int] = None
    caminho_local: Optional[str] = None
    botao_download_id: Optional[str] = None

@dataclass
class ResponsavelLicitacao:
    id_licitacao_web: int
    funcao: str  # ex: Agente de Contratação, Pregoeiro, Autoridade Competente
    nome: str
    cpf_mascarado: Optional[str] = None

@dataclass
class ContratoOriginado:
    id_licitacao_web: int
    numero_contrato: str
    ano: int
    contratado_nome: str
    contratado_cnpj_cpf: str
    valor_contratado: float
    data_assinatura: Optional[str] = None
    link_muralcon: Optional[str] = None

@dataclass
class ProcedimentoLicitatorio:
    id_licitacao_web: int
    controle_tce: str  # ex: LW-009880/26
    orgao_nome: str
    id_unidade_gestora: Optional[str] = None
    esfera: str = "Municipal"  # Municipal ou Estadual
    
    numero_procedimento: Optional[str] = None
    numero_processo_adm: Optional[str] = None
    modalidade: Optional[str] = None
    objeto: Optional[str] = None
    valor_previsto: float = 0.0
    tipo_objeto: Optional[str] = None
    regime_execucao: Optional[str] = None
    criterio_julgamento: Optional[str] = None
    forma_realizacao: Optional[str] = None  # Eletrônica ou Presencial
    modo_disputa: Optional[str] = None  # Aberto, Fechado, etc.
    regime_juridico: Optional[str] = None  # Lei nº 14.133/21 ou 8.666/93
    registro_preco: bool = False
    status_licitacao: Optional[str] = None
    
    data_divulgacao: Optional[str] = None
    data_abertura: Optional[str] = None
    periodo_propostas_inicio: Optional[str] = None
    periodo_propostas_fim: Optional[str] = None
    data_homologacao: Optional[str] = None
    
    link_mural: Optional[str] = None
    artefatos: List[ArtefatoLicitacao] = field(default_factory=list)
    responsaveis: List[ResponsavelLicitacao] = field(default_factory=list)
    contratos: List[ContratoOriginado] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)

@dataclass
class NormativoContratacao:
    sigla: str  # ex: IN TCE-PI nº 02/2026
    ano: int
    titulo: str
    objeto: str
    sistemas_relacionados: List[str]  # Licitações Web, Contratos Web, Obras Web, etc.
    prazos_principais: List[str]
    status: str = "Vigente"
