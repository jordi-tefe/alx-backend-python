# 📁 python-generators-0x00

## 🔰 Project: Advanced Python – Generators

This project introduces advanced usage of **Python generators** to handle large datasets efficiently, simulate real-time data processing, and optimize performance in data-driven applications. 

It is part of the **ALX Backend Python track**.

---

## 📌 Task 0: Getting Started with Python Generators

### 🎯 Objective
Create a Python script to:
- Set up a MySQL database `ALX_prodev`
- Create a table `user_data`
- Populate it using a CSV file `user_data.csv`

This task lays the foundation for generator-based data processing by preparing and seeding a realistic dataset into MySQL.

---

### 🛠 Files

- `seed.py` – Main logic to set up DB, table, and insert data from CSV.
- `0-main.py` – Used to test the setup logic.
- `user_data.csv` – Sample dataset to seed the database.

---

### 🧱 Table Schema

| Column Name | Type         | Description                     |
|-------------|--------------|---------------------------------|
| user_id     | VARCHAR(36)  | Primary Key (UUID format)       |
| name        | VARCHAR(255) | User's full name (not null)     |
| email       | VARCHAR(255) | User's email address (not null) |
| age         | DECIMAL      | User's age (not null)           |

The `user_id` column is **indexed** for optimized retrieval.

---

### 🧪 How to Run

1. Ensure MySQL server is running.
2. Update MySQL credentials in `seed.py`:
   ```python
   user="your_username",
   password="your_password"
