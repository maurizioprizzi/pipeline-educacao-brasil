"""Ponto de entrada da transformação e carga no DuckDB."""

import json
import pandas as pd

from src.config import RAW_DIR
from src.transformation.parse import parse_estados, parse_agregado
from src.transformation.load import get_connection, load_dataframe
from src.logger import get_logger

logger = get_logger(__name__)


def run_transformation():
    """Parseia os JSONs brutos e carrega no DuckDB."""
    logger.info("Início da transformação e carga")

    # --- Dados IBGE ---
    df_estados = parse_estados(RAW_DIR / "ibge_estados.json")
    df_populacao = parse_agregado(RAW_DIR / "ibge_populacao.json", "populacao")
    df_pib = parse_agregado(RAW_DIR / "ibge_pib.json", "pib_mil_reais")

    # --- Dados INEP ---
    inep_path = RAW_DIR / "inep_censo_escolar_2023.json"
    df_inep = pd.read_json(inep_path)
    logger.info(f"INEP: {len(df_inep)} registros carregados")

    # Carregar no DuckDB
    conn = get_connection()

    load_dataframe(conn, df_estados, "estados")
    load_dataframe(conn, df_populacao, "populacao")
    load_dataframe(conn, df_pib, "pib")
    load_dataframe(conn, df_inep, "educacao")

    # --- Tabelas no banco ---
    logger.info("--- Tabelas no banco ---")
    tables = conn.execute("SHOW TABLES").fetchall()
    for table in tables:
        count = conn.execute(f"SELECT COUNT(*) FROM {table[0]}").fetchone()[0]
        logger.info(f"  {table[0]}: {count} registros")

    conn.close()
    logger.info("Transformação e carga finalizadas")


if __name__ == "__main__":
    run_transformation()