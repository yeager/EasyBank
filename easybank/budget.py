"""Budget data model with JSON persistence."""

import json
import os
from datetime import datetime
from pathlib import Path


DATA_DIR = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")) / "easybank"
DATA_FILE = DATA_DIR / "budget.json"

# Expense categories with Swedish names and icon keys
CATEGORIES = {
    "food": {"sv": "Mat", "en": "Food", "icon": "food"},
    "home": {"sv": "Hem", "en": "Home", "icon": "home"},
    "transport": {"sv": "Transport", "en": "Transport", "icon": "transport"},
    "clothes": {"sv": "Kläder", "en": "Clothes", "icon": "clothes"},
    "fun": {"sv": "Nöje", "en": "Fun", "icon": "fun"},
    "health": {"sv": "Hälsa", "en": "Health", "icon": "health"},
    "other": {"sv": "Övrigt", "en": "Other", "icon": "other"},
}


def _default_data():
    return {
        "income": 0,
        "transactions": [],
        "created": datetime.now().isoformat(),
    }


def load_budget():
    """Load budget data from JSON file."""
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return _default_data()


def save_budget(data):
    """Save budget data to JSON file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_transaction(data, amount, category, description=""):
    """Add an expense transaction (negative amount)."""
    data["transactions"].append({
        "amount": -abs(amount),
        "category": category,
        "description": description,
        "date": datetime.now().isoformat(),
    })
    save_budget(data)
    return data


def add_income(data, amount):
    """Set the monthly income."""
    data["income"] = abs(amount)
    save_budget(data)
    return data


def get_total_expenses(data):
    """Get total expenses (positive number)."""
    return abs(sum(t["amount"] for t in data["transactions"]))


def get_balance(data):
    """Get current balance."""
    return data["income"] - get_total_expenses(data)


def get_balance_fraction(data):
    """Get balance as fraction of income (0.0 to 1.0)."""
    if data["income"] <= 0:
        return 1.0
    fraction = get_balance(data) / data["income"]
    return max(0.0, min(1.0, fraction))


def get_expenses_by_category(data):
    """Get expenses grouped by category."""
    expenses = {}
    for t in data["transactions"]:
        cat = t.get("category", "other")
        expenses[cat] = expenses.get(cat, 0) + abs(t["amount"])
    return expenses


def clear_transactions(data):
    """Clear all transactions (new month)."""
    data["transactions"] = []
    save_budget(data)
    return data
