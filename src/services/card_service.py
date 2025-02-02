from pymongo import MongoClient
from bson import ObjectId
from src.utils.flutterwave import FlutterwaveAPI

class CardService:
    def __init__(self, db_uri: str, db_name: str):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]
        self.flutterwave_api = FlutterwaveAPI()

    def create_card(self, user_id: str, card_data: dict):
        card_data['user_id'] = ObjectId(user_id)
        card = self.db.cards.insert_one(card_data)
        return str(card.inserted_id)

    def list_cards(self, user_id: str):
        return list(self.db.cards.find({"user_id": ObjectId(user_id)}))

    def fund_card(self, card_id: str, amount: float):
        card = self.db.cards.find_one({"_id": ObjectId(card_id)})
        if card:
            # Integrate with Flutterwave API to fund the card
            response = self.flutterwave_api.fund_card(card_id, amount)
            return response
        return None

    def delete_card(self, card_id: str):
        result = self.db.cards.delete_one({"_id": ObjectId(card_id)})
        return result.deleted_count > 0