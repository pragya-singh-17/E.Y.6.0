from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db, ValidationRun, ProviderScore, DriftScore

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("")
async def get_stats(db: Session = Depends(get_db)):
    latest = (
        db.query(ValidationRun)
        .order_by(ValidationRun.started_at.desc())
        .first()
    )
    total_pcs = db.query(ProviderScore).count()
    avg_pcs = None
    if total_pcs:
        avg_pcs = (
            sum(s.pcs for s in db.query(ProviderScore).all()) / total_pcs
        )

    drift_rows = db.query(DriftScore).all()
    drift_dist = {"Low": 0, "Medium": 0, "High": 0}
    for d in drift_rows:
        if d.bucket in drift_dist:
            drift_dist[d.bucket] += 1

    return {
        "latest_run": {
            "id": latest.id if latest else None,
            "type": latest.run_type if latest else None,
            "count_processed": latest.count_processed if latest else 0,
            "auto_updates": latest.auto_updates if latest else 0,
            "manual_reviews": latest.manual_reviews if latest else 0,
            "started_at": latest.started_at if latest else None,
            "finished_at": latest.finished_at if latest else None,
        },
        "avg_pcs": avg_pcs,
        "drift_distribution": drift_dist,
    }
