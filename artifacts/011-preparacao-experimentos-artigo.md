# Preparação, experimentos e artigo — 22/11/2026

## Prompt integral do usuário

Atue no repositório atual do projeto CARCDSI. Complete a preparação de dados, os experimentos e o artigo científico, tomando os documentos em docs/ como referência de escopo. A mudança de decisão deste pedido prevalece sobre escolhas anteriores: os modelos principais serão CatBoost e Chronos-2, com baselines temporais. Trabalhe de forma autônoma, preserve alterações existentes e não invente resultados.\
\- Leia AGENTS.md, instruções aplicáveis, todos os arquivos pertinentes em docs/, a estrutura de src/, requirements.txt, os testes existentes e o conteúdo e modelo TeX em paper/.\
\- Localize e siga as skills disponíveis para construção do artigo e para sua formatação, bem como instruções de arquivos relacionados. Identifique-as pelo que encontrar no projeto, sem supor seus nomes. Caso uma não esteja disponível, prossiga com os recursos existentes e registre a limitação.\
\- Identifique os CSVs dos 12 meses de 2025 do SCR.data no local existente no projeto. Não presuma que estejam em src/ ou que haja dados presentes: descubra os caminhos reais. Preserve os dados brutos e não os publique se forem grandes ou houver restrições.\
\- Verifique o estado de implementação antes de modificá-lo. Ajuste os documentos de arquitetura e planejamento afetados para refletir os modelos efetivamente utilizados. Preserve entregas históricas já submetidas, identificando decisões anteriores e a atualização, em vez de reescrever fatos históricos.\
O objetivo é prever, para cada perfil elegível, um mês à frente, as proporções de inadimplência e de ativos problemáticos. Considere como base os CSVs mensais de janeiro a dezembro de 2025, usando somente os dados encontrados e registrando versões, procedência, datas de extração e limitações.\
\- Inspecione cabeçalho real, codificação, separador, formato decimal, tipos, dicionário e metodologia oficiais disponíveis. Mapeie os nomes das colunas reais, preservando nomenclatura oficial e documentando qualquer normalização técnica.\
\- Defina explicitamente a unidade de observação e a chave da série com base nas dimensões realmente existentes; não misture perfis nem níveis de agregação, nem duplique totais e componentes. Documente filtros e tratamento de sigilo, códigos especiais, ausências, duplicatas, alterações de categorias e meses faltantes, sem interpretar ausente como zero automaticamente.\
\- Calcule carteira_inadimplencia / carteira_ativa e ativo_problematico / carteira_ativa; denominador zero ou inválido gera ausente. Registre contagens de exclusão e agregue saldos antes de dividir, quando necessário.\
\- Separe dados brutos, intermediários e resultados; permita configuração de caminhos e execução reproduzível sem depender de caminhos absolutos. Use leitura eficiente adequada ao tamanho dos arquivos.\
\- Construa as duas metas do mês t+1 para cada perfil. Faça junção por perfil e mês calendário exato, não simplesmente pela próxima linha: nunca associe meses não consecutivos. Construa lags e médias móveis apenas com histórico disponível até o instante de previsão, sem atravessar séries.\
\- Verifique datas de publicação, revisões e disponibilidade real dos dados quando houver evidência. Se não for possível reproduzir o histórico das publicações, declare que a avaliação usa data-base e dados disponíveis na extração, e que pode ser otimista operacionalmente.\
\- Use divisão cronológica comum a todos os modelos e defina um protocolo explícito. Como ponto de partida, origens de previsão em janeiro–agosto para treino, setembro–outubro para validação e novembro para teste, correspondendo a targets de fevereiro–setembro, outubro–novembro e dezembro, respectivamente. Ajuste somente se necessário por janelas de histórico ou dados ausentes; documente exatamente quais meses são usados como entrada e target. A construção de janelas pode reduzir significativamente as observações. Nunca use o target de novembro para treinar um modelo que simule uma previsão cuja origem ocorra antes de esse target estar disponível.\
\- Separe seleção de hiperparâmetros e ajustes do teste final. Considere backtesting adicional por origem temporal dentro do desenvolvimento, se viável. Não apresente os resultados como prova de generalização robusta: há apenas 12 meses e um único ciclo sazonal. Baseline sazonal de 12 meses não é avaliável para uma previsão de um mês à frente com apenas os 12 meses de 2025; registre-o como indisponível sem buscar outros anos sem autorização.\
\- Determine regras para perfis novos, curtos ou ausentes, e reporte a cobertura de cada método. Para comparações principais, avalie os mesmos perfis, datas, targets e informações disponíveis; explicite quaisquer diferenças e não complete lacunas com valores futuros.\
\- Implemente baseline ingênuo (última observação válida no mês imediatamente anterior à previsão); média móvel e drift apenas onde existirem históricos válidos suficientes. Identifique casos sem previsão e reporte cobertura.\
\- Treine CatBoost para regressão usando características do perfil e atributos históricos disponíveis. Escolha abordagem de dois modelos ou saída múltipla de modo fundamentado e reprodutível; trate categorias e ausência segundo comportamento verificado da biblioteca. Ajuste hiperparâmetros apenas na validação; salve configuração, semente e modelos.\
\- Implemente Chronos-2 (amazon/chronos-2) pré-treinado para previsão de um mês, especificando checkpoint, versão, contexto, variáveis, estratégia para os dois targets e configuração de execução. Faça um experimento sem ajuste e, se os recursos e a biblioteca efetivamente permitirem, fine-tuning no treino, selecionando-o por validação. Treinar CatBoost nos dados é treinamento supervisionado; não o descreva como pré-treinamento de um modelo fundacional. Fine-tuning é opcional e não deve ser relatado como realizado sem execução.\
\- Garanta condições justas ou apresente claramente o contraste quando as entradas diferirem; informe custo e limites computacionais. Se checkpoint, rede, dependências, memória ou dados impedirem uma execução, mantenha a integração executável e documente o bloqueio, comandos e testes realizados. Nunca use previsões ou dados simulados como resultados reais.\
\- Avalie cada target com MAE principal, RMSE e R², distinguindo proporções de pontos percentuais; registre amostras por métrica, cobertura e condições em que R² não está definido. Compare baselines e modelos no mesmo conjunto elegível. Apresente ainda erros por período e grupos relevantes quando houver amostras, e identifique previsões fora do intervalo válido sem ocultá-las; qualquer pós-processamento deve ser pré-definido e aplicado igualmente quando cabível.\
\- Implemente pipelines executáveis para ingestão, validação, preparação, atributos, divisão, treinamento, previsão e avaliação, reutilizando a arquitetura existente e mantendo serviços de LLM desacoplados. Organize saídas para reproduzir tabelas e gráficos e alimentar o briefing com números calculados.\
\- Não envie dados confidenciais ou credenciais a serviços externos; não exponha segredos. O gerador de briefing não calcula métricas nem altera previsões. Inclua metadados, filtros, registros de execução, cobertura, limitações e dependências em requirements.txt conforme as convenções existentes.\
\- Após implementar e executar as etapas possíveis, crie em docs/ um Markdown didático para explicar o funcionamento efetivo do projeto, baseado no código final, e não em um desenho hipotético. Inclua fluxogramas Mermaid do caminho dos CSVs brutos até a avaliação e os resultados, além dos fluxos de treinamento, inferência e briefing quando implementados. Para cada etapa, apresente caminhos reais relativos ao repositório, arquivos, funções e classes responsáveis, bibliotecas usadas e seu papel, entradas e saídas, formatos, transformações e comandos reais para execução. Inclua pequenos trechos de código retirados da implementação e explique-os em português, junto a exemplos de dados de entrada e saída sem inventar resultados. Explique as divisões temporais, os targets, os baselines, o treinamento do CatBoost, o uso e eventual fine-tuning do Chronos-2, as métricas e onde os artefatos são armazenados. Distinga o que foi implementado, executado, opcional ou permanece pendente; descreva bloqueios reais. Atualize o fluxo ao final para refletir fielmente o projeto entregue.\
\- Execute testes relevantes: alinhamento por mês e perfil, lacunas temporais, denominador zero, divisão sem vazamento, dependência estrita do passado, métricas, cobertura e integração entre etapas. Adicione testes com dados pequenos e sintéticos identificados como tal. Execute treinamento e avaliação reais quando recursos e dados permitirem; reporte comandos e resultados efetivos.\
\- Utilize as skills e o template TeX encontrados em paper/; preserve a estrutura e as exigências de formatação. Escreva em português, com resumo em português e abstract em inglês, incluindo palavras-chave e keywords se exigidas pelo template.\
\- Aborde problema, dados agregados, objetivos, metodologia, protocolo temporal, baselines, CatBoost, Chronos-2, métricas, resultados reais, discussão, limitações e referências verificáveis. Evite alegações de causalidade ou risco individual.\
\- Use somente fontes reais verificadas e resultados efetivamente produzidos. Se algo não for executável, marque explicitamente a seção como pendente e não preencha tabelas com números inventados; mantenha o texto coerente com o estado dos experimentos.\
\- Gere tabelas e gráficos a partir dos resultados quando disponíveis, compile o PDF se as ferramentas existirem e verifique referências, overflow e apresentação. Caso não compile, entregue o TeX consistente e explique o bloqueio.\
Informe arquivos alterados, protocolo realmente adotado, disponibilidade dos 12 meses, tratamentos, modelos efetivamente executados, métricas reais ou impedimentos, testes e compilação. Diferencie com clareza o que foi implementado do que foi treinado e avaliado. Não faça push nem publique o repositório sem solicitação explícita.

