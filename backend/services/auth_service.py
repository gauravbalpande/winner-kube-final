from typing import Optional, Tuple
from models.user import UserCreate, UserLogin
from core.security import hash_password, verify_password, create_access_token
from supabase_client.supabase_client import get_supabase_admin_client
from datetime import datetime

class AuthService:
    def __init__(self):
        self.supabase = get_supabase_admin_client()
    
    async def register_user(self, user_data: UserCreate) -> Tuple[Optional[dict], Optional[str]]:
        """Register a new user"""
        try:
            # Check if user already exists
            existing = self.supabase.table('users').select('*').eq('username', user_data.username).execute()
            
            if existing.data:
                return None, "Username already exists"
            
            # Check if email already exists
            existing_email = self.supabase.table('users').select('*').eq('email', user_data.email).execute()
            
            if existing_email.data:
                return None, "Email already registered"
            
            # Hash password
            hashed_password = hash_password(user_data.password)
            
            # Create user
            user_insert = {
                "username": user_data.username,
                "email": user_data.email,
                "password_hash": hashed_password,
                "created_at": datetime.utcnow().isoformat()
            }
            
            result = self.supabase.table('users').insert(user_insert).execute()
            
            if not result.data:
                return None, "Failed to create user"
            
            user = result.data[0]
            
            # Create wallet with initial balance
            wallet_insert = {
                "user_id": user['id'],
                "balance": 1000.0  # Initial balance
            }
            
            self.supabase.table('wallets').insert(wallet_insert).execute()
            
            return user, None
            
        except Exception as e:
            print(f"Registration error: {e}")
            return None, str(e)
    
    async def authenticate_user(self, login_data: UserLogin) -> Tuple[Optional[dict], Optional[str], Optional[str]]:
        """Authenticate user and return user data with token"""
        try:
            # Fetch user from database
            result = self.supabase.table('users').select('*').eq('username', login_data.username).execute()
            
            if not result.data:
                return None, None, "Invalid username or password"
            
            user = result.data[0]
            
            # Verify password
            if not verify_password(login_data.password, user['password_hash']):
                return None, None, "Invalid username or password"
            
            # Create access token
            token_data = {
                "sub": user['id'],
                "username": user['username']
            }
            access_token = create_access_token(token_data)
            
            # Remove sensitive data
            user_response = {
                "id": user['id'],
                "username": user['username'],
                "email": user['email']
            }
            
            return user_response, access_token, None
            
        except Exception as e:
            print(f"Authentication error: {e}")
            return None, None, str(e)

auth_service = AuthService()