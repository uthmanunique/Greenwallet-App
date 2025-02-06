
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

# New fields for profile update
    home_address: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    utility_bill: Optional[str] = None  # You might store a URL or file path
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    occupation: Optional[str] = None

    # New fields for identity verification
    id_document: Optional[str] = None  # URL or file path for ID document
    selfie: Optional[str] = None         # URL or file path for selfie
    kyc_verified: bool = False           # Whether KYC has been completed