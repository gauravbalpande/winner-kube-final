from fastapi import APIRouter, Depends
from core.security import get_current_user

router = APIRouter()

@router.get("/status")
async def payment_status(current_user: dict = Depends(get_current_user)):
    """Get payment gateway status"""
    # TODO: Integrate real payment gateway here in future
    # Possible integrations: Stripe, PayPal, Razorpay, etc.
    
    return {
        "status": "coming_soon",
        "message": "Payment Gateway Integration Coming Soon",
        "supported_methods": [],
        "note": "This endpoint will support deposits and withdrawals in future releases"
    }

@router.post("/deposit")
async def deposit(current_user: dict = Depends(get_current_user)):
    """Deposit funds (placeholder)"""
    # TODO: Implement payment gateway deposit logic
    return {
        "status": "not_implemented",
        "message": "Deposit functionality will be available soon"
    }

@router.post("/withdraw")
async def withdraw(current_user: dict = Depends(get_current_user)):
    """Withdraw funds (placeholder)"""
    # TODO: Implement payment gateway withdrawal logic
    return {
        "status": "not_implemented",
        "message": "Withdrawal functionality will be available soon"
    }