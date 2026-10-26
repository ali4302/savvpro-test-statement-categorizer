# Statement Categorizer

A full-stack app that uploads a bank or credit-card statement, classifies each transaction with a rules-based categorizer, and lets the user review ambiguous rows before finalizing the total spend by category.

## Use case
This app is built for a freelance consultant who wants a quick tax-time review of personal or business card spending. It recognizes recurring merchants, handles refunds, and flags uncertain transactions as `Needs Review` instead of guessing.

## Tech stack
- Backend: Python + FastAPI
- Frontend: Next.js + React
- Transaction rules: custom Python logic with keyword matching, amount checks, and review thresholds
- Tests: pytest

## Setup

### 1) Install Python dependencies

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Install frontend dependencies

```bash
cd frontend
npm install
```

### 3) Run the backend

```bash
cd backend
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4) Run the frontend

```bash
cd frontend
npm run dev
```

Open the frontend in your browser at `http://localhost:3000`.

## Example CSV format

```csv
Date,Description,Amount
2024-06-01,ADOBE CREATIVE CLOUD,-59.99
2024-06-02,UBER *TRIP,-19.40
2024-06-03,TRANSFER TO SAVINGS,-200.00
2024-06-04,JOES CAFE 9921,-18.50
2024-06-06,ADOBE REFUND,29.99
```

## How the categorizer works
The app does not call an external AI model. Instead, it uses a rules engine that:
- normalizes merchant names
- checks positive vs. negative amounts
- matches recurring merchant keywords to categories
- flags anything that is not confidently matched as `Needs Review`

## Test command

```bash
cd backend
source .venv/bin/activate
pytest -q
```

## Notes
- All data is fake and designed for demos.
- The app intentionally prefers a review queue over bad guesses.
