# Expense Tracker (CLI)

A command-line expense tracker built with Python and OOP. Supports multiple accounts, transaction history, category budgets, transfers between accounts, and JSON-based persistence between sessions.

## Features

- **Multiple accounts** — create and switch between separate named accounts, each with its own transaction history
- **Transactions** — add, edit, and delete income/expense entries with date, amount, category, and description
- **Categories** — organize transactions into predefined categories (food, rent, utilities, transportation, entertainment, healthcare, shopping, education, income, savings, misc)
- **Budgets** — set a spending budget per category, per account
- **Account transfers** — move funds between two accounts, with validation for invalid amounts and insufficient balance
- **Sorting** — view transactions sorted by date or grouped by category
- **Persistence** — all data automatically saves to `exptra.json` and reloads the next time the program runs

## Requirements

- Python 3.12+ (uses PEP 701 nested f-string quotes)
- No external dependencies — uses only the Python standard library (`json`, `datetime`)

## Usage

Run the tracker from the terminal:

```bash
python tracker.py
```

You'll see a main menu:

```
=== Expense Tracker ===
1) View accounts / balances
2) Select an account
3) Create new account
4) Transfer between accounts
5) View all transactions
6) Save & Exit
```

Select an account (option 2) to access its own menu for adding, editing, deleting, sorting, and budgeting transactions.

Data is saved automatically when you choose **Save & Exit** (option 6), and reloaded automatically the next time you run the program.

## Data Storage

All account data is stored locally in `exptra.json`, structured as:

```json
{
  "account_name": {
    "transactions": [
      {
        "id": 1,
        "amount": 200,
        "category": "food/groceries",
        "date": "02-08-2026",
        "description": "groceries",
        "trans_type": false
      }
    ],
    "budget": {
      "food/groceries": 300
    }
  }
}
```

`trans_type` is `true` for income and `false` for expenses.

## Project Structure

```
tracker.py       # Tracker class + CLI menu loop
exptra.json      # Auto-generated data file (created on first save)
```

## Notes

This project was built as a learning exercise in Python OOP — it makes use of instance methods, `@staticmethod`, `@classmethod`, and `@property` where each was the appropriate fit for the behavior involved.
