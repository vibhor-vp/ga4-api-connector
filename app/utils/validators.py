"""
utils/validators.py

Common validation helpers shared across routes.

Currently includes:
- Date format validation (YYYY-MM-DD)
"""

from datetime import datetime

def validate_date(date_str: str) -> bool:
    """Validate date format YYYY-MM-DD"""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False