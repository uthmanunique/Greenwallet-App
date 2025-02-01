from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransactionBase(BaseModel):
    amount: float
    currency: str
    description: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: str
    user_id: str
    created_at: datetime

    class Config:
        orm_mode = True