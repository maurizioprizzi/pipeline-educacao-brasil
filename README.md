# Pipeline de Dados — Educação Pública no Brasil

Pipeline completa de engenharia e análise de dados sobre educação
pública brasileira, construída com ferramentas open source no Linux.

## Sobre o Projeto

Este projeto constrói uma pipeline end-to-end que coleta, armazena,
transforma, analisa e visualiza indicadores de educação pública no
Brasil — cruzando dados do IBGE, INEP e dados.gov.br.

Perguntas que o projeto responde:

- Como a taxa de alfabetização evoluiu por região?
- Existe correlação entre IDH municipal e desempenho no IDEB?
- Quais estados investem mais por aluno e qual o retorno?

## Stack Técnico

- **Python 3.12** — linguagem principal
- **DuckDB** — banco analítico local (OLAP, colunar, zero config)
- **pandas** — transformação de dados
- **matplotlib + plotly** — visualizações
- **Makefile + cron** — orquestração
- **pytest** — testes automatizados
- **GitHub Actions** — CI/CD

## Estrutura do Projeto
```
pipeline-educacao-brasil/
├── data/
│   ├── raw/                # Dados brutos (não versionados)
│   ├── processed/          # Dados limpos e transformados
│   └── analytics/          # Tabelas analíticas finais
├── src/
│   ├── ingestion/          # Scripts de coleta
│   ├── transformation/     # Limpeza e transformação
│   ├── analysis/           # Queries analíticas
│   └── visualization/      # Gráficos e dashboards
├── tests/                  # Testes automatizados
├── docs/                   # Documentação e decisões
├── Makefile                # Orquestrador principal
└── requirements.txt        # Dependências Python
```

## Como Executar
```bash
git clone https://github.com/maurizioprizzi/pipeline-educacao-brasil.git
cd pipeline-educacao-brasil

# Setup completo
make setup

# Pipeline completa
make run

# Ver comandos disponíveis
make help
```

## Evolução do Projeto

| Dia | Etapa                    | Status |
|-----|--------------------------|--------|
| 1   | Setup e estrutura        | ✅      |
| 2   | Ingestão de dados        | ✅      |
| 3   | Armazenamento (DuckDB)   | ✅      |
| 4   | Limpeza e transformação  | ✅      |
| 5   | Análise exploratória     | 🔲      |
| 6   | Visualização             | 🔲      |
| 7   | Orquestração             | 🔲      |
| 8   | Testes e CI              | 🔲      |
| 9   | Documentação final       | 🔲      |

## Fontes de Dados

- **IBGE** — Censo, PNAD, indicadores socioeconômicos
- **INEP** — IDEB, Censo Escolar, matrículas
- **dados.gov.br** — Portal de dados abertos do governo federal

## Licença

MIT