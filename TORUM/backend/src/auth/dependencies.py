from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import JWTError

from database import get_db
from .models import Token_Blacklist, User
from .exceptions import CredentialException, InvalidUser, BlacklistedToken
from .services import decode_access_token

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