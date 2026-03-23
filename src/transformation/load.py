"""
Carrega DataFrames no DuckDB.
"""

import duckdb

from src.config import DUCKDB_PATH
from src.logger import get_logger

logger = get_logger(__name__)


def get_connection() -> duckdb.DuckDBPyConnection:
    """Abre conexão com o banco DuckDB."""
    DUCKDB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = duckdb.connect(str(DUCKDB_PATH))
    logger.info(f"Conectado ao DuckDB em {DUCKDB_PATH}")
    return conn


def load_dataframe(conn: duckdb.DuckDBPyConnection, df, table_name: str) -> None:
    """Carrega um DataFrame como tabela no DuckDB (substitui se existir)."""
    conn.execute(f"DROP TABLE IF EXISTS {table_name}")
    conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")
    count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    logger.info(f"Tabela '{table_name}': {count} registros carregados")