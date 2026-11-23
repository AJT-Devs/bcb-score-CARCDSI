> Registro histórico do protocolo CatBoost/Chronos. Os modelos clássicos foram posteriormente adicionados; consulte o README e funcionamento efetivo para o fluxo atual.

# Decisão vigente em 22/11/2026

Este documento substitui as escolhas prospectivas de modelos dos entregáveis e do plano Qwen. Os entregáveis 1 e 2 e o plano Qwen são registros históricos, não evidência de experimentos executados. O pedido atual determina CatBoost, Chronos-2 e baselines temporais. Nenhum resultado de Qwen, regressão linear, árvore ou k-NN é reivindicado.

## Contrato científico

- Objetivo: previsão descritiva de risco agregado, por perfil, de duas proporções em t+1; não classificar tomadores individuais.
- Responsável pela decisão de escopo: solicitante do projeto. Não há promoção automática para produção.
- Sucesso: MAE menor na validação, reportando RMSE, R², cobertura e limites; teste final não seleciona configurações.
- Erros inaceitáveis: vazamento temporal, mistura de perfis, zero artificial, resultados simulados apresentados como reais.
- Hipótese: histórico recente e perfil contêm sinal; baseline ingênuo é a referência mínima.
- Restrição: apenas 2025, CPU e disponibilidade por data-base. Nenhum outro ano foi baixado.
- Fallback: abstenção explícita quando falta contexto; integração bloqueada não recebe números inventados.

## Dados e chave

Arquivos reais: `data/raw/scrdata_202501.csv` até `scrdata_202512.csv`. Cada arquivo tem cerca de 100 MB; a leitura faz chunks de 50 mil linhas. São 24 colunas originais, sem mudança dos nomes oficiais. A chave possui nove dimensões: `uf`, `segmento`, `cliente`, `cnae_ocupacao`, `porte`, `modalidade`, `submodalidade`, `origem`, `indexador`. Unidade de observação: uma chave completa por mês.

Não se agregam saldos no experimento atual. Se a granularidade mudar, será necessário somar saldos antes de dividir e revisar totais/componentes; a ingestão atual rejeita chaves duplicadas e categorias explícitas de total. Chaves vazias são excluídas e contadas. Não há deduplicação silenciosa. `Indisponível`, `Não informados` e `Outros` são categorias preservadas, não ausências numéricas. Alteração de grafia cria categoria/perfil distinto; não há ligação heurística de séries.

Saldos inválidos viram ausentes para o target; denominador precisa ser finito e positivo e numerador finito em `[0, carteira_ativa]`. Não se usa `numero_de_operacoes` (inclui `-1`) como saldo ou atributo. Não se tenta reidentificar registros protegidos nem inferir códigos de sigilo como zero. A metodologia consultada não foi suficiente para atribuir uma interpretação verificável ao `-1`; ele fica fora da modelagem.

Fonte: [catálogo BCB](https://dadosabertos.bcb.gov.br/dataset/scr_data), [metodologia V2](https://www.bcb.gov.br/pda/desig/metodologia_versao2.pdf), [arquivo anual 2025](https://www.bcb.gov.br/pda/desig/scrdata_2025.zip). Consulta em 22/11/2026. A licença indicada no catálogo é ODbL. CSVs brutos não foram publicados. Não foi possível comprovar a data original de extração; mtime é registrado separadamente de extração. SHA256 identifica exatamente o snapshot local.

## Protocolo congelado

| Etapa | Origens | Targets | Ajuste |
|---|---|---|---|
| Treino | jan–ago/2025 | fev–set/2025 | pesos CatBoost |
| Validação | set–out/2025 | out–nov/2025 | seleção de profundidade por alvo |
| Teste | nov/2025 | dez/2025 | somente avaliação |

Não há refit com validação. Assim, o target novembro não treina pesos para a origem setembro. A disponibilidade histórica de publicações não foi reconstruída. O BCB informa atualização no último dia útil e atraso de cerca de 30 dias; substituições de documentos podem revisar o snapshot. A hipótese de disponibilidade imediata por data-base é otimista para uso operacional. Não se declara backtest por vintage.

Janeiro pode treinar CatBoost com lags ausentes. Média3, drift3 e Chronos exigem origem e dois meses anteriores válidos; por isso a cobertura desses métodos começa em março. O target é unido pelo mesmo perfil e mês exato, não por deslocamento da próxima linha. Dezembro não é origem avaliada: janeiro/2026 está fora do escopo. Baseline sazonal de 12 meses é indisponível.

## Modelos e justiça da comparação

Dois CatBoost independentes evitam perder rótulos válidos do outro alvo. Candidatos: profundidades 4/6, 200 iterações, taxa 0,05, MAE, semente 42, quatro threads CPU. Strings categóricas com marcador de ausência; valores numéricos ausentes usam `nan_mode=Min`. Entradas: nove categorias, três saldos da origem, mês, duas proporções correntes, dois lags e média3 por alvo. Não se usa rótulo como atributo. CBM e JSON permitem recarga. O treinamento é supervisionado, não pré-treinamento fundacional.

Chronos-2: [checkpoint oficial](https://huggingface.co/amazon/chronos-2), revisão `29ec3766d36d6f73f0696f85560a422f50e8498c`, `chronos-forecasting==2.3.2`. Dois problemas univariados, contexto de três meses, horizonte um, mediana, CPU, lotes de 128, quatro threads, `cross_learning=False`. Nenhuma chamada de inferência remota: checkpoint baixado e executado localmente. Não há covariáveis futuras. Fine-tuning não foi implementado nem executado; é opcional e exigiria seleção separada em validação.

O piloto Chronos usa SHA256 do JSON da chave completa, resto zero módulo 1024. É uma amostra determinística, escolhida sem olhar targets, para limitar custo CPU. Métodos restantes são avaliados em todos os perfis elegíveis e na interseção em que Chronos efetivamente prevê. O piloto não representa cobertura integral. CatBoost usa mais informação que Chronos: a diferença de entradas impede atribuir ganhos somente à arquitetura. A integração permite execução integral pelo argumento `--chronos-sample-modulus 1`; isso não foi executado nesta rodada.

Baselines: ingênuo = valor da origem; média3 = média dos três meses contíguos; drift3 = valor atual + (atual − valor de dois meses atrás)/2. Nenhum completa lacunas. Perfil novo pode receber CatBoost; métodos históricos se abstêm sem janela. Perfil ausente na origem não recebe previsão e não pode ser avaliado nesse protocolo.

## Métricas e limitações

O corpus e o corte temporal do pré-treinamento Chronos não foram auditados quanto à presença do SCR. Um checkpoint público usado retrospectivamente não garante independência do benchmark; essa ameaça permanece mesmo com junções locais sem vazamento.

MAE principal e RMSE em proporções e pp (vezes 100); R² indefinido com n<2 ou alvo constante. Sem clipping; previsões fora de [0,1] contadas. Cobertura disponível = previsões finitas/rótulos válidos por target. Escopo `common` usa interseção dos métodos executados; sua cobertura é condicional à interseção e deve ser lida junto de `available`, cujo denominador é o conjunto total de rótulos elegíveis. Amostras diferentes não são comparação pareada.

Saídas por mês, UF, cliente e segmento são descritivas; grupos pequenos não recebem inferência estatística. Sem backtesting adicional, intervalos de confiança ou afirmação de generalização robusta. Um mês de teste e um ciclo sazonal limitam conclusões. Custo é tempo real por modelo e total no manifesto; pico de memória não instrumentado nesta rodada. Briefing não escolhe resultados nem calcula métricas.
