# Dia 11 — Machine Learning

## O que foi feito

- Regressão Linear: PIB per capita como preditor de alunos/docente
- Random Forest: importância de variáveis para qualidade educacional
- K-Means Clustering: agrupamento de estados por perfil socioeducacional
- 3 gráficos e 1 CSV de clusters exportado

## Resultados

### Regressão Linear

| Métrica | Valor |
|---------|-------|
| R² | 0.037 |
| MAE | 2.12 |
| Coeficiente | -0.000026 |

O PIB per capita sozinho explica apenas 3.7% da variação no
número de alunos por docente. A relação existe (mais PIB = menos
alunos por docente) mas é fraca. Isso é um achado legítimo:
o problema educacional é mais complexo do que só dinheiro.

### Random Forest

| Métrica | Valor |
|---------|-------|
| R² | 0.834 |
| MAE | 0.79 |

Quando usamos todas as variáveis, o modelo explica 83% da
variação. A variável mais importante é o PIB per capita (47%),
seguida do PIB total (21%) e número de escolas (16%).

### Clustering (K-Means)

| Perfil | Estados | PIB per capita médio | Alunos/docente |
|--------|---------|---------------------|----------------|
| Alto desenvolvimento | DF, MT, SC, SP, RJ, RS, MS, PR, ES, MG | R$ 56.283 | 19.4 |
| Em desenvolvimento | GO, TO, RO, AM, PA, RR, AC, BA, AP, PE, AL, RN, SE, CE, PI, PB, MA | R$ 25.154 | 21.7 |

O algoritmo identificou 2 perfis claros: 10 estados do
Sul/Sudeste/Centro-Oeste com alto desenvolvimento, e 17 estados
do Norte/Nordeste com indicadores mais baixos.

## Decisões técnicas

### Regressão linear como baseline

Começamos com o modelo mais simples possível. O R² baixo
não é falha — é informação. Mostra que uma variável sozinha
não explica o fenômeno, o que justifica usar modelos mais
complexos.

### Random Forest para interpretabilidade

Escolhemos Random Forest em vez de redes neurais porque
com 27 observações, modelos complexos fariam overfitting.
O Random Forest é robusto com poucos dados e fornece
importância de variáveis nativamente.

### StandardScaler antes do clustering

K-Means é sensível à escala das variáveis. PIB per capita
está na casa dos milhares, alunos por docente na casa das
dezenas. Sem normalização, o PIB dominaria a distância
euclidiana e o clustering ignoraria as outras variáveis.

### 3 clusters reduzidos a 2

O K-Means foi configurado com k=3, mas o grupo intermediário
não emergiu com clareza nos dados — os 27 estados se
dividiram naturalmente em 2 grupos. Isso é consistente com
a conhecida divisão socioeconômica do Brasil.

## Arquivos gerados

| Arquivo | Descrição |
|---------|-----------|
| regressao_pib_educacao.png | Scatter com linha de regressão |
| feature_importance.png | Barras de importância (Random Forest) |
| clustering_estados.png | Scatter colorido por cluster |
| clusters_estados.csv | Tabela com perfil de cada UF |

## Próximo passo

Dia 12: Documentação final, gráficos no README, post LinkedIn.