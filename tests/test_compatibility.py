from user_display_optimized import display_users, get_user_by_id, filter_users, export_users_to_string


def test_api_functions_smoke():
    users = [
        {"id": 1, "name": "Alice", "email": "a@x.com", "role": "User", "status": "Active"},
        {"id": 2, "name": "Bob", "email": "b@x.com", "role": "Admin", "status": "Inactive"},
    ]
    s = display_users(users, show_all=True)
    assert "ID=1" in s
    u = get_user_by_id(users, 2)
    assert u["name"] == "Bob"
    res = filter_users(users, {"role": "Admin"})
    assert len(res) == 1
    out = export_users_to_string(users, fmt="json")
    assert "Alice" in out
