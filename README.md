# BCB Score CARCDSI

Sistema analítico para estudar e prever risco de crédito agregado a partir dos dados mensais do Sistema de Informações de Créditos (SCR) do Banco Central do Brasil.

O projeto calcula indicadores de inadimplência e ativos problemáticos, prepara atributos para modelos de Machine Learning e prevê a evolução do risco por perfil de crédito. Todo o processamento, treinamento, avaliação e geração de resultados funciona localmente, sem LLM ou credenciais.

## Objetivos

- Analisar a evolução mensal do crédito no Brasil.
- Comparar risco por UF, segmento, cliente, porte, modalidade e submodalidade.
- Calcular a proporção de inadimplência: `carteira_inadimplencia / carteira_ativa`.
- Calcular a proporção de ativos problemáticos: `ativo_problematico / carteira_ativa`.
- Treinar modelos para apoiar previsões de risco agregado.
- Produzir briefings auditáveis a partir das métricas geradas pelos modelos.

## Dados

Os CSVs mensais não são enviados ao Git. Baixe os dados públicos do SCR e coloque-os em `data/raw/`.

- Fonte: [SCR.data - Banco Central do Brasil](https://dadosabertos.bcb.gov.br/dataset/scr_data)
- Download anual de 2025: [scrdata_2025.zip](https://www.bcb.gov.br/pda/desig/scrdata_2025.zip)
- Instruções completas: [`data/data.md`](data/data.md)

O leitor espera arquivos CSV com separador `;`. Os dados brutos devem permanecer inalterados; resultados intermediários e processados devem ficar em suas respectivas pastas dentro de `data/`.

## Estrutura do projeto

```text
.
├── artifacts/             # Logs das interações e decisões dos agentes
├── data/
│   ├── raw/               # CSVs originais, ignorados pelo Git
│   ├── interim/           # Dados intermediários, ignorados pelo Git
│   ├── processed/         # Dados preparados, ignorados pelo Git
│   └── data.md            # Instruções para obtenção e organização dos dados
├── docs/                  # Entregas e arquitetura da pesquisa
├── src/
│   ├── config/            # Configurações e constantes de domínio
│   ├── data/              # Leitura, validação e pré-processamento
│   ├── analysis/          # Análises exploratórias e estatísticas
│   ├── features/          # Engenharia e seleção de atributos
│   ├── models/            # Modelos, treinamento e avaliação
│   ├── services/ia/       # Relatórios locais de métricas
│   ├── visualization/     # Gráficos e dashboards
│   ├── pipelines/         # Orquestração dos fluxos
│   └── utils/             # Utilitários compartilhados
│
├── .env.example           # Modelo de configuração local
├── .python-version        # Python fixado em 3.14.0
├── Dockerfile             # Imagem Linux do projeto
├── compose.yaml           # Execução local com volume de dados
└── requirements.txt       # Dependências e pip fixados
```

## Requisitos

- Python `3.14.0`
- pip `26.3`
- Docker Desktop ou Docker Engine, caso use containers
- Os dados do SCR em `data/raw/` para executar a leitura real

## Ambiente local

Crie o ambiente virtual na raiz do projeto:

```powershell
.\scripts\bootstrap.ps1
```

Ative-o no PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

Valide o ambiente:

```powershell
$env:PYTHONPATH = "src"
python -m pip check
python -m compileall -q src
python src/main.py
```

O experimento é executável por `python -m pipelines.experiment --output runs/2025-pilot`, com `PYTHONPATH=src`. Consulte [o funcionamento efetivo](docs/funcionamento-efetivo.md) para comandos com o Python do `.venv`, protocolo e inferência.

## Docker

O Dockerfile usa `python:3.14.0-slim`, instala as versões declaradas em `requirements.txt` e copia somente o código-fonte. Os dados ficam fora da imagem e são montados pelo Compose como volume somente leitura.

Valide a configuração:

```powershell
docker compose config
```

Construa e execute:

```powershell
docker compose up --build
```

O comando atual do Compose valida os imports das bibliotecas principais. Ele será substituído pelo pipeline real quando existir um ponto de entrada de aplicação.

## Experimentos no terminal

Todos os exemplos usam PowerShell na raiz, após criar o ambiente e instalar `requirements.txt` conforme acima. Os arquivos de saída devem estar em diretório novo. Não é necessário Codex, chave ou serviço de LLM.

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m compileall -q src
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m pipelines.experiment --models baselines,linear,tree,knn --knn-max-train 5000 --output runs/experimento
.\.venv\Scripts\python.exe -m pipelines.evaluation_pipeline runs/experimento
Import-Csv runs/experimento/metrics.csv | Where-Object { $_.split -eq 'test' -and $_.scope -eq 'common' } | Format-Table
.\.venv\Scripts\python.exe -m pipelines.prediction_pipeline --interim data/interim/2025 --models runs/experimento/models --methods baselines,linear,tree,knn --origin 2025-11 --output runs/previsoes.csv
```

Escolha `baselines`, `linear`, `tree`, `knn`, `catboost` e/ou `chronos` com `--models`; baselines só aparecem se escolhidos. Chronos exige checkpoint local ou acesso para baixá-lo; não é um LLM de texto. Consulte `manifest.json` para falhas e tempos. Inferência persistida aceita os modelos clássicos, CatBoost e baselines; não implementa recarga de Chronos. Carregue arquivos joblib apenas de fontes confiáveis.

Para limitar custo, k-NN usa por alvo no máximo 5.000 linhas elegíveis de treino, amostradas uniformemente sem reposição com semente 42. O JSON do modelo registra total, amostra e parâmetros; aumente `--knn-max-train` apenas após medir custo. A ingestão consolida o painel em memória e pode exigir vários GB. O baseline sazonal anual não é avaliável com somente 2025.

`scope=available` mede cada modelo em todos os perfis elegíveis com previsão; `scope=common` usa a interseção dos modelos executados no alvo e partição. MAE/RMSE estão em proporção e pontos percentuais; R², cobertura, quantidades e previsões fora de [0,1] são registrados. A seleção de CatBoost usa somente validação. [Detalhes e limites](docs/funcionamento-efetivo.md).

## Validação e metodologia

As divisões de treino e teste devem respeitar a ordem de `data_base`. O denominador das proporções é `carteira_ativa` e casos de denominador zero precisam ser tratados explicitamente.

Consulte [a arquitetura e o estado de implementação](docs/arquitetura.md) para os modelos, baselines e métricas previstos nos entregáveis. O fluxo experimental com modelos clássicos, CatBoost, Chronos-2 e baselines está implementado; a distinção entre implementado e executado está nos manifestos e em [resultados-execucao.md](docs/resultados-execucao.md).

Consulte [`AGENTS.md`](AGENTS.md) para as regras completas de negócio, arquitetura, segurança e registro das atividades em `artifacts/`.

## Licença e dados

Consulte a licença e as condições de uso da fonte oficial antes de redistribuir os dados. Este repositório não inclui os CSVs brutos.

## Protocolo científico vigente

CatBoost e Chronos-2 são os modelos principais. [Decisão e protocolo](docs/protocolo-catboost-chronos2.md), [guia do código e fluxogramas](docs/funcionamento-efetivo.md), [artigo SBC](paper/main.tex). Os entregáveis e plano Qwen preservam decisões históricas. O piloto Chronos usa uma amostra determinística em CPU; não equivale à avaliação integral.

## Reprodução da comparação de 2025 com Chronos-2

Na raiz do projeto, depois de preparar o `.venv`, escolha nomes novos para as saídas; estes exemplos não sobrescrevem a execução registrada. O primeiro comando processa os 12 CSVs reais e pode exigir vários GB de memória e vários minutos. Chronos usa o checkpoint público fixado e poderá baixá-lo na primeira execução; o processamento dos dados e a inferência são locais.

```powershell
$env:PYTHONPATH = 'src'
$env:OMP_NUM_THREADS = '4'
$env:OPENBLAS_NUM_THREADS = '4'
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m compileall -q src
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m pipelines.experiment --raw data/raw --interim data/interim/2025-repro --output runs/2025-repro --models baselines,linear,tree,knn,catboost --knn-max-train 5000
.\.venv\Scripts\python.exe -m analysis.panel_audit --prepared data/interim/2025-repro/supervised.csv --output runs/2025-repro/panel_audit.json
.\.venv\Scripts\python.exe -m pipelines.chronos_pipeline --interim data/interim/2025-repro --output runs/2025-repro-chronos --modulus 1024
.\.venv\Scripts\python.exe -m pipelines.merge_forecasts runs/2025-repro runs/2025-repro-chronos --interim data/interim/2025-repro --output runs/2025-repro-comparacao
Import-Csv runs/2025-repro-comparacao/metrics.csv | Where-Object { $_.split -eq 'test' -and $_.scope -eq 'common' } | Format-Table
.\.venv\Scripts\python.exe -m visualization.export_paper runs/2025-repro-comparacao
```

O último comando atualiza os arquivos gerados do artigo. As métricas `common` comparam os mesmos perfis, que ficam limitados à amostra do Chronos; `available` mostra a cobertura sobre os rótulos elegíveis. O k-NN usa até 5.000 linhas de treino por alvo, com semente 42; Chronos é zero-shot e usa as chaves cujo hash tem resto zero módulo 1024. Não há baseline sazonal anual avaliável com apenas 2025. As datas de modificação não provam a extração: os autores informaram que os arquivos foram extraídos em 17/09/2026.
