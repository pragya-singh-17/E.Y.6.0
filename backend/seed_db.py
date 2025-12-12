import argparse
import csv
from pathlib import Path

from sqlalchemy.orm import Session

from .db import init_db, SessionLocal, Provider, Document


def seed_db(providers_csv: Path, documents_dir: Path) -> None:
    init_db()
    db: Session = SessionLocal()

    with providers_csv.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            provider = Provider(
                external_id=row["external_id"],
                name=row["name"],
                phone=row.get("phone"),
                address=row.get("address"),
                specialty=row.get("specialty"),
                license_no=row.get("license_no"),
                license_expiry=row.get("license_expiry"),
                affiliations=row.get("affiliations"),
            )
            db.add(provider)
        db.commit()

    providers = db.query(Provider).all()
    for p in providers:
        img_path = documents_dir / f"{p.external_id}.png"
        if img_path.exists():
            doc = Document(
                provider_id=p.id,
                doc_type="license",
                path=str(img_path),
            )
            db.add(doc)
    db.commit()
    db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--providers", type=str, required=True)
    parser.add_argument("--documents", type=str, required=True)
    args = parser.parse_args()
    seed_db(Path(args.providers), Path(args.documents))
