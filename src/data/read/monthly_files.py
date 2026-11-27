"""Nomes e competências dos arquivos mensais do SCR."""
import re
from pathlib import Path


def file_month(name: str) -> str | None:
    match = re.fullmatch(r"scrdata_([0-9]{4})(0[1-9]|1[0-2])\.csv", name)
    return f"{match[1]}-{match[2]}" if match else None


def monthly_files(folder: Path, start=None, end=None):
    for path in sorted(folder.glob("scrdata_*.csv")):
        month = file_month(path.name)
        if month and (start is None or month >= start) and (end is None or month <= end):
            yield month, path
