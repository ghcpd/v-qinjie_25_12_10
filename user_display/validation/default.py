from .base import Validator
from ..errors import ValidationError
from datetime import datetime


class DefaultValidator(Validator):
    def validate(self, user):
        # Return a sanitized copy with defaults
        if user is None:
            return {"id": None, "name": "", "email": "", "role": "", "status": ""}
        u = dict(user)
        # Ensure id exists
        if "id" not in u:
            u["id"] = None
        # Validate dates: keep as string but normalize if possible
        for d in ("join_date", "last_login"):
            if d in u:
                try:
                    # parse but keep as ISO
                    dt = datetime.fromisoformat(str(u[d]))
                    u[d] = dt.date().isoformat()
                except Exception:
                    u[d] = u.get(d, "")
        return u
