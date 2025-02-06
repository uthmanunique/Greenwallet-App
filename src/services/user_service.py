# # filepath: /c:/Users/Baloun Uthman/Desktop/Greenwallet-backend/src/schemas/user_service.py
from passlib.context import CryptContext
from ..models.user_response_model import UserResponseModel
from ..schemas.user_schemas import UserRegisterResponse
from ..models.user_model import UserModel
from ..utils.email_utils import send_otp_email
from ..database import users_collection  # MongoDB collection
from datetime import datetime, timedelta
from ..models.otp_model import OTP
from ..database import db  # Import database
from ..utils.jwt_utils import create_jwt_token  # Import the JWT function
import random
from fastapi import HTTPException, status  # Import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def register_user(data) -> dict:
    existing_user = await users_collection.find_one({"email": data.email})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = pwd_context.hash(data.password)
    otp = generate_otp(data.email)

    # Combine first and last name from the UserRegister schema into full_name
    full_name = f"{data.first_name} {data.last_name}"

    # Note: Adjust the phone field if your UserModel uses a different name.
    user_data = UserModel(
        full_name=full_name,
        email=data.email,
        phone=data.phone_number,
        password=hashed_password,
        otp=otp
    ).dict(by_alias=True)

    inserted_user = await users_collection.insert_one(user_data)
    new_user = await users_collection.find_one({"_id": inserted_user.inserted_id})

    send_otp_email(data.email, otp)

    # Build the response data with all required fields.
    # Convert OTP to int if it's a numeric string.
    try:
        otp_int = int(otp)
    except ValueError:
        otp_int = 0  # Or handle the conversion error appropriately

    response_data = {
        "message": "User registered. OTP sent to email.",
        "otp": otp_int,
        "access_token": "",       # You can generate a token here if needed.
        "token_type": "bearer"    # Default token type
    }

    from ..schemas.user_schemas import UserRegisterResponse  # Import here to avoid circular issues
    user_response = UserRegisterResponse(**response_data)
    
    return {"message": response_data["message"], "user": user_response}

def generate_otp(email: str) -> str:
    otp_code = generate_random_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=5)

    otp = OTP(email=email, otp_code=otp_code, expires_at=expires_at)

    db.otp_verifications.insert_one(otp.dict())  # No need to await here for single inserts
    return otp_code

async def verify_otp(email: str, otp_code: str) -> str:  # Made async
    otp_record = await db.otp_verifications.find_one({"email": email, "otp_code": otp_code})  # Await the find_one

    if not otp_record:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")  # Raise exception

    otp = OTP(**otp_record)

    if otp.expires_at < datetime.utcnow():
        await db.otp_verifications.delete_one({"email": email})  # Await delete
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP expired")  # Raise exception

    token = create_jwt_token(email)
    return token

def generate_random_otp() -> str:
    otp = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    return otp

async def get_user_by_email(email: str) -> UserModel | None:  # Define the function
    user_data = await users_collection.find_one({"email": email})  # Await the find_one
    if user_data:
        return UserModel(**user_data)  # Create a UserModel instance
    return None

async def verify_user_credentials(email: str, password: str) -> str:
    """
    Verifies user credentials. If valid, returns a JWT token.
    If credentials are invalid, returns None.
    """
    user = await get_user_by_email(email)  # Await get_user_by_email
    if user and pwd_context.verify(password, user.password):  # Use pwd_context.verify
        token = create_jwt_token(email)
        return token
    return None

# New function: Update Profile
async def update_profile(user_email: str, data: dict) -> dict:
    # data is expected to be a dict with the profile update fields.
    update_result = await users_collection.update_one(
        {"email": user_email},
        {"$set": data}
    )
    if update_result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Profile update failed")
    updated_user = await users_collection.find_one({"email": user_email})
    return updated_user

# New function: Identity Verification
async def verify_identity(user_email: str, data: dict) -> dict:
    # data is expected to be a dict with identity verification details
    update_fields = {
        "id_document": data.get("id_document"),
        "selfie": data.get("selfie"),
        "kyc_verified": True,
    }
    update_result = await users_collection.update_one(
        {"email": user_email},
        {"$set": update_fields}
    )
    if update_result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Identity verification update failed")
    updated_user = await users_collection.find_one({"email": user_email})
    return updated_user

# New function: Set PIN
async def set_pin(user_email: str, pin: str) -> dict:
    update_result = await users_collection.update_one(
        {"email": user_email},
        {"$set": {"pin": pin}}
    )
    if update_result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Failed to set PIN")
    updated_user = await users_collection.find_one({"email": user_email})
    return updated_user