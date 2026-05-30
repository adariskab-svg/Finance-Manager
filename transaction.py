"""
💰 Personal Finance Manager
PARTIE 2 — OOP Models : Transaction
Membre : ___________________________

Content :
  - Abstract class Transaction (ABC)
  - Class IncomeTransaction
  - Class ExpenseTransaction

Dependencies : import from setup_persistent.py
"""

from abc import ABC, abstractmethod
from datetime import datetime


# ── POO models ───────────────────────────────────────────────────────────────


class Transaction(ABC):
    """Abstract base class representing a financial transaction.

    Defines the common structure for all transaction types.
    Cannot be instantiated directly — must be subclassed.
    """

    def __init__(self, description, amount, category, date=None):
        """Initialize a transaction with its core attributes.

        Args:
            description: Text describing the transaction.
            amount: Transaction amount in FCFA (must be positive).
            category: Category the transaction belongs to.
            date: Date string in YYYY-MM-DD format. Defaults to today.
        """
        self._description = (description or "No description").strip() or "No description"
        self._category = category
        self._date = date or datetime.now().strftime("%Y-%m-%d")
        self.amount = amount

    @property
    def description(self):
        """Return the transaction description."""
        return self._description

    @property
    def amount(self):
        """Return the transaction amount."""
        return self._amount

    @amount.setter
    def amount(self, value):
        """Set the transaction amount, ensuring it is positive.

        Args:
            value: Amount to set.

        Raises:
            ValueError: If the amount is zero or negative.
        """
        value = float(value)
        if value <= 0:
            raise ValueError("Amount must be positive.")
        self._amount = value

    @property
    def category(self):
        """Return the transaction category."""
        return self._category

    @property
    def date(self):
        """Return the transaction date as a string."""
        return self._date

    @property
    @abstractmethod
    def emoji(self):
        """Return the emoji representing this transaction type."""
        pass

    @property
    @abstractmethod
    def transaction_type(self):
        """Return the transaction type as a string ('income' or 'expense')."""
        pass

    @abstractmethod
    def render(self):
        """Return a formatted string for display in the terminal."""
        pass

    def to_dict(self):
        """Convert the transaction to a dictionary for JSON storage.

        Returns:
            Dictionary with type, description, amount, category and date.
        """
        return {
            "type": self.transaction_type,
            "description": self.description,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
        }


class IncomeTransaction(Transaction):
    """Represents an income transaction (money received)."""

    @property
    def emoji(self):
        """Return the income emoji."""
        return "💵"

    @property
    def transaction_type(self):
        """Return the transaction type as 'income'."""
        return "income"

    def render(self):
        """Return a formatted income line for terminal display."""
        return f"{self.emoji} [{self.date}] {self.description[:25]:<25} +{self.amount:8.2f} FCFA  ({self.category})"


class ExpenseTransaction(Transaction):
    """Represents an expense transaction (money spent)."""

    @property
    def emoji(self):
        """Return the expense emoji."""
        return "💸"

    @property
    def transaction_type(self):
        """Return the transaction type as 'expense'."""
        return "expense"

    def render(self):
        """Return a formatted expense line for terminal display."""
        return f"{self.emoji} [{self.date}] {self.description[:25]:<25} -{self.amount:8.2f} FCFA  ({self.category})"