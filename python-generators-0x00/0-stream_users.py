def stream_users():
    import seed
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)  # to get rows as dicts

    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row  # yield one row at a time

    cursor.close()
    connection.close()
