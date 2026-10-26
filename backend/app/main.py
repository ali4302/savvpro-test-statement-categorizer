from typing import Any, Dict, List

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.categorizer import parse_statement_csv

app = FastAPI(title="Statement Categorizer", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/api/upload")
async def upload_statement(file: UploadFile = File(...)) -> Dict[str, Any]:
    content = await file.read()
    text = content.decode("utf-8-sig")
    rows = parse_statement_csv(text)
    totals = summarize_rows(rows)
    return {"rows": rows, "summary": totals}


def summarize_rows(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    category_totals: Dict[str, float] = {}
    review_count = 0
    spend_total = 0.0

    for row in rows:
        category = row.get("category", "Needs Review")
        amount = float(row.get("amount", 0) or 0)
        if category == "Needs Review":
            review_count += 1
        if category not in category_totals:
            category_totals[category] = 0.0
        category_totals[category] += amount
        if amount < 0:
            spend_total += abs(amount)

    return {
        "category_totals": category_totals,
        "review_count": review_count,
        "spend_total": round(spend_total, 2),
        "transaction_count": len(rows),
    }
