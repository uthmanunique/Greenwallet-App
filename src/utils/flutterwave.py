from fastapi import HTTPException
import requests

class Flutterwave:
    BASE_URL = "https://api.flutterwave.com/v3"
    SECRET_KEY = "FLWSECK_TEST-7f3003c53642b43aa50741bdc34022ec-X"  # Replace with your actual secret key

    @classmethod
    def create_payment(cls, amount, currency, email, tx_ref):
        url = f"{cls.BASE_URL}/charges?type=mobilemoneyghana"
        headers = {
            "Authorization": f"Bearer {cls.SECRET_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "tx_ref": tx_ref,
            "amount": amount,
            "currency": currency,
            "email": email,
            "payment_type": "mobilemoneyghana"
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        return response.json()

    @classmethod
    def verify_payment(cls, tx_ref):
        url = f"{cls.BASE_URL}/charges/verify_by_txref/{tx_ref}"
        headers = {
            "Authorization": f"Bearer {cls.SECRET_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        return response.json()

    @classmethod
    def create_virtual_card(cls, amount, currency):
        url = f"{cls.BASE_URL}/virtual-cards"
        headers = {
            "Authorization": f"Bearer {cls.SECRET_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "amount": amount,
            "currency": currency,
            "email": "user@example.com"  # Replace with actual user email
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        return response.json()