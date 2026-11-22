> Registro histórico preservado. Em 22/11/2026, a decisão vigente passou a CatBoost e Chronos-2 com baselines temporais. Este texto não comprova execução dos modelos anteriores. Consulte [o protocolo atual](protocolo-catboost-chronos2.md) e [o funcionamento efetivo](funcionamento-efetivo.md).

# Plano de desenvolvimento para treinamento do Qwen 3.5 9B

**Objetivo.** Medir se representações aprendidas pelo Qwen melhoram a previsão de inadimplência e ativos problemáticos agregados do SCR.data, um mês à frente, em comparação com as referências do projeto.

**Escopo.** O [Entregável 1](entregavel-1.md) define as proporções e o papel do LLM no briefing. O [Entregável 2](entregavel-2.md) define o horizonte, os regressores, os baselines e as métricas. A [arquitetura atual](arquitetura.md) já possui leitura e cálculo inicial de proporções. O painel temporal, o treinamento e a avaliação ainda precisam ser implementados.

**Desenho experimental.** Usar o backbone textual do checkpoint oficial `Qwen/Qwen3.5-9B` como extrator de atributos e uma cabeça de regressão supervisionada com duas saídas numéricas. O código calcula os rótulos e avalia as previsões. A cabeça é executada em `src/models/`, sem geração de texto no caminho da previsão. O briefing em `src/services/ia/` continua consumindo resultados calculados pelo pipeline. O Qwen entra como modelo experimental adicional. [Checkpoint oficial](https://huggingface.co/Qwen/Qwen3.5-9B) · [Arquitetura em Transformers](https://huggingface.co/docs/transformers/main/model_doc/qwen3_5).

## 1. Construir o painel supervisionado

- [ ] Inventariar `data/raw/` por mês de referência, esquema, cobertura e disponibilidade em cada origem de previsão. Há 12 CSVs locais na inspeção inicial. Confirmar os meses em `data_base` antes de definir cortes. Ler arquivo a arquivo ou em chunks com separador `;` e preservar os brutos.
- [ ] Fixar a granularidade do perfil com as dimensões do entregável (`uf`, `segmento`, `cliente`, `cnae_ocupacao`, `porte`, `modalidade`, `submodalidade`). Validar unicidade por perfil e mês e distinguir duplicatas de linhas legítimas de granularidade mais fina. Quando agregar, somar os saldos elegíveis e então dividir. Documentar a granularidade e os filtros aplicados.
- [ ] Reusar `src/data/preprocessing/transformer.py` para calcular `proporcao_inadimplencia = carteira_inadimplencia / carteira_ativa` e `proporcao_ativos_problematicos = ativo_problematico / carteira_ativa`. Marcar denominador zero como ausente, auditar valores não finitos ou fora do intervalo admitido e contabilizar exclusões por variável e mês.
- [ ] Em `src/features/`, construir amostras com chave perfil, mês de origem `t` e mês-alvo `t+1`. Juntar os rótulos pelo mês de calendário e pelo mesmo perfil. Se faltar o mês seguinte ou o alvo for inválido, marcar o rótulo como indisponível. Usar somente dados conhecidos na origem, considerando o atraso de publicação. Testar com painel sintético contendo mês faltante, perfis distintos, divisor zero e agregação de saldos com pesos diferentes.

**Aceite.** Um painel versionado por manifesto identifica colunas, janelas históricas, meses, disponibilidade, filtros e contagens de amostras por alvo. Os testes demonstram a correspondência exata entre origem e mês-alvo.

## 2. Fixar as divisões e as referências

- [ ] Implementar `src/models/temporal_validation.py` com treino inicial, validação cronológica com origens expansivas quando houver histórico e bloco final de teste reservado por mês-alvo. Em cada origem, admitir no ajuste apenas rótulos já disponíveis naquela data. Ajustar codificação, imputação e escalas apenas no treino de cada divisão. Escolher janelas e hiperparâmetros pela validação, congelando as escolhas antes de abrir o teste.
- [ ] Implementar em `src/models/` regressão linear múltipla, árvore de decisão e k-NN com normalização numérica. Implementar em `baselines.py` último valor observado, referência sazonal do mesmo mês do ano anterior, média móvel e drift. Verificar disponibilidade desses valores na origem. Quando faltar histórico para a comparação sazonal, registrar ausência e cobertura.
- [ ] Em `evaluation.py`, alinhar previsões e observados por perfil e mês-alvo. Calcular MAE principal em pontos percentuais (`100 × MAE` para proporções na escala 0–1), RMSE em pontos percentuais e R² sem unidade, por alvo. Indicar R² indefinido para amostras insuficientes ou alvo constante. Testar as fórmulas com resultados calculados à mão e verificar que alterações em dados futuros não afetam atributos nem ajuste de origens anteriores.

**Aceite.** O pipeline gera uma tabela auditável dos modelos do entregável e dos baselines disponíveis. Se o histórico permitir apenas um teste curto, tratar a rodada como piloto e ampliar a cobertura mensal antes de concluir sobre generalização. Muitas linhas de perfis por mês não aumentam a quantidade de períodos independentes.

## 3. Treinar o Qwen com uma cabeça de regressão

- [ ] Em ambiente de treinamento isolado, verificar a combinação de Python 3.14, GPU, driver, PyTorch, Transformers, PEFT e, para o teste em 4 bits, bitsandbytes. Fixar versões e revisão do checkpoint e do tokenizador após instalar e validar a pilha. Medir memória de pico e tempo por lote em um piloto. Se não houver combinação compatível, documentar a limitação e a configuração de treinamento separada antes da execução maior. [Quantização com bitsandbytes](https://huggingface.co/docs/transformers/quantization/bitsandbytes).
- [ ] Em `src/models/qwen_regression.py`, serializar os atributos permitidos em ordem estável, incluindo contexto do perfil, proporções históricas disponíveis, ausências e calendário. Fixar o formato e verificar truncamento. Extrair a representação do último token válido usando a máscara de atenção e ligá-la a uma cabeça de duas saídas na escala 0–1. Treinar com perda MAE média sobre rótulos válidos, com máscara por alvo, e inspecionar a contribuição de cada alvo.
- [ ] Treinar primeiro apenas a cabeça com o backbone congelado. Depois treinar cabeça e adaptadores LoRA no backbone textual, usando as mesmas divisões e entradas. Começar com uma configuração curta (por exemplo, 512 tokens, microlote de uma amostra e acumulação de gradientes), condicionada à cobertura das entradas e à memória medida. Usar QLoRA em 4 bits se o piloto confirmar carregamento, gradientes e estabilidade. Selecionar checkpoint pela média dos MAEs dos dois alvos na validação e inspecionar ambos separadamente.
- [ ] Orquestrar em `src/pipelines/training_pipeline.py` e `prediction_pipeline.py`. Implementar teste local sem download com backbone substituto ou configuração mínima. No piloto na GPU, confirmar que a perda é finita, que os pesos previstos recebem gradiente, que a cabeça aprende em um lote pequeno e que recarregar cabeça, adaptador e configuração reproduz as previsões dentro da tolerância definida.

**Aceite.** O piloto salva um checkpoint recarregável e devolve duas previsões numéricas finitas para cada amostra. O manifesto registra cortes, atributos, configuração, sementes, versões, checkpoint, hardware e custo medido. Pesos e dados de execução ficam fora do Git.

## 4. Comparar e registrar no artigo

- [ ] Comparar os quatro baselines quando elegíveis, os três regressores, Qwen congelado com cabeça treinada e Qwen com ajuste de adaptadores. Reportar cobertura de cada método e usar a mesma amostra elegível para a comparação pareada por alvo. Usar o mesmo corte de disponibilidade de informações em todos os modelos.
- [ ] Para cada alvo, congelar a melhor referência convencional pela validação. No teste, reportar diferença de MAE em pontos percentuais, RMSE, R², desempenho mês a mês, erros por perfil com cobertura suficiente e custo de treinamento e inferência. Se houver meses suficientes, estimar a incerteza da diferença respeitando a dependência temporal. Registrar resultados inconclusivos quando a cobertura temporal for curta.
- [ ] Documentar no artigo os filtros, a granularidade, a amostra, o horizonte, as divisões, a configuração do Qwen e as limitações. Exportar métricas calculadas pelo código para os briefings. Registrar o resultado dos dois alvos separadamente, inclusive quando o ajuste tiver ganho em apenas um deles.

**Aceite.** O experimento entrega um manifesto e uma tabela de comparação reproduzível. A eventual adoção do Qwen depende do ganho sobre a referência, da estabilidade entre meses e do custo observado.
