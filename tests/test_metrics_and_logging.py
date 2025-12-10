from user_display import display_users
from user_display.metrics import metrics


def test_metrics_update_on_display():
    users = [{"id": 1, "name": "A", "email": "a@x.com"}]
    # reset metrics by re-creating
    metrics.increment("test_marker", 0)
    before = metrics.snapshot()
    _ = display_users(users, show_all=True, verbose=False)
    after = metrics.snapshot()
    assert after["timers"].get("display_users_count", None) == 1
