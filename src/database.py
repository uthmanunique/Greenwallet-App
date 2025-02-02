# filepath: /c:/Users/Baloun Uthman/Desktop/Greenwallet-backend/src/database.py
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

MONGO_URI = "mongodb+srv://uthmanunique:0Z3OgarH9fcPbsKy@greenwallet.zvuzd.mongodb.net/"

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client["greenwallet_db"]
    # Attempt to retrieve server information to trigger a connection error if the connection fails
    client.server_info()
    print("Connected to MongoDB")
except ServerSelectionTimeoutError as e:
    print(f"Error connecting to MongoDB: {e}")