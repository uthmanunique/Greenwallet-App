from pymongo import MongoClient
from bson import ObjectId
from src.models.wallet_model import Wallet

class WalletService:
    def __init__(self, db_url: str, db_name: str):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.wallet_collection = self.db['wallets']

    def create_wallet(self, user_id: str):
        wallet = Wallet(user_id=user_id, balance=0.0, transactions=[])
        self.wallet_collection.insert_one(wallet.dict())
        return wallet

    def get_wallet(self, user_id: str):
        return self.wallet_collection.find_one({"user_id": user_id})

    def top_up_wallet(self, user_id: str, amount: float):
        wallet = self.get_wallet(user_id)
        if wallet:
            new_balance = wallet['balance'] + amount
            self.wallet_collection.update_one({"user_id": user_id}, {"$set": {"balance": new_balance}})
            return new_balance
        return None

    def transfer_funds(self, from_user_id: str, to_user_id: str, amount: float):
        from_wallet = self.get_wallet(from_user_id)
        to_wallet = self.get_wallet(to_user_id)
        if from_wallet and to_wallet and from_wallet['balance'] >= amount:
            new_from_balance = from_wallet['balance'] - amount
            new_to_balance = to_wallet['balance'] + amount
            self.wallet_collection.update_one({"user_id": from_user_id}, {"$set": {"balance": new_from_balance}})
            self.wallet_collection.update_one({"user_id": to_user_id}, {"$set": {"balance": new_to_balance}})
            return new_from_balance, new_to_balance
        return None

    def withdraw_funds(self, user_id: str, amount: float):
        wallet = self.get_wallet(user_id)
        if wallet and wallet['balance'] >= amount:
            new_balance = wallet['balance'] - amount
            self.wallet_collection.update_one({"user_id": user_id}, {"$set": {"balance": new_balance}})
            return new_balance
        return None

    def convert_currency(self, user_id: str, amount: float, conversion_rate: float):
        wallet = self.get_wallet(user_id)
        if wallet and wallet['balance'] >= amount:
            converted_amount = amount * conversion_rate
            new_balance = wallet['balance'] - amount
            self.wallet_collection.update_one({"user_id": user_id}, {"$set": {"balance": new_balance}})
            return converted_amount
        return None