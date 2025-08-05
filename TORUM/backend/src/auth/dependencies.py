from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import JWTError
from typing import List

from backend.src.database import get_db
from backend.src.auth.models import User
from backend.src.auth.exceptions import CredentialException, InvalidUser, PermissionException
from backend.src.auth.services import decode_token
from backend.src.auth.schemas import UserResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(token: str = Depends(oauth2_scheme), 
                           db: AsyncSession = Depends(get_db)):
    try:
        payload = decode_token(token)
        email: str = payload.get("sub")
        if not email:
            raise CredentialException()
    except JWTError:
        raise CredentialException()
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        raise InvalidUser()
    return user

def require_role(required_roles: List[str]):
    async def role_checker(current_user: UserResponse = Depends(get_current_user)):
        if current_user.user_role not in required_roles:
            raise PermissionException()
        return current_user
    return role_checker