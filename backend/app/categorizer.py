import csv
import io
import re
from typing import Any, Dict, List

CATEGORIES = {
    "Software & Subscriptions": [
        "adobe",
        "creative cloud",
        "microsoft 365",
        "dropbox",
        "notion",
        "slack",
        "spotify",
        "netflix",
        "canva",
    ],
    "Travel & Transport": [
        "uber",
        "lyft",
        "airbnb",
        "delta",
        "american airlines",
        "southwest",
        "amtrak",
        "train",
        "metro",
        "shell",
        "exxon",
    ],
    "Meals & Dining": [
        "starbucks",
        "coffee",
        "restaurant",
        "pizza",
        "burger",
        "subway",
        "mcdonald",
        "chipotle",
        "panera",
    ],
    "Office & Supplies": [
        "office depot",
        "staples",
        "fedex",
        "ups",
        "amazon",
        "target",
        "walmart",
    ],
    "Groceries": [
        "whole foods",
        "trader joe",
        "kroger",
        "albertsons",
        "shoprite",
        "market",
        "supermarket",
    ],
    "Health & Wellness": [
        "cvs",
        "walgreens",
        "pharmacy",
        "gym",
        "planet fitness",
        "health",
    ],
    "Housing & Utilities": [
        "rent",
        "electric",
        "water",
        "gas",
        "utility",
        "landlord",
        "apartment",
    ],
    "Income & Transfers": [
        "paycheck",
        "salary",
        "deposit",
        "transfer from",
        "employer",
        "cashback",
    ],
    "Refund / Reimbursement": [
        "refund",
        "reimbursement",
        "credit",
    ],
}


def _normalize_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (value or "").lower()).strip()


def _match_category(description: str, amount: float) -> str:
    normalized = _normalize_text(description)
    if amount > 0:
        if any(keyword in normalized for keyword in ["refund", "reimbursement", "credit"]):
            return "Refund / Reimbursement"
        if any(keyword in normalized for keyword in ["deposit", "paycheck", "salary", "transfer from", "employer"]):
            return "Income & Transfers"
    if any(keyword in normalized for keyword in ["adobe", "creative cloud", "microsoft 365", "dropbox", "notion", "slack", "spotify", "netflix", "canva"]):
        return "Software & Subscriptions"
    if any(keyword in normalized for keyword in ["uber", "lyft", "airbnb", "delta", "american airlines", "southwest", "amtrak", "train", "metro", "shell", "exxon"]):
        return "Travel & Transport"
    if any(keyword in normalized for keyword in ["starbucks", "coffee", "restaurant", "pizza", "burger", "subway", "mcdonald", "chipotle", "panera"]):
        return "Meals & Dining"
    if any(keyword in normalized for keyword in ["office depot", "staples", "fedex", "ups", "amazon", "target", "walmart"]):
        return "Office & Supplies"
    if any(keyword in normalized for keyword in ["whole foods", "trader joe", "kroger", "albertsons", "shoprite", "market", "supermarket"]):
        return "Groceries"
    if any(keyword in normalized for keyword in ["cvs", "walgreens", "pharmacy", "gym", "planet fitness", "health"]):
        return "Health & Wellness"
    if any(keyword in normalized for keyword in ["rent", "electric", "water", "gas", "utility", "landlord", "apartment"]):
        return "Housing & Utilities"
    if any(keyword in normalized for keyword in ["paycheck", "salary", "deposit", "transfer from", "employer", "cashback"]):
        return "Income & Transfers"
    return "Needs Review"


def categorize_transaction(description: str, amount: float) -> Dict[str, Any]:
    category = _match_category(description, amount)
    is_positive = amount > 0
    needs_review = category == "Needs Review"

    if category == "Needs Review":
        confidence = "low"
    else:
        confidence = "high" if (is_positive and category in {"Refund / Reimbursement", "Income & Transfers"}) or (not is_positive and category != "Needs Review") else "medium"

    return {
        "description": description,
        "amount": amount,
        "category": category,
        "needs_review": needs_review,
        "confidence": confidence,
    }


def parse_statement_csv(csv_text: str) -> List[Dict[str, Any]]:
    stream = io.StringIO(csv_text)
    reader = csv.DictReader(stream)
    rows: List[Dict[str, Any]] = []

    for row in reader:
        description = row.get("Description") or row.get("Merchant") or row.get("Payee") or ""
        amount = row.get("Amount") or row.get("Debit") or row.get("Credit") or "0"
        try:
            numeric_amount = float(amount)
        except ValueError:
            numeric_amount = 0.0
        rows.append(categorize_transaction(description, numeric_amount))

    return rows
