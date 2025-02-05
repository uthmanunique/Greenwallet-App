# src/models/user_response_model.py
from pydantic import BaseModel
from typing import Optional

class UserResponseModel(BaseModel):
    _id: str
    full_name: str
    email: str
    phone: str
    is_verified: bool
    otp: str
    pin: Optional[str] = None

    class Config:
        orm_mode = True
