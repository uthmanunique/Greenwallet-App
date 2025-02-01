from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

class Transaction(BaseModel):
    id: str
    amount: float
    date: str
    description: str

class Wallet(BaseModel):
    id: str
    user_id: str
    balance: float
    transaction_history: List[Transaction] = []

    class Config:
        json_encoders = {
            ObjectId: str
        }