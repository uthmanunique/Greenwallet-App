from pydantic import BaseModel
from bson import ObjectId
from typing import Optional

class Card(BaseModel):
    id: Optional[str] = None
    card_number: str
    card_type: str
    expiration_date: str
    cvv: str
    balance: float

    class Config:
        json_encoders = {
            ObjectId: str
        }