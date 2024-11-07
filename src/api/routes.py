from fastapi import APIRouter, HTTPException
from src.services.usage_service import UsageService

router = APIRouter()
usage_service = UsageService()

@router.get("/usage")
async def get_usage():
    """Fetches current period usage data."""
    try:
        return await usage_service.get_current_period_usage()
    except Exception as e:
        # Log the error (consider using a logging framework)
        print(f"Error fetching usage data: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
