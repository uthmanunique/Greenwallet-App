# filepath: /c:/Users/Baloun Uthman/Desktop/Greenwallet-backend/src/routes/user_routes.py
from fastapi import APIRouter, HTTPException, Depends, Form, File, UploadFile
from fastapi.security import OAuth2PasswordBearer
from src.controllers.user_controller import UserController
from src.schemas.user_schemas import UserRegister, UserLogin, VerifyOTP, UserProfileUpdate, SetPIN

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()
user_controller = UserController()

@router.post("/register")
async def register_user(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    phone_number: str = Form(...),
    password: str = Form(...)
):
    user = UserRegister(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        password=password
    )
    return user_controller.register_user(user)

@router.post("/login")
async def login_user(
    email: str = Form(...),
    password: str = Form(...)
):
    user = UserLogin(
        email=email,
        password=password
    )
    return user_controller.login_user(user)

@router.post("/verify-otp")
async def verify_otp(
    email: str = Form(...),
    otp: int = Form(...)
):
    data = VerifyOTP(email=email, otp=otp)
    return user_controller.verify_otp(data)

@router.put("/update-profile/{email}")
async def update_profile(
    email: str,
    home_address: str = Form(...),
    country: str = Form(...),
    state: str = Form(...),
    city: str = Form(...),
    utility_bill: UploadFile = File(...),
    date_of_birth: str = Form(...),
    gender: str = Form(...),
    occupation: str = Form(...),
    identity_verification: UploadFile = File(...),
    document_type: str = Form(...),
    token: str = Depends(oauth2_scheme)
):
    user_controller.user_service.verify_access_token(token)
    profile_data = UserProfileUpdate(
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
    return user_controller.update_profile(email, profile_data)

@router.post("/set-pin")
async def set_pin(
    email: str = Form(...),
    pin: str = Form(...),
    token: str = Depends(oauth2_scheme)
):
    user_controller.user_service.verify_access_token(token)
    data = SetPIN(email=email, pin=pin)
    return user_controller.set_pin(data)