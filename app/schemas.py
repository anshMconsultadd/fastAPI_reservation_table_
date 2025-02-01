
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str


class RegiterUser(UserCreate):
    role: str
    
class TableCreate(BaseModel):
    capacity: int

class TableUpdate(BaseModel):
    capacity: int
    is_reserved: bool

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginSchema(BaseModel):
    username: str
    password: str