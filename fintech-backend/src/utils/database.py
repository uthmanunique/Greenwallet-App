from pymongo import MongoClient
from bson.objectid import ObjectId
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "fintech_db")

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

def get_collection(collection_name):
    return db[collection_name]

def close_connection():
    client.close()