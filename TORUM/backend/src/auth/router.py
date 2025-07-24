from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..database import get_db
from .exceptions import UserExistedCheck, InvalidPassword, InvalidUser, PostNotFound
from .models import User, Token_Blacklist, Post, Refresh_Token
from .schemas import UserCreate, UserResponse, PostCreate, PostUpdate
from .services import get_password_hash, verify_password, create_access_token, create_refresh_token
from .dependencies import get_current_user, oauth2_scheme

#---------------------------------------------------------------#

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
        hashed_password = hashed_pw
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
####     END REGISTER ROUTE     #####

#---------------------------------------------------------------#

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
    refresh_token = create_refresh_token(data={"sub": user.email})
    new_refresh_token = Refresh_Token(
        refresh_token = refresh_token,
        user_id = user.user_id
    )
    db.add(new_refresh_token)
    await db.commit()
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
####     END LOGIN ROUTE     #####

#---------------------------------------------------------------#

####     LOGOUT ROUTE     #####
logout_route = APIRouter(
    tags=["Logout"]
)

@logout_route.post('/logout')
async def logout(token: str = Depends(oauth2_scheme), 
                 db: AsyncSession = Depends(get_db), 
                 current_user: UserResponse = Depends(get_current_user)):
    blacklisted = Token_Blacklist(token = token)
    db.add(blacklisted)
    await db.commit()
    result = await db.execute(select(Refresh_Token).where(Refresh_Token.user_id == current_user.user_id))
    refresh_token = result.scalars().first()
    if refresh_token:
        refresh_token.is_expired = True
        await db.commit()
    return {"message": "Logout Successfully"}
####     END LOGOUT ROUTE     #####

#---------------------------------------------------------------#

####     GET USER ROUTE     #####
get_user_route = APIRouter(
    tags=["Get_user"]
)

@get_user_route.get('/me', response_model=UserResponse)
async def get_user(current_user: UserResponse = Depends(get_current_user)):
    return current_user
####     END GET USER ROUTE     #####

#---------------------------------------------------------------#

####     POST ROUTE     ####
post_route = APIRouter(
    tags=["Posts"]
)

@post_route.post('/create-post')
async def create_post(post: PostCreate, 
                      db: AsyncSession = Depends(get_db), 
                      current_user: UserResponse = Depends(get_current_user)):
    new_post = Post(
        post_owner = current_user.user_id,
        post_title = post.post_title,
        post_content = post.post_content
    )

    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post

@post_route.get('/view-post/{id}')
async def view_post(id: str, 
                    db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post).where(Post.post_id == id))
    viewing_post = result.scalars().first()
    if not viewing_post:
        raise PostNotFound()
    return viewing_post

@post_route.put('/update-post/{id}')
async def update_post(id: str, 
                      update_request: PostUpdate, 
                      db: AsyncSession = Depends(get_db), 
                      current_user: UserResponse = Depends(get_current_user)):
    result = await db.execute(select(Post).where(Post.post_id == id, Post.post_owner == current_user.user_id))
    post = result.scalars().first()
    if not post:
        raise PostNotFound()
    for key, value in update_request.dict().items():
        setattr(post, key, value)
    await db.commit()
    await db.refresh(post)
    return {"message": "Post updated successfully !"}

@post_route.delete('/delete-post/{id}')
async def delete_post(id: str, 
                      db: AsyncSession = Depends(get_db), 
                      current_user: UserResponse = Depends(get_current_user)):
    result = await db.execute(select(Post).where(Post.post_id == id, Post.post_owner == current_user.user_id))
    post = result.scalars().first()
    if not post:
        raise PostNotFound()
    await db.delete(post)
    await db.commit()
    return {"message": "Post deleted successfully !"}
####     END POST ROUTE     ####

#---------------------------------------------------------------#