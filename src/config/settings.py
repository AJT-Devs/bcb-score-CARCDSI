"""Configuração centralizada e orientada a variáveis de ambiente."""

from dataclasses import dataclass
from functools import lru_cache
import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INTERIM = Path("data/interim/scr")
SCR_DRIVE_FOLDER_ID = "1aCvm6NC_WQwB-muz1c-bctyFDmyRlHy-"


@dataclass(frozen=True)
class Settings:
    project_root: Path
    raw_data_dir: Path


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    raw_data_dir = Path(os.getenv("DATA_RAW_DIR", str(PROJECT_ROOT / "data" / "raw")))
    return Settings(
        project_root=PROJECT_ROOT,
        raw_data_dir=raw_data_dir,
    )
