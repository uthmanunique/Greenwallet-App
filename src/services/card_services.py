import os
import httpx
from fastapi import HTTPException, status
from ..schemas.card_schemas import VirtualCardCreate, VirtualCardResponse

# Flutterwave configuration
FLUTTERWAVE_BASE_URL = "https://api.flutterwave.com/v3"
FLUTTERWAVE_SECRET_KEY = os.getenv("FLUTTERWAVE_SECRET_KEY", "FLWSECK_TEST-7f3003c53642b43aa50741bdc34022ec-X")


# UfitPay configuration
UFITPAY_BASE_URL = "https://api.ufitpay.com/v1"
UFITPAY_API_KEY = os.getenv("UFITPAY_API_KEY")
UFITPAY_API_TOKEN = os.getenv("UFITPAY_API_TOKEN")


async def verify_bvn(bvn: str) -> bool:
    headers = {
        "Authorization": f"Bearer {FLUTTERWAVE_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{FLUTTERWAVE_BASE_URL}/kyc/bvns/{bvn}", headers=headers)
    
    print("BVN Verification Response:", response.status_code, response.text)  # Debugging

    if response.status_code == 200:
        data = response.json()
        # Adjust based on actual Flutterwave response structure
        if data.get("status") == "success":
            return True
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"BVN verification failed: {response.text}")


async def create_virtual_card(user_email: str, card_data: dict) -> VirtualCardResponse:
    bvn = card_data.get("bvn")
    currency = card_data.get("currency")
    first_name = card_data.get("first_name")
    last_name = card_data.get("last_name")
    phone = card_data.get("phone")

    # First, verify the BVN via Flutterwave (now only passing the BVN)
    is_verified = await verify_bvn(bvn)
    if not is_verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="BVN verification failed")

    headers = {
        "Authorization": f"Bearer {FLUTTERWAVE_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "currency": currency,
        "user_email": user_email,
        "first_name": first_name,
        "last_name": last_name,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{FLUTTERWAVE_BASE_URL}/virtual-cards", json=payload, headers=headers)
    
    if response.status_code not in [200, 201]:
        raise HTTPException(status_code=response.status_code, detail="Virtual card creation failed")

    card_info = response.json().get("data", {})
    return VirtualCardResponse(
        card_id=card_info.get("id", ""),
        card_number=card_info.get("card_number", ""),
        cvv=card_info.get("cvv", ""),
        expiry_date=card_info.get("expiry_date", "")
    )