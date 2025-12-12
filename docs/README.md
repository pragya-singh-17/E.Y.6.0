# Provider Data Validation & Directory (Agentic AI) — Stage 1–11

This is a hackathon-style end-to-end prototype demonstrating an agentic AI pipeline for provider data validation, PCS (Provider Credibility Score), and Provider Data Drift Detection.

## Quick start

```powershell
python -m backend.reset_demo_state
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
cd frontend
npm install
npm start
```

Then in the UI, click **Run Daily Batch** and open:

- Provider ID 1 — high PCS green band, low drift (phone auto-updated from NPI/Maps, very few mismatches).
- Provider ID 2 — red PCS, high drift (conflicting address/phone + near-expiry license → manual review queue).

The dashboard shows latest run stats, PCS distribution via average PCS, and drift distribution.

## PCS and Drift

PCS is computed nightly after each batch as:

$$PCS = 100 \times (0.25\,SRM + 0.15\,FR + 0.10\,ST + 0.15\,MB + 0.10\,DQ + 0.10\,RP + 0.10\,LH + 0.05\,HA)$$

Where each component is in [0,1] and calculated as described in the problem statement. The backend also stores each sub-score so the UI can render a PCS radar-style breakdown for every provider.

Drift is a 0–1 risk score with buckets Low/Medium/High and recommended next check days (30/14/7). It is more aggressive for:

- recently changed profiles,
- providers close to / past license expiry,
- and low-PCS providers with frequent mismatches.

## Demo flow

1. Reset state and start backend + frontend.
2. In the app, press **Run Daily Batch** to process the seeded providers.
3. On the dashboard, observe processed count, auto-updates, manual reviews, average PCS, and drift distribution.
4. Open Provider ID 1 and ID 2 from the provider list to see PCS badge (green vs red), drift chip (Low vs High), PCS breakdown, confidence table, and audit log entries for both auto-updates and manual actions.
5. Open Manual Review tab to approve/override low-confidence suggestions.

## Why PCS & Drift matter

PCS surfaces long-term provider reliability and allows prioritisation of manual QA. Green-band providers can be safely auto-published, amber ones sampled, and red-band providers routed to manual review.

Drift detection predicts which providers are likely to change soon (address/phone/license), enabling proactive scheduling and outreach instead of purely reactive validation cycles. High-drift providers are automatically scheduled for more frequent re-checks (weekly), while low-drift, high-PCS providers can be scanned less often, reducing ops load.
