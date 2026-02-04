import os
from user_display_optimized import display_users, get_user_by_id, filter_users, export_users_to_string, sample_users


def test_display_and_get():
    out = display_users(sample_users[:5], show_all=True)
    assert "PROCESSED=5" in out
    u = get_user_by_id(sample_users, 3)
    assert u is not None and u.get('id') == 3
    assert get_user_by_id(sample_users, 9999) is None


def test_filter_simple():
    res = filter_users(sample_users, {"name": "User1"})
    assert any(u['id'] == 1 for u in res)
    res2 = filter_users(sample_users, {"email": "user2@example.com"})
    assert any(u['id'] == 2 for u in res2)
    res3 = filter_users(sample_users, {"role": "Admin"})
    assert all(u['role'] == 'Admin' for u in res3)


def test_export_contains_header_and_footer():
    s = export_users_to_string(sample_users[:3])
    assert s.startswith('EXPORT_BEGIN')
    assert s.strip().endswith('EXPORT_END')
