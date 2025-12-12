# Project: Provider Data Validation & Directory (Agentic AI)

## Overview
This workspace contains a full-stack application for validating healthcare provider data using a multi-agent AI system.

## Tech Stack
- **Backend:** Python (FastAPI), SQLite, SQLAlchemy
- **Frontend:** React (Webpack), CSS Modules
- **AI/ML:** Custom Agent Logic, Pytesseract (OCR), ReportLab (PDF)

## Key Features
- **Agents:** Validation, Enrichment, QA, Directory Management.
- **Scoring:** Provider Credibility Score (PCS) & Data Drift Detection (PDDD).
- **Workflow:** Automated batch processing with manual review fallback.

## Development Rules
- **Ports:**
  - Backend: 8000
  - Frontend: 3020 (Do not use default 3000)
- **Database:** provider_directory.db (SQLite)
- **Testing:** Use backend/reset_demo_state.py to reset data for demos.
- **Frontend Proxy:** Configured in webpack.config.js to forward /api to localhost:8000.

## Common Tasks
- **Run Batch:** Trigger via UI button 'Run Daily Batch'.
- **Reset Data:** Run python -m backend.reset_demo_state.
