#!/usr/bin/env python3
import sqlite3
import functools

# ✅ Decorator to automatically manage DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

# ✅ Example function using the connection decorator
@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# ✅ Test function with connection handling
if __name__ == '__main__':
    user = get_user_by_id(user_id=1)
    print(user)
