#!/usr/bin/env python3
import sqlite3
import functools

# ✅ Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Log the query from args or kwargs
        query = kwargs.get('query') if 'query' in kwargs else args[0]
        print(f"[LOG] Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper

# ✅ Function using the decorator
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# ✅ Test fetch with logging
if __name__ == '__main__':
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
