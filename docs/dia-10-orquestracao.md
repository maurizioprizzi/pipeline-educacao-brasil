# Dia 10 — Orquestração

## O que foi feito

- Script run_pipeline.py que orquestra 5 etapas de ponta a ponta
- Logger atualizado para escrever em terminal e arquivo
- make run executa a pipeline completa com um comando
- Timing por etapa e relatório final

## Resultado da execução

| Etapa | Tempo |
|-------|-------|
| Ingestão IBGE | 0.9s |
| Ingestão INEP | 2.9s |
| Transformação e carga | 0.1s |
| Análise | 0.1s |
| Visualização | 2.1s |
| Total | 6.2s |

## Decisões técnicas

### Orquestrador Python em vez de shell script

O run_pipeline.py importa e chama cada módulo diretamente,
em vez de chamar subprocessos. Isso permite capturar exceções,
medir tempo por etapa, e gerar um relatório final estruturado.
Um shell script não teria essa granularidade.

### Logging em arquivo

O logger agora escreve tanto no terminal quanto em
logs/pipeline.log. Em produção, isso permite auditoria e
debug sem precisar estar olhando o terminal. O arquivo de
log não é versionado (está no .gitignore).

### Idempotência

A pipeline pode rodar várias vezes sem efeitos colaterais.
Cada etapa sobrescreve os dados anteriores (DROP TABLE IF
EXISTS + CREATE TABLE). Não há acúmulo de dados duplicados.

### Tratamento de falhas

Se uma etapa falha, o pipeline loga o erro e continua para
as próximas. No final, reporta quais etapas falharam e
retorna exit code 1. Isso permite uso em cron ou CI — se
falhar, o cron pode enviar alerta.

## Próximo passo

Dia 11: Machine Learning (regressão, random forest, clustering).