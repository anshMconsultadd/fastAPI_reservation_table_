from fastapi.testclient import TestClient
from main import app
from app.models import User
from app.auth import get_password_hash
from app.database import SessionLocal, engine, Base
from sqlalchemy.orm import Session
import pytest



@pytest.fixture(scope="module")
def db():
    
    Base.metadata.create_all(bind=engine)
    db_session = SessionLocal()
    yield db_session
    db_session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def create_user(db: Session):
    
    user_data = User(username="testuser", password=get_password_hash("password123"), role="user")
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return user_data


@pytest.fixture()
def create_admin(db: Session):
  
    admin_data = User(username="admin", password=get_password_hash("password123"), role="admin")
    db.add(admin_data)
    db.commit()
    db.refresh(admin_data)
    return admin_data



client = TestClient(app)



def test_login_for_access_token(db, create_user):
    
    response = client.post(
        "/token", 
        data={"username": "testuser", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"



def test_view_available_tables(db, create_user):
 
    response = client.post(
        "/token", 
        data={"username": "testuser", "password": "password123"}
    )
    access_token = response.json()["access_token"]

    
    response = client.get(
        "/user/tables", 
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    
    assert isinstance(response.json(), list)

