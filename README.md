User Display Module — Optimized

This project refactors a chaotic baseline display module into a modular, concurrent-safe, and extensible package.

Highlights
- O(1) id lookup via index in UserStore
- Buffered string builders for fast display
- Single-pass filtering with optional caching
- Pluggable formatters (compact, json, table)
- Pluggable filters and validators
- Validation with fallback recovery and single-pass date parsing
- Structured logging and simple metrics
- Snapshot support for consistent concurrent reads

API Compatibility
The following API functions are preserved in user_display_optimized.py
- display_users(users, show_all=True, verbose=False)
- get_user_by_id(users, uid)
- filter_users(users, criteria)
- export_users_to_string(users)

Testing
- Tests are in /tests using pytest
- A heavy performance test for 50k users exists but is skipped by default. To run it, set environment variable UD_RUN_PERF=1 before invoking run_tests.ps1

Run tests
- Windows PowerShell: ./run_tests.ps1

Package Structure
- user_display/
  - store.py: UserStore with index, snapshot and caching
  - formatters/: compact, json_fmt, table
  - filters/: regex, composite
  - validation/: default validator
  - metrics.py, plugins.py, logging_utils.py

Notes
- The 50k performance test is optimistic: real timing depends on machine. Use UD_RUN_PERF=1 to run the test on a CI machine.
