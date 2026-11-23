# 014 — Experimento real de 2025 e revisão do artigo

## Prompt integral do usuário

Execute e avalie os modelos de previsão do projeto com os dados reais disponíveis de 2025. Ao final, atualize o artigo científico em paper/ com os resultados efetivamente obtidos e revise sua redação.

CONTEXTO E OBJETIVO

O projeto prevê, para o mês seguinte, duas proporções agregadas do SCR.data:

- carteira_inadimplencia / carteira_ativa;
- ativo_problematico / carteira_ativa.

Use somente os CSVs de 2025 já disponíveis. Os autores informam que os CSVs foram extraídos em 17 de setembro de 2026. Registre essa data como informação fornecida pelos autores; não alegue que ela foi comprovada apenas pela data de modificação dos arquivos.

ESTADO INICIAL

1. Leia as instruções aplicáveis e examine o estado atual do repositório, incluindo alterações ainda não commitadas. Preserve essas alterações.

2. Examine o fluxo de treinamento, avaliação e exportação, os testes, a implementação dos modelos clássicos e o artigo paper/main.tex.

3. Identifique quais modelos já estão implementados e quais resultados existentes são de execuções anteriores. Não presuma que um resultado antigo pertence à nova execução.

TESTES E EXPERIMENTO

4. Execute a suíte completa de testes automatizados, a compilação do código e pip check usando o ambiente .venv. Corrija falhas relacionadas ao trabalho quando necessário e execute novamente as validações afetadas.

5. Execute o experimento com dados reais para os modelos disponíveis:

   - regressão linear múltipla;
   - árvore de decisão para regressão;
   - k-vizinhos mais próximos para regressão (k-NN);
   - CatBoost;
   - Chronos-2;
   - baselines temporais disponíveis.

6. Respeite o protocolo temporal existente: treino, validação e teste em ordem cronológica. Não use dados futuros para ajustar transformações, selecionar amostras de treino ou treinar previsões de meses anteriores. Não escolha hiperparâmetros ou modelos com base no teste final.

7. O Chronos-2 é usado como modelo pré-treinado em modo zero-shot, salvo se o código e o protocolo comprovarem outra coisa. Não descreva seu uso como treinamento ou fine-tuning se apenas a inferência for executada. Se necessário, obtenha o checkpoint público e execute-o localmente.

8. Considere o custo computacional do k-NN e do Chronos. Use as regras de amostragem implementadas e registre seus parâmetros, tamanhos e cobertura. Execute a avaliação completa do protocolo configurado, sem representar uma amostra como se fosse a totalidade dos perfis.

9. Para cada alvo e modelo, reporte MAE, RMSE, R², número de observações avaliadas, cobertura e previsões fora de [0,1], além do tempo de execução quando medido. Compare os modelos nos mesmos perfis quando possível e apresente também a cobertura sobre o conjunto elegível. Explique diferenças de atributos e de amostragem que afetem a comparação.

10. Não há histórico suficiente para avaliar adequadamente o baseline sazonal anual com os dados disponíveis. Registre essa limitação e não invente resultados.

11. Confira os manifestos e os arquivos gerados: uma execução que termina com um modelo bloqueado não comprova que aquele modelo foi avaliado. Se houver falha de download, memória, tempo ou outro recurso, tente resolver dentro do escopo autorizado. Se não for possível, registre claramente a limitação e não apresente o modelo como executado.

12. Preserve os CSVs brutos e os resultados anteriores. Use diretórios de saída novos para as execuções. Não inclua dados brutos, credenciais, segredos ou arquivos locais indevidos no Git.

ATUALIZAÇÃO DO ARTIGO

13. Depois das execuções, atualize paper/main.tex e os arquivos gerados necessários em paper/ com base nos resultados reais e verificáveis. Gere tabelas e figuras a partir das saídas do código. Não invente métricas, experimentos, referências ou conclusões.

