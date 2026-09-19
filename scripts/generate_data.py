import sqlite3
import random

conn = sqlite3.connect("data/ledger.db")
cursor = conn.cursor()

departments = [("Marketing",), ("Sales",), ("Operations",), ("Engineering",)]
cursor.executemany("INSERT INTO departments (department_name) VALUES (?);", departments)

accounts = [
    ("Product Revenue", "revenue"),
    ("Service Revenue", "revenue"),
    ("Salaries", "expense"),
    ("Rent", "expense"),
    ("Marketing Spend", "expense")
]
cursor.executemany("INSERT INTO accounts (account_name, account_type) VALUES (?, ?);", accounts)

months = [f"2025-{str(m).zfill(2)}" for m in range(1, 13)]
ledger_entries = []

for month in months:
    for dept_id in range(1, 5):
        for acct_id in range(1, 6):
            entry_date = f"{month}-15"
            base = 5000 if acct_id <= 2 else 2000
            amount = round(base * random.uniform(0.8, 1.3), 2)
            ledger_entries.append((entry_date, dept_id, acct_id, amount))

cursor.executemany("""
INSERT INTO general_ledger (entry_date, department_id, account_id, amount)
VALUES (?, ?, ?, ?);
""", ledger_entries)

budget_entries = []
for month in months:
    for dept_id in range(1, 5):
        for acct_id in range(1, 6):
            base = 5000 if acct_id <= 2 else 2000
            budgeted = round(base * random.uniform(0.9, 1.1), 2)
            budget_entries.append((dept_id, acct_id, month, budgeted))

cursor.executemany("""
INSERT INTO budgets (department_id, account_id, month, budgeted_amount)
VALUES (?, ?, ?, ?);
""", budget_entries)

conn.commit()
conn.close()
print("Mock data inserted.")