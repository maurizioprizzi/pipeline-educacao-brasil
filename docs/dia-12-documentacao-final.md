# Dia 12 — Documentação Final

## O que foi feito

- README vitrine com 7 gráficos visíveis no GitHub
- Seção de principais achados validados contra o banco
- Instruções completas de execução (incluindo INEP)
- Estrutura do projeto atualizada
- Todos os 12 dias marcados como concluídos
- Dados do README conferidos via query no DuckDB antes de publicar

## Validação dos dados publicados

Antes de montar o README final, rodamos a pipeline do zero
(make run), os 27 testes (make test), e queries de conferência
no DuckDB para garantir que cada número no texto bate com
os dados reais.

| Dado | Valor confirmado | Fonte |
|------|-----------------|-------|
| Maior alunos/docente | PA = 25.7 | visao_geral_uf |
| Menor alunos/docente | PR = 16.9 | visao_geral_uf |
| Maior PIB/matrícula | DF = R$ 449.701 | visao_geral_uf |
| Menor PIB/matrícula | MA = R$ 65.077 | visao_geral_uf |
| Nordeste % população | 27.03% | visao_geral_uf |
| Nordeste % PIB | 13.8% | visao_geral_uf |
| Total matrículas | 47.304.632 | educacao |
| Total docentes | 2.361.574 | educacao |
| Total escolas | 178.476 | educacao |

## Decisões técnicas

### Gráficos versionados no Git

Os PNGs foram incluídos no repositório para que apareçam
renderizados direto no README do GitHub. Os HTMLs interativos
(plotly) continuam fora do Git por serem grandes. Qualquer
pessoa pode gerá-los rodando make visualize.

### Validação antes de publicação

Profissionais de dados validam antes de publicar. Rodamos
make run + make test + queries manuais antes de escrever
o README final. Um número errado no README destruiria a
credibilidade do projeto inteiro.

### README como vitrine

O README é a primeira coisa que um recrutador, jornalista
ou potencial cliente vê. Por isso priorizamos: achados no
topo, gráficos visíveis sem clicar, instruções de execução
claras, e a tabela de evolução mostrando o processo completo.

## Resumo do projeto completo

| Métrica | Valor |
|---------|-------|
| Dias de desenvolvimento | 12 |
| Fontes de dados | 2 (IBGE + INEP) |
| Tabelas no DuckDB | 6 |
| Gráficos gerados | 7 estáticos + 2 interativos |
| Modelos de ML | 3 (regressão, RF, K-Means) |
| Testes automatizados | 27 |
| Pipeline completa | 15 segundos |
| Custo de licença | R$ 0 |