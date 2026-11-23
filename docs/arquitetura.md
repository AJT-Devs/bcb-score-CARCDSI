# Arquitetura e escopo científico vigente

Atualização de 22/11/2026: os modelos principais são CatBoost e Chronos-2, com baselines temporais. Os entregáveis históricos e o plano Qwen preservam decisões anteriores e não descrevem o experimento vigente. A arquitetura anterior continha principalmente pontos de extensão para modelagem; esta rodada conecta um fluxo executável.

## Responsabilidades

1. `src/config/`: caminhos configuráveis e constantes oficiais. A chave real inclui origem e indexador.
2. `src/data/read/panel.py`: ingestão em chunks, validação de esquema/mês/chave, auditoria SHA256. O leitor genérico CSVReader permanece disponível. Nenhum modifica os brutos. O leitor compõe `data/validation/data_validator.py` e `panel_validator.py` para esquema, mês, totais e unicidade.
3. `src/data/preprocessing/transformer.py`: proporções com máscaras de denominador e numerador inválidos. Não treina modelos.
4. `src/features/temporal.py`: junções exatas por perfil e calendário para targets t+1, lags e média3, sem preenchimento de lacunas.
5. `src/models/`: baselines, cortes, métricas, dois CatBoost independentes e Chronos-2 local zero-shot. A seleção usa somente validação; o teste não refaz ajuste.
6. `src/pipelines/experiment.py`: composição e registro de dados, modelos, previsões, métricas, cobertura e limitações. `prediction_pipeline.py` recarrega CatBoost e reutiliza atributos na inferência em lote.
7. `src/visualization/experiment.py` e `export_paper.py`: figura, tabela TeX e evidências pequenas derivadas de resultados calculados.
8. `src/services/ia/`: interpretação desacoplada. O experimento exporta briefing numérico sem chamada externa.

Regressão linear múltipla, árvore e k-NN usam pipeline scikit-learn persistido em `models/classical_regression.py`, com imputação e codificação ajustadas no treino. O k-NN usa amostragem reproduzível do treino para limitar custo.

## Contratos e limites

Unidade: nove dimensões oficiais por mês. Não agregar perfis implicitamente nem somar totais/componentes. Brutos em `data/raw`; intermediários em `data/interim/2025`; resultados/modelos em `runs/` ignorado; evidências pequenas em `paper/generated`. Caminhos de dados e resultados são configuráveis.

Treino: origens jan–ago, targets fev–set; validação: set–out, targets out–nov; teste: novembro, target dezembro. Sem refit. Publicações históricas não reconstruídas: o atraso oficial torna a hipótese por data-base potencialmente otimista operacionalmente. Baseline sazonal12 indisponível.

CatBoost usa perfil, saldos e histórico; Chronos usa três proporções históricas por alvo. Comparação na interseção dos métodos efetivamente executados; cobertura total também é reportada. Piloto Chronos amostrado por chave para limitar custo CPU. Fine-tuning não implementado nem executado. Um ciclo anual e um mês de teste não comprovam generalização robusta.

Detalhes, comandos, funções e fluxos: [funcionamento efetivo](funcionamento-efetivo.md), [protocolo](protocolo-catboost-chronos2.md) e [execução](resultados-execucao.md).

## Resultados locais

O experimento grava métricas, previsões e `briefing_input.json` sem credenciais ou envio a terceiros. `services/ia/briefing.py` oferece somente formatação local determinística; as integrações Gemini e NVIDIA NIM foram removidas.
