"""
Intentionally more chaotic and inefficient baseline.
Used as the starting point for a major refactor.
"""

import time
import random
import json
from datetime import datetime


def display_users(users, show_all=True, verbose=False):
    """
    Worse version:
    - Still O(n^2) string concatenation
    - Random sleep injected
    - Sometimes prints partial user
    - Repeated JSON serialization for no reason
    - No guarantee of field existence
    """
    result = ""
    count = 0

    for u in users:
        if verbose:
            print("BEGIN_PROCESS_USER", u.get("id"))

        # Unnecessary serialization/deserialization
        try:
            u2 = json.loads(json.dumps(u))
        except Exception:
            # silently skip or partially display
            u2 = {"id": u.get("id", None)}

        # Highly redundant field extraction
        s = ""
        s += "ID=" + str(u2.get("id", "N/A"))
        s += " | NAME=" + str(u2.get("name", ""))
        s += " | EMAIL=" + str(u2.get("email", ""))
        s += " | ROLE=" + str(u2.get("role", ""))
        s += " | STATUS=" + str(u2.get("status", ""))
        s += " | JOIN_DATE=" + str(u2.get("join_date", ""))
        s += " | LAST_LOGIN=" + str(u2.get("last_login", ""))

        # Random partial corruption
        if random.random() < 0.03:
            s = s[: random.randint(5, max(5, len(s) // 2))]

        result += s + "\n"
        count += 1

        # Worse artificial delay
        time.sleep(random.random() * 0.02)

    if show_all:
        result += "PROCESSED=" + str(count) + "\n"

    return result


def get_user_by_id(users, uid):
    """
    Much worse than before:
    - Randomly scans from a shuffled list
    - Linear search multiple times
    - Randomly returns malformed data
    """
    indices = list(range(len(users)))
    random.shuffle(indices)

    for i in indices:
        u = users[i]
        if u.get("id") == uid:
            # 10% chance to corrupt the user
            if random.random() < 0.1:
                return {"error": "corrupted", "id": uid}
            return u

    return None


def filter_users(users, criteria):
    """
    Worse filter:
    - Case handling inconsistent
    - Redundant checks
    - Random extra passes
    - No guaranteed determinism
    """
    res = []

    # Random useless extra loop
    for _ in range(random.randint(1, 3)):
        for u in users:
            include = True

            # Hard-coded inconsistent case sensitivity
            if "name" in criteria:
                if criteria["name"].lower() not in u.get("name", "").lower():
                    include = False

            if "email" in criteria:
                if criteria["email"] not in u.get("email", ""):
                    include = False

            if "role" in criteria:
                if u.get("role") != criteria["role"]:
                    include = False

            if "status" in criteria:
                if u.get("status") != criteria["status"]:
                    include = False

            if include and u not in res:
                res.append(u)

    return res


def export_users_to_string(users):
    """
    Worse exporter:
    - Repeated heavy timestamp formatting
    - Random sorting
    - Redundant string building
    """
    header = "EXPORT_BEGIN\n" + ("=" * 120) + "\n"
    out = header

    # Random ordering
    tmp = list(users)
    random.shuffle(tmp)

    for u in tmp:
        block = ""
        block += "UserID: " + str(u.get("id", "N/A")) + "\n"
        block += "  Name: " + str(u.get("name", "")) + "\n"
        block += "  LastLoginParsed: " + str(
            datetime.strptime(
                u.get("last_login", "2000-01-01"), "%Y-%m-%d"
            ).timestamp()
        ) + "\n"
        block += "-" * 120 + "\n"
        out += block

    out += "EXPORT_END\n"
    return out


sample_users = [
    {
        "id": i,
        "name": f"User{i}",
        "email": f"user{i}@example.com",
        "role": random.choice(["Admin", "User", "Mod"]),
        "status": random.choice(["Active", "Inactive"]),
        "join_date": "2023-01-01",
        "last_login": "2025-11-26",
    }
    for i in range(1, 101)
]
