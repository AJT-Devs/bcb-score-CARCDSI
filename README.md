# BCB Score CARCDSI

Sistema analítico para estudar e prever risco de crédito agregado a partir dos dados mensais do Sistema de Informações de Créditos (SCR) do Banco Central do Brasil.

O projeto calcula indicadores de inadimplência e ativos problemáticos, prepara atributos para modelos de Machine Learning e prevê a evolução do risco por perfil de crédito. Em uma etapa posterior, os resultados calculados pelo código podem ser interpretados por um LLM para gerar briefings. O LLM não é responsável por calcular métricas ou inventar previsões.

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
├── docs/                  # Entregas e documentação acadêmica
├── src/
│   ├── config/            # Configurações e constantes de domínio
│   ├── data/              # Leitura, validação e pré-processamento
│   ├── analysis/          # Análises exploratórias e estatísticas
│   ├── features/          # Engenharia e seleção de atributos
│   ├── models/            # Modelos, treinamento e avaliação
│   ├── services/ia/       # Clientes, prompts e relatórios de LLM
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
py -3.14 -m venv .venv
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

O ponto de entrada atual confirma a configuração do projeto. Os pipelines de treinamento e predição serão conectados quando os experimentos forem implementados.

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

## Configuração de LLM

Copie `.env.example` para `.env` e preencha as chaves localmente. Nunca versione `.env`:

```powershell
Copy-Item .env.example .env
```

Variáveis disponíveis:

- `NVIDIA_API_KEY`: chave do NVIDIA NIM.
- `GEMINI_API_KEY`: chave do Google Gemini.
- `NVIDIA_MODEL`: modelo NVIDIA utilizado.
- `GEMINI_MODEL`: modelo Gemini utilizado.
- `LLM_REQUEST_TIMEOUT_SECONDS`: timeout das requisições.
- `DATA_RAW_DIR`: diretório dos CSVs brutos.

As requisições são feitas por `src/services/ia/client.py`. Testes automatizados não devem chamar provedores reais; use mocks ou stubs.

## Validação e metodologia

As divisões de treino e teste devem respeitar a ordem de `data_base`. O denominador das proporções é `carteira_ativa` e casos de denominador zero precisam ser tratados explicitamente.

Consulte [`AGENTS.md`](AGENTS.md) para as regras completas de negócio, arquitetura, segurança e registro das atividades em `artifacts/`.

## Licença e dados

Consulte a licença e as condições de uso da fonte oficial antes de redistribuir os dados. Este repositório não inclui os CSVs brutos.
