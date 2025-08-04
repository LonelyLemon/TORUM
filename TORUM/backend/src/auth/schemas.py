from uuid import UUID
from fastapi import Form
from datetime import datetime
from typing import Optional, Annotated
from pydantic import BaseModel, EmailStr, StringConstraints



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
    user_role: str

    class Config:
        from_attributes = True

class PostCreate(BaseModel):
    post_title: str
    post_content: str

class PostUpdate(BaseModel):
    post_title: Optional[str] = None
    post_content: Optional[str] = None

class Reading_Documents_Response(BaseModel):
    docs_id: UUID
    docs_owner: UUID
    docs_title: str
    docs_description: Optional[str] = None
    docs_tags: str
    docs_file_path: str
    uploaded_at: datetime

    class Config:
        from_attributes = True