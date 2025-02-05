
# # filepath: /c:/Users/Baloun Uthman/Desktop/Greenwallet-backend/src/controllers/user_controller.py
# from src.schemas.user_schemas import UserRegister, UserLogin, VerifyOTP, UserProfileUpdate, SetPIN
# from src.services.user_service import UserService

# class UserController:
#     def __init__(self):
#         self.user_service = UserService()

#     def get_users(self):
#         return self.user_service.get_users()

#     def register_user(self, user: UserRegister):
#         return self.user_service.register_user(user)

#     def login_user(self, user: UserLogin):
#         return self.user_service.login_user(user)

#     def verify_otp(self, email: str, otp: int):
#         return self.user_service.verify_otp(email.otp)

#     def update_profile(self, email: str, profile_data: UserProfileUpdate):
#         return self.user_service.update_profile(email, profile_data)

#     def set_pin(self, data: SetPIN):
#         return self.user_service.set_pin(data.email, data.pin)