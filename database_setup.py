import sqlite3

print("Setting up the database...")

# Connect to (or create) the database file
conn = sqlite3.connect('passwords.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Drop tables if they exist to ensure a clean setup
cursor.execute("DROP TABLE IF EXISTS passwords;")
cursor.execute("DROP TABLE IF EXISTS users;")

print("Existing tables dropped (if they existed).")

# SQL command to create a table named 'passwords'
# This table will store an ID, the name of the service (e.g., "Google"),
# and the actual password for that service.
create_table_query = """
CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_name TEXT NOT NULL,
    password_value TEXT NOT NULL
);
"""

cursor.execute(create_table_query)

print("Table 'passwords' created successfully (if it didn't exist).")

# SQL command to create a table named 'users'
create_users_table_query = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    pin TEXT NOT NULL
);
"""

cursor.execute(create_users_table_query)

print("Table 'users' created successfully (if it didn't exist).")

# Check if the admin user already exists
cursor.execute("SELECT * FROM users WHERE username = 'admin'")
if cursor.fetchone() is None:
    # Insert a default admin user
    cursor.execute("INSERT INTO users (username, password, pin) VALUES (?, ?, ?)", ('admin', 'password', '078123'))
    print("Default admin user created.")



# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database setup complete.")