14. Revise todo o artigo para que ele apresente a pesquisa e o sistema desenvolvido como um artigo científico, com linguagem clara e impessoal quando apropriado. Evite transformá-lo em uma auditoria de repositório ou manual de execução.

   Em particular:
   - substitua a afirmação de data de extração desconhecida pela data de 17 de setembro de 2026, informada pelos autores;
   - apresente os procedimentos de reprodutibilidade de maneira concisa, sem depender de referências a caminhos, comandos, exportadores ou fixtures para explicar o estudo;
   - descreva a seleção amostral do Chronos pela metodologia e cobertura, em vez de destacar um argumento de linha de comando;
   - retire pendências administrativas, como confirmação de afiliação ou limite de páginas, do corpo da discussão científica;
   - atualize a descrição do papel do Codex, caso seja pertinente ao artigo, sem afirmar que ele calculou métricas, gerou previsões ou foi integrado ao pipeline;
   - atualize título, resumos, metodologia, resultados, discussão e conclusão para que sejam coerentes entre si e com os experimentos realizados;
   - revise números escritos diretamente no texto para evitar conflitos com as tabelas e a nova execução.

15. Preserve as limitações científicas relevantes, incluindo o uso exclusivo de 2025, a ausência de avaliação sazonal anual, o mês de teste, o atraso de publicação dos dados, a ausência de reconstrução dos vintages, as diferenças de cobertura e o risco não auditado de contaminação do pré-treinamento do Chronos. Não retire limitações apenas para deixar a redação mais fluida.

16. Preserve o template SBC em paper/template/. Compile o artigo com as ferramentas disponíveis, resolva referências e inspecione visualmente o PDF gerado. Verifique resumos, tabelas, figuras, legendas e cortes de texto. Se não conseguir compilar ou inspecionar, informe isso claramente.

17. Não invente afiliação, e-mail ou limite de páginas. Informe essas pendências separadamente na resposta final, se ainda estiverem abertas.

RESTRIÇÕES E RESPOSTA FINAL

- Não faça commits, branches ou publicação.
- Não edite o arquivo .env nem exponha segredos.
- Preserve o trabalho existente de outras pessoas ou agentes.
- Ao final, apresente:
  1. os testes executados e seus resultados;
  2. quais modelos foram efetivamente executados ou ficaram bloqueados;
  3. os principais resultados reais, com cobertura e limitações;
  4. as mudanças feitas no artigo;
  5. se o PDF foi compilado e inspecionado;
  6. os comandos para reproduzir o experimento sem usar o Codex.

## Estado inicial e protocolo

As alterações não commitadas preexistentes, inclusive o registro 013 e os modelos clássicos, foram mantidas. O artigo e seus dados gerados iniciais reportavam uma execução anterior; não foram confundidos com a nova execução. A data de extração de 17/09/2026 é informação fornecida pelos autores; mtime não é comprovação. A avaliação usa apenas arquivos 2025, origens de treino janeiro–agosto, validação setembro–outubro, teste novembro com alvo dezembro. Chronos é zero-shot com seleção SHA256 de chaves módulo 1024; k-NN usa até 5.000 linhas de treino, semente 42, sem seleção pelo teste. O baseline sazonal anual é inelegível.

## Execuções e decisões

A execução integral `runs/2025-experimento-novo` leu 3.764.842 observações em 12 arquivos e 399.480 perfis distintos. Seus hashes correspondem aos 12 hashes historicamente registrados; os resultados numéricos abaixo provêm da nova execução. Não houve chaves vazias excluídas, denominadores inválidos ou alvos inválidos segundo as regras implementadas. O painel auditado registra 236.638 perfis em todos os meses. Linear e árvore ajustaram 2.415.028 linhas por alvo; k-NN ajustou 5.000 das 2.415.028 linhas elegíveis, amostradas uniformemente sem reposição e semente 42. Os modelos de árvore e linear mantiveram pré-processamento ajustado no treino; CatBoost escolheu profundidade na validação.

Comandos executados (PowerShell, raiz, `.venv`, `PYTHONPATH=src`; saídas novas):

```powershell
$env:PYTHONPATH='src'
$env:OMP_NUM_THREADS='4'
$env:OPENBLAS_NUM_THREADS='4'
.\.venv\Scripts\python.exe -m pipelines.experiment --raw data/raw --interim data/interim/2025-novo --output runs/2025-experimento-novo --models baselines,linear,tree,knn,catboost --knn-max-train 5000
.\.venv\Scripts\python.exe -m analysis.panel_audit --prepared data/interim/2025-novo/supervised.csv --output runs/2025-experimento-novo/panel_audit.json
.\.venv\Scripts\python.exe -m pipelines.chronos_pipeline --interim data/interim/2025-novo --output runs/2025-chronos-novo --modulus 1024
.\.venv\Scripts\python.exe -m pipelines.merge_forecasts runs/2025-experimento-novo runs/2025-chronos-novo --interim data/interim/2025-novo --output runs/2025-comparacao-nova
.\.venv\Scripts\python.exe -m visualization.export_paper runs/2025-comparacao-nova
```

