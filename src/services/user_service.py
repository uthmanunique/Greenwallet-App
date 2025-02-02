# from pymongo import MongoClient
# from bson import ObjectId
# from passlib.context import CryptContext
# from fastapi import HTTPException
# from src.models.user_model import UserModel

# class UserService:
#     def __init__(self, db: MongoClient):
#         self.db = db
#         self.collection = self.db.users
#         self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#     def hash_password(self, password: str) -> str:
#         return self.pwd_context.hash(password)

#     def verify_password(self, plain_password: str, hashed_password: str) -> bool:
#         return self.pwd_context.verify(plain_password, hashed_password)

#     def register_user(self, user_data: dict) -> UserModel:
#         user_data['password'] = self.hash_password(user_data['password'])
#         new_user = UserModel(**user_data)
#         result = self.collection.insert_one(new_user.dict())
#         new_user.id = str(result.inserted_id)
#         return new_user

#     def authenticate_user(self, email: str, password: str) -> UserModel:
#         user = self.collection.find_one({"email": email})
#         if not user or not self.verify_password(password, user['password']):
#             raise HTTPException(status_code=401, detail="Invalid credentials")
#         return UserModel(**user)

#     def get_user_profile(self, user_id: str) -> UserModel:
#         user = self.collection.find_one({"_id": ObjectId(user_id)})
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#         return UserModel(**user)

#     def update_user_profile(self, user_id: str, update_data: dict) -> UserModel:
#         result = self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
#         if result.modified_count == 0:
#             raise HTTPException(status_code=404, detail="User not found or no changes made")
#         return self.get_user_profile(user_id)

#     def verify_kyc(self, user_id: str, kyc_data: dict) -> UserModel:
#         result = self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"kyc_verified": True, "kyc_data": kyc_data}})
#         if result.modified_count == 0:
#             raise HTTPException(status_code=404, detail="User not found or KYC already verified")
#         return self.get_user_profile(user_id)

# filepath: /c:/Users/Baloun Uthman/Desktop/Greenwallet-backend/src/services/user_service.py
from passlib.context import CryptContext
from fastapi import HTTPException
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def get_users(self):
        # Mocked data instead of database interaction
        return [{"username": "ademola"}, {"username": "balogun"}]

    def register_user(self, user):
        hashed_password = pwd_context.hash(user.password)
        user_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone_number": user.phone_number,
            "password": hashed_password
        }
        # Mocked database insertion
        # db.users.insert_one(user_data)
        otp = self.send_otp(user.email)
        return {"message": "User registered successfully. Please verify your email.", "otp": otp}

    def login_user(self, user):
        # Mocked database lookup
        db_user = {"email": "testuser@example.com", "password": pwd_context.hash("testpassword")}
        if not db_user or not pwd_context.verify(user.password, db_user["password"]):
            raise HTTPException(status_code=400, detail="Invalid email or password")
        return {"message": "User logged in successfully"}

    def send_otp(self, email):
        otp = random.randint(100000, 999999)
        msg = MIMEMultipart()
        msg['From'] = 'your-email@example.com'
        msg['To'] = email
        msg['Subject'] = 'Your OTP Code'
        body = f'Your OTP code is {otp}'
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.example.com', 587)
        server.starttls()
        server.login('your-email@example.com', 'your-email-password')
        text = msg.as_string()
        server.sendmail('your-email@example.com', email, text)
        server.quit()
        return otp
    
    def verify_otp(self, data):
        # Mocked OTP verification
        if data.otp == 123456:
            return {"message": "OTP verified successfully"}
        else:
            raise HTTPException(status_code=400, detail="Invalid OTP")

    def update_profile(self, email, profile_data):
        # Mocked database update
        # db.users.update_one({"email": email}, {"$set": profile_data})
        return {"message": "Profile updated successfully"}

    def set_pin(self, email, pin):
        hashed_pin = pwd_context.hash(pin)
        # Mocked database update
        # db.users.update_one({"email": email}, {"$set": {"pin": hashed_pin}})
        return {"message": "PIN set successfully"}