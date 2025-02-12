# from dotenv import load_dotenv
# import os

# load_dotenv()  # ✅ Load environment variables before anything else!
# # ✅ Print for debugging
# print(f"DEBUG: EMAIL_ADDRESS = {os.getenv('EMAIL_ADDRESS')}")
# print(f"DEBUG: EMAIL_PASSWORD = {os.getenv('EMAIL_PASSWORD')}")


# from fastapi import FastAPI, Depends, HTTPException, Form
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from src.routes.user_routes import router as user_router
# from src.services.user_service import UserService

# app = FastAPI()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# user_service = UserService()

# @app.post("/token")
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = {"email": form_data.username, "password": form_data.password}
#     response = user_service.login_user(user)

#     if isinstance(response, dict) and "access_token" not in response:
#         raise HTTPException(status_code=400, detail="Invalid email or password")
    
#     return response

# app.include_router(user_router, prefix="/api/users")

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the API"}

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
origins = ["192.168.43.78:5000"
            # You can add additional origins as needed:
            # "http://localhost:3000",
            # "https://your-frontend-domain.com"
]           # Change this to specific domains in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(user_router, prefix="/api/users")

# Root endpoint (Health check)
@app.get("/")
async def root():
    return {"message": "GreenWallet API is running"}
