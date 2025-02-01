from pymongo import MongoClient
from bson import ObjectId
from passlib.context import CryptContext
from fastapi import HTTPException
from src.models.user_model import UserModel

class UserService:
    def __init__(self, db: MongoClient):
        self.db = db
        self.collection = self.db.users
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def register_user(self, user_data: dict) -> UserModel:
        user_data['password'] = self.hash_password(user_data['password'])
        new_user = UserModel(**user_data)
        result = self.collection.insert_one(new_user.dict())
        new_user.id = str(result.inserted_id)
        return new_user

    def authenticate_user(self, email: str, password: str) -> UserModel:
        user = self.collection.find_one({"email": email})
        if not user or not self.verify_password(password, user['password']):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return UserModel(**user)

    def get_user_profile(self, user_id: str) -> UserModel:
        user = self.collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserModel(**user)

    def update_user_profile(self, user_id: str, update_data: dict) -> UserModel:
        result = self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="User not found or no changes made")
        return self.get_user_profile(user_id)

    def verify_kyc(self, user_id: str, kyc_data: dict) -> UserModel:
        result = self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"kyc_verified": True, "kyc_data": kyc_data}})
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="User not found or KYC already verified")
        return self.get_user_profile(user_id)