from uuid import UUID

from pydantic import BaseModel, EmailStr



class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

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
    post_title: str
    post_content: str