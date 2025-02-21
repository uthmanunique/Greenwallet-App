import random
import string
import os
import httpx
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from ..schemas.card_schemas import VirtualCardCreate, VirtualCardResponse

# Flutterwave configuration (ensure you have these in your .env or config)
FLUTTERWAVE_BASE_URL = "https://api.flutterwave.com/v3"
FLUTTERWAVE_SECRET_KEY = os.getenv("FLUTTERWAVE_SECRET_KEY")


async def verify_bvn(bvn: str, first_name: str, last_name: str, phone: str) -> bool:
    headers = {
        "Authorization": f"Bearer {FLUTTERWAVE_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "bvn": bvn,
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{FLUTTERWAVE_BASE_URL}/bvn/verify", json=payload, headers=headers)
    print("BVN Verification Response:", response.status_code, response.text)
    if response.status_code == 200:
        data = response.json()
        # Adjust these keys based on Flutterwave's actual response structure
        if data.get("status") == "success" and data.get("data", {}).get("verified") is True:
            return True
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="BVN verification failed")

async def create_virtual_card(user_email: str, card_data: dict) -> VirtualCardResponse:
    bvn = card_data.get("bvn")
    currency = card_data.get("currency")
    first_name = card_data.get("first_name")
    last_name = card_data.get("last_name")
    phone = card_data.get("phone")

    # First, verify the BVN via Flutterwave
    is_verified = await verify_bvn(bvn, first_name, last_name, phone)
    if not is_verified:
        # The verify_bvn function now raises an HTTPException if verification fails.
        # This line is just for clarity.
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
        # Add any additional fields required by Flutterwave's virtual card API.
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