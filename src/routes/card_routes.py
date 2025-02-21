from fastapi import APIRouter, HTTPException, Depends
from ..schemas.card_schemas import VirtualCardCreate, VirtualCardResponse
from ..services.card_services import create_virtual_card
from ..utils.jwt_utils import verify_jwt_token  # Ensure this returns the user email from token

router = APIRouter()

@router.post("/create", response_model=VirtualCardResponse)
async def create_card_route(
    card: VirtualCardCreate = Depends(VirtualCardCreate.as_form),
    user_email: str = Depends(verify_jwt_token)
):
    try:
        new_card = await create_virtual_card(user_email, card.dict())
        return new_card
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