Docker está instalado na maquina, gere o venv e use o python do venv do projeto, nao existe python na maquina

## Estado inicial, hipótese e validação escolhida

Git inicialmente limpo. Foram lidos AGENTS.md, documentos de docs/, estrutura e módulos src/, testes, requisitos, template TeX e estilo local. Modelos/atributos/pipelines eram principalmente pontos de extensão. Hipótese: a preparação existente não considerava todas as dimensões e a leitura padrão não interpretava decimal vírgula; sem painel por calendário, deslocamentos poderiam associar meses errados. Validação: fixtures sintéticas pequenas com lacunas, perfis distintos e denominador zero, antes de avaliar os CSVs reais.

Skills encontradas: `.agents/skills/creating-sbc-paper/SKILL.md`, `mle-workflow/SKILL.md`, `scikit-learn/SKILL.md` e `scientific-thinking-scholar-evaluation/SKILL.md`; também skill PDF do runtime para inspeção visual. Sem delegação de subagentes. Template original preservado em `paper/template/`.

## Ações e decisão arquitetural

Python portátil 3.14.0 em `.tools/` e `.venv/` criado; todas as execuções Python usam `.venv/Scripts/python.exe`. Pacotes instalados no venv, incluindo CatBoost 1.2.10 e chronos-forecasting 2.3.2. Ambos tiveram wheels compatíveis; PyTorch instalado é CPU. Nada instalado como Python do sistema. Novos caminhos locais ignorados no Git e Docker.

