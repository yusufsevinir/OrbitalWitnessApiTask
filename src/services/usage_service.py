from src.clients.external_api_client import ExternalAPIClient
from src.utils.credit_calculator import CreditCalculator

class UsageService:
    def __init__(self):
        self.api_client = ExternalAPIClient()
        self.credit_calculator = CreditCalculator()
    
    async def get_current_period_usage(self):
        messages = await self.api_client.get_current_period_messages()
        usage = []
    
        for message in messages:
            usage_entry = {
                "message_id": int(message["id"]),
                "timestamp": message["timestamp"]
            }
            
            report_id = message.get("report_id")
            if report_id:
                report_id = int(report_id)
                report_details = await self.api_client.get_report_details(report_id)
                if report_details:
                    usage_entry["report_name"] = report_details["name"]
                    credits = report_details["credit_cost"]
                else:
                    credits = self.credit_calculator.calculate_message_credits(message["text"])
            else:
                credits = self.credit_calculator.calculate_message_credits(message["text"])
            
            usage_entry["credits_used"] = float(credits)
            usage.append(usage_entry)
            
        return {"usage": usage}