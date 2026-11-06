# Instruções para agentes de IA

## Escopo

Este arquivo define as regras para agentes de IA que analisarem, modificarem ou executarem este projeto. As instruções se aplicam a todo o repositório, salvo instruções mais específicas em arquivos localizados em subdiretórios.

## Contexto de negócio

O projeto analisa dados mensais do Sistema de Informações de Créditos (SCR) do Banco Central do Brasil. O objetivo é estudar e prever risco de crédito agregado, com foco em:

- proporção de inadimplência: `carteira_inadimplencia / carteira_ativa`;
- proporção de ativos problemáticos: `ativo_problematico / carteira_ativa`;
- comparação de risco por UF, segmento, cliente, porte, modalidade e submodalidade;
- geração de briefings em linguagem natural a partir de métricas produzidas por modelos de Machine Learning.

Os dados e as métricas calculadas são a fonte de verdade. Um LLM pode interpretar e redigir resultados, mas não pode calcular, alterar ou inventar previsões.

## Regras de negócio

1. Preserve a semântica das colunas oficiais do SCR. Não renomeie colunas ou targets sem atualizar `src/config/constants.py`, os consumidores e a documentação.
2. Considere `carteira_ativa` como denominador das proporções. Trate denominador zero explicitamente e nunca produza divisão silenciosa por zero.
3. Separe as etapas de leitura, validação, pré-processamento, engenharia de atributos, modelagem e interpretação.
4. Como os dados são mensais, divisões de treino e teste devem respeitar a ordem temporal. Não use meses futuros para treinar previsões de meses anteriores.
5. Relate limitações, dados ausentes, filtros e decisões metodológicas junto dos resultados.
6. O LLM deve receber métricas e contexto já calculados pelo código. Não delegue ao LLM a validação estatística, o cálculo das proporções ou a escolha silenciosa de resultados.
7. Não faça chamadas reais a provedores durante testes automatizados. Use mocks, stubs ou validações sem rede.
8. Nunca inclua chaves, tokens, dados pessoais ou respostas contendo segredos em código, commits, logs ou `artifacts/`.

## Registro obrigatório de interações

Toda tarefa realizada por um agente deve ser registrada em `artifacts/`:

- crie um arquivo Markdown numerado sequencialmente, por exemplo `004-descricao-da-tarefa.md`;
- inclua o prompt integral do usuário;
- inclua a resposta/ações realizadas pelo agente;
- liste arquivos criados ou alterados;
- registre validações executadas, resultados e limitações;
- não copie credenciais, tokens ou conteúdo sensível para o log;
- mantenha os logs anteriores; nunca sobrescreva ou reordene registros existentes.

Quando uma tarefa alterar comportamento, documente também a decisão arquitetural e o impacto esperado.

## Estrutura da aplicação

A implementação deve respeitar as responsabilidades abaixo:

- `src/config/`: configurações, caminhos, variáveis de ambiente e constantes de domínio.
- `src/data/read/`: leitura e consolidação dos CSVs mensais; não deve conter modelagem.
- `src/data/validation/`: integridade, colunas obrigatórias, tipos, duplicidades e valores inconsistentes.
- `src/data/preprocessing/`: limpeza, codificação, transformações numéricas e pipeline de preparação.
- `src/analysis/`: análise exploratória, estatística e correlação.
- `src/features/`: criação e seleção de atributos de domínio.
- `src/models/`: contratos, treinamento, predição e avaliação dos modelos.
- `src/services/ia/`: clientes, prompts, briefings e relatórios de LLM.
- `src/visualization/`: gráficos e dashboards.
- `src/pipelines/`: orquestração dos fluxos de treinamento e predição.
- `src/utils/`: utilitários realmente compartilhados; não use esta pasta como depósito genérico.

Novos módulos devem ser colocados na camada que possui a responsabilidade correspondente. Pipelines devem compor módulos existentes, não duplicar suas regras.

## Dados e arquivos locais

- Os CSVs de desenvolvimento ficam em `data/raw/`.
- O leitor deve aceitar múltiplos arquivos e o separador `;` usado pelo SCR.
- Dados brutos não devem ser alterados pelo código de leitura.
- `data/` é ignorado pelo Git e não deve ser adicionado ao commit sem decisão explícita.
- No Compose, `data/raw` é montado como volume somente leitura em `/app/data/raw`.
- Não carregue um dataset inteiro em memória sem necessidade; prefira amostras, chunks ou agregações quando a tarefa permitir.

## Python e dependências

- A versão oficial do Python é `3.14.0`, registrada em `.python-version`.
- O pip fixado é `26.3`; respeite as versões declaradas em `requirements.txt`.
- Use o ambiente `.venv` para desenvolvimento local.
- Não instale dependências diretamente no sistema operacional.
- Ao adicionar uma dependência, justifique sua necessidade, atualize `requirements.txt` e valide a instalação.
- Prefira a biblioteca padrão quando ela resolver o problema sem aumentar complexidade.
- Mantenha imports, tipos e nomes claros. Evite estado global mutável e efeitos colaterais em importação.

## Docker e Compose

- A imagem deve permanecer baseada em `python:3.14.0-slim`, salvo decisão documentada.
- O Dockerfile deve instalar dependências antes de copiar o código para preservar cache de camadas.
- Não copie `.venv`, dados locais, chaves ou caches para a imagem.
- O Compose deve montar os dados como somente leitura e manter segredos fora do arquivo versionado.
- Use `docker compose config` para validar alterações no Compose.
- O `Dockerfile` atualmente possui apenas uma verificação de ambiente como comando padrão. Atualize o comando somente quando existir um ponto de entrada real da aplicação.

## Credenciais e LLMs

- Configure credenciais localmente em `.env`, usando `.env.example` como referência.
- Nunca edite `.env` para inserir segredos em uma alteração versionável.
- Use `NVIDIA_API_KEY` para NVIDIA NIM e `GEMINI_API_KEY` para Gemini.
- Modelos e timeout devem ser configuráveis por `NVIDIA_MODEL`, `GEMINI_MODEL` e `LLM_REQUEST_TIMEOUT_SECONDS`.
- O cliente deve falhar de forma explícita quando a chave necessária não estiver configurada.
- Preserve o formato de resposta e o provedor ao criar abstrações novas, para permitir auditoria.

## Fluxo de trabalho do agente

Antes de editar:

1. leia este arquivo e as instruções locais aplicáveis;
2. verifique o estado atual dos arquivos relacionados;
3. formule uma hipótese sobre o caminho de código afetado;
4. escolha uma validação pequena que possa confirmar ou refutar a hipótese.

Depois de editar:

1. execute a validação mais próxima do comportamento alterado;
2. corrija erros da mesma área antes de ampliar o escopo;
3. registre comandos, resultados e limitações em `artifacts/`;
4. confira `git diff` e confirme que nenhum segredo ou arquivo local foi incluído.

Não reverta alterações feitas por outras pessoas ou agentes. Não faça commits, branches ou mudanças destrutivas sem solicitação explícita.

## Validações mínimas

Para alterações de Python, quando aplicável:

```powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe -m compileall -q src
.\.venv\Scripts\python.exe -m pip check
```

Para alterações de container:

```powershell
docker compose config
docker compose up --build
```

Se Docker, credenciais ou outro recurso externo não estiver disponível, registre a limitação no `artifact` em vez de simular sucesso.
