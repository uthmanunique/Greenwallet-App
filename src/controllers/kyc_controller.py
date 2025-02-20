from ..schemas.kyc_schemas import KYCRequest, KYCResponse
from ..services.kyc_services import verify_kyc

class KYCController:
    async def verify_kyc(self, kyc_request: KYCRequest) -> KYCResponse:
        result = await verify_kyc(kyc_request.email, kyc_request.dict())
        return KYCResponse(**result)
