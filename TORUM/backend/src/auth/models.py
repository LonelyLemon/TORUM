import uuid
import os

from sqlalchemy import Column, String, Integer, Boolean, Text, UUID, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, validates

from backend.src.database import Base

####     USER TABLE      ####

class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    user_role = Column(String, default="user")

    post = relationship("Post", back_populates="owner")
    docs = relationship("Reading_Documents", back_populates="documents_owner")
    refresh = relationship("Refresh_Token", back_populates="curr_user")

    @validates('user_role')
    def validate_role(self, key, value):
        valid_roles = {"user", "moderator", "admin"}
        if value not in valid_roles:
            raise ValueError(f"Invalid Role !")
        return value
####    END USER TABLE      ####

#---------------------------------------------------------------#

####     POST TABLE      ####

class Post(Base):
    __tablename__ = "posts"

    post_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    post_owner = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    post_title = Column(String, nullable=False)
    post_content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    owner = relationship("User", back_populates="post")

####     END POST TABLE      ####

#---------------------------------------------------------------#

####     READING DOCUMENTS TABLE      ####

class Reading_Documents(Base):
    __tablename__ = "reading_documents"

    docs_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    docs_owner = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    docs_title = Column(String, nullable=False)
    docs_description = Column(Text)
    docs_tags = Column(String, default="Documents")
    docs_file_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    documents_owner = relationship("User", back_populates="docs")

    @validates('docs_file_path')
    def validate_file_extension(self, key, docs_file_path):
        allowed_extension = {'.pdf', '.docx'}
        ext = os.path.splitext(docs_file_path)[1].lower()
        if ext not in allowed_extension:
            raise ValueError("Only .pdf and .docx files are allowed !")
        return docs_file_path

####     END READING DOCUMENTS TABLE      ####

#---------------------------------------------------------------#

####     TOKEN TABLE     ####

class Token_Blacklist(Base):
    __tablename__ = "token_blacklist"

    token_id = Column(Integer, primary_key=True)
    token = Column(Text, nullable=False, unique=True)
    is_blacklisted = Column(Boolean, default=True)

class Refresh_Token(Base):
    __tablename__ = "refresh_token"

    refresh_token_id = Column(Integer, primary_key=True)
    refresh_token = Column(Text, nullable=False, unique=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    is_expired = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    curr_user = relationship("User", back_populates="refresh")

####     END TOKEN TABLE      ####

#---------------------------------------------------------------#