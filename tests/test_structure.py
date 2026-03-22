"""
Testes de estrutura do projeto.

Valida que diretórios e configurações essenciais existem.
"""

from pathlib import Path

import pytest

from src.config import ROOT_DIR, RAW_DIR, PROCESSED_DIR, ANALYTICS_DIR, OUTPUTS_DIR, SOURCES


class TestProjectStructure:
    """Valida a estrutura de diretórios do projeto."""

    @pytest.mark.parametrize(
        "directory",
        [RAW_DIR, PROCESSED_DIR, ANALYTICS_DIR, OUTPUTS_DIR],
        ids=["raw", "processed", "analytics", "outputs"],
    )
    def test_data_directories_exist(self, directory: Path):
        assert directory.exists(), f"Diretório não encontrado: {directory}"
        assert directory.is_dir(), f"Não é um diretório: {directory}"

    @pytest.mark.parametrize(
        "module",
        ["src/ingestion", "src/transformation", "src/analysis", "src/visualization"],
    )
    def test_source_modules_exist(self, module: str):
        module_path = ROOT_DIR / module
        init_path = module_path / "__init__.py"
        assert module_path.exists(), f"Módulo não encontrado: {module}"
        assert init_path.exists(), f"__init__.py ausente em: {module}"


class TestConfig:
    """Valida que as configurações estão corretas."""

    def test_sources_not_empty(self):
        assert len(SOURCES) > 0, "Nenhuma fonte de dados configurada"

    def test_sources_have_required_keys(self):
        required_keys = {"url", "description", "format"}
        for name, source in SOURCES.items():
            missing = required_keys - set(source.keys())
            assert not missing, f"Fonte '{name}' sem chaves: {missing}"

    def test_sources_urls_are_https(self):
        for name, source in SOURCES.items():
            assert source["url"].startswith("https://"), (
                f"Fonte '{name}' não usa HTTPS"
            )