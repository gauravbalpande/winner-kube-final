from supabase import create_client, Client
from core.config import settings
import os

def get_supabase_client() -> Client:
    """Initialize and return Supabase client"""
    supabase_url = os.getenv("SUPABASE_URL") or settings.SUPABASE_URL
    supabase_key = os.getenv("SUPABASE_KEY") or settings.SUPABASE_KEY
    
    if not supabase_url or not supabase_key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
    
    try:
        return create_client(supabase_url, supabase_key)
    except Exception as e:
        print(f"Error creating Supabase client: {e}")
        print(f"Supabase URL: {supabase_url[:30]}..." if supabase_url else "Supabase URL: Not set")
        raise

def get_supabase_admin_client() -> Client:
    """Initialize and return Supabase admin client with service key"""
    supabase_url = os.getenv("SUPABASE_URL") or settings.SUPABASE_URL
    supabase_service_key = os.getenv("SUPABASE_SERVICE_KEY") or settings.SUPABASE_SERVICE_KEY
    
    if not supabase_url or not supabase_service_key:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in environment variables")
    
    try:
        return create_client(supabase_url, supabase_service_key)
    except Exception as e:
        print(f"Error creating Supabase admin client: {e}")
        print(f"Supabase URL: {supabase_url[:30]}..." if supabase_url else "Supabase URL: Not set")
        raise