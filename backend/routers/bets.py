from fastapi import APIRouter, Depends, HTTPException, status
from models.bet import BetCreate
from core.security import get_current_user
from services.bet_service import bet_service

router = APIRouter()

@router.post("/horse")
async def place_horse_bet(bet_data: BetCreate, current_user: dict = Depends(get_current_user)):
    """Place a bet on horse race"""
    user_id = current_user["user_id"]
    
    # Validate bet amount
    if bet_data.bet_amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bet amount must be greater than 0"
        )
    
    # Validate horse choice (1-4)
    if bet_data.horse_choice not in [1, 2, 3, 4]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid horse choice. Must be between 1 and 4"
        )
    
    result = await bet_service.place_horse_bet(user_id, bet_data)
    
    if result is None or "error" in result:
        error_message = result.get("error", "Failed to place bet") if result else "Failed to place bet"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message
        )
    
    return result