Implementação por camadas: leitura estrita em chunks, chave de nove dimensões incluindo origem/indexador, proporções válidas, junções exatas, lags/média3, cortes fixos, baselines, dois CatBoost independentes, Chronos local zero-shot, métricas/cobertura, inferência com recarga, exportação de artigo e briefing desacoplado. Não há refit com validação. Não se agregam saldos de perfis; duplicatas abortam. Nenhum dado ausente vira zero.

Impacto: fluxo antes reservado agora executável e auditável; documentos históricos apenas recebem aviso de atualização. CatBoost recebe perfil/saldos/histórico; Chronos somente histórico de três meses por alvo. Piloto CPU Chronos usa amostra SHA256 módulo 1024; limitação explícita, comparação comum sem imputação futura. Fine-tuning não executado. Dados, modelos e previsões por perfil ficam fora do Git.

## Arquivos criados/alterados

- Configuração: `.gitignore`, `.dockerignore`, `requirements.txt`, `scripts/bootstrap.ps1`, `README.md`, `src/config/constants.py`.
- Dados/atributos: `src/data/read/csv_reader.py`, `src/data/read/panel.py`, `src/data/preprocessing/transformer.py`, `src/features/temporal.py`.
- Modelos: `src/models/baselines.py`, `evaluation.py`, `temporal_validation.py`, `catboost_regression.py`, `chronos_forecast.py`.
- Pipelines: `src/pipelines/experiment.py`, `training_pipeline.py`, `prediction_pipeline.py`.
- Figuras/artigo: `src/visualization/experiment.py`, `export_paper.py`, `paper/main.tex`, `paper/references.bib`, PDF e evidências em `paper/generated/` quando exportados.
- Documentos: `docs/arquitetura.md`, avisos nos entregáveis 1/2 e plano Qwen; `docs/protocolo-catboost-chronos2.md`, `funcionamento-efetivo.md`, `resultados-execucao.md`.
- Testes: `tests/test_temporal.py`, `test_ingestion.py`, `test_models.py`; testes de briefing existentes preservados.
- Este registro `artifacts/011-preparacao-experimentos-artigo.md`.

