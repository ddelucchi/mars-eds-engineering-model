# Contributing

Changes should improve traceability, reproducibility, or physical fidelity.

Before opening a pull request:

1. Keep new physical constants or baseline parameters configurable.
2. Document the source or rationale for every new default.
3. Distinguish measured, literature-derived, assumed, and fitted values.
4. Add or update tests when model behavior changes.
5. Run `ruff check src tests` and `pytest -q`.
6. Do not describe unvalidated calculations as measured performance.

For changes that alter governing equations, update `docs/physics-model.md` and
explain the validation consequence in the pull request.
