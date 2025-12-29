"""
config.py

Centralized configuration loading.

- Loads environment variables
- Relies on GOOGLE_APPLICATION_CREDENTIALS for GA4 auth
- Keeps configuration concerns separate from application logic
"""

from dotenv import load_dotenv
import os

load_dotenv()