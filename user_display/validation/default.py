from .base import Validator
from ..logging_utils import struct_log
from datetime import datetime

class DefaultValidator(Validator):
    def __init__(self, strict=False):
        self.strict = strict

    def validate(self, user):
        # Ensure basic fields and types
        if not isinstance(user, dict):
            struct_log('warn', 'Invalid user type, replacing with minimal dict', original=repr(user))
            return {"id": None, "corrupted": True}

        out = {}
        out['id'] = user.get('id')
        out['name'] = user.get('name') or ''
        out['email'] = user.get('email') or ''
        out['role'] = user.get('role') or 'User'
        out['status'] = user.get('status') or 'Unknown'
        out['join_date'] = user.get('join_date') or '1970-01-01'
        out['last_login'] = user.get('last_login') or '1970-01-01'

        # parse dates once and store timestamps
        try:
            out['_join_ts'] = int(datetime.strptime(out['join_date'], '%Y-%m-%d').timestamp())
        except Exception:
            out['_join_ts'] = 0
            struct_log('debug', 'Invalid join_date', user_id=out['id'], join_date=out['join_date'])

        try:
            out['_last_login_ts'] = int(datetime.strptime(out['last_login'], '%Y-%m-%d').timestamp())
        except Exception:
            out['_last_login_ts'] = 0
            struct_log('debug', 'Invalid last_login', user_id=out['id'], last_login=out['last_login'])

        return out