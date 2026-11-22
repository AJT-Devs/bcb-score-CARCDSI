> Registro histórico preservado. Em 22/11/2026, a decisão vigente passou a CatBoost e Chronos-2 com baselines temporais. Este texto não comprova execução dos modelos anteriores. Consulte [o protocolo atual](protocolo-catboost-chronos2.md) e [o funcionamento efetivo](funcionamento-efetivo.md).

Apresentar os Modelos de Machine Learning que serão utilizados e as métricas de desempenho dos modelos.

# Dataset e objetivos

O projeto utilizará o conjunto de dados SCR.data — Dados Mensais (Versão 2), disponibilizado pelo Banco Central do Brasil.

As variáveis-alvo serão:

- **Proporção de Inadimplência:** `carteira_inadimplencia / carteira_ativa`
- **Proporção de Ativos Problemáticos:** `ativo_problematico / carteira_ativa`

O objetivo será prever essas duas proporções para períodos futuros, considerando características como unidade federativa, segmento financeiro, tipo de cliente, atividade econômica, porte e modalidade de crédito.

A tarefa será de regressão supervisionada aplicada à previsão temporal, pois os targets são valores numéricos contínuos. Inicialmente, será adotado um horizonte de previsão de um mês à frente.

# Modelos de Machine Learning

## 1. Regressão Linear Múltipla

A Regressão Linear Múltipla será utilizada como modelo inicial de referência supervisionado, relacionando as variáveis explicativas com as proporções futuras de inadimplência e ativos problemáticos.

O modelo possui baixa complexidade computacional e permite interpretar os coeficientes associados às variáveis de entrada. Isso facilita a análise da relação entre os perfis de crédito e os indicadores de risco, estabelecendo uma comparação com modelos mais complexos.

## 2. Árvore de Decisão para Regressão

A Árvore de Decisão para Regressão será utilizada para identificar relações não lineares entre as características das operações financeiras e as variáveis-alvo.

O modelo permite dividir os dados segundo características dos perfis de crédito, identificando combinações associadas a diferentes níveis de risco. Sua estrutura também facilita a interpretação das regras utilizadas nas previsões. Serão controlados parâmetros como profundidade máxima e quantidade mínima de amostras por folha para reduzir o risco de overfitting.

## 3. k-Vizinhos Mais Próximos para Regressão (k-NN)

O k-NN para Regressão será utilizado como modelo comparativo, estimando os targets com base nos valores observados em perfis semelhantes.

O algoritmo permite explorar relações locais entre observações sem exigir uma relação linear entre os atributos e os targets. Será necessário normalizar os atributos numéricos e avaliar o impacto das variáveis categóricas codificadas, considerando o custo computacional e a dimensionalidade do dataset.

## Baselines

- **Ingênuo:** utiliza o último valor observado como previsão do período seguinte.
- **Sazonal Ingênuo:** utiliza o valor do período sazonal correspondente, quando houver histórico suficiente.
- **Média Móvel:** prevê o próximo período a partir da média dos valores recentes.
- **Drift:** projeta a tendência média observada na série temporal.

Esses baselines permitirão verificar se os algoritmos de Machine Learning realmente apresentam ganhos em relação a estratégias simples de previsão.

# Métricas de desempenho

Os modelos serão avaliados separadamente para cada variável-alvo, utilizando as seguintes métricas:

- **MAE — Mean Absolute Error (Erro Absoluto Médio):** será a métrica principal, pois expressa a magnitude média dos erros de previsão na mesma unidade do target. Quando as proporções forem apresentadas em porcentagem, o erro poderá ser interpretado em pontos percentuais.

- **RMSE — Root Mean Squared Error (Raiz do Erro Quadrático Médio):** será utilizada para penalizar erros elevados, permitindo identificar modelos que apresentam previsões especialmente distantes dos valores reais, algo relevante para o monitoramento de risco financeiro.

- **R² — Coeficiente de Determinação:** será utilizado para avaliar a capacidade explicativa dos modelos em relação à variação dos targets, considerando também a possibilidade de resultados negativos quando o modelo apresenta desempenho inferior à previsão constante pela média.

O MAPE não será adotado como métrica principal devido à sua sensibilidade a proporções próximas de zero.
