# 013 — Entregável 2: modelos clássicos e execução local

## Prompt integral do usuário

Implemente o que falta no projeto para cumprir a proposta do entregável 2,
seguindo os requisitos abaixo.

OBJETIVO

O projeto deve funcionar diretamente pelo terminal, sem depender de qualquer outro LLM. O Codex será opcional: pode executar comandos e explicar resultados, mas não participa dos cálculos nem é necessário para
treinar, testar ou avaliar os modelos.

ESCOPO

1. Implemente os modelos originalmente propostos no entregável 2:
   - regressão linear múltipla;
   - árvore de decisão para regressão;
   - k-vizinhos mais próximos para regressão (k-NN).

2. Integre esses modelos ao fluxo experimental existente, preservando os
   baselines, o CatBoost e o Chronos-2. Permita que uma pessoa escolha quais
   modelos executar por comandos no terminal.

3. Use exclusivamente os dados disponíveis de 2025. Mantenha a separação
   temporal existente entre treino, validação e teste. Não use dados futuros
   para treinar previsões de meses anteriores nem escolha modelos com base
   no resultado do teste final.

4. Avalie separadamente os dois alvos existentes:
   - carteira_inadimplencia / carteira_ativa;
   - ativo_problematico / carteira_ativa.

5. Compare os modelos com MAE, RMSE e R². Registre também cobertura,
   quantidade de observações, tempo de execução e previsões fora de [0, 1].
   Para comparações entre modelos, identifique claramente quando os
   resultados se referirem aos mesmos perfis e quando não se referirem.

6. O baseline sazonal anual não pode ser avaliado adequadamente com apenas
   2025. Registre essa limitação de forma explícita; não invente resultados
   nem crie dados artificiais para apresentá-los como resultados reais.

7. Considere o custo de processamento e memória, principalmente do k-NN.
   Faça uma avaliação prática de custo antes de executar uma comparação
   integral. Se uma amostra de treino for necessária, use um procedimento
   reproduzível que não utilize dados futuros nem os resultados do teste
   para selecionar a amostra. Registre tamanho, regra de seleção,
   parâmetros e limitações. Não apresente a amostra como se fosse a base
   completa.

8. Ajuste o pré-processamento de cada modelo somente com dados de treino.
   Trate valores ausentes e categorias não vistas sem vazamento temporal.
   Preserve os nomes e a semântica das colunas oficiais do SCR.

9. Salve os modelos e as informações necessárias para reproduzir as
   previsões, incluindo o pré-processamento, a configuração e as métricas.
   Use os mecanismos e formatos já existentes no projeto quando fizer
   sentido.

REMOÇÃO DAS INTEGRAÇÕES ANTIGAS

10. Remova as integrações ativas de Gemini e NVIDIA NIM, pois não serão
    utilizadas. Examine e atualize os consumidores, testes, configurações,
    exemplos de variáveis de ambiente e documentação relacionados.

11. Preserve o fluxo que gera métricas e resultados legíveis. O processamento e a avaliação devem continuar funcionando
    sem credenciais, serviços externos de LLM ou chamadas de rede a eles.
    Preserve os registros históricos existentes.

VALIDAÇÃO E ENTREGA

12. Antes de alterar o código, examine a arquitetura, os testes e o estado
    atual do repositório. Não reverta alterações de outras pessoas.

13. Adicione testes relevantes para os novos modelos, incluindo separação
    temporal, tratamento de dados ausentes, avaliação e recarga dos modelos.
    Não faça chamadas reais a provedores externos nos testes.

14. Execute os testes existentes e os novos, compile o código e rode
    pip check no ambiente .venv. Execute também uma validação com os dados
    reais quando for viável. Se algum treinamento for inviável por tempo,
    memória ou outro recurso, explique a limitação e não afirme que foi
    executado.

15. Atualize as instruções para mostrar, com exemplos em PowerShell, como
    preparar o ambiente, executar testes, escolher e treinar modelos,
    consultar resultados e fazer previsões sem o Codex.

16. Ao terminar, informe o que foi implementado, os comandos disponíveis,
    os resultados efetivamente obtidos e as limitações que permanecerem.
    Diferencie claramente resultados reais de testes com dados sintéticos.

IMPORTANTE

- Não faça commits, não crie branches e não altere os dados brutos.
- Não inclua credenciais ou segredos em código, logs ou resultados.
- Não peça confirmação para escolhas técnicas rotineiras: use o contexto do
  projeto e siga até concluir o trabalho autorizado.

