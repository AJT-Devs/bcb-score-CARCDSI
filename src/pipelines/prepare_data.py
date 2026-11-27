"""Extrai os CSVs ausentes e, opcionalmente, busca ZIPs no Google Drive."""
import argparse
import re
import subprocess
from pathlib import Path
from zipfile import BadZipFile

from config.settings import PROJECT_ROOT, SCR_DRIVE_FOLDER_ID, get_settings
from data.read.archives import unpack_archives
from data.read.monthly_files import monthly_files


def download_archives(folder, remote, years):
    patterns = [f"scrdata_{year}.zip" for year in years] or ["scrdata_[0-9][0-9][0-9][0-9].zip"]
    subprocess.run(
        ["rclone", "copy", f"{remote}:", str(folder), "--drive-root-folder-id", SCR_DRIVE_FOLDER_ID,
         "--ignore-existing", "--max-depth", "1",
         *[arg for pattern in patterns for arg in ("--include", pattern)]],
        check=True,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compressed", type=Path, default=PROJECT_ROOT / "data" / "compressed")
    parser.add_argument("--raw", type=Path, default=get_settings().raw_data_dir)
    parser.add_argument("--years", nargs="+", metavar="AAAA")
    parser.add_argument("--drive-remote", metavar="NOME", help="Remote do tipo Drive configurado no rclone")
    args = parser.parse_args()
    years = set(args.years or [])
    if any(not re.fullmatch(r"[0-9]{4}", year) for year in years):
        parser.error("--years espera anos com quatro dígitos")
    missing = sorted(year for year in years if not (args.compressed / f"scrdata_{year}.zip").is_file())
    try:
        if args.drive_remote and (missing or not years):
            download_archives(args.compressed, args.drive_remote, missing)
        archives = [path for path in sorted(args.compressed.glob("scrdata_*.zip"))
                    if re.fullmatch(r"scrdata_[0-9]{4}", path.stem)
                    and (not years or path.stem[-4:] in years)]
        uncovered = years - {path.stem[-4:] for path in archives}
        raw_months = {month for month, _ in monthly_files(args.raw)}
        unavailable = {year for year in uncovered
                       if any(f"{year}-{month:02}" not in raw_months for month in range(1, 13))}
        if unavailable or (not archives and not raw_months):
            parser.error(f"ZIPs ausentes em {args.compressed} ({', '.join(sorted(unavailable)) or 'nenhum ZIP encontrado'})")
        extracted, skipped = unpack_archives(archives, args.raw)
    except (OSError, ValueError, BadZipFile, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Falha ao preparar dados ({error}).\n")
    print(f"{extracted} CSVs extraídos em {args.raw}. {skipped} CSVs de ZIPs já existentes.")


if __name__ == "__main__":
    main()
