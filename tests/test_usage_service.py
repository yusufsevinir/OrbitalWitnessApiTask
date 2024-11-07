import pytest
from unittest.mock import AsyncMock, MagicMock
from src.services.usage_service import UsageService

@pytest.mark.asyncio
async def test_usage_with_valid_report_id():
    """
    Test the `UsageService` with a valid report ID.
    Ensures credits are fetched from the report details.
    """
    # Arrange
    service = UsageService()
    service.api_client = AsyncMock()  # Mock the API client
    service.credit_calculator = MagicMock()  # Mock the credit calculator

    # Mock data
    service.api_client.get_current_period_messages.return_value = [
        {"id": "1", "timestamp": "2024-11-07T10:00:00Z", "report_id": "100"}
    ]
    service.api_client.get_report_details.return_value = {
        "name": "Short Lease Report",
        "credit_cost": 15,
    }

    # Act
    result = await service.get_current_period_usage()

    # Assert
    assert result == {
        "usage": [
            {
                "message_id": 1,
                "timestamp": "2024-11-07T10:00:00Z",
                "report_name": "Short Lease Report",
                "credits_used": 15.0,
            }
        ]
    }


@pytest.mark.asyncio
async def test_usage_without_report_id():
    """
    Test the `UsageService` without a report ID.
    Ensures credits are calculated from the message text.
    """
    # Arrange
    service = UsageService()
    service.api_client = AsyncMock()
    service.credit_calculator = MagicMock()

    service.api_client.get_current_period_messages.return_value = [
        {"id": "2", "timestamp": "2024-11-07T10:05:00Z", "text": "Sample message"}
    ]
    service.credit_calculator.calculate_message_credits.return_value = 10.5

    # Act
    result = await service.get_current_period_usage()

    # Assert
    assert result == {
        "usage": [
            {
                "message_id": 2,
                "timestamp": "2024-11-07T10:05:00Z",
                "credits_used": 10.5,
            }
        ]
    }


@pytest.mark.asyncio
async def test_usage_fallback_to_text_credits():
    """
    Test the `UsageService` with a fallback to text-based credit calculation.
    Ensures that if a `report_id` is invalid or unavailable, the credits
    are calculated from the message text.
    """
    # Arrange
    service = UsageService()
    service.api_client = AsyncMock()
    service.credit_calculator = MagicMock()

    # Mock data
    service.api_client.get_current_period_messages.return_value = [
        {
            "id": "3",
            "timestamp": "2024-11-07T10:10:00Z",
            "report_id": "101",
            "text": "Fallback example",
        }
    ]
    service.api_client.get_report_details.return_value = None  # Simulate 404 or unavailable report
    service.credit_calculator.calculate_message_credits.return_value = 12.3

    # Act
    result = await service.get_current_period_usage()

    # Assert
    assert result == {
        "usage": [
            {
                "message_id": 3,
                "timestamp": "2024-11-07T10:10:00Z",
                "credits_used": 12.3,
            }
        ]
    }

    # Ensure fallback behavior: report details were not found, and credit calculator was called
    service.api_client.get_report_details.assert_awaited_once_with(101)
    service.credit_calculator.calculate_message_credits.assert_called_once_with(
        "Fallback example"
    )