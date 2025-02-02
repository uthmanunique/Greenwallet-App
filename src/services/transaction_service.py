from pymongo import MongoClient
from bson import ObjectId
from src.models.transaction_model import Transaction

class TransactionService:
    def __init__(self, db_url: str, db_name: str):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db['transactions']

    def create_transaction(self, transaction_data):
        transaction = Transaction(**transaction_data)
        result = self.collection.insert_one(transaction.dict())
        return str(result.inserted_id)

    def get_transaction_by_id(self, transaction_id: str):
        transaction = self.collection.find_one({"_id": ObjectId(transaction_id)})
        return Transaction(**transaction) if transaction else None

    def get_all_transactions(self, user_id: str):
        transactions = self.collection.find({"user_id": user_id})
        return [Transaction(**transaction) for transaction in transactions]

    def update_transaction(self, transaction_id: str, update_data):
        self.collection.update_one({"_id": ObjectId(transaction_id)}, {"$set": update_data})

    def delete_transaction(self, transaction_id: str):
        self.collection.delete_one({"_id": ObjectId(transaction_id)})