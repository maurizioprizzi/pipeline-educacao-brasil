"""Ponto de entrada da visualização."""

import pandas as pd

from src.config import ANALYTICS_DIR, OUTPUTS_DIR
from src.visualization.charts import (
    chart_pib_per_capita_bar,
    chart_regiao_pie,
    chart_scatter_pop_pib,
)
from src.logger import get_logger

logger = get_logger(__name__)


def run_visualization():
    """Lê os CSVs analíticos e gera todos os gráficos."""
    logger.info("Início da geração de visualizações")

    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    # Carregar dados
    df_uf = pd.read_csv(ANALYTICS_DIR / "visao_geral_uf.csv")
    df_regiao = pd.read_csv(ANALYTICS_DIR / "resumo_regional.csv")
    logger.info(f"Dados carregados: {len(df_uf)} UFs, {len(df_regiao)} regiões")

    # Gerar gráficos
    chart_pib_per_capita_bar(df_uf)
    chart_regiao_pie(df_regiao)
    chart_scatter_pop_pib(df_uf)

    logger.info("Visualizações concluídas")


if __name__ == "__main__":
    run_visualization()