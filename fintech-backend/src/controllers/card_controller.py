from fastapi import APIRouter, HTTPException
from schemas.card_schema import CardCreate, CardResponse
from services.card_service import CardService

router = APIRouter()
card_service = CardService()

@router.post("/cards", response_model=CardResponse)
async def create_card(card: CardCreate):
    try:
        return await card_service.create_card(card)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/cards", response_model=list[CardResponse])
async def list_cards():
    try:
        return await card_service.list_cards()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/cards/{card_id}/fund", response_model=CardResponse)
async def fund_card(card_id: str, amount: float):
    try:
        return await card_service.fund_card(card_id, amount)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/cards/{card_id}", response_model=dict)
async def delete_card(card_id: str):
    try:
        await card_service.delete_card(card_id)
        return {"detail": "Card deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))