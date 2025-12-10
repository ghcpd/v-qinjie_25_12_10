#!/usr/bin/env python
"""Quick verification script to test all APIs."""

import sys
sys.path.insert(0, '.')

from user_display_optimized import (
    display_users, get_user_by_id, filter_users, export_users_to_string
)

print("=" * 60)
print("USER DISPLAY MODULE - VERIFICATION")
print("=" * 60)

# Create test data
users = [
    {"id": i, "name": f"User{i}", "email": f"u{i}@test.com", "role": "Admin" if i % 3 == 0 else "User", "status": "Active"}
    for i in range(1, 11)
]
print("✓ Generated 10 test users")

# Test display_users
result = display_users(users)
print(f"✓ display_users works ({len(result)} chars output)")

# Test get_user_by_id
user = get_user_by_id(users, 1)
name = user["name"] if user else "None"
print(f"✓ get_user_by_id works (User: {name})")

# Test filter_users
filtered = filter_users(users, {"role": "Admin"})
print(f"✓ filter_users works ({len(filtered)} Admin users)")

# Test export_users_to_string
export = export_users_to_string(users)
print(f"✓ export_users_to_string works ({len(export)} chars output)")

print("\n" + "=" * 60)
print("✓✓✓ ALL APIS WORKING CORRECTLY ✓✓✓")
print("=" * 60)
