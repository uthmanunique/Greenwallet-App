# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from src.routes.user_routes import router as user_router
# from src.routes.wallet_routes import router as wallet_router
# from src.routes.transaction_routes import router as transaction_router
# from src.routes.card_routes import router as card_router

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(user_router, prefix="/api/users", tags=["users"])
# app.include_router(wallet_router, prefix="/api/wallet", tags=["wallet"])
# app.include_router(transaction_router, prefix="/api/transactions", tags=["transactions"])
# app.include_router(card_router, prefix="/api/cards", tags=["cards"])

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the Green Wallet API"}


# filepath: /c:/Users/Baloun Uthman/Desktop/Greenwallet-backend/src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.user_routes import router as user_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/api/users", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Green Wallet API"}