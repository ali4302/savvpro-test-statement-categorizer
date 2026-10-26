# AI usage log

This project was built with a local coding workflow and did not use a large external AI model to make transaction decisions. The "brain" of the app is a custom rules engine written in Python.

## Tools used
- VS Code Copilot via agent assistance for project structure, code generation, and debugging help
- Python and frontend tooling for local verification and build checks

## How AI helped
- Suggested a clean project structure and file layout
- Drafted the initial backend and frontend scaffolding
- Helped refine the category keyword map and review workflow
- Assisted with documentation and README writing

## Where AI got things wrong
- It initially suggested broad merchant matches that created false positives.
- It needed manual constraints to avoid classifying refunds as income.
- The final logic was tightened to be conservative and route uncertain rows to `Needs Review`.

## Token usage
No external AI provider API tokens were used for classification. The environment used local development assistance only, so there are no provider token logs to attach. The project therefore stores the decision logic directly in source code instead of calling a hosted model.

## Verification evidence
The relevant verification steps were run locally using the installed Python test suite and a frontend build check. The app logic is deterministic and auditable in source control instead of hidden behind a model call.
