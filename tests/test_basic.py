import time
from user_display_optimized import display_users, get_user_by_id, export_users_to_string


sample = [{"id": i, "name": f"User{i}", "email": f"u{i}@ex.com", "role": "User", "status": "Active"} for i in range(1, 101)]


def test_display_basic():
    out = display_users(sample, show_all=True, verbose=False, profile="compact")
    assert "PROCESSED=100" in out
    assert "ID=1" in out


def test_get_user_by_id():
    u = get_user_by_id(sample, 10)
    assert u["id"] == 10


def test_export_json():
    s = export_users_to_string(sample, profile="json")
    assert '"count": 100' in s
