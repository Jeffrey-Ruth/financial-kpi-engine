# Automated Financial KPI & Executive Briefing Engine

A local pipeline that transforms raw general ledger data into executive-ready financial briefings using SQL and the Claude API.

## What it does

1. **Database layer (SQLite):** Stores general ledger transactions, department budgets, and account classifications in a relational schema.
2. **KPI calculation (SQL + Python):** Computes three core financial KPIs:
   - Net margin by month
   - Month-over-month revenue growth
   - Budget-to-actual variance by department
3. **AI-generated narrative (Claude API):** Feeds the calculated KPIs into Claude with strict grounding constraints, generating a written executive briefing that highlights trends, risks, and cost drivers — using only the numbers provided, with no invented figures.

## Why grounding matters

The prompt explicitly instructs Claude to use only the numbers supplied in the data and never estimate or invent figures. This was a deliberate design choice: in a financial reporting context, a hallucinated number isn't just a minor error, it can lead to a real business decision made on false information. The output is verified against the source calculations before being trusted.

## Tech stack

- **Python** — data processing, orchestration
- **SQLite** — relational database
- **Anthropic Claude API** — narrative generation
- **python-dotenv** — secure API key management

## Project structure

```
financial-kpi-engine/
├── data/
│   └── ledger.db
├── sql/
│   └── kpi_queries.sql
├── scripts/
│   ├── create_db.py
│   ├── generate_mock_data.py
│   └── generate_briefing.py
├── output/
│   └── briefing_report.md
└── .env (not committed)
```

## Sample output

See [`output/briefing_report.md`](output/briefing_report.md) for a full example of a generated executive briefing.

## How to run it

1. Clone the repo and create a virtual environment
2. Install dependencies: `pip install anthropic python-dotenv`
3. Add your own Claude API key to a `.env` file: `ANTHROPIC_API_KEY=your-key-here`
4. Run `python scripts/create_db.py` to build the database
5. Run `python scripts/generate_mock_data.py` to populate it with sample data
6. Run `python scripts/generate_briefing.py` to generate a briefing

## What I learned

This was my first project working with SQL joins, aggregate functions, and window function style logic. I later simplified some of the logic into Python to make the project easier to understand. It was also my first time integrating an LLM API into a data pipeline, which gave me hands-on experience with using AI while still keeping the results grounded in the underlying data.
