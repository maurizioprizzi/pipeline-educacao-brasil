"""
Modelos de Machine Learning aplicados aos dados educacionais.

1. Regressão Linear — PIB per capita prediz alunos por docente?
2. Random Forest — quais variáveis mais influenciam a educação?
3. K-Means Clustering — agrupamento de estados por perfil socioeducacional
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error

from src.config import ANALYTICS_DIR, OUTPUTS_DIR
from src.logger import get_logger

logger = get_logger(__name__)


def run_ml_models():
    """Executa todos os modelos de ML."""
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(ANALYTICS_DIR / "visao_geral_uf.csv")
    logger.info(f"Dados carregados: {len(df)} UFs")

    regression_analysis(df)
    feature_importance(df)
    clustering_analysis(df)

    logger.info("Modelos de ML concluídos")


def regression_analysis(df: pd.DataFrame) -> None:
    """Regressão linear: PIB per capita vs alunos por docente."""
    X = df[["pib_per_capita"]].values
    y = df["alunos_por_docente"].values

    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)

    r2 = r2_score(y, y_pred)
    mae = mean_absolute_error(y, y_pred)

    logger.info(f"Regressão Linear: R² = {r2:.3f}, MAE = {mae:.2f}")
    logger.info(f"  Coeficiente: {model.coef_[0]:.6f}")
    logger.info(f"  Intercepto: {model.intercept_:.2f}")
    logger.info(f"  Interpretação: a cada R$ 10.000 de PIB per capita,")
    logger.info(f"  o número de alunos por docente reduz em {abs(model.coef_[0]) * 10000:.1f}")

    # Cores por região
    cores_regiao = {
        "Norte": "#1D9E75", "Nordeste": "#D85A30", "Sudeste": "#534AB7",
        "Sul": "#185FA5", "Centro-Oeste": "#BA7517",
    }
    cores = [cores_regiao[r] for r in df["regiao_nome"]]

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.scatter(df["pib_per_capita"], df["alunos_por_docente"], c=cores, s=80, zorder=3)

    # Linha de regressão
    x_line = np.linspace(X.min(), X.max(), 100)
    y_line = model.predict(x_line.reshape(-1, 1))
    ax.plot(x_line, y_line, color="#888", linestyle="--", linewidth=1.5, label=f"R² = {r2:.3f}")

    # Labels dos estados
    for _, row in df.iterrows():
        ax.annotate(row["uf_sigla"], (row["pib_per_capita"], row["alunos_por_docente"]),
                     fontsize=8, ha="left", va="bottom", xytext=(4, 4),
                     textcoords="offset points")

    ax.set_xlabel("PIB per capita (R$)")
    ax.set_ylabel("Alunos por docente")
    ax.set_title("Regressão: PIB per capita vs alunos por docente", fontsize=14, fontweight="bold")
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"R$ {x:,.0f}"))
    ax.legend(fontsize=11)

    from matplotlib.patches import Patch
    legend = [Patch(color=c, label=r) for r, c in cores_regiao.items()]
    ax.legend(handles=legend + [plt.Line2D([0], [0], color="#888", linestyle="--", label=f"R² = {r2:.3f}")],
              loc="upper right", fontsize=9)

    plt.tight_layout()
    filepath = OUTPUTS_DIR / "regressao_pib_educacao.png"
    fig.savefig(filepath, dpi=150)
    plt.close(fig)
    logger.info(f"Salvo: {filepath}")


def feature_importance(df: pd.DataFrame) -> None:
    """Random Forest: importância das variáveis para alunos/docente."""
    features = ["pib_per_capita", "populacao", "matriculas", "escolas", "pib_mil_reais"]
    X = df[features].values
    y = df["alunos_por_docente"].values

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    y_pred = model.predict(X)

    r2 = r2_score(y, y_pred)
    mae = mean_absolute_error(y, y_pred)
    logger.info(f"Random Forest: R² = {r2:.3f}, MAE = {mae:.2f}")

    importances = pd.DataFrame({
        "variavel": features,
        "importancia": model.feature_importances_
    }).sort_values("importancia", ascending=True)

    logger.info("Importância das variáveis:")
    for _, row in importances.iterrows():
        bar = "█" * int(row["importancia"] * 50)
        logger.info(f"  {row['variavel']:20s} {row['importancia']:.3f} {bar}")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(importances["variavel"], importances["importancia"], color="#534AB7")
    ax.set_xlabel("Importância")
    ax.set_title("Importância das variáveis — Random Forest", fontsize=14, fontweight="bold")

    plt.tight_layout()
    filepath = OUTPUTS_DIR / "feature_importance.png"
    fig.savefig(filepath, dpi=150)
    plt.close(fig)
    logger.info(f"Salvo: {filepath}")


def clustering_analysis(df: pd.DataFrame) -> None:
    """K-Means: agrupa estados por perfil socioeducacional."""
    features = ["pib_per_capita", "alunos_por_docente", "matriculas_por_mil_hab"]
    X = df[features].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(X_scaled)

    cluster_names = {}
    for c in range(3):
        cluster_df = df[df["cluster"] == c]
        avg_pib = cluster_df["pib_per_capita"].mean()
        if avg_pib > 50000:
            cluster_names[c] = "Alto desenvolvimento"
        elif avg_pib > 30000:
            cluster_names[c] = "Desenvolvimento intermediário"
        else:
            cluster_names[c] = "Em desenvolvimento"

    df["perfil"] = df["cluster"].map(cluster_names)

    logger.info("Clusters identificados:")
    for perfil in sorted(df["perfil"].unique()):
        estados = df[df["perfil"] == perfil]["uf_sigla"].tolist()
        avg_pib = df[df["perfil"] == perfil]["pib_per_capita"].mean()
        avg_alunos = df[df["perfil"] == perfil]["alunos_por_docente"].mean()
        logger.info(f"  {perfil}:")
        logger.info(f"    Estados: {', '.join(estados)}")
        logger.info(f"    PIB per capita médio: R$ {avg_pib:,.0f}")
        logger.info(f"    Alunos/docente médio: {avg_alunos:.1f}")

    cores_cluster = {
        "Alto desenvolvimento": "#534AB7",
        "Desenvolvimento intermediário": "#BA7517",
        "Em desenvolvimento": "#D85A30",
    }

    fig, ax = plt.subplots(figsize=(10, 7))
    for perfil, cor in cores_cluster.items():
        mask = df["perfil"] == perfil
        ax.scatter(df.loc[mask, "pib_per_capita"], df.loc[mask, "alunos_por_docente"],
                   c=cor, s=100, label=perfil, zorder=3)

    for _, row in df.iterrows():
        ax.annotate(row["uf_sigla"], (row["pib_per_capita"], row["alunos_por_docente"]),
                     fontsize=8, ha="left", va="bottom", xytext=(4, 4),
                     textcoords="offset points")

    ax.set_xlabel("PIB per capita (R$)")
    ax.set_ylabel("Alunos por docente")
    ax.set_title("Clustering de estados por perfil socioeducacional", fontsize=14, fontweight="bold")
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"R$ {x:,.0f}"))
    ax.legend(fontsize=10)

    plt.tight_layout()
    filepath = OUTPUTS_DIR / "clustering_estados.png"
    fig.savefig(filepath, dpi=150)
    plt.close(fig)
    logger.info(f"Salvo: {filepath}")

    # Salvar CSV com clusters
    output = df[["uf_sigla", "uf_nome", "regiao_nome", "pib_per_capita",
                  "alunos_por_docente", "matriculas_por_mil_hab", "perfil"]]
    filepath_csv = ANALYTICS_DIR / "clusters_estados.csv"
    output.to_csv(filepath_csv, index=False)
    logger.info(f"Salvo: {filepath_csv}")


if __name__ == "__main__":
    run_ml_models()