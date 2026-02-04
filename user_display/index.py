class Index:
    def __init__(self, users):
        # users is a list; build id_map and attribute maps
        self.id_map = {}
        self.role_map = {}
        self.status_map = {}
        self._build(users)

    def _build(self, users):
        for i, u in enumerate(users):
            uid = u.get("id")
            self.id_map[uid] = i
            role = u.get("role")
            status = u.get("status")
            if role is not None:
                self.role_map.setdefault(role, set()).add(i)
            if status is not None:
                self.status_map.setdefault(status, set()).add(i)

    def add_users(self, users, start_index=0):
        for offset, u in enumerate(users):
            i = start_index + offset
            uid = u.get("id")
            self.id_map[uid] = i
            role = u.get("role")
            status = u.get("status")
            if role is not None:
                self.role_map.setdefault(role, set()).add(i)
            if status is not None:
                self.status_map.setdefault(status, set()).add(i)

    def get_by_id(self, uid):
        idx = self.id_map.get(uid)
        if idx is None:
            return None
        return self._get_user_by_index(idx)

    def _get_user_by_index(self, idx):
        # Placeholder: store doesn't belong here; the store will access using index
        # but for simplification we will let store pass
        raise NotImplementedError("Index cannot fetch user without store")

    def ids_for_role(self, role):
        return set(self.role_map.get(role, set()))

    def ids_for_status(self, status):
        return set(self.status_map.get(status, set()))
