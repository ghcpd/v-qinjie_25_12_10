import time
from user_display.store import UserStore


def make_users(n=50000):
    return [
        {"id": i, "name": f"User{i}", "email": f"u{i}@example.com", "role": "User"}
        for i in range(1, n + 1)
    ]


def test_display_50k_performance():
    users = make_users(50000)
    s = UserStore()
    t0 = time.perf_counter()
    out = s.display_users(users, show_all=False, formatter="compact")
    t1 = time.perf_counter()
    dt = t1 - t0
    # We want this to be fast — but bench environments differ.
    # Assert it's under 1.0s in CI; target faster in real runs.
    assert dt < 1.0, f"display_users is slower than expected: {dt:.3f}s"


def test_filter_50k_performance():
    users = make_users(50000)
    s = UserStore()
    criteria = {"name": "User49999"}
    t0 = time.perf_counter()
    res = s.filter_users(users, criteria, parallel=False)
    t1 = time.perf_counter()
    dt = t1 - t0
    assert dt < 0.5, f"filter_users slower than expected: {dt:.3f}s"
    assert any(u.get("id") == 49999 for u in res)


def test_id_lookup_50k_performance():
    users = make_users(50000)
    s = UserStore()
    t0 = time.perf_counter()
    u = s.get_user_by_id(users, 12345)
    t1 = time.perf_counter()
    dt = (t1 - t0) * 1000.0
    # ID lookup should be low ms-scale
    assert dt < 5.0, f"get_user_by_id too slow: {dt:.3f}ms"
    assert u and u.get("id") == 12345
