from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timezone, timedelta

from backend.src.auth.config import JWT_ALGORITHM, JWT_EXPIRATION_HOURS, JWT_SECRET_KEY, REFRESH_TOKEN_HOURS


pwd_context = CryptContext(schemes="bcrypt", deprecated="auto")


# Password Hashing/Verification
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
# End Password Hashing/Verification


# JWT Token
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRATION_HOURS)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=REFRESH_TOKEN_HOURS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> str:
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
# End JWT Token