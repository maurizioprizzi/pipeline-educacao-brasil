# Pipeline de Dados — Educação Pública no Brasil

Pipeline completa de engenharia e análise de dados sobre educação
pública brasileira, construída com ferramentas open source no Linux.

## Sobre o Projeto

Este projeto constrói uma pipeline end-to-end que coleta, armazena,
transforma, analisa e visualiza indicadores de educação pública no
Brasil — cruzando dados do IBGE e INEP com informações socioeconômicas.

Perguntas que o projeto responde:

- Como o PIB per capita se distribui entre estados e regiões?
- Qual a relação entre riqueza econômica e infraestrutura educacional?
- Quais regiões concentram mais matrículas, escolas e docentes por habitante?

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

| Dia | Etapa                                    | Status |
|-----|------------------------------------------|--------|
| 1   | Setup e estrutura                        | ✅      |
| 2   | Ingestão de dados (IBGE)                 | ✅      |
| 3   | Armazenamento (DuckDB)                   | ✅      |
| 4   | Tabelas analíticas e métricas derivadas  | ✅      |
| 5   | Visualizações (matplotlib + plotly)      | ✅      |
| 6   | Novas fontes de dados (INEP)             | 🔲      |
| 7   | Limpeza de dados sujos e transformação   | 🔲      |
| 8   | Cruzamentos complexos e análise avançada | 🔲      |
| 9   | Visualizações avançadas                  | 🔲      |
| 10  | Testes de qualidade de dados + CI        | 🔲      |
| 11  | Orquestração (cron, idempotência, logs)  | 🔲      |
| 12  | Documentação final e README vitrine      | 🔲      |

## Fontes de Dados

- **IBGE** — População, PIB, indicadores socioeconômicos por UF
- **INEP** — Censo Escolar, matrículas, escolas, docentes

## Licença

MIT