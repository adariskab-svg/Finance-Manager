"""
💰 Personal Finance Manager
PARTIE 6 — Features & Main Program
Membre : Adaris

Content :
  - manage_budget()  → monthly budget and alert threshold management
  - main()           → main loop, complete interactive menu
  - Entry point      → if __name__ == "__main__"

Dependencies :
  - partie1_config_persistance.py      → FILE_PATH
  - partie4_budget_affichage.py        → BudgetTracker, line, main_menu
  - partie5_authentification_saisie.py → authenticate_user, register_account,
                                         enter_amount, enter_percentage, choose_category
"""

from partie1_config_persistance import FILE_PATH
from partie4_budget_affichage import BudgetTracker, line, main_menu
from partie5_authentification_saisie import (
    authenticate_user,
    register_account,
    enter_amount,
    enter_percentage,
    choose_category,
)


# ── Features ────────────────────────────────────────────────────────────────


def manage_budget(tracker):
    """Display and update the monthly budget and alert threshold.

    Shows the current budget and alert settings, then lets the user
    change the monthly budget amount or the low-budget alert percentage.

    Args:
        tracker: BudgetTracker instance managing the finance data.
    """
    print(f"\n  🎯  Current monthly budget: {tracker.monthly_budget:.2f} FCFA")
    print(f"  ⚠️  Current low-budget alert: {tracker.alert_threshold:.0f}% remaining")
    line("·")
    print("  1. Change budget")
    print("  2. Change alert threshold")
    print("  3. Back")
    choice = input("  Choice: ").strip()
    if choice == "1":
        new_budget = enter_amount("  New monthly budget (FCFA): ")
        tracker.monthly_budget = new_budget
        print(f"  ✅  Budget set to {new_budget:.2f} FCFA!")
    elif choice == "2":
        new_threshold = enter_percentage("  New alert threshold (%): ")
        tracker.alert_threshold = new_threshold
        print(f"  ✅  Alert threshold set to {new_threshold:.0f}%")


# ── Main program ──────────────────────────────────────────────────────────────


def main():
    """Run the main program loop with an interactive menu.

    Loads existing data, authenticates the user, then displays
    a menu allowing the user to manage income, expenses, budget,
    transactions, and user accounts until they choose to exit.
    """
    tracker = BudgetTracker(FILE_PATH)
    tracker.load()
    tracker.save()

    if not authenticate_user(tracker):
        return

    while True:
        print()
        main_menu()
        choice = input("  Your choice: ").strip()

        if choice == "1":
            description = input("  Description: ").strip() or "No description"
            amount = enter_amount("  Amount (FCFA): ")
            tracker.add_transaction("income", description, amount, "Income")
            print(f"\n  ✅  Income of {amount:.2f} FCFA added!")
        elif choice == "2":
            description = input("  Description: ").strip() or "No description"
            amount = enter_amount("  Amount (FCFA): ")
            category = choose_category()
            tracker.add_transaction("expense", description, amount, category)
            print(f"\n  ✅  Expense of {amount:.2f} FCFA added!")
        elif choice == "3":
            tracker.view_transactions()
        elif choice == "4":
            tracker.monthly_summary()
        elif choice == "5":
            manage_budget(tracker)
        elif choice == "6":
            tracker.view_transactions()
            if not tracker.transactions:
                continue
            tx_index = input("  Number to delete (0 to cancel): ").strip()
            if tx_index.isdigit():
                index = int(tx_index) - 1
                removed = tracker.delete_transaction(index)
                if removed:
                    print(f"  ✅  '{removed.description}' deleted.")
                elif tx_index != "0":
                    print("  ⚠️  Invalid number.")
        elif choice == "7":
            register_account(tracker)
        elif choice == "8":
            tracker.view_users()
        elif choice == "9":
            query = input("  Search term (username, name or email): ").strip()
            matches = tracker.search_users(query)
            print(f"\n  🔎  Search results for '{query or ''}'")
            line()
            if not matches:
                print("  No matching users found.")
            else:
                for index, user in matches:
                    username = user.get("username") or user.get("name") or "Unknown"
                    display_name = user.get("name") or username
                    email = user.get("email") or "No email"
                    print(f"  {index:3}. {username:<20} | {display_name:<20} | {email}")
            line()
        elif choice == "10":
            tracker.view_users()
            if not tracker.users:
                continue
            user_index = input("  User number to edit (0 to cancel): ").strip()
            if user_index.isdigit() and user_index != "0":
                index = int(user_index) - 1
                if not 0 <= index < len(tracker.users):
                    print("  ⚠️  Invalid user number.")
                else:
                    current_user = tracker.users[index]
                    new_name = input(f"  New name ({current_user['name']}): ").strip() or None
                    new_email = input(f"  New email ({current_user['email'] or 'No email'}): ").strip() or None
                    updated = tracker.update_user(index, name=new_name, email=new_email)
                    if updated:
                        print(f"  ✅  User '{updated['name']}' updated!")
                    else:
                        print("  ⚠️  Invalid user number.")
        elif choice == "11":
            tracker.view_users()
            if not tracker.users:
                continue
            user_index = input("  User number to delete (0 to cancel): ").strip()
            if user_index.isdigit() and user_index != "0":
                index = int(user_index) - 1
                if not 0 <= index < len(tracker.users):
                    print("  ⚠️  Invalid user number.")
                else:
                    removed = tracker.delete_user(index)
                    if removed:
                        print(f"  ✅  User '{removed['name']}' deleted.")
                    else:
                        print("  ⚠️  Invalid user number.")
        elif choice == "12":
            print("\n  👋  See you soon! Good money management.\n")
            break
        else:
            print("  ⚠️  Invalid choice. Please enter a number between 1 and 12.")

        input("\n  Press Enter to continue...")


if __name__ == "__main__":
    main()