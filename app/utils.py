from fastapi import HTTPException, Depends
from jose import jwt, JWTError
from app.models import User
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi import status
from app.config import SECRET_KEY, ALGORITHM
from app.auth import oauth2_scheme

# Utility function to validate and decode JWT token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception


# Admin access control function
def admin_required(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")


# User access control function
def user_required(user: User = Depends(get_current_user)):
    if user.role != "user" and user.role != "admin":
        raise HTTPException(status_code=403, detail="User access required")
