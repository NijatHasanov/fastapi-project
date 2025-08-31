from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from jose import jwt
from app.config import settings

ALGORITHM = "HS256"

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token with expiration.
    """
    to_encode = data.copy()
    if expires_delta is None:
        expires_delta = timedelta(minutes=60)
    
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=ALGORITHM)

def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Decode and return the JWT payload. Raises JWTError on invalid/expired token.
    """
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[ALGORITHM])