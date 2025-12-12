from datetime import datetime
from typing import Literal

from sqlalchemy.orm import Session

from .db import Provider, ValidationRun
from .agents import (
    validate_provider,
    extract_from_pdf,
    enrich_provider,
    qa_evaluate,
    apply_updates,
)
from .pcs_drift import recompute_pcs_for_all, recompute_drift_for_all


BatchType = Literal["daily", "weekly", "onboarding"]


def run_batch(db: Session, batch_type: BatchType = "daily", limit: int = 200) -> ValidationRun:
    run = ValidationRun(run_type=batch_type, started_at=datetime.utcnow())
    db.add(run)
    db.commit()
    db.refresh(run)

    providers = (
        db.query(Provider)
        .order_by(Provider.last_verified_at.is_(None), Provider.last_verified_at)
        .limit(limit)
        .all()
    )

    auto_updates = 0
    manual_reviews = 0

    for provider in providers:
        external_data = validate_provider(db, provider.id)
        ocr_data = extract_from_pdf(db, provider.id)
        enrichment = enrich_provider(db, provider.id, external_data, ocr_data)
        decisions = qa_evaluate(db, provider.id, external_data, enrichment)
        res = apply_updates(db, provider.id, decisions)
        auto_updates += res["auto_updates"]
        manual_reviews += res["manual_reviews"]

    recompute_pcs_for_all(db)
    recompute_drift_for_all(db)

    run.count_processed = len(providers)
    run.auto_updates = auto_updates
    run.manual_reviews = manual_reviews
    run.finished_at = datetime.utcnow()
    db.commit()
    db.refresh(run)
    return run
