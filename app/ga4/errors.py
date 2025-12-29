from fastapi import HTTPException


def handle_ga4_error(error: Exception) -> HTTPException:
    """Handle GA4 API errors and return appropriate HTTP responses"""
    error_msg = str(error)
    error_code = getattr(error, "code", 500)

    if error_code == 403:
        return HTTPException(
            status_code=403,
            detail="Permission denied. Check if service account has access to the GA4 property."
        )
    elif error_code == 404:
        return HTTPException(
            status_code=404,
            detail="GA4 property not found. Verify the property_id is correct."
        )
    elif error_code == 400:
        return HTTPException(
            status_code=400,
            detail=f"Invalid request parameters: {error_msg}"
        )
    else:
        return HTTPException(
            status_code=500,
            detail=f"GA4 API error: {error_msg}"
        )
    
    # if "PERMISSION_DENIED" in error_msg or "permission" in error_msg.lower():
    #     return HTTPException(
    #         status_code=403,
    #         detail="Permission denied. Check if service account has access to the GA4 property."
    #     )
    # elif "NOT_FOUND" in error_msg or "not found" in error_msg.lower():
    #     return HTTPException(
    #         status_code=404,
    #         detail="GA4 property not found. Verify the property_id is correct."
    #     )
    # elif "INVALID_ARGUMENT" in error_msg:
    #     return HTTPException(
    #         status_code=400,
    #         detail=f"Invalid request parameters: {error_msg}"
    #     )
    # else:
    #     return HTTPException(
    #         status_code=500,
    #         detail=f"GA4 API error: {error_msg}"
    #     )