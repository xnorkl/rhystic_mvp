from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from pydantic.networks import EmailStr
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
import os

from rhystic.database import get_db
from rhystic.api.models.user import User

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRegistration(BaseModel):
    username: str
    password: str
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/register", status_code=201)
async def register_user(user: UserRegistration, db: Session = Depends(get_db)):
    # Check if username already exists
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Create new user
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"id": db_user.id, "username": db_user.username}

@router.post("/token")
async def login_for_token(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Find user
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate JWT token here
    token = jwt.encode(
        {
            "sub": str(user.id),  # Convert UUID to string
            "exp": datetime.now(tz=timezone.utc) + timedelta(hours=1)
        },
        os.getenv("JWT_SECRET_KEY"),
        algorithm="HS256"
    )
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": 3600
    } 