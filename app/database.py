from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:consultadd@localhost:3306/hotel_table_booking"

# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:consultadd@host.docker.internal:3306/hotel_table_booking"
import os

# Check if running inside Docker (by checking for an environment variable)
IS_DOCKER = os.getenv("IS_DOCKER", "false").lower() == "true"

if IS_DOCKER:
    SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:consultadd@host.docker.internal:3306/hotel_table_booking"
else:
    SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:consultadd@localhost:3306/hotel_table_booking"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)  
    password = Column(String(255))  
    role = Column(String(50), default="user")  


class Table(Base):
    __tablename__ = "tables"
    id = Column(Integer, primary_key=True, index=True)
    capacity = Column(Integer)
    is_reserved = Column(Boolean, default=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)
