from user_display.filters import RegexFilter, CompositeFilter


def make_users():
    return [
        {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "Admin"},
        {"id": 2, "name": "Bob", "email": "bob@acme.com", "role": "User"},
        {"id": 3, "name": "bobby", "email": "bobby@acme.com", "role": "User"},
    ]


def test_composite_case_insensitive():
    users = make_users()
    f = CompositeFilter()
    assert f.match(users[1], {"name": "bob"})
    assert f.match(users[2], {"name": "Bob"})


def test_regex_filter():
    users = make_users()
    r = RegexFilter()
    assert r.match(users[1], {"email": "/^bob@acme/"})
    assert not r.match(users[0], {"email": "/^bob@acme/"})
