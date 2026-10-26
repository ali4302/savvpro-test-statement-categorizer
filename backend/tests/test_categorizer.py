from app.categorizer import categorize_transaction, parse_statement_csv


def test_software_subscription_is_categorized():
    result = categorize_transaction("ADOBE CREATIVE CLOUD", -59.99)
    assert result["category"] == "Software & Subscriptions"
    assert result["needs_review"] is False


def test_unknown_transaction_needs_review():
    result = categorize_transaction("JOES CAFE 9921", -18.5)
    assert result["category"] == "Needs Review"
    assert result["needs_review"] is True


def test_refund_is_not_income():
    result = categorize_transaction("ADOBE REFUND", 29.99)
    assert result["category"] == "Refund / Reimbursement"
    assert result["needs_review"] is False


def test_parse_statement_csv_reads_rows():
    csv_data = "Date,Description,Amount\n2024-06-01,ADOBE CREATIVE CLOUD,-59.99\n2024-06-02,JOES CAFE 9921,-18.50\n"
    rows = parse_statement_csv(csv_data)
    assert len(rows) == 2
    assert rows[0]["category"] == "Software & Subscriptions"
    assert rows[1]["category"] == "Needs Review"
