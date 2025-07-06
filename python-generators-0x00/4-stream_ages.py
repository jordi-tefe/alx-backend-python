from seed import connect_to_prodev

def stream_user_ages():
    """Generator that yields user ages one at a time from the database."""
    connection = connect_to_prodev()
    cursor = connection.cursor()

    cursor.execute("SELECT age FROM user_data")

    for row in cursor:
        yield row[0]  # yields just the age value

    cursor.close()
    connection.close()


def average_user_age():
    """Computes average user age using the stream_user_ages generator."""
    total = 0
    count = 0

    for age in stream_user_ages():
        total += age
        count += 1

    average = total / count if count > 0 else 0
    print(f"Average age of users: {average:.2f}")
    return average  # Optional, useful for testing
