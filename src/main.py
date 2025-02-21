# src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from src.routes.card_routes import router as card_router  # New import from card_routes.py file

from src.routes.user_routes import router as user_router
from src.routes.invoice_routes import router as invoice_router  # New import

load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="GreenWallet API",
    description="API for GreenWallet fintech app",
    version="1.0.0"
)

# For development, you might allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from any domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(user_router, prefix="/api/users")
app.include_router(invoice_router, prefix="/api/invoice")
app.include_router(card_router, prefix="/api/cards")

# Root endpoint (Health check)
@app.get("/")
async def root():
    return {"message": "GreenWallet API is running"}
