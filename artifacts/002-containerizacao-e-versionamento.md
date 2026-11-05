# Log 002 - Versionamento do runtime e containerização

## Prompt

Deixe fixada a versão do python e pip no projeto (deve subir para o remote). Vou rodar o projeto num container. Crie um dockerfile e compose com base nas dependencias do projeto (linux).
Em artifacts, coloque MDs detalhados do que foi feito (prompt e resposta), como um log (requisito do projeto), comece pelo prompt anterior, e faça um desse prompt

## Resposta

O projeto passou a declarar explicitamente as versões do runtime e do gerenciador de pacotes:

- `.python-version` fixa o interpretador em `3.14.0`.
- `requirements.txt` fixa `pip==26.3` e as dependências diretas de análise de dados e Machine Learning.
- O `Dockerfile` utiliza a imagem Linux `python:3.14.0-slim`, mantendo a mesma versão do Python usada no ambiente local.

### Dockerfile

O Dockerfile:

1. Usa uma imagem oficial e enxuta do Python para Linux.
2. Define `/app` como diretório de trabalho.
3. Desabilita arquivos `.pyc` e habilita saída não bufferizada.
4. Copia primeiro o `requirements.txt`, favorecendo o cache das camadas Docker.
5. Instala exatamente o pip definido no projeto e depois as dependências.
6. Copia o conteúdo de `src/` para a imagem.
7. Executa `python --version` por padrão, pois o projeto ainda não possui um módulo de entrada da aplicação.

### Compose

O `compose.yaml` define o serviço `app`, constrói a imagem localmente e executa uma verificação de imports das bibliotecas principais. O comando pode ser substituído posteriormente pelo ponto de entrada real da aplicação quando ele for implementado.

### Contexto de build

O `.dockerignore` evita enviar para o daemon Docker o ambiente virtual local, dados brutos, artefatos de log e caches. Isso reduz o contexto de build e evita transportar dependências instaladas no Windows para a imagem Linux.

### Comandos de uso

Construir e executar a validação do ambiente:

```powershell
docker compose up --build
```

Construir somente a imagem:

```powershell
docker build -t bcb-score-carcdsi:local .
```

Executar um comando Python na imagem:

```powershell
docker compose run --rm app python --version
```

### Validação

A instalação local foi validada com `pip check` e com imports de `matplotlib`, `numpy`, `pandas` e `sklearn`. A validação Docker deve ser executada em uma máquina com Docker Desktop ou Docker Engine disponível.
