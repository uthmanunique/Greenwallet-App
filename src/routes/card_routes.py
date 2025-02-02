from fastapi import HTTPException
from schemas.card_schema import CardCreate, CardResponse
from services.card_service import CardService

class CardController:
    def __init__(self):
        self.card_service = CardService()

    async def create_card(self, card: CardCreate) -> CardResponse:
        try:
            card_id = self.card_service.create_card(card.dict())
            return CardResponse(success=True, message="Card created successfully", card={"id": card_id, **card.dict()})
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def list_cards(self) -> list[CardResponse]:
        try:
            cards = self.card_service.list_cards()
            return [CardResponse(success=True, message="Card fetched successfully", card=card) for card in cards]
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def fund_card(self, card_id: str, amount: float) -> CardResponse:
        try:
            card = self.card_service.fund_card(card_id, amount)
            if not card:
                raise HTTPException(status_code=404, detail="Card not found")
            return CardResponse(success=True, message="Card funded successfully", card=card)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def delete_card(self, card_id: str) -> bool:
        try:
            result = self.card_service.delete_card(card_id)
            if not result:
                raise HTTPException(status_code=404, detail="Card not found")
            return True
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))