"""Protocolo congelado: ajuste até target setembro, seleção outubro/novembro."""


def split_masks(frame):
    return {"train": frame.month.between("2025-01", "2025-08"),
            "validation": frame.month.between("2025-09", "2025-10"),
            "test": frame.month.eq("2025-11")}
