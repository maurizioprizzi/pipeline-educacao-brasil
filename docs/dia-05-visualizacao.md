# Dia 5 — Visualizações

## O que foi feito

- Gráfico de barras horizontais — PIB per capita por UF (matplotlib)
- Gráfico de pizza — distribuição do PIB por região (matplotlib)
- Scatter plot interativo — População vs PIB per capita (plotly)
- Paleta de cores consistente por região em todos os gráficos

## Arquivos gerados

| Arquivo | Tipo | Descrição |
|---------|------|-----------|
| pib_per_capita_uf.png | Estático | Ranking das 27 UFs por PIB per capita |
| pib_por_regiao.png | Estático | Pizza com percentual do PIB por região |
| scatter_pop_pib.html | Interativo | Bolhas de população vs PIB per capita |

## Decisões técnicas

### Dois tipos de output

Gráficos estáticos (PNG) são bons para README, apresentações
e LinkedIn. O gráfico interativo (HTML) mostra domínio de
plotly e pode ser aberto no navegador com hover e zoom.

### Paleta de cores por região

Definimos um dicionário de cores fixo (CORES_REGIAO) usado
em todos os gráficos. Isso mantém consistência visual e
facilita a leitura quando alguém vê múltiplos gráficos.

### Separação dados vs visualização

Os gráficos leem os CSVs de data/analytics/, não acessam
o DuckDB diretamente. Cada etapa da pipeline depende apenas
da saída da etapa anterior — nunca pula camadas.

## Próximo passo

Dia 6: Orquestração e automação da pipeline.