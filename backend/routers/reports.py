from io import BytesIO

from fastapi import APIRouter, Depends, Response
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from sqlalchemy.orm import Session

from ..db import get_db, ValidationRun, ProviderScore, DriftScore

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/latest", response_class=Response)
async def latest_report(db: Session = Depends(get_db)) -> Response:
    latest = (
        db.query(ValidationRun)
        .order_by(ValidationRun.started_at.desc())
        .first()
    )

    scores = db.query(ProviderScore).all()
    drifts = db.query(DriftScore).all()

    avg_pcs = None
    if scores:
        avg_pcs = sum(s.pcs for s in scores) / len(scores)

    drift_dist = {"Low": 0, "Medium": 0, "High": 0}
    for d in drifts:
        if d.bucket in drift_dist:
            drift_dist[d.bucket] += 1

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "Provider Validation Summary Report")
    y -= 30

    c.setFont("Helvetica", 11)
    if latest:
        c.drawString(40, y, f"Latest run ID: {latest.id} ({latest.run_type})")
        y -= 18
        c.drawString(40, y, f"Processed: {latest.count_processed} | Auto-updates: {latest.auto_updates} | Manual reviews: {latest.manual_reviews}")
        y -= 18
    else:
        c.drawString(40, y, "No runs yet.")
        y -= 18

    c.drawString(40, y, f"Average PCS: {avg_pcs:.1f}" if avg_pcs is not None else "Average PCS: N/A")
    y -= 24

    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Drift distribution:")
    y -= 18
    c.setFont("Helvetica", 11)
    c.drawString(60, y, f"Low: {drift_dist['Low']}")
    y -= 14
    c.drawString(60, y, f"Medium: {drift_dist['Medium']}")
    y -= 14
    c.drawString(60, y, f"High: {drift_dist['High']}")
    y -= 24

    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Policy notes:")
    y -= 18
    c.setFont("Helvetica", 11)
    c.drawString(60, y, "- PCS ≥ 85 (green): safe for auto-publish.")
    y -= 14
    c.drawString(60, y, "- PCS 70–84 (amber): sampled with audit trail.")
    y -= 14
    c.drawString(60, y, "- PCS < 70 (red): manual review required.")
    y -= 14
    c.drawString(60, y, "- High drift: weekly re-check; Low drift: monthly.")

    c.showPage()
    c.save()

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return Response(content=pdf_bytes, media_type="application/pdf")
