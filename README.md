# Finance Manager

A personal finance management application written in Python. The tool helps you track income and expenses, monitor your monthly budget, and save all records locally in a JSON file.

## Overview

This project is a console-based finance manager that lets you:

- add income entries
- add expense entries
- view all recorded transactions
- display a monthly summary (income, expenses, balance)
- set and update a monthly budget
- configure a budget alert threshold
- delete existing transactions
- create personal accounts with a username and password
- log in with either the default admin credentials or a saved account

All data is persisted in `mes_finances.json`, so your records remain available between runs.

## How it works

The application starts from `main.py` and displays an interactive menu in the terminal.

The main features are:

1. **Transaction management**
   - Add income or expense entries with a description, amount, category, and date.
   - Expenses can be assigned to categories such as Housing, Food, Transport, Health, Leisure, Clothing, Education, and Other.
   - Income entries are stored separately and shown with a positive balance in reports.

2. **Monthly summary**
   - Shows total income, total expenses, and net balance for the current month.
   - Breaks expenses down by category so you can see where money is going.
   - Calculates budget usage percentage and remaining budget.

3. **Budget alerts**
   - You can define a monthly budget.
   - You can define an alert threshold as a percentage of budget remaining.
   - When the remaining budget falls below the chosen threshold, the summary warns you.

4. **Persistence**
   - Data is saved automatically after every add, edit, or delete operation.
   - The default storage file is `mes_finances.json`.

## File structure

- `main.py` : interactive application and menu logic
- `mes_finances.json` : saved transactions and budget settings
- `README.md` : project documentation

## Running the application

From the project folder, run:

```bash
python main.py
```

The terminal menu will guide you through each action.

## Example data format

The saved JSON file stores transactions and budget settings like this:

```json
{
  "transactions": [
    {
      "type": "income",
      "description": "salary",
      "amount": 1500000.0,
      "category": "Income",
      "date": "2026-05-26"
    },
    {
      "type": "expense",
      "description": "rent",
      "amount": 1500.0,
      "category": "Housing",
      "date": "2026-05-26"
    }
  ],
  "monthly_budget": 150000.0,
  "alert_threshold": 20.0
}
```

## Notes

- The application is designed for local personal use.
- It does not require any external libraries.
- The data file can be edited manually if needed, but it is recommended to use the app menu for changes.


## GITHUB LINK
 https://github.com/jemimakiendrebeogo/Finance-Project.git
 https://github.com/raoulkabore57-maker/Finance-project-
 https://github.com/adariskab-svg/Finance-Project.git
 https://github.com/steph29kab-cyber/Finance-Project.git
 https://github.com/kabre03/Finance-project-
https://github.com/KANANVictoireTheresiaFlavie/Finance-Project.git