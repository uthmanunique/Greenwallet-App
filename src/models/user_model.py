from pydantic import BaseModel, EmailStr
from bson import ObjectId
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    password: str
    full_name: str
    phone_number: str
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    is_verified: bool = False

    class Config:
        json_encoders = {
            ObjectId: str
        }

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)