# Dia 8 — Visualizações Avançadas

## O que foi feito

- 3 novos gráficos cruzando dados IBGE + INEP
- Total de 6 gráficos gerados automaticamente
- Paleta de cores consistente em todos os gráficos

## Gráficos gerados

| Arquivo | Tipo | Descrição |
|---------|------|-----------|
| pib_per_capita_uf.png | Estático | PIB per capita por UF |
| pib_por_regiao.png | Estático | Distribuição do PIB por região |
| scatter_pop_pib.html | Interativo | População vs PIB per capita |
| alunos_por_docente_uf.png | Estático | Alunos por docente por UF com média |
| pib_por_matricula_uf.png | Estático | PIB por matrícula por UF |
| scatter_pib_educacao.html | Interativo | PIB per capita vs alunos por docente |

## Decisões técnicas

### Linha de média no gráfico

O gráfico de alunos por docente inclui uma linha tracejada
com a média nacional. Isso dá contexto imediato — o leitor
vê quais estados estão acima ou abaixo da média sem precisar
calcular mentalmente.

### Scatter com tamanho das bolhas

No scatter PIB vs educação, o tamanho das bolhas representa
o número de matrículas. Isso adiciona uma terceira dimensão
ao gráfico sem poluir visualmente.

## Próximo passo

Dia 9: Testes de qualidade de dados.