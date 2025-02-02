from pydantic import BaseModel
from typing import Optional

class CardCreate(BaseModel):
    card_name: str
    card_type: str
    currency: str
    amount: float

class Card(BaseModel):
    id: str
    card_name: str
    card_type: str
    currency: str
    amount: float

class CardUpdate(BaseModel):
    card_name: Optional[str] = None
    card_type: Optional[str] = None
    amount: Optional[float] = None

class CardResponse(BaseModel):
    success: bool
    message: str
    card: Optional[Card] = None

class CardListResponse(BaseModel):
    success: bool
    message: str
    cards: list[Card] = []