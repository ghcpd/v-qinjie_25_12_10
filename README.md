User Display Modular Rework

This project refactors the legacy user_display module into a modular, concurrent, and testable package.

Structure:
- user_display/: core modules (store, formatters, filters, validation, plugins)
- user_display_optimized.py: compatibility wrapper preserving public API
- tests/: pytest test suite including a performance test generating 50k users

Usage examples available in tests. Run `pytest -q` to execute.
