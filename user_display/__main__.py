from .store import UserStore
from .formatters.compact import CompactFormatter

def main():
    # quick demo
    users = [{'id': i, 'name': f'User{i}', 'email': f'user{i}@example.com', 'role':'User', 'status':'Active', 'join_date':'2023-01-01', 'last_login':'2025-01-01'} for i in range(1,21)]
    store = UserStore(users)
    fmt = CompactFormatter()
    print(fmt.format_many(store.list_users()))

if __name__ == '__main__':
    main()