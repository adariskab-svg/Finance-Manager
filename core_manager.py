from datetime import datetime

from setup_persistent import load_data, save_data, FILE_PATH
from transaction import IncomeTransaction, ExpenseTransaction


class FinanceManager:
    """Main personal finance manager.

    Handles transactions, users, monthly budget,
    and data storage in a JSON file.
    """

    def __init__(self, file_path=FILE_PATH):
        """Initialize the manager with the data file path.

        Args:
            file_path: Path to the JSON save file.
        """
        self._file_path = file_path
        self._data = load_data()
        self._transactions = []
        self._users = list(self._data.get("users", []))

    @property
    def transactions(self):
        """Return a copy of the transactions list."""
        return list(self._transactions)

    @property
    def users(self):
        """Return a copy of the users list."""
        return list(self._users)

    @property
    def credentials(self):
        """Return any stored credentials from the file.

        The application no longer uses a built-in admin account,
        so credentials are kept empty by default.
        """
        stored_credentials = self._data.get("credentials") or {}
        if not isinstance(stored_credentials, dict):
            stored_credentials = {}
        return {
            "username": str(stored_credentials.get("username", "")).strip(),
            "password": str(stored_credentials.get("password", "")).strip(),
        }

    @property
    def monthly_budget(self):
        """Return the monthly budget set by the user."""
        return float(self._data.get("monthly_budget", 0.0))

    @monthly_budget.setter
    def monthly_budget(self, value):
        """Update the monthly budget and save immediately.

        Args:
            value: New monthly budget amount.
        """
        self._data["monthly_budget"] = float(value)
        self.save()

    @property
    def alert_threshold(self):
        """Return the budget alert threshold as a percentage."""
        return float(self._data.get("alert_threshold", 20.0))

    @alert_threshold.setter
    def alert_threshold(self, value):
        """Update the alert threshold and save immediately.

        Args:
            value: New alert percentage.
        """
        self._data["alert_threshold"] = float(value)
        self.save()

    def load(self):
        """Load data from the JSON file and rebuild transaction objects.

        Normalizes user entries and recreates Transaction objects
        from the saved data.

        Clears any saved credentials so authentication depends only
        on registered users.

        Returns:
            List of loaded transactions.
        """
        self._data = load_data()
        self._data["credentials"] = {}
        normalized_users = []
        for index, user in enumerate(self._data.get("users", [])):
            if not isinstance(user, dict):
                continue

            normalized_user = dict(user)
            username = str(normalized_user.get("username") or normalized_user.get("name") or "").strip()
            if not username:
                username = f"user_{index + 1}"

            normalized_user["username"] = username
            normalized_user["name"] = str(normalized_user.get("name") or username).strip() or username
            normalized_user["email"] = (normalized_user.get("email") or "").strip() or None
            normalized_user["password"] = str(normalized_user.get("password") or "").strip() or None
            normalized_users.append(normalized_user)

        self._data["users"] = normalized_users
        self._transactions = []
        self._users = list(normalized_users)
        for entry in self._data.get("transactions", []):
            self._transactions.append(self._build_transaction(entry))
        return self._transactions

    def _build_transaction(self, entry):
        """Create a Transaction object from a data dictionary.

        Args:
            entry: Dictionary containing transaction data.

        Returns:
            An IncomeTransaction or ExpenseTransaction object.
        """
        tx_type = entry.get("type", "expense")
        transaction_class = IncomeTransaction if tx_type == "income" else ExpenseTransaction
        return transaction_class(
            description=entry["description"],
            amount=entry["amount"],
            category=entry["category"],
            date=entry["date"],
        )

    def save(self):
        """Save all data to the JSON file."""
        self._data["transactions"] = [transaction.to_dict() for transaction in self._transactions]
        self._data["users"] = list(self._users)
        save_data(self._data)

    def add_transaction(self, tx_type, description, amount, category):
        """Add a new transaction and save.

        Args:
            tx_type: Transaction type — 'income' or 'expense'.
            description: Description of the transaction.
            amount: Amount in FCFA.
            category: Transaction category.

        Returns:
            The created transaction object.
        """
        transaction_class = IncomeTransaction if tx_type == "income" else ExpenseTransaction
        transaction = transaction_class(description, amount, category)
        self._transactions.append(transaction)
        self.save()
        return transaction

    def add_user(self, username, password, name=None, email=None):
        """Create a new user account.

        Args:
            username: Unique username.
            password: Account password.
            name: Display name (optional).
            email: Email address (optional).

        Returns:
            The created user dictionary.

        Raises:
            ValueError: If username is empty or already taken.
        """
        cleaned_username = (username or "").strip()
        cleaned_password = (password or "").strip()
        if not cleaned_username:
            raise ValueError("Username is required.")
        if not cleaned_password:
            raise ValueError("Password is required.")

        for existing_user in self._users:
            if str(existing_user.get("username") or "").strip().lower() == cleaned_username.lower():
                raise ValueError("Username already taken.")

        display_name = (name or cleaned_username).strip() or cleaned_username
        user = {
            "username": cleaned_username,
            "password": cleaned_password,
            "name": display_name,
            "email": (email or "").strip() or None,
        }
        self._users.append(user)
        self.save()
        return user

    def update_user(self, index, name=None, email=None):
        """Update an existing user's information.

        Args:
            index: Position of the user in the list.
            name: New display name (optional).
            email: New email address (optional).

        Returns:
            The updated user dictionary, or None if index is invalid.
        """
        if not 0 <= index < len(self._users):
            return None

        user = self._users[index]
        if name is not None:
            cleaned_name = (name or "").strip()
            if not cleaned_name:
                raise ValueError("User name is required.")
            user["name"] = cleaned_name

        if email is not None:
            user["email"] = (email or "").strip() or None

        self.save()
        return user

    def delete_user(self, index):
        """Delete a user from the list.

        Args:
            index: Position of the user to delete.

        Returns:
            The deleted user, or None if index is invalid.
        """
        if 0 <= index < len(self._users):
            removed = self._users.pop(index)
            self.save()
            return removed
        return None

    def delete_transaction(self, index):
        """Delete a transaction from the list.

        Args:
            index: Position of the transaction to delete.

        Returns:
            The deleted transaction, or None if index is invalid.
        """
        if 0 <= index < len(self._transactions):
            removed = self._transactions.pop(index)
            self.save()
            return removed
        return None

    def authenticate(self, username, password):
        """Check if the given credentials match an existing account.

        Authentication is based only on registered users.

        Args:
            username: Provided username.
            password: Provided password.

        Returns:
            True if credentials are correct, False otherwise.
        """
        supplied_username = str(username or "").strip()
        supplied_password = str(password or "").strip()

        for user in self._users:
            stored_username = str(user.get("username") or "").strip()
            stored_password = str(user.get("password") or "").strip()
            if stored_username == supplied_username and stored_password == supplied_password:
                return True

        return False

    def calculate_monthly_stats(self):
        """Calculate financial statistics for the current month.

        Filters transactions for the current month and computes
        total income, total expenses, balance, and category breakdown.

        Returns:
            Dictionary containing: transactions, total_income,
            total_expenses, balance, and categories.
        """
        current_month = datetime.now().strftime("%Y-%m")
        month_transactions = [tx for tx in self._transactions if tx.date.startswith(current_month)]

        total_income = sum(tx.amount for tx in month_transactions if isinstance(tx, IncomeTransaction))
        total_expenses = sum(tx.amount for tx in month_transactions if isinstance(tx, ExpenseTransaction))
        balance = total_income - total_expenses

        categories = {}
        for tx in month_transactions:
            if isinstance(tx, ExpenseTransaction):
                categories[tx.category] = categories.get(tx.category, 0.0) + tx.amount

        return {
            "transactions": month_transactions,
            "total_income": total_income,
            "total_expenses": total_expenses,
            "balance": balance,
            "categories": categories,
        }

    def view_transactions(self):
        """Display all recorded transactions in the terminal."""
        from budget import line
        print(f"\n  📋  All transactions ({len(self._transactions)} total)")
        line()

        if not self._transactions:
            print("  No transactions recorded.")
            return

        for index, transaction in enumerate(self._transactions, start=1):
            print(f"  {index:3}. {transaction.render()}")
        line()

    def view_users(self):
        """Display the list of all registered users in the terminal."""
        from budget import line
        print(f"\n  👤  Registered users ({len(self._users)} total)")
        line()

        if not self._users:
            print("  No users registered.")
            return

        for index, user in enumerate(self._users, start=1):
            username = user.get("username") or user.get("name") or "Unknown"
            display_name = user.get("name") or username
            email = user.get("email") or "No email"
            print(f"  {index:3}. {username:<20} | {display_name:<20} | {email}")
        line()

    def search_users(self, query):
        """Search for users by name, username, or email.

        Args:
            query: Search text.

        Returns:
            List of (index, user) tuples matching the search.
        """
        term = (query or "").strip().lower()
        if not term:
            return []

        matches = []
        for index, user in enumerate(self._users, start=1):
            username = (user.get("username") or "").lower()
            name = (user.get("name") or "").lower()
            email = (user.get("email") or "").lower()
            if term in username or term in name or term in email:
                matches.append((index, user))
        return matches

    def monthly_summary(self):
        """Display a complete financial summary for the current month.

        Shows income, expenses, net balance, and expense breakdown
        by category in the terminal.
        """
        from budget import line
        stats = self.calculate_monthly_stats()
        month_name = datetime.now().strftime("%B %Y")

        print(f"\n  📊  Summary — {month_name}")
        line()
        print(f"  Income        : +{stats['total_income']:10.2f} FCFA")
        print(f"  Expenses      :  {stats['total_expenses']:10.2f} FCFA")
        line("·")
        print(f"  Net balance   : {'+' if stats['balance'] >= 0 else ''}{stats['balance']:10.2f} FCFA  {'✅' if stats['balance'] >= 0 else '⚠️'}")

        if stats["transactions"]:
            print(f"\n  Expenses by category:")
            for category, amount in sorted(stats["categories"].items(), key=lambda item: -item[1]):
                pct_cat = (amount / stats["total_expenses"] * 100) if stats["total_expenses"] > 0 else 0
                print(f"    {category:<15} {amount:8.2f} FCFA  ({pct_cat:.0f}%)")
        line()