from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import JWTError
from typing import List

from backend.src.database import get_db
from backend.src.auth.models import Token_Blacklist, User
from backend.src.auth.exceptions import CredentialException, InvalidUser, BlacklistedToken, PermissionException
from backend.src.auth.services import decode_access_token
from backend.src.auth.schemas import UserResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(token: str = Depends(oauth2_scheme), 
                           db: AsyncSession = Depends(get_db)) -> str:
    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        if not email:
            raise CredentialException()
    except JWTError:
        raise CredentialException()
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    blacklisted_result = await db.execute(select(Token_Blacklist).where(Token_Blacklist.token == token))
    blacklisted = blacklisted_result.scalars().first()
    if not user:
        raise InvalidUser()
    if blacklisted:
        raise BlacklistedToken()
    return user

async def require_role(required_roles: List[str]):
    async def role_checker(current_user: UserResponse = Depends(get_current_user)):
        if current_user.user_role not in required_roles:
            raise PermissionException()
        return current_user
    return role_checker