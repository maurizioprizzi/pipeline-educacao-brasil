"""
Configurações centralizadas do projeto.

Todos os caminhos e parâmetros ficam aqui.
Nenhum outro módulo deve hardcodar caminhos.
"""

from pathlib import Path

# ============================================================================
# Caminhos
# ============================================================================

ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
ANALYTICS_DIR = DATA_DIR / "analytics"
OUTPUTS_DIR = ROOT_DIR / "outputs"

# ============================================================================
# Fontes de dados
# ============================================================================

SOURCES = {
    "ibge_estados": {
        "url": "https://servicodados.ibge.gov.br/api/v1/localidades/estados",
        "description": "Lista de estados brasileiros com região — IBGE",
        "format": "json",
    },
    "ibge_populacao": {
        "url": "https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/2021/variaveis/9324?localidades=N3[all]",
        "description": "População estimada por UF 2021 — IBGE",
        "format": "json",
    },
    "ibge_pib": {
        "url": "https://servicodados.ibge.gov.br/api/v3/agregados/5938/periodos/2021/variaveis/37?localidades=N3[all]",
        "description": "PIB a preços correntes por UF 2021 — IBGE",
        "format": "json",
    },
}

# ============================================================================
# DuckDB
# ============================================================================

DUCKDB_PATH = DATA_DIR / "educacao.duckdb"

# ============================================================================
# Parâmetros
# ============================================================================

REQUEST_TIMEOUT = 30
REQUEST_RETRIES = 3
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"