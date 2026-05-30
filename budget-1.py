"""
💰 Personal Finance Manager
PARTIE 4 — BudgetTracker & Display
Member : ___________________________

Contents:
  - BudgetTracker class (inherits from FinanceManager)
    · Overrides monthly_summary() with budget tracking and alerts
  - Display functions: line(), title(), main_menu()

Dependencies:
  - core_manager.py → FinanceManager
"""

from datetime import datetime

from core_manager import FinanceManager


# ── BudgetTracker ─────────────────────────────────────────────────────────────


class BudgetTracker(FinanceManager):
    """
    Extends the FinanceManager class by adding monthly budget tracking.

    This class provides a detailed monthly financial summary including:
    - total income;
    - total expenses;
    - net balance;
    - monthly budget monitoring;
    - low-budget alerts;
    - expense breakdown by category.
    """

    def monthly_summary(self):
        """
        Displays a financial summary for the current month.

        The summary includes:
        - total income;
        - total expenses;
        - net balance;
        - monthly budget status;
        - budget usage progress bar;
        - alert when the remaining budget reaches the warning threshold;
        - expenses grouped by category.
        """
        stats = self.calculate_monthly_stats()
        month_name = datetime.now().strftime("%B %Y")

        print(f"\n  📊  Summary — {month_name}")
        line()
        print(f"  Income        : +{stats['total_income']:10.2f} FCFA")
        print(f"  Expenses      :  {stats['total_expenses']:10.2f} FCFA")
        line("·")
        print(
            f"  Net balance   : "
            f"{'+' if stats['balance'] >= 0 else ''}"
            f"{stats['balance']:10.2f} FCFA  "
            f"{'✅' if stats['balance'] >= 0 else '⚠️'}"
        )

        budget = self.monthly_budget

        if budget > 0:
            remaining = budget - stats["total_expenses"]
            pct = (stats["total_expenses"] / budget) * 100
            remaining_pct = max(0.0, (remaining / budget) * 100)
            alert_threshold = self.alert_threshold
            bar = int(pct / 5)

            print(f"\n  Monthly budget : {budget:.2f} FCFA")
            print(f"  Used           : {pct:.1f}%  [{'█' * bar}{'░' * (20 - bar)}]")
            print(
                f"  Remaining      : {remaining:.2f} FCFA  "
                f"{'✅' if remaining >= 0 else '🚨 Over budget!'}"
            )
            print(f"  Alert threshold: {alert_threshold:.0f}% remaining")

            if remaining_pct <= alert_threshold and remaining >= 0:
                print(
                    f"  🚨 Low budget alert: "
                    f"only {remaining_pct:.1f}% of budget remaining!"
                )

        if stats["transactions"]:
            print("\n  Expenses by category:")

            for category, amount in sorted(
                stats["categories"].items(),
                key=lambda item: -item[1]
            ):
                pct_cat = (
                    (amount / stats["total_expenses"] * 100)
                    if stats["total_expenses"] > 0
                    else 0
                )

                print(
                    f"    {category:<15} "
                    f"{amount:8.2f} FCFA  ({pct_cat:.0f}%)"
                )

        line()


# ── Display ───────────────────────────────────────────────────────────────────


def line(char="─", n=50):
    """
    Prints a horizontal separator line.

    Args:
        char (str): Character used to draw the line.
        n (int): Number of times the character is repeated.
    """
    print(char * n)


def title(text):
    """
    Displays a formatted title surrounded by separator lines.

    Args:
        text (str): The title text to display.
    """
    line()
    print(f"  💰  {text}")
    line()


def main_menu():
    """
    Displays the main menu of the application.

    The menu provides access to:
    - transaction management;
    - financial summaries and statistics;
    - budget settings;
    - user management;
    - application exit.
    """
    title("PERSONAL FINANCE MANAGER")

    print("  📁  Transactions")
    print("  1. ➕  Add income")
    print("  2. ➖  Add expense")
    print("  3. 📋  View all transactions")
    print("  4. 📊  Monthly summary")
    print("  5. 🎯  Budget settings")
    print("  6. 🗑️   Delete a transaction")

    print()
    print("  👤  Users")
    print("  7. 🆕  Create account")
    print("  8. 📋  View users")
    print("  9. 🔎  Search user")
    print(" 10. ✏️   Edit user")
    print(" 11. 🗑️   Delete user")

    print()
    print(" 12. 🚪  Exit")

    line()