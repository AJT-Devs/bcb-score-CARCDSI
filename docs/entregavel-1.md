> Registro histórico preservado. Em 22/11/2026, a decisão vigente passou a CatBoost e Chronos-2 com baselines temporais. Este texto não comprova execução dos modelos anteriores. Consulte [o protocolo atual](protocolo-catboost-chronos2.md) e [o funcionamento efetivo](funcionamento-efetivo.md).

Conjunto de Dados (Dataset):
Informe o dataset utilizado.
Observação: Caso utilize um dataset diferente do Lending Club Dataset, é obrigatório incluir:
URL para acesso público/download do dataset.
Dicionário de dados (descrição breve das principais variáveis/colunas).

Objetivos do Sistema (Targets):
Defina claramente quais são as variáveis-alvo (targets) e o objetivo principal da predição/análise do sistema.

Descrição do Sistema:
Apresente uma breve síntese sobre o funcionamento e o propósito do sistema (máximo de 200 palavras).

--

# Conjunto de Dados (Dataset):
Sistema de Informações de Créditos (SCR.data) Dados mensais (Versão 2) - Banco Central do Brasil.

- **URL para acesso público/download:** https://dadosabertos.bcb.gov.br/dataset/scr_data/resource/b8f105b9-fb9c-49ea-8f45-6d8df20f702a
Caminho de donwload dos dataset usados https://www.bcb.gov.br/pda/desig/scrdata_2025.zip, https://www.bcb.gov.br/pda/desig/scrdata_2026.zip

- **Dicionário de dados (principais variáveis/colunas):**
  - `data_base`: Data de referência do fechamento do período.   
  - `uf`: Unidade da Federação, baseada no CEP de residência (PF) ou sede (PJ).   
  - `segmento`: Agrupamento do tipo de instituição financeira, como Banco, Fintech ou Cooperativa.   
  - `cliente`, `cnae_ocupacao` e `porte`: Classificam o tipo de cliente (PF/PJ), sua atividade econômica ou ocupação e faixa de rendimento/tamanho da empresa.   
  - `modalidade` e `submodalidade`: Especificam a natureza da operação (ex: Financiamento imobiliário, Arrendamento, etc).   
  - `carteira_ativa`: Valor total (saldo) das operações de crédito a vencer e vencidas.   
  - `carteira_inadimplencia`: Somatório financeiro das operações com alguma parcela vencida há mais de 90 dias.   
  - `ativo_problematico`: Carteira de operações classificadas com indícios de que a obrigação não será integralmente honrada ou em atraso superior a 90 dias.

# Objetivos do Sistema (Targets):

- **Variável-alvo (Target):** Proporção de Inadimplência (calculada no pré-processamento pela fórmula: `carteira_inadimplencia / carteira_ativa`) e Proporção de Ativos Problemáticos (`ativo_problematico / carteira_ativa`).

- **Objetivo Principal:** Prever o nível de risco de crédito consolidado (macro-risco) para diferentes perfis, identificando quais segmentos econômicos, portes de empresas e modalidades de operação possuem maior propensão à inadimplência sistêmica.

# Descrição do Sistema:
O sistema consistirá em uma plataforma analítica para avaliação de risco financeiro macroeconômico, alimentada pela base do Sistema de Informações de Créditos (SCR) do Banco Central. Inicialmente, o sistema realizará a ingestão e o pré-processamento de dados massivos agregados, estruturando e encodificando variáveis categóricas complexas (como setor CNAE e modalidades financeiras). Utilizando algoritmos de Machine Learning (como regressão ou árvores de decisão), o sistema modelará padrões históricos para prever as taxas de inadimplência e o volume de ativos problemáticos futuros de determinados perfis de crédito. Para fechar o ciclo de inteligência, o sistema integrará Large Language Models (LLMs) para consumir as métricas geradas pelo modelo preditivo e transformá-las em "briefings" dinâmicos em linguagem natural. Isso permitirá que dados complexos e predições matemáticas sejam comunicados de forma clara e acessível, automatizando a geração de relatórios estratégicos sobre a saúde do crédito no país.