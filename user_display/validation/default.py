from .base import Validator, ValidationError


class DefaultValidator(Validator):
    required_fields = ["id", "name", "email"]

    def validate(self, user):
        missing = [f for f in self.required_fields if f not in user or user.get(f) is None]
        if missing:
            raise ValidationError(f"Missing fields: {missing}")
        # basic type checks
        if not isinstance(user.get("id"), int):
            raise ValidationError("id must be int")
        return True

    def recover(self, user):
        # fill sensible defaults
        u = dict(user)
        if "id" not in u or not isinstance(u.get("id"), int):
            u["id"] = -1
        if "name" not in u:
            u["name"] = "<unknown>"
        if "email" not in u:
            u["email"] = ""
        return u
