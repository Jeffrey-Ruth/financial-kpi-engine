import sqlite3

conn = sqlite3.connect("data/ledger.db")
cursor = conn.cursor()

cursor.execute("""
WITH actuals AS (
    SELECT
        department_id,
        substr(entry_date, 1, 7) AS month,
        SUM(amount) AS actual_amount
    FROM general_ledger
    GROUP BY department_id, month
),
budgeted AS (
    SELECT
        department_id,
        month,
        SUM(budgeted_amount) AS budgeted_amount
    FROM budgets
    GROUP BY department_id, month
)
SELECT
    d.department_name,
    a.month,
    a.actual_amount,
    b.budgeted_amount,
    ROUND((a.actual_amount - b.budgeted_amount) * 100.0 / b.budgeted_amount, 2) AS variance_pct
FROM actuals a
JOIN budgeted b ON a.department_id = b.department_id AND a.month = b.month
JOIN departments d ON a.department_id = d.department_id
ORDER BY d.department_name, a.month;
""")

results = cursor.fetchall()
for row in results:
    print(row)

conn.close()