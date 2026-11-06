"""Ponto de entrada inicial do projeto."""

from config.settings import get_settings


def main() -> None:
    settings = get_settings()
    print(f"Projeto bcb-score-CARCDSI configurado para {settings.raw_data_dir}")


if __name__ == "__main__":
    main()