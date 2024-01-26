from pydantic import BaseModel, validator
from typing import Optional
import bcrypt
salt_rounds = 12

class UserModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    deleted: bool = False
    role: str = 'user'

    @validator("password")
    def hash_password(cls, value):
        return bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt(salt_rounds)).decode('utf-8')
    
    @validator("email")
    def convert_email_to_lowercase(cls, value):
        return value.lower()

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "Yazeed",
                "last_name": "Ali",
                "email": "Yazeed@gmail.com",
                "password": "yazeed@12",
                "deleted": False,
                "role": "user"
            }
        }

class UpdateUserModel(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    
class UserLogin(BaseModel):
    email: str
    password: str

class TokenModel(BaseModel):
    token: str