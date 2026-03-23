# Dia 3 — Armazenamento com DuckDB

## O que foi feito

- Parsers para transformar JSONs aninhados do IBGE em tabelas planas
- Carga no DuckDB com criação automática de tabelas
- Primeira query cruzando estados, população e PIB

## Tabelas criadas

| Tabela | Registros | Colunas |
|--------|-----------|---------|
| estados | 27 | uf_id, uf_sigla, uf_nome, regiao_sigla, regiao_nome |
| populacao | 27 | uf_id, uf_nome, ano, populacao |
| pib | 27 | uf_id, uf_nome, ano, pib_mil_reais |

## Decisões técnicas

### Parser genérico para agregados

A API do IBGE usa a mesma estrutura para todos os endpoints
de agregados (população, PIB, alfabetização). O parse_agregado()
recebe o nome da coluna como parâmetro e funciona para qualquer
endpoint — quando adicionarmos novas fontes, basta uma linha.

### DuckDB em vez de CSVs intermediários

Poderíamos salvar os DataFrames como CSV em data/processed/.
Mas o DuckDB permite queries SQL diretamente, JOINs entre
tabelas, e é mais rápido que ler CSVs toda vez. O banco é
um arquivo só (educacao.duckdb) e não precisa de servidor.

### CREATE TABLE AS SELECT

Usamos a integração nativa DuckDB + pandas: passamos o
DataFrame direto no SQL sem precisar inserir linha por linha.
Isso é muito mais rápido e limpo.

## Próximo passo

Dia 4: Limpeza, validação e criação de tabelas analíticas.