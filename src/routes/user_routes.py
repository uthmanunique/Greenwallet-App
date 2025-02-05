# # filepath: /c:/Users/Baloun Uthman/Desktop/Greenwallet-backend/src/routes/user_routes.py
# from fastapi import APIRouter, HTTPException, Depends, Form, File, UploadFile
# from fastapi.security import OAuth2PasswordBearer
# from src.controllers.user_controller import UserController
# from src.schemas.user_schemas import UserRegister, UserLogin, VerifyOTP, UserProfileUpdate, SetPIN
# from src.schemas.user_schemas import UserRegister, UserRegisterResponse

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# router = APIRouter()
# user_controller = UserController()


# @router.post("/register")
# async def register_user(
#     first_name: str = Form(...),
#     last_name: str = Form(...),
#     email: str = Form(...),
#     phone_number: str = Form(...),
#     password: str = Form(...)
# ):
#     user = UserRegister(
#         first_name=first_name,
#         last_name=last_name,
#         email=email,
#         phone_number=phone_number,
#         password=password
#     )
#     return user_controller.register_user(user)

# @router.post("/login")
# async def login_user(
#     email: str = Form(...),
#     password: str = Form(...)
# ):
#     user = UserLogin(
#         email=email,
#         password=password
#     )
#     return user_controller.login_user(user)

# # @router.post("/verify-otp")
# # async def verify_otp(
# #     email: str = Form(...),
# #     otp: int = Form(...)
# # ):
# #     data = VerifyOTP(email=email, otp=otp)
# #     return user_controller.verify_otp(data)
# @router.post("/verify-otp")
# async def verify_otp(data: VerifyOTP):
#     return user_controller.verify_otp(data.email, data.otp)  # ✅ Fix: Pass `email` and `otp` separately

# @router.put("/update-profile/{email}")
# async def update_profile(
#     email: str,
#     home_address: str = Form(...),
#     country: str = Form(...),
#     state: str = Form(...),
#     city: str = Form(...),
#     utility_bill: UploadFile = File(...),
#     date_of_birth: str = Form(...),
#     gender: str = Form(...),
#     occupation: str = Form(...),
#     identity_verification: UploadFile = File(...),
#     document_type: str = Form(...),
#     token: str = Depends(oauth2_scheme)
# ):
#     user_controller.user_service.verify_access_token(token)
#     profile_data = UserProfileUpdate(
#         home_address=home_address,
#         country=country,
#         state=state,
#         city=city,
#         utility_bill=utility_bill,
#         date_of_birth=date_of_birth,
#         gender=gender,
#         occupation=occupation,
#         identity_verification=identity_verification,
#         document_type=document_type
#     )
#     return user_controller.update_profile(email, profile_data)

# @router.post("/set-pin")
# async def set_pin(
#     email: str = Form(...),
#     pin: str = Form(...),
#     token: str = Depends(oauth2_scheme)
# ):
#     user_controller.user_service.verify_access_token(token)
#     data = SetPIN(email=email, pin=pin)
#     return user_controller.set_pin(data)

# src/routes/user_routes.py
from fastapi import APIRouter, HTTPException, Depends
from ..schemas.user_schemas import UserRegister, UserRegisterResponse
from ..services.user_service import register_user, verify_otp, generate_otp
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

@router.get("/protected")
async def protected_route(email: str = Depends(verify_jwt_token)):
    return {"message": f"Hello {email}, you are authorized!"}