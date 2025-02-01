from fastapi import APIRouter, HTTPException
from src.controllers.transaction_controller import TransactionController

router = APIRouter()
transaction_controller = TransactionController()

@router.get("/transactions")
async def get_all_transactions():
    return await transaction_controller.get_all_transactions()

@router.get("/transactions/{transaction_id}")
async def get_transaction(transaction_id: str):
    transaction = await transaction_controller.get_transaction(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.post("/transactions")
async def create_transaction(transaction_data: dict):
    return await transaction_controller.create_transaction(transaction_data)

@router.delete("/transactions/{transaction_id}")
async def delete_transaction(transaction_id: str):
    success = await transaction_controller.delete_transaction(transaction_id)
    if not success:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"detail": "Transaction deleted successfully"}