## Comandos e evidências

Bootstrap via uv portátil: `uv python install 3.14.0 --install-dir .tools/python`, `uv venv --python .tools/python/cpython-3.14.0-windows-x86_64-none/python.exe .venv`, instalação das versões de requirements no `.venv`.

`$env:PYTHONPATH='src'; .venv/Scripts/python.exe -m unittest discover -s tests -v`: 15 testes passaram na execução intermediária, incluindo treinamento/recarga real em fixture explicitamente sintética. Não são resultados SCR e não há chamadas reais a provedores nos testes.

`python -m compileall -q src` e `python -m pip check` com o Python do venv: aprovados nas verificações intermediárias.

`python -m pipelines.experiment --output runs/2025-pilot --models catboost,chronos`: execução real iniciada; conclusão e valores finais registrados em `docs/resultados-execucao.md` e manifestos, sem antecipação de sucesso neste registro.

Download local do checkpoint público `amazon/chronos-2`, revisão `29ec3766d36d6f73f0696f85560a422f50e8498c`, concluído em `.tools/chronos-2`. Nenhum CSV foi enviado ao Hugging Face.

`tectonic -k --keep-logs main.tex` em paper/: primeira compilação concluída, seguida de ajuste de codificação de fonte T1 para respeitar Times no XeTeX. Poppler disponível para renderizar e inspecionar PDF. Artigo não contém autoria/afiliação inventadas: campos explicitamente pendentes de confirmação antes de submissão.

Docker CLI encontrada em `C:/Users/Tulio/AppData/Local/Programs/DockerDesktop/resources/bin/docker.exe`, fora do PATH. `docker compose config` válido. `docker version` inicialmente falhou no engine/named pipe, mesmo após iniciar Docker Desktop oculto. A validação de build/up depende desse serviço e é registrada separadamente, sem simular sucesso.

## Fontes verificadas e limitações

BCB catálogo SCR.data e metodologia V2 foram consultados em 22/11/2026. Confirmam nove dimensões, atraso de aproximadamente 30 dias, possibilidade de substituição de documentos e mudança na definição de ativo problemático em jan/2025. Extração local original desconhecida; mtime não é data de extração. Avaliação por data-base e snapshot atual pode ser otimista operacionalmente.

Referências primárias verificadas: `https://arxiv.org/abs/1706.09516`, `https://arxiv.org/abs/2510.15821`, documentação CatBoost e repositório/checkpoint oficial Chronos. Só dados de 2025; sazonal12 indisponível; sem generalização robusta, causalidade ou risco individual. Pico de memória não instrumentado. Não houve commits, branches, push ou publicação.

## Informação complementar integral do usuário

Resposta à pergunta sobre autoria, afiliação e e-mails: “João Alves Passos, Túlio Kenji Yoshimura”.

Os dois nomes foram incorporados ao artigo; afiliação permanece explicitamente pendente e e-mails não foram inventados.

## Encerramento efetivo

