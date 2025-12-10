from user_display.store import UserStore


def make_users(n=5000):
    return [
        {"id": i, "name": f"User{i}", "email": f"user{i}@example.com", "role": "User"}
        for i in range(1, n + 1)
    ]


def test_parallel_same_as_sequential():
    users = make_users()
    s = UserStore()
    criteria = {"name": "User1"}
    seq = s.filter_users(users, criteria, parallel=False)
    par = s.filter_users(users, criteria, parallel=True)
    # sets should match in content
    assert {u["id"] for u in seq} == {u["id"] for u in par}
