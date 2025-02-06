# filepath: /c:/Users/Baloun Uthman/Desktop/Greenwallet-backend/src/schemas/user_schemas.py
from pydantic import BaseModel
from fastapi import Form, File, UploadFile
from pydantic import BaseModel, EmailStr


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

# New schema for updating profile (profile update fields only)
class UserProfileUpdate(BaseModel):
    home_address: str
    country: str
    state: str
    city: str
    # For simplicity, we assume the utility bill is sent as a string (e.g., a URL)
    utility_bill: str
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

# New schema for identity verification
class IdentityVerification(BaseModel):
    # For simplicity, we expect the client to send file URLs or base64 strings.
    # In a real application, you would handle file uploads and store them.
    id_document: str  # URL or file path of the ID document
    selfie: str       # URL or file path of the selfie
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

    @classmethod
    def as_form(
        cls,
        email: str = Form(...),
        pin: str = Form(...)
    ):
        return cls(email=email, pin=pin)