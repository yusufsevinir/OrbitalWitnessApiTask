from src.clients.external_api_client import ExternalAPIClient
from src.utils.credit_calculator import CreditCalculator

class UsageService:
    def __init__(self):
        self.api_client = ExternalAPIClient()
        self.credit_calculator = CreditCalculator()
    
    async def get_current_period_usage(self):
        """
        Retrieves and processes usage data for the current period.
        Returns a list of usage entries with message details and credit consumption.
        
        Returns:
            dict: Contains 'usage' key with list of usage entries
        
        Raises:
            Exception: If there's an error fetching or processing messages
        """
        try:
            # Fetch all messages for current period
            messages = await self.api_client.get_current_period_messages()
            usage = []
        
            for message in messages:
                try:
                    # Initialize basic usage entry with required fields
                    usage_entry = {
                        "message_id": int(message["id"]),
                        "timestamp": message["timestamp"]
                    }
                    
                    # Handle report-based messages
                    report_id = message.get("report_id")
                    if report_id:
                        try:
                            report_id = int(report_id)
                            # Fetch additional details if message is report-based
                            report_details = await self.api_client.get_report_details(report_id)
                            if report_details:
                                usage_entry["report_name"] = report_details["name"]
                                credits = report_details["credit_cost"]
                            else:
                                # Fallback to calculator if report details not found
                                credits = self.credit_calculator.calculate_message_credits(message["text"])
                        except ValueError:
                            # Handle invalid report_id format
                            credits = self.credit_calculator.calculate_message_credits(message["text"])
                    else:
                        # Calculate credits for regular messages
                        credits = self.credit_calculator.calculate_message_credits(message["text"])
                    
                    usage_entry["credits_used"] = float(credits)
                    usage.append(usage_entry)
                
                except (KeyError, ValueError) as e:
                    # Log individual message processing errors but continue with other messages
                    print(f"Error processing message {message.get('id', 'unknown')}: {str(e)}")
                    continue
            
            return {"usage": usage}
        
        except Exception as e:
            # Log the error and re-raise for proper handling upstream
            print(f"Error fetching usage data: {str(e)}")
            raise