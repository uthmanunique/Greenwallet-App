from fastapi import APIRouter, HTTPException
from src.models.wallet_model import Wallet
from src.schemas.wallet_schema import WalletSchema
from src.services.wallet_service import WalletService

router = APIRouter()
wallet_service = WalletService()

@router.get("/wallet/balance/{user_id}", response_model=WalletSchema)
async def get_balance(user_id: str):
    balance = await wallet_service.get_balance(user_id)
    if balance is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return balance

@router.post("/wallet/topup", response_model=WalletSchema)
async def top_up(wallet: WalletSchema):
    updated_wallet = await wallet_service.top_up(wallet)
    return updated_wallet

@router.post("/wallet/transfer", response_model=WalletSchema)
async def transfer_funds(wallet: WalletSchema):
    updated_wallet = await wallet_service.transfer(wallet)
    return updated_wallet

@router.post("/wallet/withdraw", response_model=WalletSchema)
async def withdraw_funds(wallet: WalletSchema):
    updated_wallet = await wallet_service.withdraw(wallet)
    return updated_wallet

@router.post("/wallet/convert", response_model=WalletSchema)
async def convert_currency(wallet: WalletSchema):
    updated_wallet = await wallet_service.convert(wallet)
    return updated_wallet