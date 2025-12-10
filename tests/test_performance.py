import time

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


def test_display_50000_timing():
    users = make_users(50000)
    store = UserStore(users=users)
    t0 = time.perf_counter()
    s = store.display_users(fmt="compact", show_all=False)
    t1 = time.perf_counter()
    elapsed_ms = (t1 - t0) * 1000
    print("display elapsed ms:", elapsed_ms)
    assert elapsed_ms < 120_000  # allow wider headroom in CI


def test_filter_50000_timing():
    users = make_users(50000)
    store = UserStore(users=users)
    t0 = time.perf_counter()
    res = store.filter_users({"role": "Admin"})
    t1 = time.perf_counter()
    elapsed_ms = (t1 - t0) * 1000
    print("filter elapsed ms:", elapsed_ms)
    # Index-based filter should be quick
    assert elapsed_ms < 20000  # 20s


def test_lookup_fast():
    users = make_users(50000)
    store = UserStore(users=users)
    t0 = time.perf_counter()
    u = store.get_user_by_id(49999)
    t1 = time.perf_counter()
    elapsed_ms = (t1 - t0) * 1000
    print("lookup ms:", elapsed_ms)
    assert elapsed_ms < 5  # milliseconds
