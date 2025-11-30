import httpx
from typing import Optional, Dict, Any
from core.config import settings

class MCPClient:
    """
    MCP (Model Context Protocol) Client for handling database operations
    through the MCP server layer
    """
    
    def __init__(self):
        self.base_url = settings.MCP_SERVER_URL
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def close(self):
        await self.client.aclose()
    
    async def authenticate_user(self, username: str, password_hash: str) -> Optional[Dict[str, Any]]:
        """Authenticate user through MCP"""
        try:
            response = await self.client.post(
                f"{self.base_url}/mcp/auth",
                json={"username": username, "password_hash": password_hash}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"MCP authentication error: {e}")
            return None
    
    async def get_user_balance(self, user_id: str) -> Optional[float]:
        """Get user wallet balance through MCP"""
        try:
            response = await self.client.get(
                f"{self.base_url}/mcp/balance/{user_id}"
            )
            response.raise_for_status()
            data = response.json()
            return data.get("balance")
        except Exception as e:
            print(f"MCP balance fetch error: {e}")
            return None
    
    async def update_balance(self, user_id: str, new_balance: float) -> bool:
        """Update user wallet balance through MCP"""
        try:
            response = await self.client.put(
                f"{self.base_url}/mcp/balance/{user_id}",
                json={"balance": new_balance}
            )
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"MCP balance update error: {e}")
            return False
    
    async def create_bet_record(self, bet_data: Dict[str, Any]) -> Optional[str]:
        """Create bet record through MCP"""
        try:
            response = await self.client.post(
                f"{self.base_url}/mcp/bets",
                json=bet_data
            )
            response.raise_for_status()
            data = response.json()
            return data.get("bet_id")
        except Exception as e:
            print(f"MCP bet creation error: {e}")
            return None

# Global MCP client instance
mcp_client = MCPClient()