import json
from user_display.formatters import CompactFormatter, JSONFormatter, TableFormatter


def test_compact_formatting():
    f = CompactFormatter()
    s = f.format({"id": 1, "name": "Alice", "email": "a@example.com"})
    assert "ID=1" in s and "NAME=Alice" in s


def test_json_formatting():
    f = JSONFormatter()
    o = {"id": 2, "name": "Bob"}
    s = f.format(o)
    parsed = json.loads(s)
    assert parsed["id"] == 2 and parsed["name"] == "Bob"


def test_table_export():
    f = TableFormatter()
    hdr = f.header()
    assert "EXPORT_BEGIN" in hdr
    exported = f.export({"id": 3, "name": "C"})
    assert "UserID: 3" in exported
