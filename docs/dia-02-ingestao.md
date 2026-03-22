# Dia 2 — Ingestão de Dados

## O que foi feito

- Exploração dos endpoints da API do IBGE
- Testes de disponibilidade em 5 endpoints
- Script de ingestão com retry e tratamento de erros
- Salvamento dos dados brutos em data/raw/ como JSON

## Fontes validadas

| Endpoint | Dados | Status |
|----------|-------|--------|
| /localidades/estados | Lista de UFs com região | OK |
| /agregados/6579 | População estimada por UF | OK |
| /agregados/5938 | PIB por UF | OK |
| /agregados/7128 | Taxa de alfabetização | Instável (500) |
| /agregados/5803 | IDEB | Instável (500) |

## Decisões técnicas

### Retry com backoff progressivo

A API do IBGE é instável — dois dos cinco endpoints testados
retornaram erro 500. O script faz até 3 tentativas com espera
crescente (2s, 4s) entre elas. Se falhar, loga o erro e segue
para a próxima fonte sem derrubar a pipeline inteira.

### JSON bruto sem transformação

Os dados são salvos exatamente como vieram da API. Nenhuma
limpeza ou transformação acontece nesta etapa. Isso garante
que temos sempre o dado original para reprocessar se a lógica
de transformação mudar depois.

### Logging em vez de print

Toda a ingestão usa o módulo de logging centralizado. Cada
request logado com timestamp, nome da fonte e resultado.
Isso facilita debug em produção e mostra profissionalismo.

## Arquivos criados

- src/ingestion/extract.py — lógica de fetch + retry + save
- src/ingestion/run.py — ponto de entrada (chamado pelo Makefile)

## Próximo passo

Dia 3: Carregar os JSONs brutos no DuckDB e modelar o schema.