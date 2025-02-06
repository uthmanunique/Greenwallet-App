
# src/routes/user_routes.py
from fastapi import APIRouter, HTTPException, Depends
from ..schemas.user_schemas import IdentityVerification, SetPIN, UserProfileUpdate, UserRegister, UserRegisterResponse
from ..services.user_service import (
    register_user,
    verify_otp,
    verify_user_credentials,
    create_jwt_token,
    update_profile,
    verify_identity,
    set_pin
)
from ..utils.email_utils import send_otp_email
from pydantic import BaseModel
from ..services.user_service import verify_user_credentials, create_jwt_token
from ..models.user_model import UserModel
from ..database import users_collection
from datetime import datetime, timedelta
from ..utils.jwt_utils import create_jwt_token, verify_jwt_token
from passlib.context import CryptContext


router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/auth/register", response_model=UserRegisterResponse)
async def register(user_data: UserRegister):
    result = await register_user(user_data)
    # If an error occurs, the service raises an HTTPException,
    # so we simply return the user response:
    return result['user']  # 'user' is expected to be an instance of UserRegisterResponse

@router.post("/verify-otp")
async def verify_otp_route(email: str, otp: str):
    token = await verify_otp(email, otp)
    if not token:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    return {"message": "OTP verified. Login successful.", "token": token}

@router.post("/login")
async def login(data: LoginRequest):
    token = await verify_user_credentials(data.email, data.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}

# New endpoint: Update Profile
@router.put("/users/profile/update")
async def update_user_profile(data: UserProfileUpdate, email: str = Depends(verify_jwt_token)):
    # 'email' is obtained from the token verification dependency
    updated_user = await update_profile(email, data.dict())
    return {"message": "Profile updated successfully", "user": updated_user}

# New endpoint: Identity Verification
@router.post("/users/kyc/verify")
async def identity_verification(data: IdentityVerification, email: str = Depends(verify_jwt_token)):
    updated_user = await verify_identity(email, data.dict())
    return {"message": "Identity verification successful", "user": updated_user}

@router.post("/users/pin/set")
async def pin_setup(data: SetPIN, email: str = Depends(verify_jwt_token)):
    updated_user = await set_pin(email, data.pin)
    return {"message": "PIN set successfully", "user": updated_user}


@router.get("/protected")
async def protected_route(email: str = Depends(verify_jwt_token)):
    return {"message": f"Hello {email}, you are authorized!"}
