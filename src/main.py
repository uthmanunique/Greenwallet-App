from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from src.routes.user_routes import router as user_router

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="GreenWallet API",
    description="API for GreenWallet fintech app",
    version="1.0.0"
)

# Allow frontend to access API (CORS settings)
origins = [
    "http://192.168.43.78:5000",  # ✅ Corrected IP format
    "http://localhost:5000",      # ✅ Added missing comma
    "http://127.0.0.1:5000",      # ✅ Added 127.0.0.1 (important for local testing)
    "http://105.119.11.30:5000", # 
    os.getenv("FRONTEND_URL", ""), # ✅ Dynamic origin from .env
    "*"                           # ✅ Allow all origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin for origin in origins if origin],  # ✅ Filter out empty values
    allow_credentials=True,
    allow_methods=["*"],  # ✅ Allow all HTTP methods
    allow_headers=["*"],  # ✅ Allow all headers
)

# Include API routes
app.include_router(user_router, prefix="/api/users")

# Root endpoint (Health check)
@app.get("/")
async def root():
    return {"message": "GreenWallet API is running"}
