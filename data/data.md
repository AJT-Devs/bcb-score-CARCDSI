# Dados do projeto

Esta pasta contém os dados utilizados pelo projeto de análise de risco de crédito do SCR.

## Estrutura

```text
data/
├── compressed/ # ZIPs anuais locais (scrdata_AAAA.zip)
├── raw/        # CSVs originais baixados do Banco Central
├── interim/    # Dados intermediários gerados durante o processamento
├── processed/  # Dados prontos para análise ou modelagem
└── external/   # Dados auxiliares de fontes externas
```

As pastas podem ser criadas localmente conforme o fluxo evoluir. Arquivos `.csv`, `.parquet`, `.feather`, `.pkl`, `.pickle` e `.joblib` são ignorados pelo Git para evitar o envio de datasets e artefatos potencialmente grandes ou sensíveis.

## Dados brutos do SCR

O acervo compactado cobre janeiro de 2015 a setembro de 2026, com os doze meses de 2015 a 2025 e janeiro a setembro de 2026. Os 12 ZIPs estão na [pasta compartilhada do Google Drive](https://drive.google.com/drive/u/1/folders/1aCvm6NC_WQwB-muz1c-bctyFDmyRlHy-).

Na raiz, coloque os ZIPs em `data/compressed/` e execute:

```powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe -m pipelines.prepare_data
```

O comando verifica os nomes dos CSVs dentro dos ZIPs e extrai apenas os meses ainda ausentes em `data/raw/`. Use `--years 2015 2026` para limitar a seleção de arquivos anuais. Com os arquivos atuais, os CSVs ocupam cerca de 12 GB.

Para baixar pelo Drive no mesmo comando, deixe o [rclone](https://rclone.org/drive/) disponível no PATH e configure um remote do tipo Google Drive com acesso de leitura à pasta compartilhada. Neste exemplo, o remote se chama `scr-drive`. Os ZIPs locais são preservados.

```powershell
.\.venv\Scripts\python.exe -m pipelines.prepare_data --drive-remote scr-drive
```

O leitor espera em `data/raw/`:

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
5. Para reproduzir o experimento do artigo, use o intervalo de janeiro a dezembro de 2025 indicado no README.

O módulo [`src/data/read/csv_reader.py`](../src/data/read/csv_reader.py) descobre todos os CSVs dessa pasta, lê os arquivos com separador `;` e permite consolidá-los em um DataFrame.
