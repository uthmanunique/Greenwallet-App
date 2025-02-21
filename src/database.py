# src/database.py
from motor.motor_asyncio import AsyncIOMotorClient
import os

# MongoDB URI from environment variables (make sure .env is properly configured or hardcode)
MONGO_URI = "mongodb+srv://uthmanunique:0Z3OgarH9fcPbsKy@greenwallet.zvuzd.mongodb.net/"

client = AsyncIOMotorClient(MONGO_URI)
db = client["greenwallet_db"]

# Export the 'users' collection to be used in services
users_collection = db["users"]  # This defines the collection name 'users'

# Define the invoices collection:
invoices_collection = db.invoices