### Instrução posterior integral

```kotlin
Não edite, regenere ou compile o artigo nem qualquer arquivo dentro de
paper/. Mantenha o paper exatamente como está. Se as mudanças tornarem
alguma informação do artigo desatualizada, apenas informe isso na resposta final.
```

## Decisão arquitetural e ações

Três regressores independentes por alvo foram integrados ao experimento com pipeline scikit-learn persistido, imputação mediana, escala e one-hot ajustados apenas no treino. Árvores usam profundidade 12, folha mínima 5, semente 42; k-NN usa até cinco vizinhos, força bruta, e amostra uniforme sem reposição do treino com semente 42, limitada por padrão a 5.000 linhas por alvo. É uma aproximação cuja geometria e seleção podem afetar o desempenho. A divisão e a seleção de CatBoost permanecem temporais; o teste não escolhe parâmetros. Escopo comum usa a interseção dos métodos, e disponível pode ter perfis diferentes. Inferência bloqueia origens anteriores à disponibilidade dos rótulos de treino. Integrações Gemini/NVIDIA foram removidas e briefing local preserva números sem rede. Baseline sazonal anual é impossível com 2025. Chronos continua opcional e pode precisar baixar checkpoint.

## Arquivos alterados/criados

- `src/models/classical_regression.py`; `src/pipelines/experiment.py`, `evaluation_pipeline.py`, `prediction_pipeline.py`; `src/visualization/experiment.py`.
- `src/services/ia/__init__.py`, `briefing.py`, `report_generator.py`; removidos `client.py` e `prompts.py`; `src/config/settings.py`, `.env.example`.
- `tests/test_classical.py`, `tests/test_pipeline.py`, `tests/test_briefing.py`.
- `README.md`, `docs/arquitetura.md`, `docs/funcionamento-efetivo.md`, `docs/protocolo-catboost-chronos2.md`, `AGENTS.md`, este registro.
- Saídas locais ignoradas: `runs/2025-cost-pilot`, `runs/2025-real-sample`.

## Validação e resultados

- `.venv/Scripts/python.exe -m unittest discover -s tests -v` com `PYTHONPATH=src`: 15 testes passaram, incluindo dados exclusivamente sintéticos para treinamento e avaliação.
- `python -m compileall -q src`, `python -m pip check`: concluídos; nenhuma dependência quebrada.
- Piloto real de custo antes da comparação: primeiras 10.000 linhas de janeiro e fevereiro, 9.474 rótulos válidos de treino, 1.000 previsões para um alvo. Linear 0,079 s / pico acumulado do processo 189,7 MB; árvore 0,103 s / 190,8 MB; k-NN 0,093 s / 266,6 MB, treinado com 5.000 linhas. Picos são acumulados e não isolados; amostra não representativa e não extrapolação de custo integral.
- Experimento real amostral: primeiras 10.000 linhas de cada CSV mensal, não representativas da distribuição nacional. Em `runs/2025-real-sample/result-final`, modelos clássicos e baselines foram executados nos dois alvos. Tempo conjunto dos dois alvos: linear 3,38 s, árvore 5,22 s, k-NN 8,64 s; inclui ajuste e previsões das partições de avaliação, na execução e máquina locais. Para inadimplência, treino k-NN 5.000 de 75.637 linhas elegíveis. A interseção de teste contém 8.843 perfis elegíveis; MAE em pp: ingênuo 3,834; linear 5,303; árvore 5,206; k-NN 6,441. Para ativos problemáticos: ingênuo 4,581; linear 5,949; árvore 6,069; k-NN 7,621. RMSE, R², cobertura e valores fora de faixa estão em `metrics.csv`; não são resultados nacionais.
- `pipelines.prediction_pipeline` recarregou os três modelos e baselines para novembro: os resultados coincidiram com as previsões do experimento em 10.000 perfis, dois alvos e seis métodos; `pipelines.evaluation_pipeline` também foi executado.
- A comparação integral não foi executada; os CSVs brutos somam 1,22 GB e o pipeline consolida painéis e junções em memória. O piloto não mede memória ou tempo necessários para a base completa. CatBoost e Chronos não foram executados no experimento real desta tarefa. Não se comprova inviabilidade da execução integral.
- `git diff --check` passou. Nenhum arquivo em `paper/` foi editado ou compilado. O artigo continua descrevendo o estudo anterior de CatBoost e Chronos e não incorpora os três novos modelos.
