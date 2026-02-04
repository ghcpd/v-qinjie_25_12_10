from user_display.validation.default import DefaultValidator


def test_missing_fields():
    v = DefaultValidator()
    u = v.validate(None)
    assert u["id"] is None
    assert u["name"] == ""


def test_date_normalization():
    v = DefaultValidator()
    u = v.validate({"id": 1, "last_login": "2025-01-02T03:04:05"})
    assert u["last_login"] == "2025-01-02"
