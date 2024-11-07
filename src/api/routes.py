from fastapi import APIRouter, HTTPException
from src.services.usage_service import UsageService

router = APIRouter()
usage_service = UsageService()

@router.get("/usage")
async def get_usage():
    try:
        return await usage_service.get_current_period_usage()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
