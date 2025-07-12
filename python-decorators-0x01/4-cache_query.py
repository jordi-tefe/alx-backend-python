#!/usr/bin/env python3
import sqlite3
import functools

# In-memory query cache
query_cache = {}

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

# ✅ NEW: Cache decorator
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print("⚡ Returning cached result")
            return query_cache[query]
        print("💾 Caching new result")
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

# ✅ Function using caching
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# ✅ Test it
if __name__ == '__main__':
    users = fetch_users_with_cache(query="SELECT * FROM users")
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)
