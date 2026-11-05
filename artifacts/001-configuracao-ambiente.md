# Log 001 - Configuração do ambiente

## Prompt

Estou criando o repositorio do meu projeto final com base em projeto-final. O tema está em entregavel-1.
Crie o ambiente venv, seguindo padroes e boas praticas de arquitetura de projetos. Atualize dependencias do requirements.txt
adicione arquivos que nao vao pro github (dependencias) no gitignore

## Resposta

Foi criado o ambiente virtual `.venv` com Python 3.14.0.

O arquivo `requirements.txt` foi reorganizado para declarar as dependências diretas utilizadas pelo projeto:

- `numpy==2.5.2`
- `pandas==3.0.5`
- `matplotlib==3.11.1`
- `scikit-learn==1.9.1`

As dependências transitivas passaram a ser resolvidas pelo instalador a partir dessas bibliotecas principais. O `.gitignore` foi ampliado para ignorar o ambiente virtual, caches do Python, artefatos de build, configurações locais e a pasta local de dados.

A instalação foi validada com `pip check` e com imports de NumPy, pandas, Matplotlib e scikit-learn.
