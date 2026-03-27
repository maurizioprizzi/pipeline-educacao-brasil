"""
Extrai dados da Sinopse Estatística do Censo Escolar (INEP).

Lê o XLSX e extrai matrículas, docentes e escolas agregados por UF.
"""

import glob

import openpyxl
import pandas as pd

from src.config import RAW_DIR
from src.logger import get_logger

logger = get_logger(__name__)

XLSX_PATTERN = "data/external/sinopse_estatistica_censo_escolar_2023/*.xlsx"


def _find_xlsx() -> str:
    """Localiza o arquivo XLSX da sinopse."""
    files = glob.glob(XLSX_PATTERN)
    if not files:
        raise FileNotFoundError(
            f"XLSX não encontrado em {XLSX_PATTERN}. "
            "Rode: wget -O data/external/sinopse_2023.zip "
            "'https://download.inep.gov.br/dados_abertos/sinopses_estatisticas/"
            "sinopses_estatisticas_censo_escolar_2023.zip' && "
            "unzip data/external/sinopse_2023.zip -d data/external/"
        )
    return files[0]


def _is_uf_row(row) -> bool:
    """Verifica se a linha é uma agregação por UF (não município)."""
    regiao = str(row[0]).strip() if row[0] else ""
    uf = str(row[1]).strip() if row[1] else ""
    municipio = str(row[2]).strip() if row[2] else ""
    codigo = str(row[3]).strip() if row[3] else ""

    return (
        regiao != ""
        and uf != ""
        and municipio == ""
        and codigo == ""
        and regiao != "Brasil"
    )


def extract_sheet(wb, sheet_name: str, coluna_valor: str) -> pd.DataFrame:
    """Extrai dados de uma aba, filtrando só as linhas de UF."""
    ws = wb[sheet_name]
    rows = []

    for row in ws.iter_rows(min_row=12, max_col=5, values_only=True):
        if _is_uf_row(row):
            valor = row[4]
            try:
                valor = int(valor) if valor else 0
            except (ValueError, TypeError):
                valor = 0

            rows.append({
                "regiao_nome": str(row[0]).strip(),
                "uf_nome": str(row[1]).strip(),
                coluna_valor: valor,
            })

    df = pd.DataFrame(rows)
    logger.info(f"[{sheet_name}] {len(df)} UFs extraídas — coluna: {coluna_valor}")
    return df


def run_inep_extraction():
    """Extrai matrículas, docentes e escolas do XLSX do INEP."""
    xlsx_path = _find_xlsx()
    logger.info(f"Abrindo {xlsx_path}...")

    wb = openpyxl.load_workbook(xlsx_path, read_only=True)

    df_matriculas = extract_sheet(wb, "Educação Básica 1.1", "matriculas")
    df_docentes = extract_sheet(wb, "Educação Básica 2.1", "docentes")
    df_escolas = extract_sheet(wb, "Educação Básica 3.1", "escolas")

    wb.close()

    # Juntar tudo em uma tabela só
    df = df_matriculas.merge(df_docentes, on=["regiao_nome", "uf_nome"])
    df = df.merge(df_escolas, on=["regiao_nome", "uf_nome"])
    df["ano"] = 2023
    df["fonte"] = "INEP/Censo Escolar"

    # Salvar
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    filepath = RAW_DIR / "inep_censo_escolar_2023.json"
    df.to_json(filepath, orient="records", force_ascii=False, indent=2)
    logger.info(f"Salvo: {filepath} — {len(df)} registros")

    # Preview
    logger.info(f"\n{df.to_string(index=False)}")

    return df


if __name__ == "__main__":
    run_inep_extraction()