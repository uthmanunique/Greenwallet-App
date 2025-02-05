# from pydantic import BaseModel, EmailStr
# from bson import ObjectId
# from typing import Optional
# from datetime import datetime

# class User(BaseModel):
#     id: Optional[str] = None
#     email: EmailStr
#     password: str
#     full_name: str
#     phone_number: str
#     created_at: datetime = datetime.utcnow()
#     updated_at: datetime = datetime.utcnow()
#     is_verified: bool = False

#     class Config:
#         json_encoders = {
#             ObjectId: str
#         }

#     def update(self, **kwargs):
#         for key, value in kwargs.items():
#             setattr(self, key, value)

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId

class UserModel(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    full_name: str
    email: EmailStr
    phone: str
    password: str  # Hashed password
    is_verified: bool = False
    otp: Optional[str] = None  # OTP for email verification
    pin: Optional[str] = None  # For transactions
