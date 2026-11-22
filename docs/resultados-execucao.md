# Execução real de 22/11/2026

## Ambiente e dados

Python portátil 3.14.0 foi baixado dentro do projeto e `.venv` criado; todos os comandos Python foram executados com `.venv/Scripts/python.exe`. Bibliotecas originais instaladas nas versões fixadas. Adicionadas e instaladas `catboost==1.2.10` e `chronos-forecasting==2.3.2`; PyTorch 2.15.0+cpu, sem CUDA disponível nessa instalação. Bibliotecas não foram instaladas no sistema operacional.

Foram encontrados e lidos os 12 CSVs em `data/raw/`, janeiro–dezembro de 2025: **3.764.842 observações**, **1.215.722.830 bytes** e **399.480 perfis distintos**. Apenas **236.638** perfis aparecem em todos os doze meses. Não faltam meses globais, mas há lacunas por perfil. `data_audit.json` registra SHA256 por arquivo; data original de extração desconhecida. A modificação local indicada nos arquivos é 17/09/2026; isso não comprova extração.

Leitura UTF-8, separador `;`, vírgula decimal, campos entre aspas. Nove dimensões reais preservadas, incluindo `origem` e `indexador`. Não se agregam níveis, duplicam totais ou somam duplicatas. Não foram encontradas chaves vazias nem razões inválidas pelas regras implementadas. Categorias especiais mantidas; número de operações não é usado. A auditoria de categorias registra o desaparecimento de uma submodalidade após janeiro, sem unificação automática.

Na origem novembro há 308.434 perfis observados, dos quais 11.570 não têm o mesmo perfil em dezembro; portanto há 296.864 rótulos elegíveis por alvo. Para a média de três meses, 22.396 perfis de novembro não têm janela completa, antes da interseção com rótulos. `panel_audit.json` detalha cada mês e quantidade de observações por perfil. Dezembro não tem t+1 no escopo e não é origem avaliada.

## Protocolo

Origens de treino janeiro–agosto (targets fevereiro–setembro); validação setembro–outubro (targets outubro–novembro); teste novembro (target dezembro). Sem refit com validação. Targets e lags por mês calendário exato e perfil completo. Ausência não é zero. Métricas não ponderadas por saldo, em proporção e pp. Sem clipping; valores fora do intervalo são contados.

Avaliação por data-base e snapshot local, sem vintages de publicação. O BCB informa atraso aproximado de 30 dias e possibilidade de substituições; resultados podem ser otimistas operacionalmente. Sazonal12 indisponível. Não foram baixados outros anos. Sem causalidade, risco individual ou prova de generalização robusta.

## Chronos-2 executado

Comando: `python -m pipelines.chronos_pipeline --output runs/chronos-pilot`, precedido de `PYTHONPATH=src`, usando o Python do venv. Pipeline isolado sobre o painel preparado, sem refazer CatBoost.

Checkpoint público executado **localmente**, revisão `29ec3766d36d6f73f0696f85560a422f50e8498c`; dois alvos univariados, contexto três meses, horizonte um, mediana, CPU com quatro threads, sem cross-learning. **Zero-shot executado; fine-tuning não executado.** Download cerca de 478 MB, registrado separadamente; não houve envio de CSVs.

Amostra determinística: SHA256 da chave JSON UTF-8, resto zero módulo 1024. Foram selecionadas **384 chaves** entre todos os perfis. No teste há **284 rótulos válidos** na amostra, dos quais **267** possuem contexto completo comum aos quatro métodos abaixo. Cobertura Chronos sobre os rótulos da amostra: **94,014%**. A cobertura integral sobre todos os perfis é muito menor e deve ser consultada no experimento completo; esta tabela não representa todo o painel.

