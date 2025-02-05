# In your utils/jwt_utils.py
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from typing import Optional
from src.config import Config  # Assuming Config holds your SECRET_KEY and ALGORITHM

def create_jwt_token(email: str) -> str:
    expiration_time = datetime.utcnow() + timedelta(hours=1)
    payload = {
        "sub": email,
        "exp": expiration_time
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return token

def verify_jwt_token(token: str) -> Optional[str]:  # Returns the email if valid, None otherwise
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        email: str = payload.get("sub")
        return email
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except Exception as e: #Catching general exception, for better logging, you can add more explicit exceptions
        print(f"JWT Verification Error: {e}") #Log the error for debugging
        return None  # Or raise HTTPException if you want to handle it differently