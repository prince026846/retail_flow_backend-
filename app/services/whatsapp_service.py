import os
import httpx
import asyncio
from typing import Optional, Dict, Any
from datetime import datetime

class WhatsAppService:
    """Professional WhatsApp Service using Meta Cloud API (Graph API)."""
    
    def __init__(self):
        # Configuration from environment variables
        self.access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
        self.phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
        self.version = os.getenv("WHATSAPP_API_VERSION", "v21.0")
        self.enabled = os.getenv("ENABLE_WHATSAPP_BILLING", "true").lower() == "true"
        self.country_code = os.getenv("WHATSAPP_COUNTRY_CODE", "+91")
        
        # Meta API Endpoint
        self.api_url = f"https://graph.facebook.com/{self.version}/{self.phone_number_id}/messages"

    def format_phone_number(self, phone: str) -> str:
        """Format phone number for WhatsApp Meta API (digits only)."""
        digits = ''.join(filter(str.isdigit, phone))
        
        # If number doesn't start with country code, add it
        cc = self.country_code.replace("+", "")
        if not digits.startswith(cc):
            digits = cc + digits
        
        return digits

    def format_bill_message(self, shop_name: str, bill_url: str, total: float) -> str:
        """Format a clear, professional WhatsApp message."""
        return (
            f"🛍️ *{shop_name}* - Order Confirmation\n\n"
            f"Thank you for your purchase! Your bill is ready.\n\n"
            f"💰 *Total:* ₹{total:.2f}\n"
            f"📄 *View Bill:* {bill_url}\n\n"
            f"We hope to see you again soon! 🙏\n"
            f"_Powered by RetailFlow_"
        )

    async def send_text_message(self, to_phone: str, message: str) -> dict:
        """Sends a direct WhatsApp text message via Meta API."""
        if not self.enabled:
            return {"success": False, "message": "WhatsApp service is disabled."}
            
        if not self.access_token or not self.phone_number_id:
            return {
                "success": False, 
                "message": "WhatsApp API credentials (Token/Phone ID) missing in .env"
            }

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        
        formatted_phone = self.format_phone_number(to_phone)
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": formatted_phone,
            "type": "text",
            "text": {"body": message}
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                print(f"🚀 Sending WhatsApp to {formatted_phone} via Meta API...")
                response = await client.post(self.api_url, headers=headers, json=payload)
                result = response.json()
                
                if response.status_code == 200:
                    print(f"✅ WhatsApp Sent! ID: {result.get('messages', [{}])[0].get('id')}")
                    return {
                        "success": True, 
                        "message": "Sent successfully",
                        "message_id": result.get("messages", [{}])[0].get("id")
                    }
                else:
                    error_data = result.get("error", {})
                    error_msg = error_data.get("message", "Unknown Meta API error")
                    print(f"❌ Meta API Error: {error_msg}")
                    return {"success": False, "message": f"WhatsApp API Error: {error_msg}"}
            except Exception as e:
                print(f"❌ Connection Error: {str(e)}")
                return {"success": False, "message": f"Network error: {str(e)}"}

# Global Instance for use in the app
whatsapp_service = WhatsAppService()

async def send_bill_whatsapp(phone_number: str, order_data: dict,
                             shop_name: str, bill_url: str, total: float) -> dict:
    """Async helper to format and send a bill via WhatsApp."""
    message = whatsapp_service.format_bill_message(shop_name, bill_url, total)
    return await whatsapp_service.send_text_message(phone_number, message)