| Target | Método | n comum | MAE (pp) | RMSE (pp) | R² |
|---|---|---:|---:|---:|---:|
| Inadimplência | Ingênuo | 267 | 3,822464 | 14,406837 | 0,802631 |
| Inadimplência | Média3 | 267 | 4,935687 | 15,263259 | 0,778468 |
| Inadimplência | Drift3 | 267 | 5,107895 | 15,881296 | 0,760165 |
| Inadimplência | Chronos-2 | 267 | 4,064837 | 14,566307 | 0,798238 |
| Ativos problemáticos | Ingênuo | 267 | 3,733121 | 13,025259 | 0,876387 |
| Ativos problemáticos | Média3 | 267 | 5,866780 | 15,491147 | 0,825154 |
| Ativos problemáticos | Drift3 | 267 | 5,667232 | 15,835316 | 0,817298 |
| Ativos problemáticos | Chronos-2 | 267 | 4,072841 | 13,297577 | 0,871165 |

Nesta amostra e mês, o ingênuo teve MAE menor que Chronos nos dois targets. Isso não prova superioridade geral. Houve 17 previsões Chronos fora de [0,1] entre as 267 avaliadas para inadimplência, e 31 para ativos problemáticos, sem ocultação ou clipping. Contando previsões sem rótulo disponível, são 19 e 34. A execução isolada, incluindo leitura preparada, levou **74,613 segundos** no ambiente em uso; não é tempo puro de inferência. O custo da ingestão original e do download é separado.

## Validações e compilação

- `python -m unittest discover -s tests -v`: **16 testes aprovados**, sem provedores reais. Fixtures identificadas como sintéticas, incluindo integração CSV→atributos→treinamento→persistência→avaliação e equivalência da reavaliação salva.
- `python -m compileall -q src`: aprovado nas verificações executadas.
- `python -m pip check`: `No broken requirements found`.
- Docker CLI encontrada fora do PATH; `docker compose config` válido. `docker compose up --build` falhou porque o engine/named pipe não estava disponível, inclusive após tentativa de iniciar Desktop oculto. Nenhum sucesso de container é reivindicado.
- Tectonic e Poppler encontrados. Artigo compilado com referências resolvidas e fonte Times/T1. Inspeção visual intermediária das quatro páginas sem cortes; resumos na primeira página. Exportação final de resultados requer nova compilação e inspeção, registrada no encerramento.

Não foram feitas chamadas reais aos clientes de briefing; somente exportação do pacote de métricas e testes locais. Nenhum segredo, CSV bruto ou modelo foi incluído no Git. Não houve commit, branch, push ou publicação.

## Estado do experimento completo

O comando `python -m pipelines.experiment --output runs/2025-pilot --models catboost,chronos` concluiu o treinamento dos dois CatBoost e a avaliação dos baselines no painel completo. A tentativa Chronos dessa execução inicial tentou resolver o checkpoint remoto e foi bloqueada pela rede. O piloto local independente já tinha concluído com o checkpoint baixado. As execuções originais foram preservadas e consolidadas em `runs/2025-comparison` com junção exata por perfil, origem, mês-alvo e target; o hash do dicionário de perfis foi conferido. O código final prefere o checkpoint local quando disponível. Nenhum número foi simulado para contornar o bloqueio.

### CatBoost e comparação consolidada

Dois regressores treinados com **2.415.028 amostras por alvo**; **591.891** rótulos de validação. Profundidade escolhida: **6 para inadimplência e 4 para ativos problemáticos**, com 200 iterações, taxa 0,05, MAE e semente 42. Sem refit. Treinamento dos quatro candidatos e predição do CatBoost: **1508.717 segundos**. Pico de memória não medido; leituras pontuais do processo indicaram aproximadamente 5–6,4 GB, sem caracterizar pico.

Na interseção comum aos cinco métodos executados, há **267 perfis por target**. A cobertura do Chronos em relação aos **296.864** rótulos totais do teste é **0,08994%**; a taxa de 94,014% citada antes é condicional à amostra SHA256.

