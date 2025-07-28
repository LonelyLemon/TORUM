from uuid import UUID
from typing import Optional
from pydantic import BaseModel, EmailStr



class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    user_id: UUID
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

class PostCreate(BaseModel):
    post_title: str
    post_content: str

class PostUpdate(BaseModel):
    post_title: Optional[str] = None
    post_content: Optional[str] = None