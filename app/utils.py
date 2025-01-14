from fastapi import HTTPException,Depends
from app.models import User
from app.auth import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.database import get_db


# Utility function to validate and decode JWT token
def get_current_user(token: str, db: Session = Depends(get_db)):
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        # If no username in the token, raise an error
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication")

        # Fetch the user from the database
        user = db.query(User).filter(User.username == username).first()

        # If user is not found, raise an error
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate token")


# Admin access control function
def admin_required(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")


# User access control function (can be used for both regular users and admins)
def user_required(user: User = Depends(get_current_user)):
    if user.role != "user" and user.role != "admin":
        raise HTTPException(status_code=403, detail="User access required")