| Target | Método | n comum | MAE (pp) | RMSE (pp) | R² | Fora de [0,1] |
|---|---|---:|---:|---:|---:|---:|
| Inadimplência | naive | 267 | 3.822464 | 14.406837 | 0.802631 | 0 |
| Inadimplência | mean3 | 267 | 4.935687 | 15.263259 | 0.778468 | 0 |
| Inadimplência | drift3 | 267 | 5.107895 | 15.881296 | 0.760165 | 12 |
| Inadimplência | catboost | 267 | 3.863386 | 14.279879 | 0.806094 | 92 |
| Inadimplência | chronos | 267 | 4.064837 | 14.566307 | 0.798238 | 17 |
| Ativos problemáticos | naive | 267 | 3.733121 | 13.025259 | 0.876387 | 0 |
| Ativos problemáticos | mean3 | 267 | 5.866780 | 15.491147 | 0.825154 | 0 |
| Ativos problemáticos | drift3 | 267 | 5.667232 | 15.835316 | 0.817298 | 23 |
| Ativos problemáticos | catboost | 267 | 3.860552 | 12.980211 | 0.877241 | 16 |
| Ativos problemáticos | chronos | 267 | 4.072841 | 13.297577 | 0.871165 | 31 |

O ingênuo teve menor MAE nos dois targets tanto na comparação comum quanto no conjunto completo de rótulos para os métodos de cobertura integral. No conjunto completo, MAE ingênuo/CatBoost: **3,422765/3,475328 pp** para inadimplência e **4,081347/4,145032 pp** para ativos problemáticos. CatBoost apresentou RMSE menor que o ingênuo nesses conjuntos, mostrando que a ordenação depende da métrica; MAE permaneceu pré-definida como principal. Não se conclui superioridade robusta de nenhum método.

Previsões CatBoost fora de [0,1] entre pares avaliáveis completos: **92.681** para inadimplência e **12.138** para ativos problemáticos. Sem clipping. A tabela CSV inclui também previsões fora do intervalo sem target disponível (`out_of_range_all`). Os erros por origem, UF, cliente e segmento estão em `paper/generated/metrics.csv`; recortes são descritivos e podem ter n pequeno.

Comandos finais (sempre com Python do venv e `PYTHONPATH=src`):

```powershell
.\.venv\Scripts\python.exe -m pipelines.merge_forecasts runs/2025-pilot runs/chronos-pilot --output runs/2025-comparison
.\.venv\Scripts\python.exe -m visualization.export_paper runs/2025-comparison
```

A consolidação não retreina modelos nem altera previsões; reavalia os mesmos valores e preserva os manifestos de origem. Os hashes de código no manifesto consolidado são da finalização, não uma alegação de captura no início da execução longa. Refatorações posteriores de auditoria e avaliação não mudaram atributos, cortes ou hiperparâmetros.

### Encerramento e inspeção final

Artigo final em `paper/main.pdf`: **5 páginas A4**, compilado com Tectonic e BibTeX, usando o template SBC local preservado. Todas as cinco páginas foram renderizadas com Poppler e inspecionadas visualmente: resumos na primeira página, tabelas legíveis com legenda acima, figura com legenda abaixo, referências resolvidas e sem overflow. Permanecem avisos de underfull hbox/vbox (espaçamento) e avisos não impeditivos de pacote/codificação sob XeTeX; não houve overfull nem referência indefinida. O Fontconfig emitiu mensagem de configuração, mas as fontes Times do template foram incorporadas e renderizadas corretamente.

Autores informados pelo usuário: **João Alves Passos e Túlio Kenji Yoshimura**. Afiliação e e-mails não foram fornecidos; a afiliação permanece pendente e nenhum e-mail foi inventado. Limite de páginas do evento não informado.

Validação da consolidação: MAE, RMSE, R², n e contagem fora do intervalo permaneceram iguais às execuções reais de origem, com tolerância de `1e-12`. O CSV consolidado apenas alinha previsões e recalcula a interseção comum. As 16 verificações automatizadas passaram; compileall, pip check e git diff --check aprovados. Resultados não incluem mocks nem fixtures sintéticas.
