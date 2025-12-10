"""Pytest configuration helpers.

Ensures the repository root is added to sys.path so tests import the local
`user_display` package reliably regardless of how the test runner is invoked.
"""
import sys
from pathlib import Path


def pytest_sessionstart(session):
    # Insert project root at the front of sys.path so local package imports succeed
    root = Path(__file__).resolve().parents[1]
    p = str(root)
    if p not in sys.path:
        sys.path.insert(0, p)
