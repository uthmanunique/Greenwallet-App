# filepath: /c:/Users/Baloun Uthman/Desktop/Greenwallet-backend/src/schemas/user_schemas.py
from pydantic import BaseModel
from fastapi import Form, File, UploadFile

class UserRegister(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    password: str

    @classmethod
    def as_form(
        cls,
        first_name: str = Form(...),
        last_name: str = Form(...),
        email: str = Form(...),
        phone_number: str = Form(...),
        password: str = Form(...)
    ):
        return cls(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, password=password)

class UserLogin(BaseModel):
    email: str
    password: str

    @classmethod
    def as_form(
        cls,
        email: str = Form(...),
        password: str = Form(...)
    ):
        return cls(email=email, password=password)

class VerifyOTP(BaseModel):
    email: str
    otp: int

    @classmethod
    def as_form(
        cls,
        email: str = Form(...),
        otp: int = Form(...)
    ):
        return cls(email=email, otp=otp)

class UserProfileUpdate(BaseModel):
    home_address: str
    country: str
    state: str
    city: str
    utility_bill: UploadFile
    date_of_birth: str
    gender: str
    occupation: str
    identity_verification: UploadFile
    document_type: str

    @classmethod
    def as_form(
        cls,
        home_address: str = Form(...),
        country: str = Form(...),
        state: str = Form(...),
        city: str = Form(...),
        utility_bill: UploadFile = File(...),
        date_of_birth: str = Form(...),
        gender: str = Form(...),
        occupation: str = Form(...),
        identity_verification: UploadFile = File(...),
        document_type: str = Form(...)
    ):
        return cls(
            home_address=home_address,
            country=country,
            state=state,
            city=city,
            utility_bill=utility_bill,
            date_of_birth=date_of_birth,
            gender=gender,
            occupation=occupation,
            identity_verification=identity_verification,
            document_type=document_type
        )

class SetPIN(BaseModel):
    email: str
    pin: str

    @classmethod
    def as_form(
        cls,
        email: str = Form(...),
        pin: str = Form(...)
    ):
        return cls(email=email, pin=pin)