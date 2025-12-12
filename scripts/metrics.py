from sqlalchemy.orm import Session

from backend.db import SessionLocal, ProviderScore, DriftScore, Document


def main() -> None:
    db: Session = SessionLocal()
    scores = db.query(ProviderScore).all()
    if scores:
        avg_pcs = sum(s.pcs for s in scores) / len(scores)
        print(f"Average PCS: {avg_pcs:.2f}")
    drifts = db.query(DriftScore).all()
    dist = {"Low": 0, "Medium": 0, "High": 0}
    for d in drifts:
        if d.bucket in dist:
            dist[d.bucket] += 1
    print("Drift distribution:", dist)
    docs = db.query(Document).all()
    if docs:
        avg_ocr = sum((d.ocr_confidence or 0.0) for d in docs) / len(docs)
        print(f"Average OCR confidence: {avg_ocr:.2f}")
    db.close()


if __name__ == "__main__":
    main()
