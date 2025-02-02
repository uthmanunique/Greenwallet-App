# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from src.services.user_service import UserService

# router = APIRouter()

# class UserRegister(BaseModel):
#     username: str
#     email: str
#     password: str

# class UserLogin(BaseModel):
#     email: str
#     password: str

# class UserProfileUpdate(BaseModel):
#     username: str = None
#     email: str = None

# class KYCVerification(BaseModel):
#     user_id: str
#     document: str

# user_service = UserService()

# @router.post("/register")
# async def register(user: UserRegister):
#     return await user_service.register(user)

# @router.post("/login")
# async def login(user: UserLogin):
#     return await user_service.login(user)

# @router.get("/profile/{user_id}")
# async def fetch_profile(user_id: str):
#     profile = await user_service.fetch_profile(user_id)
#     if not profile:
#         raise HTTPException(status_code=404, detail="User not found")
#     return profile

# @router.put("/profile/{user_id}")
# async def update_profile(user_id: str, user: UserProfileUpdate):
#     updated_user = await user_service.update_profile(user_id, user)
#     if not updated_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return updated_user

# @router.post("/kyc")
# async def verify_kyc(kyc: KYCVerification):
#     return await user_service.verify_kyc(kyc)


# filepath: /c:/Users/Baloun Uthman/Desktop/Greenwallet-backend/src/controllers/user_controller.py
from src.schemas.user_schemas import UserRegister, UserLogin, VerifyOTP, UserProfileUpdate, SetPIN
from src.services.user_service import UserService

class UserController:
    def __init__(self):
        self.user_service = UserService()

    def get_users(self):
        return self.user_service.get_users()

    def register_user(self, user: UserRegister):
        return self.user_service.register_user(user)

    def login_user(self, user: UserLogin):
        return self.user_service.login_user(user)

    def verify_otp(self, data: VerifyOTP):
        return self.user_service.verify_otp(data)

    def update_profile(self, email: str, profile_data: UserProfileUpdate):
        return self.user_service.update_profile(email, profile_data)

    def set_pin(self, data: SetPIN):
        return self.user_service.set_pin(data.email, data.pin)