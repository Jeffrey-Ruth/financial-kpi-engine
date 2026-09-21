import sqlite3
import os
from dotenv import load_dotenv
from anthropic import Anthropic

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "..", "data", "ledger.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()


# KPI 1: Net Margin by Month

cursor.execute("""
SELECT
    substr(entry_date, 1, 7) AS month,
    SUM(CASE WHEN a.account_type = 'revenue' THEN gl.amount ELSE 0 END) AS total_revenue,
    SUM(CASE WHEN a.account_type = 'expense' THEN gl.amount ELSE 0 END) AS total_expense
FROM general_ledger gl
JOIN accounts a ON gl.account_id = a.account_id
GROUP BY month;
""")
net_margin_raw = cursor.fetchall()


net_margin_results = []
for month, revenue, expense in net_margin_raw:
    margin_pct = round((revenue - expense) / revenue * 100, 2)
    net_margin_results.append((month, revenue, expense, margin_pct))

net_margin_text = "Net Margin by Month:\n"
for month, revenue, expense, margin_pct in net_margin_results:
    net_margin_text += f"{month}: Revenue ${revenue:.2f}, Expense ${expense:.2f}, Margin {margin_pct}%\n"


# KPI 2: Month over Month Revenue Growth

cursor.execute("""
SELECT
    substr(gl.entry_date, 1, 7) AS month,
    SUM(gl.amount) AS total_revenue
FROM general_ledger gl
JOIN accounts a ON gl.account_id = a.account_id
WHERE a.account_type = 'revenue'
GROUP BY month
ORDER BY month;
""")
monthly_revenue = cursor.fetchall()

mom_growth_results = []
previous_revenue = None

for month, revenue in monthly_revenue:
    if previous_revenue is None:
        mom_growth_results.append((month, revenue, None, None))
    else:
        growth_pct = round((revenue - previous_revenue) / previous_revenue * 100, 2)
        mom_growth_results.append((month, revenue, previous_revenue, growth_pct))
    previous_revenue = revenue

mom_growth_text = "Month-over-Month Revenue Growth:\n"
for month, revenue, prev_revenue, growth_pct in mom_growth_results:
    if growth_pct is None:
        mom_growth_text += f"{month}: Revenue ${revenue:.2f} (no prior month to compare)\n"
    else:
        mom_growth_text += f"{month}: Revenue ${revenue:.2f}, Previous Revenue ${prev_revenue:.2f}, Growth Percentage {growth_pct}%\n"


# KPI 3: Budget to Actual Variance by Department

cursor.execute("""
SELECT
    department_id,
    substr(entry_date, 1, 7) AS month,
    SUM(amount) AS actual_amount
FROM general_ledger
GROUP BY department_id, month;
""")
actuals_raw = cursor.fetchall()

cursor.execute("""
SELECT
    department_id,
    month,
    SUM(budgeted_amount) AS budgeted_amount
FROM budgets
GROUP BY department_id, month;
""")
budgets_raw = cursor.fetchall()

cursor.execute("SELECT department_id, department_name FROM departments;")
department_names = dict(cursor.fetchall())  


budget_lookup = {}
for dept_id, month, budgeted_amount in budgets_raw:
    budget_lookup[(dept_id, month)] = budgeted_amount


variance_results = []
for dept_id, month, actual_amount in actuals_raw:
    budgeted_amount = budget_lookup.get((dept_id, month))
    if budgeted_amount is not None:
        variance_pct = round((actual_amount - budgeted_amount) / budgeted_amount * 100, 2)
        dept_name = department_names[dept_id]
        variance_results.append((dept_name, month, actual_amount, budgeted_amount, variance_pct))

variance_text = "Budget-to-Actual Variance by Department:\n"
for dept_name, month, actual_amount, budgeted_amount, variance_pct in variance_results:
    variance_text += f"{dept_name} - {month}: Actual ${actual_amount:.2f}, Budgeted ${budgeted_amount:.2f}, Variance {variance_pct}%\n"

conn.close()

print("Net margin rows:", len(net_margin_results))
print("MoM growth rows:", len(mom_growth_results))
print("Variance rows:", len(variance_results))



load_dotenv()
client = Anthropic()

prompt = f"""You are a financial analyst writing an executive briefing for a CFO.

You must follow these strict rules:
- Only use the numbers provided below. Do not calculate, estimate, or invent any numbers.
- Every specific number you mention in your narrative must come directly from the data below.
- If you're unsure about a number, do not include it.

Here is the financial data for the year:

{net_margin_text}

{mom_growth_text}

{variance_text}

Write a concise executive briefing (3-4 short paragraphs) covering:
1. Overall financial health and margin trends
2. Notable revenue growth or decline months, with possible reasons a CFO would want investigated
3. Departments or months with significant budget variance that need attention
"""

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1000,
    messages=[{"role": "user", "content": prompt}]
)

briefing_text = response.content[0].text
output_path = os.path.join(script_dir, "..", "output", "briefing_report.md")
with open(output_path, "w") as f:
    f.write(briefing_text)

print("Briefing saved to output/briefing_report.md")
print(briefing_text)