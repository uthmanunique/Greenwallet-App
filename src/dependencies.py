from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from .config import SECRET_KEY, ALGORITHM  # Make sure SECRET_KEY and ALGORITHM are defined in your config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_jwt_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return email  # Can return more user data if needed
    
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")