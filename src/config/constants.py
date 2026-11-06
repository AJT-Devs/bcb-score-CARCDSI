"""Constantes de domínio do dataset SCR."""

DATA_SEPARATOR = ";"
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
    "carteira_ativa",
    "carteira_inadimplencia",
    "ativo_problematico",
)