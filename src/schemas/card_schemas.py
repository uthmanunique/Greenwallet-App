from pydantic import BaseModel
from fastapi import Form

class VirtualCardCreate(BaseModel):
    bvn: str
    currency: str
    first_name: str
    last_name: str
    phone: str

    @classmethod
    def as_form(
        cls,
        bvn: str = Form(...),
        currency: str = Form(...),
        first_name: str = Form(...),
        last_name: str = Form(...),
        phone: str = Form(...)
    ):
        return cls(
            bvn=bvn,
            currency=currency,
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )

class VirtualCardResponse(BaseModel):
    card_id: str
    card_number: str
    cvv: str
    expiry_date: str
    # Add additional fields as needed
