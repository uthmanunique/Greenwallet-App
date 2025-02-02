from pydantic import BaseModel
from bson import ObjectId
from typing import Optional
from datetime import datetime

class Transaction(BaseModel):
    id: Optional[str] = None
    user_id: str
    amount: float
    transaction_type: str  # e.g., 'credit' or 'debit'
    description: Optional[str] = None
    created_at: datetime = datetime.now()

    class Config:
        json_encoders = {
            ObjectId: str
        }