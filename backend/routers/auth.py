from fastapi import APIRouter, HTTPException, status
from models.user import UserCreate, UserLogin
from services.auth_service import auth_service

router = APIRouter()

@router.post("/register")
async def register(user_data: UserCreate):
    """Register a new user"""
    user, error = await auth_service.register_user(user_data)
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    
    return {
        "message": "User registered successfully",
        "user": user
    }

@router.post("/login")
async def login(login_data: UserLogin):
    """Authenticate user and return access token"""
    user, token, error = await auth_service.authenticate_user(login_data)
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error
        )
    
    return {
        "message": "Login successful",
        "user": user,
        "token": token,
        "token_type": "bearer"
    }