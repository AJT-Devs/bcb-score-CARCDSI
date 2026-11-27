"""Publica CSVs mensais completos a partir dos ZIPs locais."""
import os
from pathlib import Path, PurePosixPath
import shutil
from tempfile import NamedTemporaryFile
from zipfile import ZipFile

from data.read.monthly_files import file_month


def unpack_archives(archives: list[Path], raw: Path) -> tuple[int, int]:
    raw.mkdir(parents=True, exist_ok=True)
    extracted = skipped = 0
    for path in archives:
        year = path.stem.removeprefix("scrdata_")
        with ZipFile(path) as archive:
            members = {}
            for entry in archive.infolist():
                name = PurePosixPath(entry.filename.replace("\\", "/")).name
                month = file_month(name)
                if entry.is_dir() or month is None:
                    continue
                if not month.startswith(f"{year}-") or name in members:
                    raise ValueError(f"Mês fora do ano ou duplicado em {path.name} ({name})")
                members[name] = entry
            if not members:
                raise ValueError(f"Nenhum CSV mensal em {path.name}")
            for name, entry in sorted(members.items()):
                destination = raw / name
                if destination.is_file():
                    skipped += 1
                    continue
                with NamedTemporaryFile(dir=raw, suffix=".part", delete=False) as output:
                    temporary = Path(output.name)
                try:
                    with archive.open(entry) as source, temporary.open("wb") as output:
                        shutil.copyfileobj(source, output, length=1024 * 1024)
                    if os.name == "nt":
                        temporary.rename(destination)
                    else:
                        destination.hardlink_to(temporary)
                except FileExistsError:
                    skipped += 1
                else:
                    extracted += 1
                finally:
                    temporary.unlink(missing_ok=True)
    return extracted, skipped
