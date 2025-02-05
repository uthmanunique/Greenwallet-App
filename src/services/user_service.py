# # filepath: /c:/Users/Baloun Uthman/Desktop/Greenwallet-backend/src/schemas/user_service.py

# import smtplib
# import random
# import jwt
# import logging
# import os
# from datetime import datetime, timedelta
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from passlib.context import CryptContext
# from fastapi import HTTPException
# from fastapi.responses import JSONResponse
# from src.database import db
# from src.schemas.user_schemas import UserRegister, UserRegisterResponse

# # Load environment variables
# SECRET_KEY = os.getenv('SECRET_KEY')
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30))
# EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
# EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
#     raise ValueError("Missing EMAIL_ADDRESS or EMAIL_PASSWORD in environment variables!")

# # ✅ Ensure MongoDB has the `otps` collection
# if "otps" not in db.list_collection_names():
#     db.create_collection("otps", capped=False)

# # Use Argon2 for stronger password hashing
# pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# # Logging setup
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class UserService:
#     def send_otp(self, email):
#         try:  # ✅ Fixed indentation
#             otp = random.randint(100000, 999999)
#             otp_data = {
#                 "email": email,
#                 "otp": otp,
#                 "expires_at": datetime.utcnow() + timedelta(minutes=10)
#             }
#             db.otps.insert_one(otp_data)

#             # ✅ Debugging: Print email and password before login
#             print(f"DEBUG: Sending OTP to {email}")
#             print(f"DEBUG: Using EMAIL_ADDRESS = {EMAIL_ADDRESS}")

#             msg = MIMEMultipart()
#             msg['From'] = EMAIL_ADDRESS
#             msg['To'] = email
#             msg['Subject'] = 'Your OTP Code'
#             msg.attach(MIMEText(f'Your OTP code is {otp}', 'plain'))

#             server = smtplib.SMTP('smtp.gmail.com', 587)
#             server.starttls()

#             # ✅ Debugging: Check if SMTP login is actually happening
#             print("DEBUG: Logging into SMTP server...")
#             server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
#             print("DEBUG: SMTP login successful inside FastAPI!")

#             server.sendmail(EMAIL_ADDRESS, email, msg.as_string())
#             server.quit() 

#             print("DEBUG: OTP email sent successfully!")
#             return {"message": "OTP sent successfully"}
#         except smtplib.SMTPException as e:
#             logger.error(f"SMTP error in send_otp: {e}")
#             raise HTTPException(status_code=500, detail="Email sending failed")
#         except Exception as e:
#             logger.error(f"Unexpected error in send_otp: {e}")
#             raise HTTPException(status_code=500, detail="Internal Server Error")

#     def register_user(self, user):
#         """
#         Registers a new user and sends an OTP for email verification.
#         """
#         try:
#             existing_user = db.users.find_one({"email": user.email})
#             if existing_user:
#                 raise HTTPException(status_code=400, detail="User already exists")  # ✅ Fixed

#             if not user.email or "@" not in user.email:  # ✅ Validate email format
#                 raise HTTPException(status_code=400, detail="Invalid email format")

#             hashed_password = pwd_context.hash(user.password)
#             user_data = {
#                 "first_name": user.first_name,
#                 "last_name": user.last_name,
#                 "email": user.email,
#                 "phone_number": user.phone_number,
#                 "password": hashed_password
#             }
#             db.users.insert_one(user_data)

#                 # ✅ Generate OTP and Token
#             otp_response = self.send_otp(user.email)  # Sending OTP
#             access_token = self.create_access_token(data={"sub": user.email})  # Generating JWT

            
            
#             return UserRegisterResponse(
#                 message="User registered successfully. Please verify your email.",
#                 otp=otp_response,  # ✅ OTP is returned
#                 access_token=access_token,  # ✅ Token is returned
#                 token_type="bearer"
#             )
        
#         except Exception as e:
#             logger.error(f"Error in register_user: {e}")
#             raise HTTPException(status_code=500, detail="Internal Server Error")

#     def verify_otp(self, email, otp):
#         """
#         Verifies OTP from MongoDB.
#         """
#         try:
#             otp_entry = db.otps.find_one({"email": email}, sort=[("expires_at", -1)])
#             if otp_entry and otp_entry["otp"] == otp and otp_entry["expires_at"] > datetime.utcnow():
#                 return {"message": "OTP verified successfully"}
#             else:
#                 raise HTTPException(status_code=400, detail="Invalid or expired OTP")
#         except Exception as e:
#             logger.error(f"Error in verify_otp: {e}")
#             raise HTTPException(status_code=500, detail="Internal Server Error")

