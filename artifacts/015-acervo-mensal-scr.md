# Preparação do acervo mensal do SCR

## Prompt integral

> em data/zip adicionei os arquivos em zip de 2015 a 2025 (todos os meses) e 2026 (mes 1 a 9)
> em data.md deixei o link do drive com os zips.
> Caso nao esteja adequado a organizacao de arquivos, mude o nome da pasta zip (serao dados compactados).
> Fça scripts para descompactar e jogar os arquivos em raw caso nao tenha os arquivos em raw.
> Caso tenha jeito, script para se nao houver os zips baixar do drive.
> Mude o codigo para se adequar ao uso de dados de outros anos. No artigo, mude as limitações tambem. Seguindo o padrao de arquitetura e as skills.
> Configure o gitignore para enviar somente a pasta com arquivos compactados, não os arquivos em sí

## Entrega e decisões

- A pasta `data/zip` passou a se chamar `data/compressed`. O Git pode incluir `data/compressed/.gitkeep`. O conteúdo dos ZIPs, dos dados brutos e as divisões temporais geradas no intermediário ficam locais.
- A leitura de arquivos mensais e a extração ficaram em `src/data/read`. O pipeline de preparação coordena a cópia opcional de ZIPs via rclone e publica somente CSVs ausentes. O extrator lê o ZIP em fluxo, usa apenas o nome mensal validado e publica o arquivo final após a cópia completa, sem substituir CSVs existentes.
- A ingestão aceita competências de qualquer ano pelo padrão oficial de nome. O experimento aceita um intervalo inclusivo. A origem mais recente com mês seguinte observado vai para teste, as duas anteriores vão para validação e as demais para treino. Lacunas não criam pares artificiais. O corte é salvo para que avaliação, Chronos, consolidação e inferência respeitem o mesmo calendário. Artefatos antigos sem essa informação usam o protocolo de 2025. A inferência com CatBoost considera o último alvo usado também na seleção de profundidade.
- O artigo SBC registra a cobertura do acervo e as verificações metodológicas necessárias para ampliá-lo. O PDF foi recompilado com as métricas executadas no recorte de 2025.

## Arquivos

- Configuração e documentação no `.gitignore`, `README.md`, `data/data.md`, `data/compressed/.gitkeep` e `docs/funcionamento-efetivo.md`.
- Leitura em `src/config/settings.py`, `src/data/read/archives.py`, `src/data/read/monthly_files.py` e `src/data/read/panel.py`.
- Corte e auditoria em `src/models/temporal_validation.py`, `src/analysis/panel_audit.py` e `tests/test_temporal.py`.
- Orquestração em `src/pipelines/prepare_data.py`, `experiment.py`, `chronos_pipeline.py`, `evaluation_pipeline.py`, `merge_forecasts.py` e `prediction_pipeline.py` na mesma pasta.
- Artigo em `paper/main.tex` e `paper/main.pdf`, além deste registro.

## Validações e limites

- A primeira execução de `python -m pipelines.prepare_data` extraiu 129 CSVs e preservou os 12 CSVs existentes de 2025. A repetição extraiu zero. Foram conferidos as 141 competências consecutivas e os tamanhos dos CSVs contra os 12 ZIPs.
- `python -m compileall -q src`, `python -m pip check` e os 17 testes offline de `python -m unittest discover -s tests` passaram. A validação fora do sandbox permitiu os diretórios temporários do Python 3.14. CatBoost 1.2.10, já fixado pelo projeto, foi instalado apenas no ambiente local.
- Experimentos reais com baselines concluíram nos recortes 2015-11 a 2016-03 e 2025-11 a 2026-03. Inferência por CLI com origem 2026-02 e reavaliação das previsões salvas do segundo recorte concluíram. A execução ponta a ponta com o acervo inteiro não foi realizada. O painel consolidado ainda exige memória proporcional ao recorte.
- A chamada do rclone foi validada com mock, incluindo o filtro de ano e a preservação de ZIPs existentes. O download real do Drive depende de um remote com acesso configurado e não foi executado.
- Tectonic 0.17.0 compilou o PDF com BibTeX e referências resolvidas. A conferência visual abrangeu primeira página, tabelas de resultado, figura, limitações e referências. O PDF tem seis páginas A4. Permanecem os avisos de caminho do pacote SBC e de `inputenc` ignorado pelo motor UTF-8. O limite do evento não foi informado.
- `git diff --check` passou. O Git ignora os ZIPs, CSVs e resultados locais. Nenhuma credencial ou dado mensal foi incluído no diff.
