# In your models/otp_model.py
from pydantic import BaseModel
from datetime import datetime
from pydantic import Field

class OTP(BaseModel):
    email: str
    otp_code: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
