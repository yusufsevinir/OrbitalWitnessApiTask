import pytest
from unittest.mock import AsyncMock
from src.clients.external_api_client import ExternalAPIClient

@pytest.mark.asyncio
async def test_get_current_period_messages():
    """
    Test the `get_current_period_messages` method.
    Ensures it fetches the correct message data from the endpoint.
    """
    client = ExternalAPIClient()
    client.get_current_period_messages = AsyncMock(return_value=[{"id": "1"}])

    messages = await client.get_current_period_messages()
    assert messages == [{"id": "1"}]


@pytest.mark.asyncio
async def test_get_report_details():
    """
    Test the `get_report_details` method.
    Ensures it fetches report details correctly or handles 404 responses.
    """
    client = ExternalAPIClient()
    client.get_report_details = AsyncMock(
        side_effect=[{"name": "Report A", "credit_cost": 10}, None]
    )

    # Valid report
    report = await client.get_report_details("101")
    assert report == {"name": "Report A", "credit_cost": 10}

    # Missing report
    missing_report = await client.get_report_details("999")
    assert missing_report is None