CREATE TABLE departments(
    department_id INTEGER PRIMARY KEY,
    department_name TEXT NOT NULL
);

CREATE TABLE accounts(
    account_id INTEGER PRIMARY KEY,
    account_name TEXT NOT NULL,
    account_type TEXT NOT NULL -- revenue/expense
);

CREATE TABLE general_ledger(
    entry_id INTEGER PRIMARY KEY,
    entry_date DATE NOT NULL,
    department_id INTEGER NOT NULL,
    account_id INTEGER NOT NULL,
    account REAL NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

CREATE TABLE budgets(
    budget_id INTEGER PRIMARY KEY,
    department_id INTEGER NOT NULL,
    account_id INTEGER NOT NULL,
    month TEXT NOT NULL, --format YYYY-MM
    budgeted_amount REAL NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);