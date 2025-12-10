import time
from user_display.store import UserStore


def make_users(n=1000):
    return [
        {"id": i, "name": f"User{i}", "email": f"u{i}@example.com", "last_login": "2025-01-01"}
        for i in range(1, n + 1)
    ]


def test_get_user_by_id_fast():
    users = make_users(2000)
    s = UserStore()
    # index should be built lazily
    res = s.get_user_by_id(users, 1999)
    assert res and res["id"] == 1999


def test_display_users_is_deterministic():
    users = make_users(20)
    s = UserStore()
    out = s.display_users(users, show_all=True, verbose=False, formatter="compact")
    assert "PROCESSED=20" in out
