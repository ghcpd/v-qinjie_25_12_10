from user_display.validation.default import DefaultValidator
from user_display.errors import ValidationError


def test_validate_happy_path():
    v = DefaultValidator()
    good = {"id": 1, "name": "A", "email": "a@x.com"}
    assert v.validate(good) == good


def test_validate_missing_fields_raises():
    v = DefaultValidator()
    try:
        v.validate({"id": 2})
        raised = False
    except ValidationError:
        raised = True
    assert raised


def test_recover_creates_defaults():
    v = DefaultValidator()
    rec = v.recover({"id": 100})
    assert rec["id"] == 100 and rec["name"] == ""
