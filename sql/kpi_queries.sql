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