O checkpoint público `amazon/chronos-2`, revisão `29ec3766d36d6f73f0696f85560a422f50e8498c`, foi obtido após bloqueio inicial de rede e executado localmente, zero-shot, sem ajuste; SHA256 dos pesos `ddcda3c7508bf2528087723e98a20707cc04b7f370ae275a9fd88078ddba4f42`. O hash da tabela de perfis foi conferido na junção. O Chronos selecionou 384 perfis pela chave, antes de ver os rótulos, e 267 de 296.864 rótulos elegíveis de teste foram previstos por alvo, cobertura total de aproximadamente 0,090%; entre os 284 rótulos da amostra, a cobertura é 94,014%. Os manifestos indicam todos os modelos como executados, nenhum bloqueado. A data de extração informada pelos autores foi acrescentada ao manifesto consolidado com a procedência explícita; os manifestos originais foram mantidos.

Tempos medidos por grupo e dois alvos: baselines 0,08 s, linear 53,99 s, árvore 226,94 s, k-NN 164,24 s, CatBoost 653,72 s e Chronos 22,27 s. Os tempos têm escopos diferentes: os supervisionados incluem ajustes e previsões, enquanto o Chronos inclui leitura do painel preparado; não são latências isoladas e a comparação temporal não é uniforme.

Na interseção dos oito métodos, em 267 observações por alvo, MAE em pp para inadimplência/ativos problemáticos: ingênuo 3,822/3,733; média3 4,936/5,867; drift3 5,108/5,667; linear 4,997/4,939; árvore 5,244/5,046; k-NN 6,594/7,005; CatBoost 3,863/3,861; Chronos 4,065/4,073. Os dados por alvo e modelo de MAE, RMSE, R², cobertura, contagens e previsões fora de faixa estão em `runs/2025-comparacao-nova/metrics.csv` e nas tabelas geradas. A cobertura do ingênuo e modelos clássicos/CatBoost foi 100%, média3 e drift3 94,167% e Chronos 0,090%, no total elegível; comparação comum não representa a população inteira.

## Arquivos desta tarefa

- `paper/main.tex`, `paper/main.pdf`; tabelas, figura, sumário, métricas, manifesto e configurações de modelos em `paper/generated/`; `paper/template/` preservado.
- `src/visualization/export_paper.py` e `src/visualization/experiment.py`: nomes legíveis, números no formato português, tempos gerados a partir dos manifestos e resumos de dados concisos.
- `tests/test_export_paper.py`: teste sintético de nomes e tempo exportados; `README.md`: exemplos de reprodução; `artifacts/014-experimento-real-e-artigo.md`: este registro.
- Saídas locais ignoradas em `runs/2025-experimento-novo`, `runs/2025-chronos-novo`, `runs/2025-comparacao-nova`, `runs/paper-review-final-v4` e intermediários em `data/interim/2025-novo`; ferramentas locais ignoradas em `.tools/`.

## Validação e limitações

`python -m unittest discover -s tests -v`: 16 testes aprovados; `python -m compileall -q src`: aprovado; `python -m pip check`: nenhuma dependência quebrada. `git diff --check` aprovado; nenhum arquivo do template alterado. O PDF foi compilado com Tectonic 0.17.0 e BibTeX, com referências resolvidas, em seis páginas, e todas as páginas foram renderizadas e inspecionadas visualmente; tabelas, figura, legendas e resumos legíveis e sem cortes. O compilador informou erro não fatal de configuração Fontconfig; fontes no PDF foram visualmente inspecionadas e nenhum caractere ausente foi reportado na compilação final. Afiliação, e-mail e limite de páginas continuam não informados.

As conclusões limitam-se aos dados de 2025, um único mês de teste e à seleção amostral indicada; a série sazonal anual não pode ser avaliada. Não há reconstrução de vintages, a publicação tem atraso e não se auditou possível contaminação do pré-treino do Chronos. Os 267 perfis comuns não podem ser apresentados como resultados nacionais. Não foram criados commits, branches ou publicações, nem alterados CSVs brutos ou `.env`.
