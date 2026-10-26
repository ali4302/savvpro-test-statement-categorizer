# Design notes

## Use case
The app targets a freelance consultant or independent contractor who wants to sort recurring spending for tax time. This is a realistic workflow because small businesses and contractors often see a mix of software subscriptions, travel, meals, and one-off transactions that need manual review.

## Why this use case works well
A statement categorizer needs to handle a lot of noise and ambiguous merchant names. Travel, food, office, and software purchases all appear in the statement, but some transactions do not belong in a spending bucket at all. The app must also recognize refunds, transfers, and edge cases such as a merchant name that is partially recognized.

## Rules-based brain
The categorizer in [backend/app/categorizer.py](backend/app/categorizer.py) uses a deterministic decision tree:

1. Normalize the transaction description.
2. Check whether the amount is positive or negative.
3. Look for merchant keywords in a curated map of categories.
4. Treat refunds and reimbursement credits as special cases.
5. Send anything not matched confidently to `Needs Review`.

This is intentionally conservative. If the app is uncertain, it asks the user to review instead of making a wrong tax classification.

## Category examples
- `ADOBE CREATIVE CLOUD` → `Software & Subscriptions`
- `UBER *TRIP` → `Travel & Transport`
- `JOES CAFE 9921` → `Meals & Dining` or `Needs Review` if ambiguous
- `ADOBE REFUND` → `Refund / Reimbursement`
- `TRANSFER TO SAVINGS` → `Needs Review` or `Income & Transfers` depending on the scenario

## Review workflow
The app shows the initial categorization immediately after upload. Any row classified as `Needs Review` stays visible and can be corrected from a dropdown. This makes the process transparent for tax filing and creates a practical final review step.

## Risk handling
The app deliberately avoids overconfident guesses. This reduces tax mistakes and improves trust because the user sees what was matched, what was uncertain, and what still needs a quick manual decision.
