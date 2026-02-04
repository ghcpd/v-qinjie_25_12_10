from user_display_optimized import filter_users


sample = [{"id": i, "name": f"User{i}", "email": f"u{i}@ex.com", "role": "User", "status": "Active"} for i in range(1, 201)]


def test_simple_filter_name():
    res = filter_users(sample, {"name": "User1"})
    assert any(u["id"] == 1 for u in res)


def test_regex_filter():
    res = filter_users(sample, {"name": "r/^User1"})
    assert any(u["id"] == 1 for u in res)


def test_parallel_filter():
    res = filter_users(sample, {"email": "u1@ex.com"}, parallel=True)
    assert any(u["id"] == 1 for u in res)
