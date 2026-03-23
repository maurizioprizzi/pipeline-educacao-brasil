"""
Parsers que transformam JSON bruto da API do IBGE em DataFrames planos.

Cada função recebe o JSON e retorna um DataFrame limpo e pronto
para carregar no DuckDB.
"""

import json
from pathlib import Path

import pandas as pd

from src.logger import get_logger

logger = get_logger(__name__)


def parse_estados(filepath: Path) -> pd.DataFrame:
    """Transforma o JSON de estados em tabela plana."""
    data = json.loads(filepath.read_text(encoding="utf-8"))

    rows = []
    for item in data:
        rows.append({
            "uf_id": item["id"],
            "uf_sigla": item["sigla"],
            "uf_nome": item["nome"],
            "regiao_sigla": item["regiao"]["sigla"],
            "regiao_nome": item["regiao"]["nome"],
        })

    df = pd.DataFrame(rows)
    logger.info(f"Estados: {len(df)} registros parseados")
    return df


def parse_agregado(filepath: Path, coluna_valor: str) -> pd.DataFrame:
    """
    Transforma o JSON de agregados do IBGE em tabela plana.

    Serve para qualquer endpoint /agregados/ (população, PIB, etc).
    O parâmetro coluna_valor define o nome da coluna com o dado.
    """
    data = json.loads(filepath.read_text(encoding="utf-8"))

    unidade = data[0].get("unidade", "")
    series = data[0]["resultados"][0]["series"]

    rows = []
    for item in series:
        uf_id = item["localidade"]["id"]
        uf_nome = item["localidade"]["nome"]

        for ano, valor in item["serie"].items():
            rows.append({
                "uf_id": int(uf_id),
                "uf_nome": uf_nome,
                "ano": int(ano),
                coluna_valor: float(valor) if valor else None,
            })

    df = pd.DataFrame(rows)
    logger.info(f"{coluna_valor}: {len(df)} registros ({unidade})")
    return df