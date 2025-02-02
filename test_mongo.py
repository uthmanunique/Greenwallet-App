# filepath: /c:/Users/Baloun Uthman/Desktop/Greenwallet-backend/test_mongo.py
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

MONGO_URI = "mongodb+srv://uthmanunique:0Z3OgarH9fcPbsKy@greenwallet.zvuzd.mongodb.net/?retryWrites=true&w=majority&tls=true&tlsInsecure=true"


try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client["greenwallet_db"]
    # Attempt to retrieve server information to trigger a connection error if the connection fails
    client.server_info()
    print("Connected to MongoDB")
    # Perform a basic operation
    db.users.insert_one({"test": "data"})
    print("Inserted test data")
except ServerSelectionTimeoutError as e:
    print(f"Error connecting to MongoDB: {e}")