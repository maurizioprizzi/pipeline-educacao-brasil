"""
Constrói tabelas analíticas a partir das tabelas brutas no DuckDB.

Cruza dados do IBGE (população, PIB) com dados do INEP (matrículas,
docentes, escolas) para gerar indicadores educacionais por UF.
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
        p.ano AS ano_ibge,
        p.populacao,
        b.pib_mil_reais,
        ROUND(b.pib_mil_reais * 1000 / p.populacao, 2) AS pib_per_capita,
        ROUND(p.populacao * 100.0 / SUM(p.populacao) OVER (), 2) AS pct_populacao,
        ROUND(b.pib_mil_reais * 100.0 / SUM(b.pib_mil_reais) OVER (), 2) AS pct_pib,
        RANK() OVER (ORDER BY b.pib_mil_reais * 1000 / p.populacao DESC) AS rank_pib_per_capita,
        ed.matriculas,
        ed.docentes,
        ed.escolas,
        ROUND(ed.matriculas * 1.0 / ed.docentes, 1) AS alunos_por_docente,
        ROUND(ed.matriculas * 1.0 / ed.escolas, 1) AS alunos_por_escola,
        ROUND(ed.matriculas * 1000.0 / p.populacao, 1) AS matriculas_por_mil_hab,
        ROUND(ed.escolas * 100000.0 / p.populacao, 1) AS escolas_por_100k_hab,
        ROUND(b.pib_mil_reais * 1000.0 / ed.matriculas, 2) AS pib_por_matricula
    FROM estados e
    JOIN populacao p ON e.uf_id = p.uf_id
    JOIN pib b ON e.uf_id = b.uf_id
    JOIN educacao ed ON e.uf_nome = ed.uf_nome
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
        SUM(matriculas) AS matriculas_total,
        SUM(docentes) AS docentes_total,
        SUM(escolas) AS escolas_total,
        ROUND(SUM(matriculas) * 1.0 / SUM(docentes), 1) AS alunos_por_docente,
        ROUND(SUM(matriculas) * 1000.0 / SUM(populacao), 1) AS matriculas_por_mil_hab,
        ROUND(SUM(pib_mil_reais) * 1000.0 / SUM(matriculas), 2) AS pib_por_matricula
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

    # Exportar CSVs
    ANALYTICS_DIR.mkdir(parents=True, exist_ok=True)

    for table in ["visao_geral_uf", "resumo_regional"]:
        df = conn.execute(f"SELECT * FROM {table}").df()
        filepath = ANALYTICS_DIR / f"{table}.csv"
        df.to_csv(filepath, index=False)
        logger.info(f"Exportado: {filepath}")

    # Preview: indicadores educacionais
    logger.info("--- Top 5 UFs: alunos por docente ---")
    preview = conn.execute("""
        SELECT uf_sigla, regiao_nome, alunos_por_docente, alunos_por_escola, matriculas_por_mil_hab
        FROM visao_geral_uf
        ORDER BY alunos_por_docente DESC
        LIMIT 5
    """).df()
    logger.info(f"\n{preview.to_string(index=False)}")

    logger.info("--- Resumo regional (educação) ---")
    preview = conn.execute("""
        SELECT regiao_nome, pib_per_capita_regiao, alunos_por_docente,
               matriculas_por_mil_hab, pib_por_matricula
        FROM resumo_regional
    """).df()
    logger.info(f"\n{preview.to_string(index=False)}")

    conn.close()
    logger.info("Tabelas analíticas concluídas")


if __name__ == "__main__":
    build_analytics()