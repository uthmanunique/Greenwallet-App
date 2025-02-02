# from fastapi import APIRouter, HTTPException
# from src.controllers.user_controller import UserController
# from src.schemas.user_schema import UserCreate, UserUpdate

# router = APIRouter()
# user_controller = UserController()

# @router.post("/register", response_model=UserCreate)
# async def register_user(user: UserCreate):
#     return await user_controller.register(user)

# @router.post("/login")
# async def login_user(user: UserCreate):
#     return await user_controller.login(user)

# @router.get("/profile/{user_id}")
# async def get_user_profile(user_id: str):
#     profile = await user_controller.fetch_profile(user_id)
#     if not profile:
#         raise HTTPException(status_code=404, detail="User not found")
#     return profile

# @router.put("/profile/{user_id}", response_model=UserUpdate)
# async def update_user_profile(user_id: str, user: UserUpdate):
#     updated_user = await user_controller.update_profile(user_id, user)
#     if not updated_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return updated_user

# @router.post("/kyc/{user_id}")
# async def verify_kyc(user_id: str):
#     result = await user_controller.verify_kyc(user_id)
#     if not result:
#         raise HTTPException(status_code=400, detail="KYC verification failed")
#     return {"detail": "KYC verification successful"}


# filepath: /c:/Users/Baloun Uthman/Desktop/Greenwallet-backend/src/routes/user_routes.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from src.controllers.user_controller import UserController
from src.schemas.user_schemas import UserRegister, UserLogin, VerifyOTP, UserProfileUpdate, SetPIN

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()
user_controller = UserController()

@router.post("/register")
async def register_user(user: UserRegister):
    return user_controller.register_user(user)

@router.post("/login")
async def login_user(user: UserLogin):
    return user_controller.login_user(user)

@router.post("/verify-otp")
async def verify_otp(data: VerifyOTP):
    return user_controller.verify_otp(data)

@router.put("/update-profile/{email}")
async def update_profile(email: str, profile_data: UserProfileUpdate, token: str = Depends(oauth2_scheme)):
    user_controller.user_service.verify_access_token(token)
    return user_controller.update_profile(email, profile_data)

@router.post("/set-pin")
async def set_pin(data: SetPIN, token: str = Depends(oauth2_scheme)):
    user_controller.user_service.verify_access_token(token)
    return user_controller.set_pin(data)