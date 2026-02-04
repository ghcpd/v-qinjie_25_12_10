from user_display_optimized import display_users

sample = [{"id": 1, "name": "Alice", "email": "a@ex.com", "role": "Admin", "status": "Active"}]


def test_compact_format():
    out = display_users(sample, profile="compact")
    assert "ID=1" in out


def test_table_format():
    out = display_users(sample, profile="table")
    assert "UserID: 1" in out


def test_json_format():
    out = display_users(sample, profile="json")
    assert '"users"' in out
