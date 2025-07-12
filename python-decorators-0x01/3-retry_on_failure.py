#!/usr/bin/env python3
import sqlite3
import functools
import time

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

# ✅ NEW: Retry decorator
def retry_on_failure(retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt == retries:
                        print("All retry attempts failed.")
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator

# ✅ Function with retry support
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")  # May fail if DB/table is missing
    return cursor.fetchall()

# ✅ Test run
if __name__ == '__main__':
    users = fetch_users_with_retry()
    print(users)
