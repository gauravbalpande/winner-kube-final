# from datetime import datetime, timedelta
# from typing import Optional
# from jose import JWTError, jwt
# from passlib.context import CryptContext
# from fastapi import HTTPException, status, Depends
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from core.config import settings

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# security = HTTPBearer()

# def hash_password(password: str) -> str:
#     """Hash a password using bcrypt"""
#     return pwd_context.hash(password)

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     """Verify a password against its hash"""
#     return pwd_context.verify(plain_password, hashed_password)

# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
#     """Create a JWT access token"""
#     to_encode = data.copy()
    
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
#     return encoded_jwt

# def decode_token(token: str) -> dict:
#     """Decode and validate JWT token"""
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         return payload
#     except JWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

# async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
#     """Dependency to get current authenticated user"""
#     token = credentials.credentials
#     payload = decode_token(token)
    
#     user_id = payload.get("sub")
#     if user_id is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials"
#         )
    
#     return {"user_id": user_id, "username": payload.get("username")}

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.config import settings

# Initialize password context with bcrypt
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # Explicitly set rounds
)
security = HTTPBearer()

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt
    Bcrypt has a 72 byte limit - this function handles it safely
    """
    try:
        # Convert to string if not already
        password = str(password).strip()
        
        # Bcrypt automatically handles the 72 byte limit internally
        # but we'll be explicit about it
        if len(password) > 72:
            password = password[:72]
        
        return pwd_context.hash(password)
    except Exception as e:
        print(f"Error hashing password: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing password"
        )

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash
    """
    try:
        # Convert to string and strip whitespace
        plain_password = str(plain_password).strip()
        
        # Apply same 72 byte limit as hashing
        if len(plain_password) > 72:
            plain_password = plain_password[:72]
        
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(f"Error verifying password: {e}")
        return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def decode_token(token: str) -> dict:
    """Decode and validate JWT token"""
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError as e:
        print(f"JWT decode error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """Dependency to get current authenticated user"""
    token = credentials.credentials
    payload = decode_token(token)
    
    user_id = payload.get("sub")
    username = payload.get("username")
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    return {
        "user_id": user_id,
        "username": username
    }


# ===================================================================
# DEBUGGING HELPER FUNCTION (Remove in production)
# ===================================================================
def test_password_hash():
    """Test function to verify password hashing works"""
    test_passwords = [
        "hello123",
        "testpass123",
        "short",
        "a" * 100  # Test with long password
    ]
    
    print("\n=== Password Hash Testing ===")
    for pwd in test_passwords:
        try:
            hashed = hash_password(pwd)
            verified = verify_password(pwd, hashed)
            print(f"✓ Password '{pwd[:20]}...' - Length: {len(pwd)} - Verified: {verified}")
        except Exception as e:
            print(f"✗ Password '{pwd[:20]}...' - Error: {e}")
    print("=== Testing Complete ===\n")

# Uncomment to test when backend starts
# test_password_hash()