import uuid

from sqlalchemy import Column, String, Integer, Boolean, Text, UUID

from ..database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    user_role = Column(String, default="trader")

class Token_Blacklist(Base):
    __tablename__ = "token_blacklist"

    token_id = Column(Integer, primary_key=True)
    token = Column(Text, nullable=False, unique=True)
    is_blacklisted = Column(Boolean, default=True)