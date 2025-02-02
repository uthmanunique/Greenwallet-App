# from pydantic import BaseModel, EmailStr
# from typing import Optional

# class UserCreate(BaseModel):
#     username: str
#     email: EmailStr
#     password: str

# class UserUpdate(BaseModel):
#     username: Optional[str] = None
#     email: Optional[EmailStr] = None
#     password: Optional[str] = None

# class UserProfile(BaseModel):
#     id: str
#     username: str
#     email: EmailStr

#     class Config:
#         orm_mode = True

# filepath: /c:/Users/Baloun Uthman/Desktop/Greenwallet-backend/src/schemas/user_schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UserRegister(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class VerifyOTP(BaseModel):
    email: EmailStr
    otp: int

class UserProfileUpdate(BaseModel):
    home_address: str
    country: str
    state: str
    city: str
    utility_bill: Optional[str] = None  # URL or path to the uploaded file
    date_of_birth: date
    gender: str
    occupation: str
    identity_verification: Optional[str] = None  # URL or path to the uploaded file
    document_type: str  # International Passport, Driver License, NIN, or Voter's Card

class SetPIN(BaseModel):
    email: EmailStr
    pin: str