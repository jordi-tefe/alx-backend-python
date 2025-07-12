#!/usr/bin/env python3
import sqlite3
import functools

# ✅ Reuse from Task 1
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# ✅ NEW: Transactional decorator
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # ✅ Commit if successful
            return result
        except Exception as e:
            conn.rollback()  # ❌ Rollback if error
            print(f"Transaction failed: {e}")
            raise
    return wrapper

# ✅ Usage of both decorators
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# ✅ Test run
if __name__ == '__main__':
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
    print("Email updated successfully.")
