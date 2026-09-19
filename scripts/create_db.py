import sqlite3


conn = sqlite3.connect("data/ledger.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS departments (
    department_id INTEGER PRIMARY KEY,
    department_name TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    account_id INTEGER PRIMARY KEY,
    account_name TEXT NOT NULL,
    account_type TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS general_ledger (
    entry_id INTEGER PRIMARY KEY,
    entry_date DATE NOT NULL,
    department_id INTEGER NOT NULL,
    account_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS budgets (
    budget_id INTEGER PRIMARY KEY,
    department_id INTEGER NOT NULL,
    account_id INTEGER NOT NULL,
    month TEXT NOT NULL,
    budgeted_amount REAL NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);
""")


conn.commit()
conn.close()

print("Database created successfully.")