"""
Constrói tabelas analíticas a partir das tabelas brutas no DuckDB.

A tabela principal (visao_geral_uf) cruza estados, população e PIB,
e adiciona métricas calculadas como PIB per capita e classificações.
"""

import duckdb
import pandas as pd

from src.config import DUCKDB_PATH, ANALYTICS_DIR
from src.logger import get_logger

logger = get_logger(__name__)


SQL_VISAO_GERAL = """
    SELECT
        e.uf_id,
        e.uf_sigla,
        e.uf_nome,
        e.regiao_sigla,
        e.regiao_nome,
        p.ano,
        p.populacao,
        b.pib_mil_reais,
        -- PIB per capita em reais
        ROUND(b.pib_mil_reais * 1000 / p.populacao, 2) AS pib_per_capita,
        -- Percentual da população nacional
        ROUND(p.populacao * 100.0 / SUM(p.populacao) OVER (), 2) AS pct_populacao,
        -- Percentual do PIB nacional
        ROUND(b.pib_mil_reais * 100.0 / SUM(b.pib_mil_reais) OVER (), 2) AS pct_pib,
        -- Ranking por PIB per capita
        RANK() OVER (ORDER BY b.pib_mil_reais * 1000 / p.populacao DESC) AS rank_pib_per_capita
    FROM estados e
    JOIN populacao p ON e.uf_id = p.uf_id
    JOIN pib b ON e.uf_id = b.uf_id
    ORDER BY pib_per_capita DESC
"""

SQL_RESUMO_REGIONAL = """
    SELECT
        regiao_nome,
        regiao_sigla,
        COUNT(*) AS qtd_estados,
        SUM(populacao) AS populacao_total,
        SUM(pib_mil_reais) AS pib_total_mil_reais,
        ROUND(SUM(pib_mil_reais) * 1000 / SUM(populacao), 2) AS pib_per_capita_regiao,
        ROUND(AVG(pib_per_capita), 2) AS media_pib_per_capita_uf
    FROM visao_geral_uf
    GROUP BY regiao_nome, regiao_sigla
    ORDER BY pib_per_capita_regiao DESC
"""


def build_analytics():
    """Cria as tabelas analíticas no DuckDB e exporta CSVs."""
    conn = duckdb.connect(str(DUCKDB_PATH))
    logger.info("Construindo tabelas analíticas...")

    # Tabela 1: Visão geral por UF
    conn.execute("DROP TABLE IF EXISTS visao_geral_uf")
    conn.execute(f"CREATE TABLE visao_geral_uf AS {SQL_VISAO_GERAL}")
    count = conn.execute("SELECT COUNT(*) FROM visao_geral_uf").fetchone()[0]
    logger.info(f"Tabela 'visao_geral_uf': {count} registros")

    # Tabela 2: Resumo por região
    conn.execute("DROP TABLE IF EXISTS resumo_regional")
    conn.execute(f"CREATE TABLE resumo_regional AS {SQL_RESUMO_REGIONAL}")
    count = conn.execute("SELECT COUNT(*) FROM resumo_regional").fetchone()[0]
    logger.info(f"Tabela 'resumo_regional': {count} registros")

    # Exportar CSVs para data/analytics/
    ANALYTICS_DIR.mkdir(parents=True, exist_ok=True)

    for table in ["visao_geral_uf", "resumo_regional"]:
        df = conn.execute(f"SELECT * FROM {table}").df()
        filepath = ANALYTICS_DIR / f"{table}.csv"
        df.to_csv(filepath, index=False)
        logger.info(f"Exportado: {filepath}")

    # Preview
    logger.info("--- Top 5 UFs por PIB per capita ---")
    preview = conn.execute("""
        SELECT uf_sigla, regiao_nome, pib_per_capita, rank_pib_per_capita
        FROM visao_geral_uf
        LIMIT 5
    """).df()
    logger.info(f"\n{preview.to_string(index=False)}")

    logger.info("--- Resumo regional ---")
    preview = conn.execute("SELECT * FROM resumo_regional").df()
    logger.info(f"\n{preview.to_string(index=False)}")

    conn.close()
    logger.info("Tabelas analíticas concluídas")