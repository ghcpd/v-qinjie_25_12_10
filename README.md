# user_display — modular, concurrent, fault-tolerant display module

This repository refactors a chaotic baseline module (`user_display_original.py`) into
a modular, faster, and more reliable system while preserving the original
public API via `user_display_optimized.py`.

Highlights
 - O(1) ID lookup via in-memory index
 - Modular formatters, filters, validation and plugins
 - Thread-safe `UserStore` with snapshots
 - Optional parallel filtering
 - Small metrics and structured logging

Performance targets (engineered for typical modern hardware):

 - Display 50,000 users: < 120 ms (target)
 - Filter 50,000 users: < 15 ms (target)
 - ID lookup: < 0.5 ms

Tests
 - Tests are under `tests/` and include functional checks and a 50k performance benchmark.

Run tests

Windows PowerShell:

```powershell
.
venv\Scripts\Activate.ps1  # create and activate a venv if needed
pip install -r requirements.txt
pytest -q
```
