

import json
import os
import sys
from abc import ABC, abstractmethod
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# ── Save file ─────────────────────────────────────────────────────────────────
FILE_PATH = "mes_finances.json"

CATEGORIES = [
    "Housing", "Food", "Transport", "Health",
    "Leisure", "Clothing", "Education", "Other"
]


# ── Load / Save ───────────────────────────────────────────────────────────────


def load_data():
    default_data = {
        "transactions": [],
        "users": [],
        "credentials": {
            "username": "admin",
            "password": "admin123",
        },
        "monthly_budget": 0.0,
        "alert_threshold": 75.0,
    }

    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError):
            return default_data

        if not isinstance(data, dict):
            return default_data

        for key, value in default_data.items():
            data.setdefault(key, value)
        return data

    return default_data


def save_data(data):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)