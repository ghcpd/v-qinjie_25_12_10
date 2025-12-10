import time
from user_display_optimized import display_users, filter_users, get_user_by_id


def _make(n):
    return [{"id": i, "name": f"User{i}", "email": f"u{i}@ex.com", "role": "User", "status": "Active"} for i in range(1, n+1)]


def test_performance_50k():
    users = _make(50000)
    t0 = time.time()
    out = display_users(users, profile="compact")
    t_display = time.time() - t0

    t0 = time.time()
    res = filter_users(users, {"name": "User49999"}, parallel=True)
    t_filter = time.time() - t0

    t0 = time.time()
    u = get_user_by_id(users, 25000)
    t_lookup = time.time() - t0

    print(f"display={t_display:.3f}s filter={t_filter:.3f}s lookup={t_lookup*1000:.3f}ms")
    # Check operations complete and are reasonably fast
    assert u["id"] == 25000
    assert t_lookup < 0.01
    assert t_filter < 2.0
    assert t_display < 5.0
