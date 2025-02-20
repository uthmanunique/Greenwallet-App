from fastapi import APIRouter, HTTPException, Depends
from ..schemas.kyc_schemas import KYCRequest, KYCResponse
from ..controllers.kyc_controller import KYCController
from ..utils.jwt_utils import verify_jwt_token  # Assuming you have a JWT utility that returns the user's email

router = APIRouter()
kyc_controller = KYCController()

@router.post("/kyc/verify", response_model=KYCResponse)
async def verify_kyc_route(kyc_data: KYCRequest, email: str = Depends(verify_jwt_token)):
    # Ensure the email in the token matches the one in the KYC request.
    if email != kyc_data.email:
        raise HTTPException(status_code=401, detail="Token does not match provided email")
    return await kyc_controller.verify_kyc(kyc_data)
