import httpx
from typing import Dict, List, Optional
from src.config import Config

class ExternalAPIClient:
    """
    Client for interacting with external blob storage API.
    Handles fetching messages and report details with proper error handling.
    """
    
    # Configure timeout for API requests (in seconds)
    TIMEOUT = 30.0
    BASE_URL = Config.BLOB_STORAGE_URL
    
    async def get_current_period_messages(self) -> List[Dict]:
        """
        Fetches all messages for the current period from blob storage.
        
        Returns:
            List[Dict]: List of message objects
            
        Raises:
            httpx.TimeoutException: If the request times out
        """
        try:
            async with httpx.AsyncClient(timeout=self.TIMEOUT) as client:
                response = await client.get(
                    f"{self.BASE_URL}/messages/current-period",
                    headers=self._get_default_headers()
                )
                response.raise_for_status()
                
                data = response.json()
                if not isinstance(data.get("messages"), list):
                    raise ValueError("Invalid response format: 'messages' must be a list")
                    
                return data["messages"]
                
        except httpx.TimeoutException:
            print(f"Request timed out while fetching messages from {self.BASE_URL}")
            raise
        except Exception as e:
            print(f"Unexpected error while fetching messages: {str(e)}")
            raise
    
    async def get_report_details(self, report_id: str) -> Optional[Dict]:
        """
        Fetches details for a specific report.
        
        Args:
            report_id (str): ID of the report to fetch
            
        Returns:
            Optional[Dict]: Report details if found, None if report doesn't exist
            
        Raises:
            httpx.TimeoutException: If the request times out
        """
        try:
            async with httpx.AsyncClient(timeout=self.TIMEOUT) as client:
                response = await client.get(
                    f"{self.BASE_URL}/reports/{report_id}",
                    headers=self._get_default_headers()
                )
                response.raise_for_status()
                
                data = response.json()
                if not isinstance(data, dict):
                    raise ValueError("Invalid response format: expected dictionary")
                    
                return data
                
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            print(f"HTTP error {e.response.status_code} while fetching report {report_id}")
            raise
        except httpx.TimeoutException:
            print(f"Request timed out while fetching report {report_id}")
            raise
        except Exception as e:
            print(f"Unexpected error while fetching report {report_id}: {str(e)}")
            raise
    
    def _get_default_headers(self) -> Dict[str, str]:
        """
        Returns default headers for API requests.
        Add authentication headers here if needed.
        """
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            # Add any authentication headers here
            # "Authorization": f"Bearer {Config.API_TOKEN}"
        }
