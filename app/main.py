from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select
from jose import jwt
from jose.exceptions import JWTError
import uvicorn
import logging
import json
from datetime import datetime, timedelta

from app.config import settings
from app.routes import root, data, users
from app.database import get_db

# Import auth functions from dedicated modules (avoiding circular imports)
from app.auth.jwt import create_access_token
from app.auth.deps import oauth2_scheme
from app.auth.service import authenticate_user, get_user_by_username
from app.auth.rate_limiter import rate_limiter

# Constants (previously missing)
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Configure logging with JSON formatter
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
)

# Configure JSON logging
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module
        }
        return json.dumps(log_record)

# Setup logging
logger = logging.getLogger("fastapi_app")
logger.setLevel(settings.LOG_LEVEL)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)

app = FastAPI(
    title="FastAPI MVP Backend",
    description="A production-ready FastAPI backend with JWT auth and PostgreSQL",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.utcnow()
    response = await call_next(request)
    duration = (datetime.utcnow() - start_time).total_seconds()
    
    logger.info(
        f"Request: {request.method} {request.url.path} Duration: {duration}s Status: {response.status_code}"
    )
    return response

# Rate limiter for token endpoints
@app.middleware("http")
async def rate_limit_token_endpoints(request: Request, call_next):
    if request.url.path in ["/token", "/refresh-token"]:
        await rate_limiter.check_rate_limit(request)
    response = await call_next(request)
    return response

# Token endpoints
@app.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token (user is now a dict, not object)
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"], "token_type": "access"},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    # Create refresh token
    refresh_token = create_access_token(
        data={"sub": user["username"], "role": user["role"], "token_type": "refresh"},
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@app.post("/refresh-token")
async def refresh_token(
    current_token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    try:
        # Decode the token
        payload = jwt.decode(current_token, settings.JWT_SECRET, algorithms=["HS256"])
        username: str = payload.get("sub")
        token_type: str = payload.get("token_type")
        
        # Verify it's a refresh token
        if token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token type"
            )
        
        # Get the user (now returns dict)
        user = await get_user_by_username(username, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        # Create new access token
        new_access_token = create_access_token(
            data={"sub": user["username"], "role": user["role"], "token_type": "access"},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate refresh token"
        )

# Health check endpoint
@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        # Test database connection
        await db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as e:
        db_status = "error"
    
    return {
        "status": "ok",
        "database": db_status,
        "version": "1.0.0"
    }

# Include routers
app.include_router(root.router)
app.include_router(data.router)
app.include_router(users.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
