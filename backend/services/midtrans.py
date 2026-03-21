import httpx
import base64
import json
import hashlib
from typing import Dict, Any, Optional
from backend.core.config import settings

class MidtransService:
    def __init__(self):
        self.server_key = settings.MIDTRANS_SERVER_KEY
        self.is_production = settings.MIDTRANS_IS_PRODUCTION
        
        if self.is_production:
            self.base_url = "https://api.midtrans.com/v2"
        else:
            self.base_url = "https://api.sandbox.midtrans.com/v2"
            
        auth_string = f"{self.server_key}:".encode("utf-8")
        self.auth_header = f"Basic {base64.b64encode(auth_string).decode('utf-8')}"
        
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": self.auth_header
        }

    async def create_qris_transaction(
        self, 
        order_id: str, 
        gross_amount: float, 
        custom_field1: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a QRIS transaction using Midtrans Core API.
        """
        payload = {
            "payment_type": "qris",
            "transaction_details": {
                "order_id": order_id,
                "gross_amount": int(gross_amount)
            }
        }
        
        if custom_field1:
            payload["custom_field1"] = custom_field1

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/charge",
                headers=self.headers,
                json=payload,
                timeout=10.0
            )
            
            response.raise_for_status()
            return response.json()

    def verify_signature(
        self, 
        order_id: str, 
        status_code: str, 
        gross_amount: str, 
        signature_key: str
    ) -> bool:
        """
        Verify Midtrans webhook signature key.
        """
        payload = f"{order_id}{status_code}{gross_amount}{self.server_key}"
        calculated_signature = hashlib.sha512(payload.encode("utf-8")).hexdigest()
        return calculated_signature == signature_key

midtrans_service = MidtransService()
