# src/config.py
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")  # This will load from .env
    ALGORITHM = os.getenv("ALGORITHM", "HS256")