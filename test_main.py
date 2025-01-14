from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
from app.models import User, Table  
from app.auth import get_password_hash
from main import app  
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
 # In-memory SQLite database for testing

# Create the engine and session local for the test database
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the test client
client = TestClient(app)

# Override the get_db dependency to use the test database
def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Setup function to create tables and insert test data
def setup_module(module):
    # Create all tables before tests run
    Base.metadata.create_all(bind=engine)

    # Insert test users and tables into the database
    db = TestSessionLocal()
    test_user = User(username="admin", password=get_password_hash("password123"), role="admin")
    db.add(test_user)
    
    test_table = Table(capacity=4, is_reserved=False)
    db.add(test_table)

    db.commit()
    db.close()

# Drop the tables after the tests to clean up
def teardown_module(module):
    # Drop all tables after tests are done
    Base.metadata.drop_all(bind=engine)

# Example test case: Checking the root route
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

# Test case for login route
def test_login_route():
    # Define login credentials (plaintext password)
    data = {"username": "admin", "password": "password123"}

    # Send POST request with JSON payload
    response = client.post("/token", json=data)

    # Validate the response
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert "access_token" in response.json(), "Access token not found"
    assert response.json()["token_type"] == "bearer"
