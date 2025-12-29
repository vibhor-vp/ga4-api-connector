"""
Response models for GA4 API endpoints
"""
from pydantic import BaseModel, Field

class OrganicTrafficData(BaseModel):
    """Single day organic traffic data"""
    date: str = Field(..., description="Date in YYYYMMDD format")
    sessions: int = Field(..., description="Number of sessions")
    active_users: int = Field(..., description="Number of active users")

class OrganicLandingPageData(BaseModel):
    """Single landing page data"""
    landing_page: str = Field(..., description="Landing page URL with query string")
    sessions: int = Field(..., description="Number of sessions")
    active_users: int = Field(..., description="Number of active users")
    conversions: float = Field(..., description="Number of conversions")
