"""
ga4/filters.py

Reusable GA4 filter expressions.

Currently includes:
- Organic Search traffic filter

Keeping filters isolated improves reuse and readability.
"""

from google.analytics.data_v1beta.types import Filter, FilterExpression

def organic_search_filter() -> FilterExpression:
    """
    Builds a GA4 filter expression for Organic Search traffic.
    """
    return FilterExpression(
        filter=Filter(
            field_name="sessionDefaultChannelGroup",
            string_filter=Filter.StringFilter(
                value="Organic Search"
            )
        )
    )
