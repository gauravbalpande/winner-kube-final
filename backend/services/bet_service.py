import random
from typing import Optional, Dict
from datetime import datetime
from models.bet import BetCreate
from services.user_service import user_service
from supabase_client.supabase_client import get_supabase_client

class BetService:
    def __init__(self):
        self.supabase = get_supabase_client()
        self.win_multiplier = 2.0  # 2x payout for winning bets
    
    async def place_horse_bet(self, user_id: str, bet_data: BetCreate) -> Optional[Dict]:
        """Process a horse race bet"""
        try:
            # Get current balance
            current_balance = await user_service.get_user_balance(user_id)
            
            if current_balance is None:
                return None
            
            if current_balance < bet_data.bet_amount:
                return {"error": "Insufficient balance"}
            
            # Randomly determine winning horse (1-4)
            winning_horse = random.randint(1, 4)
            
            # Determine result
            is_winner = bet_data.horse_choice == winning_horse
            result = "win" if is_winner else "loss"
            
            # Calculate new balance and winnings
            if is_winner:
                winnings = bet_data.bet_amount * self.win_multiplier
                new_balance = current_balance + winnings
            else:
                winnings = 0
                new_balance = current_balance - bet_data.bet_amount
            
            # Update balance
            balance_updated = await user_service.update_user_balance(user_id, new_balance)
            
            if not balance_updated:
                return {"error": "Failed to update balance"}
            
            # Record bet in database
            bet_record = {
                "user_id": user_id,
                "horse_choice": bet_data.horse_choice,
                "bet_amount": bet_data.bet_amount,
                "winning_horse": winning_horse,
                "result": result,
                "winnings": winnings,
                "created_at": datetime.utcnow().isoformat()
            }
            
            insert_result = self.supabase.table('bets').insert(bet_record).execute()
            
            if not insert_result.data:
                return {"error": "Failed to record bet"}
            
            bet_id = insert_result.data[0]['id']
            
            return {
                "id": bet_id,
                "user_id": user_id,
                "horse_choice": bet_data.horse_choice,
                "bet_amount": bet_data.bet_amount,
                "winning_horse": winning_horse,
                "result": result,
                "winnings": winnings,
                "new_balance": new_balance,
                "created_at": bet_record["created_at"]
            }
            
        except Exception as e:
            print(f"Bet processing error: {e}")
            return {"error": str(e)}

bet_service = BetService()