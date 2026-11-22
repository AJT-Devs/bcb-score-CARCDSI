"""Constantes de domínio do dataset SCR."""

DATA_SEPARATOR = ";"
PROFILE_COLUMNS = ("uf", "segmento", "cliente", "cnae_ocupacao", "porte", "modalidade", "submodalidade", "origem", "indexador")
BALANCE_COLUMNS = ("carteira_ativa", "carteira_inadimplencia", "ativo_problematico")
TARGET_DEFAULTS = ("proporcao_inadimplencia", "proporcao_ativos_problematicos")
REQUIRED_COLUMNS = (
    "data_base",
    "uf",
    "segmento",
    "cliente",
    "cnae_ocupacao",
    "porte",
    "modalidade",
    "submodalidade",
    "origem",
    "indexador",
    "carteira_ativa",
    "carteira_inadimplencia",
    "ativo_problematico",
)
