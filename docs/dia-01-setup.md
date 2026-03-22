# Dia 1 — Setup do Projeto

## O que foi feito

- Estrutura de diretórios seguindo convenções de projetos de dados
- Makefile como orquestrador central da pipeline
- Configuração centralizada (src/config.py) com caminhos e fontes
- Logger padronizado para rastreabilidade
- Testes de estrutura para validar o setup
- .gitignore configurado para projetos de dados

## Decisões técnicas

### Por que Makefile e não Airflow/Prefect?

Para uma pipeline batch com poucas etapas, um Makefile é mais
transparente e fácil de manter. Cada target é um passo da pipeline,
as dependências são explícitas, e qualquer pessoa com experiência
Linux entende imediatamente. Se o projeto crescer, migrar para
Airflow é simples — os scripts já estão modularizados.

### Por que DuckDB e não PostgreSQL?

DuckDB é um banco OLAP embarcado — zero configuração, zero servidor.
É como SQLite, mas otimizado para queries analíticas (colunar).
Para um projeto de portfólio que alguém vai clonar e rodar,
eliminar a necessidade de instalar PostgreSQL reduz a fricção a zero.

### Por que scripts .py e não Jupyter Notebooks?

Notebooks são bons para exploração, mas ruins para produção.
Scripts .py têm diff limpo no Git, são testáveis com pytest,
e rodam em CI sem configuração extra.

### Estrutura de dados em camadas

raw -> processed -> analytics

Inspirada no modelo medallion (bronze/silver/gold).
Permite reprocessar qualquer camada sem baixar tudo de novo.

## Próximo passo

Dia 2: Scripts de ingestão para baixar dados do IBGE e dados.gov.br.