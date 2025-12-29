"""
routes/ga4.py

FastAPI route definitions related to GA4 reporting.

Responsibilities:
- Request validation
- HTTP error handling
- Delegation to GA4 service layer

No GA4 query logic should exist in this file.
"""

from fastapi import APIRouter, HTTPException, Query
from google.api_core.exceptions import GoogleAPIError
from app.models.requests import TestConnectionRequest
from app.ga4.errors import handle_ga4_error
from app.utils.validators import validate_date
from app.ga4.service import GA4Service
from app.ga4.client import get_ga4_client

router = APIRouter(prefix="/ga4", tags=["GA4"])
ga4_service = GA4Service(get_ga4_client())

@router.post("/test-connection")
def test_ga4_connection(payload: TestConnectionRequest):
    """
    Validates GA4 access for the given property ID by running
    a minimal GA4 query.
    """
    try:
        response = ga4_service.test_connection(payload.property_id)
        return {
            "success": True,
            "message": f"Successfully connected to GA4 property. Rows returned: {len(response.rows)}"
            }
    except GoogleAPIError as e:
        raise handle_ga4_error(e)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/organic-traffic")
def get_organic_traffic(
    property_id: str,
    start_date: str,
    end_date: str
):
    """
    Returns daily organic traffic metrics (sessions, active users)
    for the specified GA4 property and date range.
    """
    try:
        if validate_date(start_date) and validate_date(end_date):
            return ga4_service.get_organic_traffic(property_id, start_date, end_date)
        else:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except GoogleAPIError as e:
        raise handle_ga4_error(e)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/organic-landing-pages")
def get_organic_landing_pages(
    property_id: str,
    start_date: str,
    end_date: str,
    limit: int = Query(25, le=100)
):
    """
    Returns top landing pages ranked by organic sessions.
    """
    try:
        if validate_date(start_date) and validate_date(end_date):
            return ga4_service.get_organic_landing_pages(property_id, start_date, end_date, limit)
        else:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except GoogleAPIError as e:
        raise HTTPException(status_code=500, detail=str(e))
