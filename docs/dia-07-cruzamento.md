# Dia 7 — Cruzamento IBGE + INEP no DuckDB

## O que foi feito

- Tabela educacao carregada no DuckDB (matrículas, docentes, escolas)
- JOIN entre 4 tabelas (estados, populacao, pib, educacao)
- Métricas derivadas: alunos/docente, alunos/escola, matrículas/mil hab
- Resumo regional com indicadores educacionais

## Indicadores criados

| Métrica | Descrição | Exemplo |
|---------|-----------|---------|
| alunos_por_docente | Matrículas / docentes | PA: 25.7 |
| alunos_por_escola | Matrículas / escolas | RO: 322.0 |
| matriculas_por_mil_hab | Matrículas * 1000 / população | AC: 280.0 |
| escolas_por_100k_hab | Escolas * 100000 / população | AC: 167.2 |
| pib_por_matricula | PIB * 1000 / matrículas | DF: R$ 449k |

## Decisões técnicas

### JOIN por nome da UF

Os dados do IBGE usam uf_id numérico, o INEP usa uf_nome.
O JOIN é feito por nome (e.uf_nome = ed.uf_nome). Uma
alternativa seria criar uma tabela de-para, mas como ambas
as fontes usam os mesmos nomes oficiais, o JOIN direto
funciona sem ambiguidade.

### Métricas calculadas no SQL

Todas as métricas derivadas são calculadas no SQL do DuckDB
usando window functions, não no pandas. Isso mantém a
transformação declarativa e auditável.

## Insights encontrados

- PA tem 25.7 alunos por docente — o maior do país
- Sul tem a melhor proporção: 17.7 alunos por docente
- Nordeste investe R$ 90 mil por matrícula, Centro-Oeste R$ 253 mil

## Próximo passo

Dia 8: Visualizações avançadas com os dados cruzados.