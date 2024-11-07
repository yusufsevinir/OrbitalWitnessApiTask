import httpx
from typing import Dict, List, Optional
from src.config import Config

class ExternalAPIClient:
    BASE_URL = Config.BLOB_STORAGE_URL
    
    async def get_current_period_messages(self) -> List[Dict]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/messages/current-period")
            response.raise_for_status()
            data = response.json()
            return data["messages"]
    
    async def get_report_details(self, report_id: str) -> Optional[Dict]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.BASE_URL}/reports/{report_id}")
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                raise
