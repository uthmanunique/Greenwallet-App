# filepath: /c:/Users/Baloun Uthman/Desktop/Greenwallet-backend/src/services/user_service.py
import smtplib
import random
import jwt
import logging
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from passlib.context import CryptContext
from fastapi import HTTPException

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserService:
    def get_users(self):
        # Mocked data instead of database interaction
        return [{"username": "ademola"}, {"username": "balogun"}]

    def register_user(self, user):
        try:
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
            access_token = self.create_access_token(data={"sub": user.email})
            return {"message": "User registered successfully. Please verify your email.", "otp": otp, "access_token": access_token}
        except Exception as e:
            logger.error(f"Error in register_user: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def login_user(self, user):
        try:
            # Mocked database lookup
            db_user = {"email": "testuser@example.com", "password": pwd_context.hash("testpassword")}
            if not db_user or not pwd_context.verify(user.password, db_user["password"]):
                raise HTTPException(status_code=400, detail="Invalid email or password")
            access_token = self.create_access_token(data={"sub": user.email})
            return {"message": "User logged in successfully", "access_token": access_token}
        except Exception as e:
            logger.error(f"Error in login_user: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def send_otp(self, email):
        try:
            otp = random.randint(100000, 999999)
            msg = MIMEMultipart()
            msg['From'] = 'your-email@gmail.com'
            msg['To'] = email
            msg['Subject'] = 'Your OTP Code'
            body = f'Your OTP code is {otp}'
            msg.attach(MIMEText(body, 'plain'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('your-email@gmail.com', 'your-email-password')
            text = msg.as_string()
            server.sendmail('your-email@gmail.com', email, text)
            server.quit()
            return otp
        except Exception as e:
            logger.error(f"Error in send_otp: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def verify_otp(self, data):
        try:
            # Mocked OTP verification
            if data.otp == 123456:
                return {"message": "OTP verified successfully"}
            else:
                raise HTTPException(status_code=400, detail="Invalid OTP")
        except Exception as e:
            logger.error(f"Error in verify_otp: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def update_profile(self, email, profile_data):
        try:
            # Mocked database update
            # db.users.update_one({"email": email}, {"$set": profile_data})
            return {"message": "Profile updated successfully"}
        except Exception as e:
            logger.error(f"Error in update_profile: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def set_pin(self, email, pin):
        try:
            hashed_pin = pwd_context.hash(pin)
            # Mocked database update
            # db.users.update_one({"email": email}, {"$set": {"pin": hashed_pin}})
            return {"message": "PIN set successfully"}
        except Exception as e:
            logger.error(f"Error in set_pin: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def create_access_token(self, data: dict):
        try:
            to_encode = data.copy()
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            to_encode.update({"exp": expire})
            encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
            return encoded_jwt
        except Exception as e:
            logger.error(f"Error in create_access_token: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def verify_access_token(self, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            return email
        except jwt.PyJWTError as e:
            logger.error(f"Error in verify_access_token: {e}")
            raise HTTPException(status_code=401, detail="Invalid token")