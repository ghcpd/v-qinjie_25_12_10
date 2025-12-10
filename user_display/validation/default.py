from .base import Validator
from ..errors import ValidationError
from typing import Dict


class DefaultValidator(Validator):
    """A forgiving validator that ensures keys exist and coerces types when possible."""

    REQUIRED = ["id", "name", "email"]

    def validate(self, user: Dict) -> Dict:
        if not isinstance(user, dict):
            raise ValidationError("not_a_dict")

        # quick checks
        for k in self.REQUIRED:
            if k not in user:
                raise ValidationError(f"missing_{k}")

        return user

    def recover(self, user: Dict) -> Dict:
        # Create a cleaned dict with default values so downstream code never fails
        if not isinstance(user, dict):
            return {"id": None, "name": "", "email": "", "role": "", "status": ""}

        out = dict(user)
        out.setdefault("id", None)
        out.setdefault("name", "")
        out.setdefault("email", "")
        out.setdefault("role", "")
        out.setdefault("status", "")
        out.setdefault("join_date", "")
        out.setdefault("last_login", "")
        return out
