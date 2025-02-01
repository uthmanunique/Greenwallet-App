from pydantic import BaseModel
from typing import List, Optional

class WalletBase(BaseModel):
    user_id: str
    balance: float

class WalletCreate(WalletBase):
    pass

class WalletUpdate(BaseModel):
    balance: Optional[float] = None

class Wallet(WalletBase):
    id: str
    transaction_history: List[str] = []

    class Config:
        orm_mode = True