#     def verify_otp(self, email, otp):
#         """
#         Verifies OTP from MongoDB.
#         """
#         try:
#             otp_entry = db.otps.find_one({"email": email}, sort=[("expires_at", -1)])
#             if otp_entry and otp_entry["otp"] == otp and otp_entry["expires_at"] > datetime.utcnow():
#                 return {"message": "OTP verified successfully"}
#             else:
#                 raise HTTPException(status_code=400, detail="Invalid or expired OTP")
#         except Exception as e:
#             logger.error(f"Error in verify_otp: {e}")
#             raise HTTPException(status_code=500, detail="Internal Server Error")

#     def register_user(self, user):
#         """
#         Registers a new user and sends an OTP for email verification.
#         """
#         try:
#             existing_user = db.users.find_one({"email": user.email})
#             if existing_user:
#                 return {"message": "User already exists"}, 400  # ✅ Return 400 instead of crashing

#             hashed_password = pwd_context.hash(user.password)
#             user_data = {
#                 "first_name": user.first_name,
#                 "last_name": user.last_name,
#                 "email": user.email,
#                 "phone_number": user.phone_number,
#                 "password": hashed_password
#             }
#             db.users.insert_one(user_data)

#             # Send OTP for email verification
#             self.send_otp(user.email)

#             return {"message": "User registered successfully. Please verify your email."}
#         except Exception as e:
#             logger.error(f"Error in register_user: {e}")
#             raise HTTPException(status_code=500, detail="Internal Server Error")

#     def login_user(self, user: dict): # ✅ Fix: Accept dictionary properly
#         """
#         Authenticates a user and returns an access token as an HTTPOnly cookie.
#         """
#         try:
#             email = user.get('email') # ✅ Fix: Use `.get()` to retrieve email
#             password = user.get("password")  # ✅ Fix: Use `.get()` to retrieve password

#             db_user = db.users.find_one({"email": user.email})
#             if not db_user or not pwd_context.verify(user.password, db_user["password"]):
#                 raise HTTPException(status_code=400, detail="Invalid email or password")

#             access_token = self.create_access_token(data={"sub": user.email})

#             # Return token in an HTTPOnly cookie
#             # response = JSONResponse(content={"message": "User logged in successfully"})
#             # response.set_cookie(
#             #     key="access_token",
#             #     value=f"Bearer {access_token}",
#             #     httponly=True,
#             #     secure=True,
#             #     samesite="Lax"
#             # ) 
#             # return response

#             return {
#             "message": "User logged in successfully",
#             "access_token": access_token,
#             "token_type": "bearer"
#         }
#         except Exception as e:
#             logger.error(f"Error in login_user: {e}")
#             raise HTTPException(status_code=500, detail="Internal Server Error")

#     def update_profile(self, email, profile_data):
#         """
#         Updates a user's profile.
#         """
#         try:
#             db.users.update_one({"email": email}, {"$set": profile_data})
#             return {"message": "Profile updated successfully"}
#         except Exception as e:
#             logger.error(f"Error in update_profile: {e}")
#             raise HTTPException(status_code=500, detail="Internal Server Error")

#     def set_pin(self, email, pin):
#         """
#         Sets a PIN for a user (hashed for security).
#         """
#         try:
#             hashed_pin = pwd_context.hash(pin)
#             db.users.update_one({"email": email}, {"$set": {"pin": hashed_pin}})
#             return {"message": "PIN set successfully"}
#         except Exception as e:
#             logger.error(f"Error in set_pin: {e}")
#             raise HTTPException(status_code=500, detail="Internal Server Error")

#     def create_access_token(self, data: dict):
#         """
#         Generates a JWT access token.
#         """
#         try:
#             to_encode = data.copy()
#             expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#             to_encode.update({"exp": expire})
#             encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#             return encoded_jwt
#         except Exception as e:
#             logger.error(f"Error in create_access_token: {e}")
#             raise HTTPException(status_code=500, detail="Internal Server Error")

#     def verify_access_token(self, token: str):
#         """
#         Verifies a JWT access token.
#         """
#         try:
#             payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#             email: str = payload.get("sub")
#             if email is None:
#                 raise HTTPException(status_code=401, detail="Invalid token: Missing email")
#             return {"email": email}
#         except jwt.ExpiredSignatureError:
#             logger.error("Token has expired")
#             raise HTTPException(status_code=401, detail="Token has expired. Please login again.")
#         except jwt.InvalidTokenError:
#             logger.error("Invalid token")
#             raise HTTPException(status_code=401, detail="Invalid authentication token")

# src/services/user_service.py
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
