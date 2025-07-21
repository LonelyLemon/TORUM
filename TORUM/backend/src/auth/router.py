from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import get_db
from exceptions import UserExistedCheck, InvalidPassword, InvalidUser
from models import User, Token_Blacklist
from schemas import UserCreate, UserResponse
from services import get_password_hash, verify_password, create_access_token
from dependencies import get_current_user, oauth2_scheme


####     REGISTER ROUTE     #####
register_route = APIRouter(
    tags=["Register"]
)

@register_route.post('/register', response_model=UserResponse)
async def register(user: UserCreate, 
                   db: AsyncSession = Depends(get_db)):
    existed_user = await db.execute(select(User).where((User.email == user.email)))
    if existed_user.scalars().first():
        raise UserExistedCheck()
    hashed_pw = get_password_hash(user.password)
    new_user = User(
        username = user.username,
        email = user.email,
        password = hashed_pw
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
####     END REGISTER ROUTE     #####



####     LOGIN ROUTE     #####
login_route = APIRouter(
    tags=["Login"]
)

@login_route.post('/login')
async def login(login_request: OAuth2PasswordRequestForm = Depends(), 
                db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == login_request.username))
    user = result.scalars().first()
    if not verify_password(login_request.password, user.hashed_password):
        raise InvalidPassword()
    if not user:
        raise InvalidUser()
    access_token = create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
####     END LOGIN ROUTE     #####



####     LOGOUT ROUTE     #####
logout_route = APIRouter(
    tags=["Logout"]
)

@logout_route.post('/logout')
async def logout(token: str = Depends(oauth2_scheme), 
                 db: AsyncSession = Depends(get_db), 
                 current_user: str = Depends(get_current_user)):
    blacklisted = Token_Blacklist(token = token)
    db.add(blacklisted)
    await db.commit()
    return {"message": "Logout Successfully"}
####     END LOGOUT ROUTE     #####



####     GET USER ROUTE     #####
get_user_route = APIRouter(
    tags=["Get_user"]
)

@get_user_route.get('/me', response_model=UserResponse)
async def get_user(current_user: User = Depends(get_current_user)):
    return current_user
####     END GET USER ROUTE     #####