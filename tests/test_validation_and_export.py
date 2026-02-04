from user_display.validation.default import DefaultValidator
from user_display_optimized import export_users_to_string


def test_validator_handles_bad_input():
    v = DefaultValidator()
    out = v.validate({'id': 1, 'name': None, 'last_login': 'bad-date'})
    assert out['name'] == ''
    assert '_last_login_ts' in out


def test_export_handles_corrupted_user():
    users = [{'id': 1, 'name': 'A', 'last_login': 'not-a-date'}]
    s = export_users_to_string(users)
    assert 'LastLoginTS' in s
