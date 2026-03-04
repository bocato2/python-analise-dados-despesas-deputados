# Análise de despesas parlamentares com Python

Projeto em Python para análise de dados públicos da Câmara dos Deputados.

O script realiza leitura de dados CSV, processamento, agregações e geração de relatórios.

## Tecnologias utilizadas

- Python
- csv (DictReader / DictWriter)
- Manipulação de dicionários
- Ordenação com sorted
- Processamento de dados

## Análises realizadas

- Total de despesas
- Ticket médio
- Gastos por deputado
- Gastos por partido
- Gastos por UF
- Gastos por tipo de despesa
- Top 10 deputados com maior gasto
- Top 10 fornecedores
- Identificação de despesas atípicas (outliers)

## Relatórios gerados

O script gera automaticamente:

- `top_deputados.csv`
- `top_fornecedores.csv`
- `top_tipos.csv`
- `outliers.csv`

## Como executar

```bash
python src/analise_despesas.py
