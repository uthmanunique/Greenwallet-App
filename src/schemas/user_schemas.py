from pydantic import BaseModel, EmailStr
from fastapi import Form, File, UploadFile
from typing import Optional

class UserRegister(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    password: str

class UserRegisterResponse(BaseModel):
    message: str
    otp: int
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    email: str
    password: str

class VerifyOTP(BaseModel):
    email: str
    otp: int

# Schema for updating profile (profile update fields only)
class UserProfileUpdate(BaseModel):
    home_address: str
    country: str
    state: str
    city: str
    utility_bill: str  # e.g., a URL or file path
    date_of_birth: str
    gender: str
    occupation: str

    @classmethod
    def as_form(
        cls,
        home_address: str = Form(...),
        country: str = Form(...),
        state: str = Form(...),
        city: str = Form(...),
        utility_bill: str = Form(...),
        date_of_birth: str = Form(...),
        gender: str = Form(...),
        occupation: str = Form(...)
    ):
        return cls(
            home_address=home_address,
            country=country,
            state=state,
            city=city,
            utility_bill=utility_bill,
            date_of_birth=date_of_birth,
            gender=gender,
            occupation=occupation
        )

# Define UserProfileResponse as a top-level schema
class UserProfileResponse(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    home_address: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    occupation: Optional[str] = None

# Schema for identity verification
class IdentityVerification(BaseModel):
    id_document: str  # URL or file path for the ID document
    selfie: str       # URL or file path for the selfie
    document_type: str

    @classmethod
    def as_form(
        cls,
        id_document: str = Form(...),
        selfie: str = Form(...),
        document_type: str = Form(...)
    ):
        return cls(
            id_document=id_document,
            selfie=selfie,
            document_type=document_type
        )

# Existing SetPIN schema
class SetPIN(BaseModel):
    pin: str

    @classmethod
    def as_form(
        cls,
        pin: str = Form(...)
    ):
        return cls(pin=pin)

# If needed, create a separate schema that includes email with PIN
class SetPINWithEmail(BaseModel):
    email: str
    pin: str

    @classmethod
    def as_form(
        cls,
        email: str = Form(...),
        pin: str = Form(...)
    ):
        return cls(email=email, pin=pin)
