"""
Camada de persistência em SQLite e exportação para JSON.
Armazena procedimentos licitatórios, artefatos e metadados.
"""

import sqlite3
import json
import os
from typing import List, Optional
from .models import ProcedimentoLicitatorio, ArtefatoLicitacao

class TCEStorage:
    def __init__(self, db_path: str = "dados_tce.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabela de procedimentos licitatórios
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS procedimentos (
                id_licitacao_web INTEGER PRIMARY KEY,
                controle_tce TEXT,
                orgao_nome TEXT,
                id_unidade_gestora TEXT,
                esfera TEXT,
                numero_procedimento TEXT,
                numero_processo_adm TEXT,
                modalidade TEXT,
                objeto TEXT,
                valor_previsto REAL,
                tipo_objeto TEXT,
                regime_execucao TEXT,
                criterio_julgamento TEXT,
                forma_realizacao TEXT,
                modo_disputa TEXT,
                regime_juridico TEXT,
                status_licitacao TEXT,
                data_abertura TEXT,
                link_mural TEXT,
                atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # Tabela de artefatos (documentos anexos)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS artefatos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_licitacao_web INTEGER,
                numero_ordem INTEGER,
                tipo TEXT,
                descricao TEXT,
                nome_arquivo TEXT,
                data_cadastro TEXT,
                tamanho_bytes INTEGER,
                caminho_local TEXT,
                FOREIGN KEY (id_licitacao_web) REFERENCES procedimentos(id_licitacao_web)
            )
            """)
            conn.commit()

    def salvar_procedimento(self, proc: ProcedimentoLicitatorio):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO procedimentos (
                id_licitacao_web, controle_tce, orgao_nome, id_unidade_gestora, esfera,
                numero_procedimento, numero_processo_adm, modalidade, objeto, valor_previsto,
                tipo_objeto, regime_execucao, criterio_julgamento, forma_realizacao,
                modo_disputa, regime_juridico, status_licitacao, data_abertura, link_mural
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id_licitacao_web) DO UPDATE SET
                controle_tce=excluded.controle_tce,
                objeto=excluded.objeto,
                valor_previsto=excluded.valor_previsto,
                status_licitacao=excluded.status_licitacao,
                atualizado_em=CURRENT_TIMESTAMP
            """, (
                proc.id_licitacao_web, proc.controle_tce, proc.orgao_nome, proc.id_unidade_gestora, proc.esfera,
                proc.numero_procedimento, proc.numero_processo_adm, proc.modalidade, proc.objeto, proc.valor_previsto,
                proc.tipo_objeto, proc.regime_execucao, proc.criterio_julgamento, proc.forma_realizacao,
                proc.modo_disputa, proc.regime_juridico, proc.status_licitacao, proc.data_abertura, proc.link_mural
            ))

            # Inserir artefatos
            for art in proc.artefatos:
                cursor.execute("""
                INSERT INTO artefatos (
                    id_licitacao_web, numero_ordem, tipo, descricao, nome_arquivo,
                    data_cadastro, tamanho_bytes, caminho_local
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    proc.id_licitacao_web, art.numero_ordem, art.tipo, art.descricao, art.nome_arquivo,
                    art.data_cadastro, art.tamanho_bytes, art.caminho_local
                ))
            conn.commit()

    def exportar_para_json(self, json_path: str = "licitacoes_export.json"):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM procedimentos")
            procs = [dict(r) for r in cursor.fetchall()]

            for p in procs:
                cursor.execute("SELECT * FROM artefatos WHERE id_licitacao_web = ?", (p['id_licitacao_web'],))
                p['artefatos'] = [dict(r) for r in cursor.fetchall()]

            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(procs, f, indent=2, ensure_ascii=False)
        return json_path
