import os
import time
from user_display_optimized import display_users, filter_users, get_user_by_id

# Skip long performance tests by default; enable with UD_RUN_PERF=1
SKIP = os.environ.get('UD_RUN_PERF','0') != '1'


def _make_users(n):
    return [{'id': i, 'name': f'User{i}', 'email': f'user{i}@example.com', 'role': 'Admin' if i%10==0 else 'User', 'status': 'Active', 'join_date':'2023-01-01', 'last_login':'2025-01-01'} for i in range(1,n+1)]


def test_50k_performance():
    if SKIP:
        return
    users = _make_users(50000)
    t0 = time.perf_counter()
    out = display_users(users, show_all=False)
    t_display = (time.perf_counter() - t0) * 1000.0
    print(f"display time ms: {t_display}")
    assert t_display < 120.0, f"display too slow: {t_display}ms"

    t0 = time.perf_counter()
    res = filter_users(users, {'name':'User49999'})
    t_filter = (time.perf_counter() - t0) * 1000.0
    print(f"filter time ms: {t_filter}")
    assert t_filter < 15.0, f"filter too slow: {t_filter}ms"

    t0 = time.perf_counter()
    u = get_user_by_id(users, 49999)
    t_lookup = (time.perf_counter() - t0) * 1000.0
    print(f"lookup time ms: {t_lookup}")
    assert t_lookup < 0.5, f"lookup too slow: {t_lookup}ms"
