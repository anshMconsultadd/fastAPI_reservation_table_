from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import LoginSchema, Token

SECRET_KEY = "harvey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=30)  # timedelta object
    data["exp"] = expire  # `timedelta` is not JSON serializable
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


router = APIRouter()

@router.post("/token", response_model=Token)
def login(login_data: LoginSchema, db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.username == login_data.username).first()

    
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    
    access_token = create_access_token(data={"sub": user.username})

    
    return {"access_token": access_token, "token_type": "bearer"}