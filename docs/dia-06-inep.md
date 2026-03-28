# Dia 6 — Novas Fontes de Dados (INEP)

## O que foi feito

- Download da Sinopse Estatística do Censo Escolar 2023 (145MB)
- Exploração do XLSX com 173 abas (matrículas, docentes, escolas, turmas)
- Parser que extrai dados agregados por UF de 3 abas
- Merge em tabela única com 27 registros

## Fontes extraídas

| Aba | Dados | Registros |
|-----|-------|-----------|
| Educação Básica 1.1 | Matrículas por UF | 27 |
| Educação Básica 2.1 | Docentes por UF | 27 |
| Educação Básica 3.1 | Escolas por UF | 27 |

## Decisões técnicas

### Sinopse vs microdados

Os microdados do INEP têm milhões de linhas (GBs de CSVs).
Para a análise por UF, a Sinopse Estatística já traz os dados
agregados. Usar microdados seria desperdício de processamento
sem ganho analítico para esse nível de granularidade.

### Parser genérico para planilhas do INEP

A função extract_sheet() recebe o nome da aba e o nome da
coluna de valor. Isso permite adicionar novas abas (creche,
ensino médio, EJA) com uma linha de código.

### Filtragem por nível de agregação

As planilhas misturam Brasil, regiões, UFs e municípios.
Identificamos as linhas de UF pelo padrão: região preenchida,
UF preenchida, município vazio, código vazio.

## Arquivos criados

- src/ingestion/extract_inep.py — parser do XLSX do INEP

## Próximo passo

Dia 7: Cruzamento IBGE + INEP no DuckDB.