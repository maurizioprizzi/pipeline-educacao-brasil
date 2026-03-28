# Dia 9 — Testes de Qualidade de Dados

## O que foi feito

- 16 novos testes de qualidade de dados
- 27 testes totais passando (16 dados + 11 estrutura)
- 3 categorias: completude, integridade, regras de negócio

## Testes criados

### Completude (4 testes)
- 27 estados em todas as tabelas base
- 5 regiões no resumo regional

### Integridade (5 testes)
- Sem população nula
- Sem PIB nulo
- Sem matrículas nulas ou zero
- Sem docentes nulos ou zero
- Sem estados duplicados

### Regras de negócio (7 testes)
- População sempre positiva
- PIB sempre positivo
- Matrículas nunca excedem a população
- Docentes nunca excedem as matrículas
- Alunos por docente entre 5 e 50
- Percentuais de população somam 100%
- Percentuais de PIB somam 100%

## Decisões técnicas

### Testes de dados vs testes de código

A maioria dos projetos testa apenas se o código roda.
Testes de qualidade de dados validam se os resultados
fazem sentido — é a diferença entre "o script rodou"
e "os dados estão corretos".

### Fixture com conexão read-only

Os testes usam uma conexão DuckDB em modo leitura.
Isso garante que nenhum teste pode alterar os dados
acidentalmente.

### Ranges razoáveis

O teste de alunos por docente valida que o valor está
entre 5 e 50. Valores fora desse range indicariam erro
de dados — nenhum estado brasileiro tem menos de 5 ou
mais de 50 alunos por professor.

## Próximo passo

Dia 10: Orquestração com cron, idempotência e logging.