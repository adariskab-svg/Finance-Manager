"""
Personal Finance Manager

Application entry point. Allows entering incomes, expenses, managing user
accounts, setting a monthly budget and displaying summaries.
"""

from setup_persistent import FILE_PATH, CATEGORIES
from core_manager import FinanceManager
from budget import BudgetTracker, line, main_menu


def input_non_empty(prompt: str) -> str:
    """Prompt until a non-empty string is entered.

    Args:
        prompt: Text displayed to the user.

    Returns:
        The non-empty user input string.
    """
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  ⚠️  This field cannot be empty. Please try again.")


def enter_amount(prompt: str) -> float:
    """Prompt until a valid positive float amount is entered.

    Args:
        prompt: Text displayed to the user.

    Returns:
        A positive float representing the amount.
    """
    while True:
        value = input(prompt).strip()
        try:
            amount = float(value)
            if amount <= 0:
                raise ValueError
            return amount
        except ValueError:
            print("  ⚠️  Please enter a valid positive amount.")


def enter_percentage(prompt: str) -> float:
    """Prompt until a valid percentage (0-100) is entered.

    Args:
        prompt: Text displayed to the user.

    Returns:
        A float between 0 and 100.
    """
    while True:
        value = input(prompt).strip()
        try:
            percentage = float(value)
            if not 0 <= percentage <= 100:
                raise ValueError
            return percentage
        except ValueError:
            print("  ⚠️  Please enter a valid percentage between 0 and 100.")


def choose_category() -> str:
    """Display available categories and let the user choose one.

    Returns:
        The selected category string from CATEGORIES.
    """
    print("\n  Select a category:")
    for index, category in enumerate(CATEGORIES, start=1):
        print(f"  {index}. {category}")

    while True:
        choice = input("  Category number: ").strip()
        if choice.isdigit():
            index = int(choice)
            if 1 <= index <= len(CATEGORIES):
                return CATEGORIES[index - 1]
        print("  ⚠️  Please enter a valid category number.")


def authenticate_user(tracker: FinanceManager) -> bool:
    """Handle the initial authentication flow (login or register).

    Args:
        tracker: FinanceManager instance used for authentication.

    Returns:
        True if the user successfully authenticated, False to quit.
    """
    print("\n  🔐  Login / Register")
    print("  1. Login")
    print("  2. Create a new account")
    print("  3. Quit")

    while True:
        choice = input("  Choice: ").strip()
        if choice == "1":
            attempts = 3
            for attempt in range(attempts):
                username = input_non_empty("  Username: ")
                password = input_non_empty("  Password: ")
                if tracker.authenticate(username, password):
                    print("  ✅  Authentication successful.")
                    return True
                print(f"  ⚠️  Invalid credentials. {attempts - attempt - 1} attempts left.")
            print("  ⛔  Login failed. Returning to menu.")
        elif choice == "2":
            register_account(tracker)
            print("  ✅  Account created. You can now log in.")
        elif choice == "3":
            return False
        else:
            print("  ⚠️  Please enter 1, 2 or 3.")


def register_account(tracker: FinanceManager) -> None:
    """Create a new user account through prompts.

    Args:
        tracker: FinanceManager instance used to add the user.
    """
    print("\n  🆕  Create account")
    username = input_non_empty("  Username: ")
    password = input_non_empty("  Password: ")
    name = input("  Name (optional): ").strip() or None
    email = input("  Email (optional): ").strip() or None
    try:
        tracker.add_user(username, password, name=name, email=email)
        print(f"  ✅  Account '{username}' created successfully.")
    except ValueError as exc:
        print(f"  ⚠️  {exc}")


def main() -> None:
    """Run the main interactive menu loop.

    Initializes the tracker, performs authentication, and processes user
    commands until the user chooses to exit.
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
            print("\n  🎯  Budget management")
            print(f"  Current monthly budget: {tracker.monthly_budget:.2f} FCFA")
            print(f"  Current alert threshold: {tracker.alert_threshold:.0f}%")
            print("  1. Change budget")
            print("  2. Change alert threshold")
            print("  3. Back")
            submenu_choice = input("  Choice: ").strip()
            if submenu_choice == "1":
                tracker.monthly_budget = enter_amount("  New monthly budget (FCFA): ")
                print(f"  ✅  Budget updated to {tracker.monthly_budget:.2f} FCFA")
            elif submenu_choice == "2":
                tracker.alert_threshold = enter_percentage("  New alert threshold (%): ")
                print(f"  ✅  Alert threshold updated to {tracker.alert_threshold:.0f}%")
        elif choice == "6":
            tracker.view_transactions()
            if not tracker.transactions:
                continue
            tx_index = input("  Number to delete (0 to cancel): ").strip()
            if tx_index.isdigit():
                if tx_index == "0":
                    continue
                removed = tracker.delete_transaction(int(tx_index) - 1)
                if removed:
                    print(f"  ✅  '{removed.description}' deleted.")
                else:
                    print("  ⚠️  Invalid transaction number.")
            else:
                print("  ⚠️  Please enter a number.")
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
                    continue
                current_user = tracker.users[index]
                new_name = input(f"  New name ({current_user['name']}): ").strip() or None
                new_email = input(f"  New email ({current_user.get('email') or 'No email'}): ").strip() or None
                updated = tracker.update_user(index, name=new_name, email=new_email)
                if updated:
                    print(f"  ✅  User '{updated['name']}' updated!")
                else:
                    print("  ⚠️  Could not update user.")
            else:
                print("  ⚠️  Please enter a valid user number.")
        elif choice == "11":
            tracker.view_users()
            if not tracker.users:
                continue
            user_index = input("  User number to delete (0 to cancel): ").strip()
            if user_index.isdigit() and user_index != "0":
                removed = tracker.delete_user(int(user_index) - 1)
                if removed:
                    print(f"  ✅  User '{removed['name']}' deleted.")
                else:
                    print("  ⚠️  Invalid user number.")
            else:
                print("  ⚠️  Please enter a valid user number.")
        elif choice == "12":
            print("\n  👋  Goodbye! Keep managing your money wisely.")
            break
        else:
            print("  ⚠️  Invalid choice. Please enter a number between 1 and 12.")

        input("\n  Press Enter to continue...")


if __name__ == "__main__":
    main()