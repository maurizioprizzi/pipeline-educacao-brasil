"""Ponto de entrada da transformação e carga no DuckDB."""

from src.config import RAW_DIR
from src.transformation.parse import parse_estados, parse_agregado
from src.transformation.load import get_connection, load_dataframe
from src.logger import get_logger

logger = get_logger(__name__)


def run_transformation():
    """Parseia os JSONs brutos e carrega no DuckDB."""
    logger.info("Início da transformação e carga")

    # Parsear JSONs
    df_estados = parse_estados(RAW_DIR / "ibge_estados.json")
    df_populacao = parse_agregado(RAW_DIR / "ibge_populacao.json", "populacao")
    df_pib = parse_agregado(RAW_DIR / "ibge_pib.json", "pib_mil_reais")

    # Carregar no DuckDB
    conn = get_connection()

    load_dataframe(conn, df_estados, "estados")
    load_dataframe(conn, df_populacao, "populacao")
    load_dataframe(conn, df_pib, "pib")

    # Conferir
    logger.info("--- Tabelas no banco ---")
    tables = conn.execute("SHOW TABLES").fetchall()
    for table in tables:
        logger.info(f"  {table[0]}")

    conn.close()
    logger.info("Transformação e carga finalizadas")


if __name__ == "__main__":
    run_transformation()