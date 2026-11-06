# Log 004 - Regras para agentes de IA

## Prompt

Crie uma AGENTS.md com regras de negocio (ex: documentar prompts e respostas em artifacts) e arquitetura do projeto (docker, venv, estrutura), para agentes de IA seguirem.

## Resposta

Foi criada a `AGENTS.md` na raiz do repositório para orientar agentes de IA em alterações futuras.

### Conteúdo incluído

- Contexto do domínio SCR e objetivos de risco de crédito.
- Regras para cálculo e interpretação das proporções de inadimplência e ativos problemáticos.
- Separação entre leitura, validação, pré-processamento, features, modelos e interpretação por LLM.
- Obrigatoriedade de registrar cada prompt, resposta, arquivos alterados e validações em `artifacts/`.
- Proibição de registrar credenciais, tokens ou dados sensíveis nos logs.
- Responsabilidade de cada camada da estrutura `src/`.
- Regras para uso dos CSVs em `data/raw/` e para respeitar o separador `;`.
- Python `3.14.0`, pip `26.3` e uso obrigatório do `.venv`.
- Regras de Dockerfile, Compose, cache de camadas e volume somente leitura para os dados.
- Configuração segura de `NVIDIA_API_KEY` e `GEMINI_API_KEY`.
- Fluxo de trabalho esperado antes e depois de editar código.
- Comandos mínimos de validação para Python e Docker.

### Arquivos criados

- `AGENTS.md`
- `artifacts/004-regras-para-agentes.md`

### Validação

A configuração do repositório foi conferida antes da criação da regra. As versões e estruturas referenciadas foram verificadas em `Dockerfile`, `compose.yaml`, `src/config/settings.py` e `src/services/ia/client.py`.

A regra de registrar a interação foi aplicada nesta própria tarefa. Nenhuma credencial foi incluída no documento.
