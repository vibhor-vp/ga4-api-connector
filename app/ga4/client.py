"""
ga4/client.py

GA4 client factory.

- Initializes Google Analytics Data API client
- Uses Application Default Credentials (Service Account)

This abstraction allows easy future changes
(e.g., OAuth-based client).
"""

from google.analytics.data_v1beta import BetaAnalyticsDataClient

def get_ga4_client() -> BetaAnalyticsDataClient:
    """
    Returns an authenticated GA4 Data API client.
    """
    return BetaAnalyticsDataClient()
