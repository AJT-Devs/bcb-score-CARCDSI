# Arquitetura e escopo científico

Os entregáveis [1](entregavel-1.md) e [2](entregavel-2.md) definem o estudo de risco de crédito agregado com dados mensais SCR.data. O objetivo é prever, um mês à frente, as proporções de inadimplência e de ativos problemáticos para perfis de crédito. Este documento distingue a estrutura existente das etapas ainda necessárias para produzir resultados reproduzíveis.

## Fluxo de pesquisa

1. **Dados:** `data/read/` lê CSVs mensais separados por `;`; `data/validation/` verifica integridade; `data/preprocessing/` prepara dados e calcula as duas proporções com `carteira_ativa` como denominador. Os dados brutos permanecem inalterados e denominadores zero resultam em valor ausente.
2. **Análise e atributos:** `analysis/` e `features/` reservam as análises exploratórias, estatísticas e de correlação, além da engenharia e seleção de atributos. As transformações aprendidas devem ser ajustadas somente nos dados de treino.
3. **Experimentos:** `models/` reserva regressão linear múltipla, árvore de decisão, k-NN e baselines ingênuo, sazonal ingênuo, média móvel e drift. As divisões temporais devem impedir que meses futuros influenciem o treino de meses anteriores; a avaliação deve ser separada para cada target e usar MAE principal, RMSE e R². O baseline sazonal depende de histórico suficiente.
4. **Interpretação:** `services/ia/` recebe métricas e contexto já calculados e produz briefings auditáveis; o LLM não calcula proporções, escolhe resultados silenciosamente nem cria previsões. `visualization/` reserva gráficos para comunicação científica.
5. **Orquestração:** `pipelines/` deve compor as etapas existentes, registrando períodos, filtros, dados ausentes, configurações, métricas e limitações necessários à reprodução e ao artigo.

## Estado de implementação

Existem leitura, validação básica, pré-processamento inicial e clientes LLM. Os módulos de análise, atributos, modelos, avaliação, visualização e pipelines são pontos de extensão, não experimentos funcionais. Em particular, ainda é necessário implementar a construção temporal dos targets, divisões sem vazamento, ajuste de transformações apenas no treino, baselines, modelos e métricas antes de apresentar resultados científicos. A codificação categórica existente é inicial e não constitui uma transformação treinável pronta para avaliação temporal.

## Serviços de LLM

`LLMClient` define o contrato `generate(prompt) -> LLMResponse`, que preserva provedor, texto e resposta original. `generate_briefing` aceita um cliente compatível por injeção; assim, novos provedores ou modelos podem ser implementados sem alterar o briefing. Os atalhos `gemini` e `nvidia` permanecem disponíveis e um nome desconhecido é rejeitado explicitamente. Quando `client` é fornecido, ele determina o provedor e o argumento `provider` é ignorado. Os clientes existentes mantêm seus modelos, credenciais e timeout configuráveis por ambiente. Integrações novas devem definir sua própria configuração e tratamento de credenciais, sem registrar segredos; testes usam substitutos sem rede.

## Convenções de nomes

Pacotes e módulos Python usam inglês e `snake_case`, com nomes que descrevem responsabilidades ou métodos de pesquisa. `services/ia/` é mantido conforme a estrutura do projeto. Documentos de entrega usam português e nomes em minúsculas com hífens; logs numerados em `artifacts/` mantêm seus nomes históricos. Nomes oficiais de colunas e targets não são traduzidos ou renomeados.
