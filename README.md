# GA4 Data API Connector

A FastAPI-based REST API service that connects to Google Analytics 4 (GA4) and provides organic search traffic insights.

## Features

- Test GA4 property connectivity
- Daily organic traffic metrics (sessions, active users)
- Top organic landing pages with conversion data
- Clean layered architecture (routes → service → client)
- Comprehensive error handling with GA4-specific messages
- Request validation (date format, query parameters)

## Architecture

**Pattern: Lightweight Layered Architecture**

This project uses a **simplified layered approach** - clear separation of concerns (routes → service → client) without over-engineering. The architecture keeps the codebase flat and easy to navigate while maintaining clean boundaries between API handlers, business logic, and external integrations. Perfect for small-to-medium projects that may grow later.

```
app/
├── main.py              # FastAPI application entry point
├── config.py            # Configuration & environment loading
├── ga4/                 # GA4 integration layer
│   ├── client.py        # GA4 client factory
│   ├── service.py       # Business logic for GA4 operations
│   ├── filters.py       # Reusable GA4 filter expressions
│   └── errors.py        # GA4 error handler
├── models/              # Pydantic request/response models
│   ├── requests.py
│   └── responses.py
├── routes/              # API route handlers
│   └── ga4.py           # GA4 endpoints
└── utils/               # Shared utilities
    └── validators.py    # Date validation
```

## Setup Steps

### Prerequisites

- Python 3.13
- Google Cloud project with GA4 API enabled
- Service account with access to your GA4 property
- Service account key file (JSON)

### Installation

1. **Clone/download the project**
   ```bash
   cd ga4-api-connector
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/Scripts/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Google Cloud authentication**
   - Download service account key from Google Cloud Console
   - Place it as `service-account-key.json` in project root
   - Verify `.env` file contains:
     ```
     GOOGLE_APPLICATION_CREDENTIALS="service-account-key.json"
     ```

5. **Verify the service account has:**
   - Editor or Viewer role in the Google Cloud project
   - Permissions on the GA4 property

## How to Run

### Start the server

```bash
# Development mode (with auto-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Server will be available at: `http://localhost:8000`

### Access documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Health check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "ok"}
```

## Example cURL Calls

### 1. Test GA4 Connection

Verify your service account has access to a GA4 property.

```bash
curl -X POST "http://localhost:8000/ga4/test-connection" \
  -H "Content-Type: application/json" \
  -d '{
    "property_id": "properties/123456789"
  }'
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Successfully connected to GA4 property. Rows returned: {x}"
}
```

**Response (403 Forbidden):**
```json
{
  "detail": "Permission denied. Check if service account has access to the GA4 property."
}
```

### 2. Get Organic Traffic Trends

Retrieve daily organic traffic metrics for a date range.

```bash
curl -X GET "http://localhost:8000/ga4/organic-traffic?property_id=properties/123456789&start_date=2025-12-01&end_date=2025-12-29" \
  -H "Content-Type: application/json"
```

**Response (200 OK):**
```json
[
  {
    "date": "20251201",
    "sessions": 1250,
    "active_users": 980
  },
  {
    "date": "20251202",
    "sessions": 1340,
    "active_users": 1015
  },
  {
    "date": "20251203",
    "sessions": 1180,
    "active_users": 920
  }
]
```

**Response (400 Bad Request - Invalid date):**
```json
{
  "detail": "Invalid date format. Use YYYY-MM-DD"
}
```

### 3. Get Top Organic Landing Pages

Retrieve top landing pages ranked by organic sessions.

```bash
curl -X GET "http://localhost:8000/ga4/organic-landing-pages?property_id=properties/123456789&start_date=2025-12-01&end_date=2025-12-29&limit=10" \
  -H "Content-Type: application/json"
```

**Response (200 OK):**
```json
[
  {
    "landing_page": "https://example.com/blog/seo-guide",
    "sessions": 5240,
    "active_users": 3890,
    "conversions": 156.0
  },
  {
    "landing_page": "https://example.com/products/",
    "sessions": 4120,
    "active_users": 3010,
    "conversions": 242.0
  },
  {
    "landing_page": "https://example.com/about",
    "sessions": 2890,
    "active_users": 2145,
    "conversions": 87.0
  }
]
```

### 4. Date Range Examples

```bash
# Last 7 days
curl -X GET "http://localhost:8000/ga4/organic-traffic?property_id=properties/123456789&start_date=2025-12-22&end_date=2025-12-29"

# Last 30 days
curl -X GET "http://localhost:8000/ga4/organic-traffic?property_id=properties/123456789&start_date=2025-11-29&end_date=2025-12-29"

# Specific month
curl -X GET "http://localhost:8000/ga4/organic-traffic?property_id=properties/123456789&start_date=2025-12-01&end_date=2025-12-31"
```

## Key Assumptions & Tradeoffs

### Assumptions

1. **Service Account Authentication**
   - Uses Google Application Default Credentials via `service-account-key.json`
   - Service account must have at least Viewer role on GA4 property
   - No OAuth2 support (current code is intended for backend-to-backend communication)

2. **Property ID Format**
   - Must be in format `properties/PROPERTY_ID` (e.g., `properties/123456789`)
   - Not hardcoded; passed as request parameter for flexibility
   - Validation is minimal (GA4 API returns 404 if invalid)

3. **Date Format**
   - All dates must be in `YYYY-MM-DD` format
   - No support for relative dates like "yesterday" in API calls
   - Dates are validated before calling GA4 API

4. **Organic Traffic Filter**
   - Only includes traffic from `sessionDefaultChannelGroup = "Organic Search"`
   - Excludes Direct, Referral, Paid Search, Social, etc.

5. **Metrics & Dimensions**
   - **Organic Traffic**: Daily sessions + active users
   - **Landing Pages**: Sessions, active users, conversions ranked by sessions
   - Direct access to other dimensions/metrics requires code changes

### Tradeoffs

| Tradeoff | Decision | Rationale |
|----------|----------|-----------|
| **Error Handling** | GA4-specific HTTP error codes (403, 404, 400) | Better client debugging vs. generic 500 |
| **Pagination** | No pagination for organic traffic; landing pages limited to 100 | Simpler API, covers 99% of use cases |
| **Async/Await** | Synchronous endpoints | Easier to understand & debug; can be added later if needed |
| **Caching** | No caching of GA4 responses | Real-time data; trade-off for API rate limits |
| **Request Logging** | Minimal logging | Can be added with middleware in future |
| **Authentication** | Service account only | Simpler setup than OAuth; suitable for internal tools |


### Environment Variables (Production)

```bash
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
```