"""Configuração centralizada e orientada a variáveis de ambiente."""

from dataclasses import dataclass
from functools import lru_cache
import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    project_root: Path
    raw_data_dir: Path
    nvidia_api_key: str | None
    gemini_api_key: str | None
    nvidia_model: str
    gemini_model: str
    request_timeout_seconds: int


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    raw_data_dir = Path(os.getenv("DATA_RAW_DIR", str(PROJECT_ROOT / "data" / "raw")))
    return Settings(
        project_root=PROJECT_ROOT,
        raw_data_dir=raw_data_dir,
        nvidia_api_key=os.getenv("NVIDIA_API_KEY") or None,
        gemini_api_key=os.getenv("GEMINI_API_KEY") or None,
        nvidia_model=os.getenv("NVIDIA_MODEL", "meta/llama-3.1-8b-instruct"),
        gemini_model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        request_timeout_seconds=int(os.getenv("LLM_REQUEST_TIMEOUT_SECONDS", "60")),
    )