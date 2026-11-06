# Log 003 - Arquitetura inicial do código-fonte

## Prompt

Crie a arquitetura inicial do código fonte

src/
│
├── main.py
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   └── constants.py
│
├── data/
│   ├── __init__.py
│   ├── read/
│   │   ├── __init__.py
│   │   └── csv_reader.py
│   │
│   ├── validation/
│   │   ├── __init__.py
│   │   └── data_validator.py
│   │
│   └── preprocessing/
│       ├── __init__.py
│       ├── cleaner.py
│       ├── encoder.py
│       ├── transformer.py
│       └── pipeline.py
│
├── analysis/
│   ├── __init__.py
│   ├── exploratory.py
│   ├── statistics.py
│   └── correlation.py
│
├── features/
│   ├── __init__.py
│   ├── feature_engineering.py
│   └── feature_selection.py
│
├── models/
│   ├── __init__.py
│   ├── base_model.py
│   ├── regression/
│   │   ├── __init__.py
│   │   └── regression_model.py
│   │
│   ├── tree/
│   │   ├── __init__.py
│   │   └── tree_model.py
│   │
│   ├── training.py
│   ├── prediction.py
│   └── evaluation.py
│
├── services/
│   ├── __init__.py
│   └── ia/
│       ├── __init__.py
│       ├── client.py
│       ├── prompts.py
│       ├── briefing.py
│       └── report_generator.py
│
├── visualization/
│   ├── __init__.py
│   ├── charts.py
│   └── dashboards.py
│
├── pipelines/
│   ├── __init__.py
│   ├── training_pipeline.py
│   └── prediction_pipeline.py
│
└── utils/
    ├── __init__.py
    ├── logger.py
    ├── file_manager.py
    └── helpers.py

Crie a documentação em artifacts. Em questão de criação de código, crie o código de src/data/read, lendo os .csv de /data/raw
Crie também os codigos de requisicao para LLM, de NVIDIA_API_KEY e GEMINI_API_KEY

## Resposta

A arquitetura inicial foi criada em `src/`, incluindo todos os pacotes e módulos solicitados.

### Implementações funcionais

- `config/settings.py` centraliza caminhos, modelos LLM, timeout e leitura de variáveis de ambiente.
- `config/constants.py` define o separador `;`, as colunas obrigatórias e os targets do projeto.
- `data/read/csv_reader.py` descobre CSVs em `data/raw`, lê arquivos mensais e consolida os DataFrames.
- `data/validation/data_validator.py` verifica a presença das colunas essenciais do SCR.
- `data/preprocessing/` contém limpeza, codificação, cálculo das proporções de inadimplência e ativos problemáticos, e uma função de pipeline.
- `services/ia/client.py` implementa clientes REST para NVIDIA NIM e Google Gemini usando apenas a biblioteca padrão do Python.
- `services/ia/prompts.py`, `briefing.py` e `report_generator.py` estruturam a geração de briefings sem delegar cálculos ao LLM.

### Segurança e configuração

As chaves `NVIDIA_API_KEY` e `GEMINI_API_KEY` são lidas somente em tempo de execução. O cliente Gemini envia a chave pelo header `x-goog-api-key`, evitando colocá-la na URL. O `.env.example` documenta as variáveis esperadas sem conter credenciais reais.

### Validação

- Foram descobertos 12 CSVs em `data/raw`.
- Uma amostra de duas linhas foi lida com separador `;`.
- As 24 colunas do arquivo foram verificadas contra as colunas obrigatórias.
- Todos os módulos foram compilados com `python -m compileall -q src`.
- Os imports dos clientes NVIDIA/Gemini foram validados sem chamadas de rede.

Os módulos de análise, modelos, visualização e pipelines foram criados como pontos de extensão documentados. A implementação específica desses módulos deve acompanhar a definição dos experimentos e modelos da segunda entrega do projeto.