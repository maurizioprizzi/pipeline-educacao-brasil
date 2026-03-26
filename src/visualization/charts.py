"""
Geração de gráficos estáticos (matplotlib) e interativos (plotly).

Cada função recebe um DataFrame e salva o gráfico em outputs/.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import plotly.express as px
import pandas as pd

from src.config import OUTPUTS_DIR
from src.logger import get_logger

logger = get_logger(__name__)

# Cores por região
CORES_REGIAO = {
    "Norte": "#1D9E75",
    "Nordeste": "#D85A30",
    "Sudeste": "#534AB7",
    "Sul": "#185FA5",
    "Centro-Oeste": "#BA7517",
}


def chart_pib_per_capita_bar(df: pd.DataFrame) -> None:
    """Gráfico de barras horizontais — PIB per capita por UF."""
    df_sorted = df.sort_values("pib_per_capita")
    cores = [CORES_REGIAO[r] for r in df_sorted["regiao_nome"]]

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(df_sorted["uf_sigla"], df_sorted["pib_per_capita"], color=cores)

    ax.set_xlabel("PIB per capita (R$)")
    ax.set_title("PIB per capita por UF — Brasil 2021", fontsize=14, fontweight="bold")
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"R$ {x:,.0f}"))

    # Legenda manual por região
    from matplotlib.patches import Patch
    legend = [Patch(color=c, label=r) for r, c in CORES_REGIAO.items()]
    ax.legend(handles=legend, loc="lower right", fontsize=9)

    plt.tight_layout()
    filepath = OUTPUTS_DIR / "pib_per_capita_uf.png"
    fig.savefig(filepath, dpi=150)
    plt.close(fig)
    logger.info(f"Salvo: {filepath}")


def chart_regiao_pie(df_regiao: pd.DataFrame) -> None:
    """Gráfico de pizza — distribuição do PIB por região."""
    cores = [CORES_REGIAO[r] for r in df_regiao["regiao_nome"]]

    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        df_regiao["pib_total_mil_reais"],
        labels=df_regiao["regiao_nome"],
        colors=cores,
        autopct="%1.1f%%",
        startangle=90,
        textprops={"fontsize": 11},
    )
    for t in autotexts:
        t.set_fontweight("bold")

    ax.set_title("Distribuição do PIB por Região — 2021", fontsize=14, fontweight="bold")

    plt.tight_layout()
    filepath = OUTPUTS_DIR / "pib_por_regiao.png"
    fig.savefig(filepath, dpi=150)
    plt.close(fig)
    logger.info(f"Salvo: {filepath}")


def chart_scatter_pop_pib(df: pd.DataFrame) -> None:
    """Scatter plot interativo — População vs PIB per capita (plotly)."""
    fig = px.scatter(
        df,
        x="populacao",
        y="pib_per_capita",
        color="regiao_nome",
        size="pib_mil_reais",
        hover_name="uf_nome",
        hover_data={"populacao": ":,.0f", "pib_per_capita": ":,.2f"},
        color_discrete_map=CORES_REGIAO,
        title="População vs PIB per capita por UF — 2021",
        labels={
            "populacao": "População",
            "pib_per_capita": "PIB per capita (R$)",
            "regiao_nome": "Região",
        },
    )
    fig.update_layout(template="plotly_white")

    filepath = OUTPUTS_DIR / "scatter_pop_pib.html"
    fig.write_html(str(filepath))
    logger.info(f"Salvo: {filepath}")