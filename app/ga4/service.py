"""
GA4 service layer
Business logic for GA4 operations
"""
from typing import List
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    DateRange,
    Dimension,
    Metric,
    OrderBy
)
from app.ga4.filters import organic_search_filter
from app.models.responses import OrganicTrafficData, OrganicLandingPageData

class GA4Service:
    """Service for GA4 operations"""
    
    def __init__(self, ga4_client: RunReportRequest):
        self.ga4_client = ga4_client
    
    def test_connection(self, property_id: str) -> RunReportRequest:
        """
        Test connection to GA4 property
        
        Args:
            property_id: GA4 property ID
            
        Returns:
            RunReportRequest object
        """
        request = RunReportRequest(
            property=property_id,
            dimensions=[Dimension(name="date")],
            metrics=[Metric(name="sessions")],
            date_ranges=[DateRange(start_date="yesterday", end_date="today")],
            limit=1
        )
        return self.ga4_client.run_report(request)
    
    def get_organic_traffic(
        self,
        property_id: str,
        start_date: str,
        end_date: str
    ) -> List[OrganicTrafficData]:
        """
        Get organic traffic trend data
        
        Args:
            property_id: GA4 property ID
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            List of OrganicTrafficData
        """
        request = RunReportRequest(
            property=property_id,
            dimensions=[Dimension(name="date")],
            metrics=[
                Metric(name="sessions"),
                Metric(name="activeUsers")
            ],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            dimension_filter=organic_search_filter()
        )

        response = self.ga4_client.run_report(request)

        results = []
        for row in response.rows:
            results.append(
                OrganicTrafficData(
                    date=row.dimension_values[0].value,
                    sessions=int(row.metric_values[0].value),
                    active_users=int(row.metric_values[1].value),
                )
            )

        return results
    
    def get_organic_landing_pages(
        self,
        property_id: str,
        start_date: str,
        end_date: str,
        limit: int = 25
    ) -> List[OrganicLandingPageData]:
        """
        Get top organic landing pages
        
        Args:
            property_id: GA4 property ID
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            limit: Maximum number of results (1-100)
            
        Returns:
            List of OrganicLandingPageData
        """ 
        request = RunReportRequest(
            property=property_id,
            dimensions=[Dimension(name="landingPagePlusQueryString")],
            metrics=[
                Metric(name="sessions"),
                Metric(name="activeUsers"),
                Metric(name="conversions")
            ],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            dimension_filter=organic_search_filter(),
            order_bys=[
                OrderBy(
                    metric=OrderBy.MetricOrderBy(metric_name="sessions"),
                    desc=True
                )
            ],
            limit=limit
        )

        response = self.ga4_client.run_report(request)

        results = []
        for row in response.rows:
            results.append(
                OrganicLandingPageData(
                    landing_page=row.dimension_values[0].value,
                    sessions=int(row.metric_values[0].value),
                    active_users=int(row.metric_values[1].value),
                    conversions=float(row.metric_values[2].value),
                )
            )

        return results