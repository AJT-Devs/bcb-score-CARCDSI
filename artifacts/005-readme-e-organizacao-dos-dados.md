# Log 005 - README e organização dos dados

## Prompt

Crie um readme com informações da aplicação em geral, estrutura, container, rodar o projeto, etc.
Em data, coloque informações para adicionar os csv raw e outros, altere o gitignore para mostrar as pastas em data, mas nao enviar os csv

## Resposta

Foi criado o README principal do projeto e preenchida a documentação de dados em `data/data.md`.

### README

O README documenta:

- objetivo geral da aplicação e indicadores de risco;
- fontes públicas dos dados do SCR;
- estrutura de diretórios do projeto;
- requisitos de Python, pip e Docker;
- criação e ativação do `.venv`;
- instalação e validação das dependências;
- construção e execução do Docker Compose;
- montagem dos dados como volume somente leitura;
- configuração das chaves NVIDIA/Gemini por `.env`;
- limites atuais do ponto de entrada e dos pipelines;
- referência às regras de `AGENTS.md`.

### Organização de dados

`data/data.md` agora explica as pastas `raw`, `interim`, `processed` e `external`, além das regras para manter os arquivos brutos inalterados e obter os CSVs da fonte oficial.

Foram criados `.gitkeep` em:

- `data/raw/`
- `data/interim/`
- `data/processed/`
- `data/external/`

### Gitignore

O `.gitignore` passou a ignorar CSVs e formatos comuns de dados gerados em qualquer subpasta de `data/`, mas mantém visíveis a documentação e os arquivos `.gitkeep`. Assim, a estrutura sobe para o repositório sem enviar os datasets.

### Arquivos criados ou alterados

- `README.md`
- `data/data.md`
- `data/raw/.gitkeep`
- `data/interim/.gitkeep`
- `data/processed/.gitkeep`
- `data/external/.gitkeep`
- `.gitignore`
- `artifacts/005-readme-e-organizacao-dos-dados.md`

### Validação

A validação deve confirmar que um CSV em `data/raw/` é ignorado pelo Git, enquanto `data/data.md` e os `.gitkeep` permanecem versionáveis. Nenhum arquivo CSV foi alterado ou incluído no repositório.
