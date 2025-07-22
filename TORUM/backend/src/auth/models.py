import uuid

from sqlalchemy import Column, String, Integer, Boolean, Text, UUID, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from ..database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    user_role = Column(String, default="trader")

    post = relationship("Post", back_populates="owner")
    refresh = relationship("Refresh_Token", back_populates="curr_user")

class Post(Base):
    __tablename__ = "posts"

    post_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    post_owner = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    post_title = Column(String, nullable=False)
    post_content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    owner = relationship("User", back_populates="post")

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