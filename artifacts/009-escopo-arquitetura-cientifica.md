# Registro 009 - Escopo da arquitetura científica

## Prompt integral do usuário

analise os docs/, src/ (arquitetura do projeto), deixe o escopo da arquitetura de acordo com os entregaveis em docs, altere o escopo do services/ia para permitir mais modelos nao ficando fixado em Gemini e NVIDIA, aproveite e normalize o nome dos arquivos e pastas considerando o escopo do projeto como um artigo cientifico

## Análise e decisão arquitetural

Os entregáveis estabelecem duas proporções do SCR, previsão mensal, regressão linear múltipla, árvore de decisão, k-NN, quatro baselines e avaliação por MAE, RMSE e R². A maior parte dos módulos de pesquisa era apenas estrutura inicial. A arquitetura foi documentada distinguindo funcionalidades existentes de etapas ainda não implementadas, inclusive a prevenção de vazamento temporal e a reprodução dos experimentos.

Os pontos de extensão dos modelos foram organizados em módulos `snake_case` descritivos, substituindo os pacotes genéricos de regressão e árvore e acrescentando locais para k-NN, baselines e validação temporal. As colunas oficiais e a camada `services/ia` foram preservadas conforme as regras do projeto.

O contrato `LLMClient` permite injetar clientes adicionais no briefing sem depender de uma lista fechada de provedores. Os clientes Gemini e NVIDIA existentes e o formato `LLMResponse` foram preservados; nomes de provedor desconhecidos agora falham explicitamente. Quando um cliente é injetado ele determina o provedor. Isso amplia a integração sem atribuir cálculos ou escolha de resultados ao LLM.

## Arquivos criados ou alterados

- `README.md` e `docs/arquitetura.md`.
- `src/services/ia/__init__.py`, `src/services/ia/client.py` e `src/services/ia/briefing.py`.
- `src/models/evaluation.py`, `src/models/linear_regression.py`, `src/models/decision_tree.py`, `src/models/nearest_neighbors.py`, `src/models/baselines.py` e `src/models/temporal_validation.py`.
- Removidos os pontos de extensão `src/models/regression/` e `src/models/tree/`, substituídos pelos módulos específicos acima.
- `tests/test_briefing.py` e este registro.

## Validações e limitações

- `PYTHONPATH=src python -m unittest discover -s tests -v`: três testes passaram, usando cliente substituto ou mock, sem rede. Antes da implementação, os testes de cliente adicional e provedor desconhecido falharam como esperado.
- `PYTHONPATH=src python -m compileall -q src tests`, `python -m pip check`, `python src/main.py` e `git diff --check`: concluídos sem erros; o Git informou apenas aviso de conversão de fim de linha.
- A `.venv` não está disponível; os comandos Python usaram o Python do sistema, sem instalar dependências. O `pip check` refere-se a esse ambiente, não à instalação declarada do projeto.
- Os modelos, baselines e avaliação temporal são pontos de extensão e ainda não produzem experimentos ou resultados. Não foram feitas chamadas reais a provedores.
- A alteração pré-existente em `docs/entregavel-2.md` e o registro 008 foram preservados.
