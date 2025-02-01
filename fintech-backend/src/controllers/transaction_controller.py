from fastapi import APIRouter, HTTPException
from src.models.transaction_model import Transaction
from src.schemas.transaction_schema import TransactionSchema
from src.services.transaction_service import TransactionService

router = APIRouter()
transaction_service = TransactionService()

@router.get("/transactions", response_model=list[TransactionSchema])
async def get_all_transactions():
    transactions = await transaction_service.get_all_transactions()
    return transactions

@router.get("/transactions/{transaction_id}", response_model=TransactionSchema)
async def get_transaction(transaction_id: str):
    transaction = await transaction_service.get_transaction_by_id(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction