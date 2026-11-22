"""Leitura dos CSVs mensais do SCR, sem conhecer detalhes da camada de modelo."""

from collections.abc import Iterator, Sequence
from pathlib import Path

import pandas as pd

from config.constants import DATA_SEPARATOR
from config.settings import get_settings


class CSVReader:
    """Descobre e lê arquivos SCR usando o separador oficial da base."""

    def __init__(self, data_dir: Path | str | None = None) -> None:
        self.data_dir = Path(data_dir) if data_dir else get_settings().raw_data_dir

    def files(self) -> list[Path]:
        return sorted(self.data_dir.glob("*.csv"))

    def iter_frames(self, paths: Sequence[Path] | None = None) -> Iterator[pd.DataFrame]:
        selected_paths = paths if paths is not None else self.files()
        for path in selected_paths:
            yield pd.read_csv(path, sep=DATA_SEPARATOR, decimal=",", encoding="utf-8-sig", low_memory=False)

    def read_all(self) -> pd.DataFrame:
        frames = list(self.iter_frames())
        if not frames:
            raise FileNotFoundError(f"Nenhum CSV encontrado em {self.data_dir}")
        return pd.concat(frames, ignore_index=True)


def read_monthly_csvs(data_dir: Path | str | None = None) -> pd.DataFrame:
    """Atalho para consolidar todos os CSVs mensais de um diretório."""

    return CSVReader(data_dir).read_all()
