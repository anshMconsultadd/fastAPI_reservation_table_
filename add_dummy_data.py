from app.database import Base, engine, SessionLocal
from app.models import User, Table
from app.auth import get_password_hash

db = SessionLocal()

try:
    
    db.add_all([
        User(username="admin", password=get_password_hash("password123"), role="admin"),
        User(username="user", password=get_password_hash("password123"), role="user"),
    ])
    db.commit()
    print("Dummy data added successfully!")
except Exception as e:
    db.rollback()
    print(f"Error adding dummy data: {e}")
finally:
    db.close()


Base.metadata.create_all(bind=engine)