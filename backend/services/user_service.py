from typing import Optional
from supabase_client.supabase_client import get_supabase_client

class UserService:
    def __init__(self):
        self.supabase = get_supabase_client()
    
    async def get_user_balance(self, user_id: str) -> Optional[float]:
        """Get user's wallet balance"""
        try:
            result = self.supabase.table('wallets').select('balance').eq('user_id', user_id).execute()
            
            if result.data:
                return result.data[0]['balance']
            return None
            
        except Exception as e:
            print(f"Error fetching balance: {e}")
            return None
    
    async def update_user_balance(self, user_id: str, new_balance: float) -> bool:
        """Update user's wallet balance"""
        try:
            result = self.supabase.table('wallets').update({'balance': new_balance}).eq('user_id', user_id).execute()
            
            return bool(result.data)
            
        except Exception as e:
            print(f"Error updating balance: {e}")
            return False

user_service = UserService()