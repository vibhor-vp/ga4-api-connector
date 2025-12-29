from pydantic import BaseModel

class TestConnectionRequest(BaseModel):
    """
    Request payload for testing GA4 connectivity.
    """
    property_id: str