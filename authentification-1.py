"""
Authentication helpers for the personal finance manager.

This module provides input validation, category selection, account
registration, and login support, in the same module organization style as
other project files.
"""

import importlib


if importlib.util.find_spec("partie1_config_persistance") is not None:
    module = importlib.import_module("partie1_config_persistance")
    CATEGORIES = module.CATEGORIES
else:
    CATEGORIES = ["Food", "Transport", "Housing", "Utilities", "Entertainment"]


# ── Input helpers ────────────────────────────────────────────────────────────


def enter_amount(prompt: str) -> float:
    """Prompt the user until a positive amount is entered."""
    while True:
        try:
            amount = float(input(prompt).replace(",", "."))
            if amount <= 0:
                print("  ⚠️  Amount must be positive.")
            else:
                return amount
        except ValueError:
            print("  ⚠️  Please enter a valid number.")


def enter_percentage(prompt: str) -> float:
    """Prompt the user until a valid percentage between 0 and 100 is entered."""
    while True:
        value = enter_amount(prompt)
        if value <= 100:
            return value
        print("  ⚠️  Please enter a percentage between 0 and 100.")


def choose_category() -> str:
    """Display available categories and return the user's selected category."""
    print("\n  Available categories:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"    {i}. {cat}")
    while True:
        choice = input("  Your choice (number): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            return CATEGORIES[int(choice) - 1]
        print("  ⚠️  Invalid choice.")


# ── Account management ───────────────────────────────────────────────────────


def register_account(tracker) -> bool:
    """Register a new user account through interactive prompts."""
    print("\n  🆕  Create a new account")
    try:
        username = input("  Username: ").strip()
        password = input("  Password: ").strip()
        confirm_password = input("  Confirm password: ").strip()
        display_name = input("  Full name (optional): ").strip() or None
        email = input("  Email (optional): ").strip() or None
    except EOFError:
        print("\n  🚫  Account creation interrupted.")
        return False

    if not username:
        print("  ⚠️  Username is required.")
        return False
    if not password:
        print("  ⚠️  Password is required.")
        return False
    if password != confirm_password:
        print("  ⚠️  Passwords do not match.")
        return False

    try:
        tracker.add_user(username, password, name=display_name, email=email)
    except ValueError as exc:
        print(f"  ⚠️  {exc}")
        return False

    print(f"  ✅  Account '{username}' created successfully. You can now log in.")
    return True


def authenticate_user(tracker, attempts: int = 3) -> bool:
    """Perform login or account creation until authentication succeeds."""
    print("\n  🔐  Login required")
    print("  1. Login")
    print("  2. Create account")
    print("  3. Exit")

    while True:
        choice = input("  Choice: ").strip()

        if choice == "2":
            register_account(tracker)
            print("\n  🔐  Login required")
            print("  1. Login")
            print("  2. Create account")
            print("  3. Exit")
            continue

        if choice == "3":
            print("\n  🚫  Login cancelled. Exiting.")
            return False

        if choice != "1":
            print("  ⚠️  Invalid choice.")
            continue

        for attempt in range(1, attempts + 1):
            try:
                username = input("  Username: ").strip()
                password = input("  Password: ").strip()
            except EOFError:
                print("\n  🚫  Login interrupted. Exiting.")
                return False

            if tracker.authenticate(username, password):
                print("  ✅  Authentication successful.")
                return True

            remaining = attempts - attempt
            print(f"  ⚠️  Invalid credentials. Attempts remaining: {remaining}")

        print("  🚫  Too many failed attempts. Exiting.")
        return False