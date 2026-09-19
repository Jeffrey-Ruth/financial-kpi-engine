--KPI 1: Net Margin by Month

SELECT
    substr(entry_date, 1, 7) AS month,
    SUM(CASE WHEN a.account_type = 'revenue' THEN gl.amount ELSE 0 END) AS total_revenue,
    SUM(CASE WHEN a.account_type = 'expense' THEN gl.amount ELSE 0 END) AS total_expense,
    ROUND(
        (SUM(CASE WHEN a.account_type = 'revenue' THEN gl.amount ELSE 0 END) -
         SUM(CASE WHEN a.account_type = 'expense' THEN gl.amount ELSE 0 END)) * 100.0 /
         SUM(CASE WHEN a.account_type = 'revenue' THEN gl.amount ELSE 0 END),
    2) AS net_margin_pct
FROM general_ledger gl
JOIN accounts a ON gl.account_id = a.account_id
GROUP BY month;


--KPI 2: Month over Month Revenue Growth

WITH monthly_revenue AS (
    SELECT
        substr(entry_date, 1, 7) AS month,
        SUM(gl.amount) AS total_revenue
    FROM general_ledger gl
    JOIN accounts a ON gl.account_id = a.account_id
    WHERE a.account_type = 'revenue'
    GROUP BY month
)
SELECT
    month,
    total_revenue,
    LAG(total_revenue) OVER (ORDER BY month) AS prev_month_revenue,
    ROUND(
        (total_revenue - LAG(total_revenue) OVER (ORDER BY month)) * 100.0 /
        LAG(total_revenue) OVER (ORDER BY month),
    2) AS mom_growth_pct
FROM monthly_revenue;

--KPI 3: Budget to Actual Variance by Department

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