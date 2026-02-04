import pytest
from user_display import UserStore


def make_users(n):
    return [
        {
            "id": i,
            "name": f"User{i}",
            "email": f"user{i}@example.com",
            "role": "Admin" if i % 10 == 0 else "User",
            "status": "Active" if i % 3 else "Inactive",
            "join_date": "2023-01-01",
            "last_login": "2025-11-26",
        }
        for i in range(1, n + 1)
    ]


def test_formatter_compact():
    users = make_users(3)
    s = UserStore(users=users).display_users(fmt="compact")
    assert "ID=1" in s
    assert "NAME=User1" in s


def test_formatter_json():
    users = make_users(2)
    s = UserStore(users=users).display_users(fmt="json")
    assert "User1" in s


def test_filter_by_role():
    users = make_users(20)
    store = UserStore(users=users)
    res = store.filter_users({"role": "Admin"})
    assert all(u["role"] == "Admin" for u in res)


def test_filter_regex_name():
    users = make_users(10)
    store = UserStore(users=users)
    res = store.filter_users({"name_regex": r"User[1-3]"})
    assert len(res) >= 1


def test_get_user_by_id_valid():
    users = make_users(5)
    store = UserStore(users=users)
    u = store.get_user_by_id(3)
    assert u["id"] == 3


def test_missing_fields_validation_and_recovery():
    store = UserStore(users=[{"id": 1, "name": None}])
    recovered = store.validate_and_recover({"name": "X"})
    assert recovered["id"] == -1
    assert recovered["name"] == "X"
