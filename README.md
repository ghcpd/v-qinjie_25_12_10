User Display Module (Optimized)

This project refactors the baseline user display module into a modular, high-performance, and fault-tolerant package.

Architecture
- UserStore: in-memory store with indices for O(1) lookups
- Formatters: compact, JSON, table
- Filters: regex and composite filters
- Validation: soft-failure recovery
- Metrics: lightweight counters
- Plugins: simple registry

Usage
- See user_display_optimized.py for API compatibility with the original module.

Run tests
- Install dependencies: pip install -r requirements.txt
- Run tests: pytest -q
