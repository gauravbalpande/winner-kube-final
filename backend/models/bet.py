from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BetCreate(BaseModel):
    horse_choice: int
    bet_amount: float

class BetResponse(BaseModel):
    id: str
    user_id: str
    horse_choice: int
    bet_amount: float
    winning_horse: int
    result: str  # 'win' or 'loss'
    winnings: float
    new_balance: float
    created_at: datetime