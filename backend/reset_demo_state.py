from pathlib import Path

from .db import DB_PATH
from .seed_db import seed_db
from .generate_docs import main as generate_docs


def main() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()
    providers_csv = Path(__file__).resolve().parent / "data" / "providers.csv"
    docs_dir = Path(__file__).resolve().parent / "data" / "docs"
    # Generate fresh synthetic license PNGs with readable text for OCR demo
    generate_docs()
    seed_db(providers_csv, docs_dir)


if __name__ == "__main__":
    main()
