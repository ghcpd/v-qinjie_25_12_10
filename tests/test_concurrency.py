import concurrent.futures
from user_display.store import UserStore


def test_snapshot_consistency():
    users = [{"id": i, "name": f"U{i}"} for i in range(1000)]
    s = UserStore(users)
    snap = s.snapshot()
    # Update store concurrently
    def update():
        for i in range(1000, 1100):
            try:
                s.add_user({"id": i, "name": f"U{i}"})
            except Exception:
                pass

    with concurrent.futures.ThreadPoolExecutor() as ex:
        f = ex.submit(update)
        # snapshot should not change
        assert len(snap) == 1000
        f.result()
