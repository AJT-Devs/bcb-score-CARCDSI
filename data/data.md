# Dados do projeto

Esta pasta contém os dados utilizados pelo projeto de análise de risco de crédito do SCR.

## Estrutura

```text
data/
├── raw/        # CSVs originais baixados do Banco Central
├── interim/    # Dados intermediários gerados durante o processamento
├── processed/  # Dados prontos para análise ou modelagem
└── external/   # Dados auxiliares de fontes externas
```

As pastas podem ser criadas localmente conforme o fluxo evoluir. Arquivos `.csv`, `.parquet`, `.feather`, `.pkl`, `.pickle` e `.joblib` são ignorados pelo Git para evitar o envio de datasets e artefatos potencialmente grandes ou sensíveis.

## Dados brutos do SCR

Coloque os arquivos mensais originais em `data/raw/`. O leitor espera:

- arquivos com extensão `.csv`;
- separador `;`;
- cabeçalho com as colunas oficiais do SCR;
- um arquivo por período mensal, sem alterar os dados originais.

Exemplo de nomes:

```text
data/raw/scrdata_202501.csv
data/raw/scrdata_202502.csv
```

Fonte pública:

- [SCR.data - Banco Central do Brasil](https://dadosabertos.bcb.gov.br/dataset/scr_data)
- [Arquivos mensais de 2025](https://www.bcb.gov.br/pda/desig/scrdata_2025.zip)

## Regras de uso

1. Não altere os arquivos em `raw/`; correções e transformações devem gerar arquivos em `interim/` ou `processed/`.
2. Não versione dados brutos, dados processados, modelos serializados ou outros artefatos gerados.
3. Preserve a competência mensal (`data_base`) para que os experimentos respeitem a ordem temporal.
4. Não inclua dados pessoais, credenciais ou arquivos obtidos de fonte privada.
5. Para reproduzir o projeto, cada integrante deve baixar os dados da fonte pública e colocá-los em `data/raw/` localmente.

O módulo [`src/data/read/csv_reader.py`](../src/data/read/csv_reader.py) descobre todos os CSVs dessa pasta, lê os arquivos com separador `;` e permite consolidá-los em um DataFrame.
