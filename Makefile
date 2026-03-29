.PHONY: setup run ingest transform analyze visualize test check-data clean help

# ============================================================================
# Pipeline de Dados — Educação Pública no Brasil
# ============================================================================

PYTHON := .venv/bin/python
PIP := .venv/bin/pip
PYTEST := .venv/bin/pytest
VENV := .venv

# ----------------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------------

help: ## Mostra esta ajuda
	@echo ""
	@echo "Pipeline de Dados — Educação Pública no Brasil"
	@echo "================================================"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'
	@echo ""

setup: $(VENV)/bin/activate ## Cria venv e instala dependências
	@echo "✓ Ambiente configurado com sucesso"

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	touch $(VENV)/bin/activate

# ----------------------------------------------------------------------------
# Pipeline
# ----------------------------------------------------------------------------

run: setup ## Executa pipeline completa
	$(PYTHON) -m scripts.run_pipeline

ingest: setup ## Baixa dados das fontes públicas
	@echo "→ Ingestão de dados..."
	$(PYTHON) -m src.ingestion.run
	@echo "✓ Ingestão concluída"

transform: setup ## Limpa e transforma os dados
	@echo "→ Transformação de dados..."
	$(PYTHON) -m src.transformation.run
	@echo "✓ Transformação concluída"

analyze: setup ## Executa análises exploratórias
	@echo "→ Análise exploratória..."
	$(PYTHON) -m src.analysis.run
	@echo "✓ Análise concluída"

visualize: setup ## Gera gráficos e dashboards
	@echo "→ Gerando visualizações..."
	$(PYTHON) -m src.visualization.run
	@echo "✓ Visualizações geradas"

# ----------------------------------------------------------------------------
# Qualidade
# ----------------------------------------------------------------------------

test: setup ## Roda testes automatizados
	$(PYTEST) tests/ -v --tb=short

check-data: setup ## Valida integridade dos dados
	$(PYTHON) -m src.transformation.validate
	@echo "✓ Dados validados"

# ----------------------------------------------------------------------------
# Utilitários
# ----------------------------------------------------------------------------

clean: ## Remove artefatos gerados
	@echo "→ Limpando artefatos..."
	rm -rf data/raw/* data/processed/* data/analytics/* outputs/*
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✓ Limpeza concluída"

clean-all: clean ## Remove tudo (inclui venv)
	rm -rf $(VENV)
	@echo "✓ Limpeza total concluída"