- CatBoost: dois modelos treinados com dados reais, profundidades 6 e 4, 2.415.028 linhas de treino e 591.891 de validação por alvo. Quatro candidatos e predição: 1.508,717 s. Sem refit.
- Chronos-2: zero-shot local concluído em amostra SHA256 módulo 1024; 384 chaves, 267 perfis de teste comuns. 74,613 s incluindo leitura preparada. Sem fine-tuning.
- A tentativa conjunta original teve bloqueio de rede para Chronos; resultados locais independentes foram alinhados em `runs/2025-comparison`, preservando os originais. Hash de `profiles.csv` conferido. Comando: `python -m pipelines.merge_forecasts runs/2025-pilot runs/chronos-pilot --output runs/2025-comparison`. Nenhuma previsão foi alterada; equivalência de métricas de origem verificada a 1e-12.
- Ingênuo teve menor MAE no teste nos dois targets. Na interseção dos cinco métodos (267 perfis), MAE ingênuo/CatBoost/Chronos: 3,822464/3,863386/4,064837 pp para inadimplência e 3,733121/3,860552/4,072841 pp para ativos problemáticos. Cobertura Chronos global 0,08994%; não generalizar amostra ao painel. Previsões fora de [0,1] preservadas e contadas.
- 16 testes aprovados, compileall e pip check aprovados. Compose config válido; build/up bloqueado por engine indisponível.
- Exportação por `python -m visualization.export_paper runs/2025-comparison`; PDF final SBC com 5 páginas, referências resolvidas, todas renderizadas/inspecionadas. Sem overflow; avisos de underfull e mensagens não impeditivas de pacote/Fontconfig documentados.
- Novos módulos adicionais: auditoria `analysis/panel_audit.py`, validador `data/validation/panel_validator.py`, reavaliação, piloto isolado e consolidação em `pipelines/`. Pacote numérico de briefing exportado, sem chamadas reais de LLM.
- Limitações: apenas 2025, um mês de teste, disponibilidade por data-base, extração desconhecida, vintages e corpus de pré-treinamento não auditados; fine-tuning e Chronos integral não executados. Afiliação pendente.

### Lista final de arquivos versionáveis criados/alterados

- `.dockerignore`
- `.gitignore`
- `README.md`
- `artifacts/011-preparacao-experimentos-artigo.md`
- `docs/arquitetura.md`
- `docs/entregavel-1.md`
- `docs/entregavel-2.md`
- `docs/funcionamento-efetivo.md`
- `docs/plano-treinamento-qwen-3-5-9b.md`
- `docs/protocolo-catboost-chronos2.md`
- `docs/resultados-execucao.md`
- `paper/README.md`
- `paper/generated/coverage.tex`
- `paper/generated/data-summary.tex`
- `paper/generated/data_audit.json`
- `paper/generated/discussion.tex`
- `paper/generated/manifest.json`
- `paper/generated/metrics.csv`
- `paper/generated/panel_audit.json`
- `paper/generated/proporcao_ativos_problematicos.json`
- `paper/generated/proporcao_inadimplencia.json`
- `paper/generated/results.tex`
- `paper/generated/test_mae.png`
- `paper/main.pdf`
- `paper/main.tex`
- `paper/references.bib`
- `requirements.txt`
- `scripts/bootstrap.ps1`
- `src/analysis/panel_audit.py`
- `src/config/constants.py`
- `src/data/preprocessing/transformer.py`
- `src/data/read/csv_reader.py`
- `src/data/read/panel.py`
- `src/data/validation/panel_validator.py`
- `src/features/temporal.py`
- `src/models/baselines.py`
- `src/models/catboost_regression.py`
- `src/models/chronos_forecast.py`
- `src/models/evaluation.py`
- `src/models/temporal_validation.py`
- `src/pipelines/chronos_pipeline.py`
- `src/pipelines/evaluation_pipeline.py`
- `src/pipelines/experiment.py`
- `src/pipelines/merge_forecasts.py`
- `src/pipelines/prediction_pipeline.py`
- `src/pipelines/training_pipeline.py`
- `src/visualization/experiment.py`
- `src/visualization/export_paper.py`
- `tests/test_ingestion.py`
- `tests/test_models.py`
- `tests/test_pipeline.py`
- `tests/test_temporal.py`

Dados brutos, intermediários, checkpoints, modelos e previsões por perfil continuam ignorados pelo Git. Nenhum segredo foi copiado. Nenhum commit, branch, push ou publicação.
