from fastapi import APIRouter, Depends, HTTPException, status
from core.security import get_current_user
from services.user_service import user_service

router = APIRouter()

@router.get("/balance")
async def get_balance(current_user: dict = Depends(get_current_user)):
    """Get current user's wallet balance"""
    user_id = current_user["user_id"]
    
    balance = await user_service.get_user_balance(user_id)
    
    if balance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        )
    
    return {
        "user_id": user_id,
        "balance": balance
    }
