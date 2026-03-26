# Dia 4 — Tabelas Analíticas

## O que foi feito

- Tabela visao_geral_uf cruzando estados, população e PIB
- Colunas calculadas: PIB per capita, percentuais, ranking
- Tabela resumo_regional agregando por região
- Exportação em CSV para data/analytics/

## Tabelas criadas

| Tabela | Registros | Descrição |
|--------|-----------|-----------|
| visao_geral_uf | 27 | Cada UF com população, PIB e métricas derivadas |
| resumo_regional | 5 | Agregação por região geográfica |

## Decisões técnicas

### Window functions no SQL

Usamos RANK(), SUM() OVER() e percentuais calculados direto
no SQL do DuckDB. Isso é mais eficiente do que calcular no
pandas e mostra domínio de SQL analítico — uma skill que
recrutadores valorizam muito.

### Exportação em CSV

Além de manter as tabelas no DuckDB, exportamos CSVs em
data/analytics/. Isso permite que alguém use os dados sem
precisar instalar DuckDB, e facilita a visualização no
próximo dia.

### Separação de responsabilidades

O módulo build_analytics.py contém apenas SQL e lógica de
criação de tabelas. Não tem visualização nem formatação de
saída — cada etapa da pipeline faz uma coisa só.

## Insights encontrados

- DF lidera o PIB per capita (R$ 92 mil) por ser sede do governo
- Centro-Oeste é a região mais rica per capita (agronegócio)
- Nordeste tem PIB per capita de R$ 21 mil — menos da metade do Sudeste

## Próximo passo

Dia 5: Visualizações com matplotlib e plotly.