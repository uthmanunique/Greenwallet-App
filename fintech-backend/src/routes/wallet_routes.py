from fastapi import APIRouter, HTTPException
from src.controllers.wallet_controller import WalletController

router = APIRouter()
wallet_controller = WalletController()

@router.get("/wallet/balance")
async def get_balance(user_id: str):
    balance = await wallet_controller.get_balance(user_id)
    if balance is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"balance": balance}

@router.post("/wallet/topup")
async def topup_wallet(user_id: str, amount: float):
    result = await wallet_controller.topup(user_id, amount)
    if not result:
        raise HTTPException(status_code=400, detail="Top-up failed")
    return {"message": "Top-up successful"}

@router.post("/wallet/transfer")
async def transfer_funds(sender_id: str, receiver_id: str, amount: float):
    result = await wallet_controller.transfer(sender_id, receiver_id, amount)
    if not result:
        raise HTTPException(status_code=400, detail="Transfer failed")
    return {"message": "Transfer successful"}

@router.post("/wallet/withdraw")
async def withdraw_funds(user_id: str, amount: float):
    result = await wallet_controller.withdraw(user_id, amount)
    if not result:
        raise HTTPException(status_code=400, detail="Withdrawal failed")
    return {"message": "Withdrawal successful"}

@router.post("/wallet/convert")
async def convert_currency(user_id: str, amount: float, target_currency: str):
    result = await wallet_controller.convert_currency(user_id, amount, target_currency)
    if result is None:
        raise HTTPException(status_code=400, detail="Currency conversion failed")
    return {"converted_amount": result}