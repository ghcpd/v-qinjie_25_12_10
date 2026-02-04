from user_display import CompactFormatter, JsonFormatter, TableFormatter


def _make_users(n=3):
    return [{'id': i, 'name': f'U{i}', 'email': f'u{i}@ex', 'role':'User','status':'Active','join_date':'2023-01-01','last_login':'2025-01-01'} for i in range(1,n+1)]


def test_compact():
    fmt = CompactFormatter()
    s = fmt.format_many(_make_users(2))
    assert 'ID=1' in s and 'ID=2' in s


def test_json():
    fmt = JsonFormatter()
    s = fmt.format_many(_make_users(2))
    assert 'users' in s or s.startswith('[')


def test_table():
    fmt = TableFormatter()
    s = fmt.format_many(_make_users(2))
    assert 'NAME' in s and 'EMAIL' in s
