from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from bson import ObjectId

class InvoiceModel(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    invoice_id: str
    project_name: str
    recipient: dict
    card_details: dict
    product: dict
    issue_date: date
    due_date: date
    total: float

    class Config:
        allow_population_by_field_name = True
