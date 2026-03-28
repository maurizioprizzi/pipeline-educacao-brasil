"""
Testes de qualidade de dados.

Valida integridade, consistência e regras de negócio
dos dados carregados no DuckDB.
"""

import duckdb
import pytest

from src.config import DUCKDB_PATH


@pytest.fixture
def conn():
    """Conexão com o DuckDB para os testes."""
    c = duckdb.connect(str(DUCKDB_PATH), read_only=True)
    yield c
    c.close()


class TestDataCompleteness:
    """Valida que os dados estão completos."""

    def test_all_27_states_in_estados(self, conn):
        count = conn.execute("SELECT COUNT(*) FROM estados").fetchone()[0]
        assert count == 27, f"Esperado 27 estados, encontrado {count}"

    def test_all_27_states_in_populacao(self, conn):
        count = conn.execute("SELECT COUNT(*) FROM populacao").fetchone()[0]
        assert count == 27, f"Esperado 27 registros, encontrado {count}"

    def test_all_27_states_in_educacao(self, conn):
        count = conn.execute("SELECT COUNT(*) FROM educacao").fetchone()[0]
        assert count == 27, f"Esperado 27 registros, encontrado {count}"

    def test_all_5_regions_in_resumo(self, conn):
        count = conn.execute("SELECT COUNT(*) FROM resumo_regional").fetchone()[0]
        assert count == 5, f"Esperado 5 regiões, encontrado {count}"


class TestDataIntegrity:
    """Valida que não há dados nulos ou inválidos."""

    def test_no_null_population(self, conn):
        nulls = conn.execute(
            "SELECT COUNT(*) FROM populacao WHERE populacao IS NULL"
        ).fetchone()[0]
        assert nulls == 0, f"{nulls} registros com população nula"

    def test_no_null_pib(self, conn):
        nulls = conn.execute(
            "SELECT COUNT(*) FROM pib WHERE pib_mil_reais IS NULL"
        ).fetchone()[0]
        assert nulls == 0, f"{nulls} registros com PIB nulo"

    def test_no_null_matriculas(self, conn):
        nulls = conn.execute(
            "SELECT COUNT(*) FROM educacao WHERE matriculas IS NULL OR matriculas = 0"
        ).fetchone()[0]
        assert nulls == 0, f"{nulls} estados sem matrículas"

    def test_no_null_docentes(self, conn):
        nulls = conn.execute(
            "SELECT COUNT(*) FROM educacao WHERE docentes IS NULL OR docentes = 0"
        ).fetchone()[0]
        assert nulls == 0, f"{nulls} estados sem docentes"

    def test_no_duplicate_states(self, conn):
        dupes = conn.execute("""
            SELECT uf_sigla, COUNT(*) as n
            FROM estados GROUP BY uf_sigla HAVING n > 1
        """).fetchall()
        assert len(dupes) == 0, f"Estados duplicados: {dupes}"


class TestBusinessRules:
    """Valida regras de negócio e consistência dos dados."""

    def test_population_is_positive(self, conn):
        invalid = conn.execute(
            "SELECT COUNT(*) FROM populacao WHERE populacao <= 0"
        ).fetchone()[0]
        assert invalid == 0, f"{invalid} estados com população negativa ou zero"

    def test_pib_is_positive(self, conn):
        invalid = conn.execute(
            "SELECT COUNT(*) FROM pib WHERE pib_mil_reais <= 0"
        ).fetchone()[0]
        assert invalid == 0, f"{invalid} estados com PIB negativo ou zero"

    def test_matriculas_less_than_population(self, conn):
        invalid = conn.execute("""
            SELECT COUNT(*) FROM visao_geral_uf
            WHERE matriculas > populacao
        """).fetchone()[0]
        assert invalid == 0, f"{invalid} estados com mais matrículas que habitantes"

    def test_docentes_less_than_matriculas(self, conn):
        invalid = conn.execute("""
            SELECT COUNT(*) FROM educacao
            WHERE docentes > matriculas
        """).fetchone()[0]
        assert invalid == 0, f"{invalid} estados com mais docentes que alunos"

    def test_alunos_por_docente_reasonable(self, conn):
        invalid = conn.execute("""
            SELECT COUNT(*) FROM visao_geral_uf
            WHERE alunos_por_docente < 5 OR alunos_por_docente > 50
        """).fetchone()[0]
        assert invalid == 0, f"{invalid} estados com razão alunos/docente fora de [5, 50]"

    def test_pct_populacao_sums_to_100(self, conn):
        total = conn.execute(
            "SELECT ROUND(SUM(pct_populacao), 0) FROM visao_geral_uf"
        ).fetchone()[0]
        assert total == 100, f"Soma dos percentuais de população = {total}, esperado 100"

    def test_pct_pib_sums_to_100(self, conn):
        total = conn.execute(
            "SELECT ROUND(SUM(pct_pib), 0) FROM visao_geral_uf"
        ).fetchone()[0]
        assert total == 100, f"Soma dos percentuais de PIB = {total}, esperado 100"