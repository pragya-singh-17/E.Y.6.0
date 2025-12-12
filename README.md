# Provider Data Validation & Directory (Agentic AI)

## 📌 Overview
This project is an **Agentic AI System** designed to automate the validation, enrichment, and management of healthcare provider directories. It addresses the industry-wide problem of inaccurate provider data (wrong phone numbers, addresses, expired licenses) by using a multi-agent architecture to cross-reference data from multiple sources, assign confidence scores, and predict future data drift.

## 🚀 Key Features

### Core AI Agents
1.  **Validation Agent:** Scrapes and verifies data against NPI Registry, State Medical Boards, and Google Maps.
2.  **Enrichment Agent:** Extracts data from unstructured documents (PDFs/Images) using OCR and fills missing details.
3.  **QA Agent:** Computes field-level confidence scores and decides whether to auto-update or flag for manual review.
4.  **Directory Management Agent:** Orchestrates the workflow, updates the database, and manages the manual review queue.

### 🌟 Unique Capabilities
*   **Provider Credibility Score (PCS):** A "credit score" (0-100) for doctors based on data consistency, responsiveness, and license health.
*   **Provider Data Drift Detection (PDDD):** A predictive model that identifies providers likely to have outdated info soon (e.g., expiring licenses, volatile contact info).
*   **Auto-Correction:** Automatically fixes high-confidence errors (e.g., updating a phone number confirmed by 3 sources).
*   **Smart Manual Review:** Routes only low-confidence conflicts to human reviewers, saving operational costs.

## 🛠️ Tech Stack
*   **Backend:** Python, FastAPI, SQLAlchemy, SQLite, Pytesseract (OCR), ReportLab (PDF Generation).
*   **Frontend:** React, Axios, CSS Modules.
*   **Orchestration:** Custom Python-based agent workflow.

## 📋 Prerequisites
*   **Python 3.8+**
*   **Node.js 14+**
*   **Tesseract OCR** (Optional, system has fallback if not installed)

## ⚙️ Installation & Setup

### 1. Backend Setup
Navigate to the root directory:
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.\.venv\Scripts\Activate
# Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Initialize Database and Seed Data
python -m backend.reset_demo_state
```

### 2. Frontend Setup
Navigate to the frontend directory:
```bash
cd frontend
npm install
```

## ▶️ Running the Application

### Step 1: Start the Backend
In the root directory (with virtual environment activated):
```bash
uvicorn backend.main:app --reload --port 8000
```
*The backend will run at `http://127.0.0.1:8000`*

### Step 2: Start the Frontend
Open a new terminal, navigate to `frontend`, and run:
```bash
cd frontend
npm start
```
*The frontend will run at `http://localhost:3020`*

### Step 3: Trigger Data Processing
Once both servers are running:
1.  Open the Frontend at `http://localhost:3020`.
2.  Click the **"Run Daily Batch"** button in the top right corner.
3.  Wait for the process to complete. The dashboard will populate with:
    *   Processed Providers
    *   PCS Scores (Green/Amber/Red badges)
    *   Drift Risk (Low/Medium/High chips)
    *   Manual Review Items

## 📂 Project Structure
```
EY FULL/
├── backend/
│   ├── agents.py           # Core logic for Validation, Enrichment, QA agents
│   ├── db.py               # Database models (SQLite)
│   ├── main.py             # FastAPI entry point
│   ├── orchestrator.py     # Batch processing workflow
│   ├── pcs_drift.py        # Logic for PCS and Drift scoring
│   ├── data/               # Mock data (NPI, State Board, CSVs)
│   └── routers/            # API endpoints
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React UI
│   │   └── styles.css      # Dashboard styling
│   └── webpack.config.js   # Proxy and build configuration
└── README.md
```

## 🔧 Troubleshooting

*   **Port Conflicts:**
    *   If `npm start` fails with `EADDRINUSE`, ensure port 3020 is free.
    *   If `uvicorn` fails, ensure port 8000 is free.
*   **Proxy Errors:**
    *   If the frontend shows "Network Error", ensure the backend is running on port 8000.
*   **OCR Issues:**
    *   If Tesseract is not found, the system will default to a "Neutral" confidence score and continue processing without crashing.

## 🧪 Demo Scenarios
1.  **Auto-Update:** Search for **Dr. Rohan Verma (P001)**. Note his phone number was auto-corrected based on NPI registry data.
2.  **Manual Review:** Check the "Manual Review Queue". You will see **Dr. Meera Patel (P002)** flagged for an address conflict between Hospital and State Board records.
3.  **Drift Detection:** Observe providers marked as **"Drift: High"** due to upcoming license expirations.
