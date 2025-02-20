from pydantic import BaseModel, EmailStr

class KYCRequest(BaseModel):
    email: EmailStr
    document_type: str  # e.g., "passport", "driver_license", "nin", "national_id", "voter_card"
    document_image: str  # URL or base64 encoded image of the document
    selfie_image: str    # URL or base64 encoded image of the selfie

class KYCResponse(BaseModel):
    message: str
    kyc_status: bool
    details: str = None
