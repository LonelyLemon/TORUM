from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.src.database import get_db
from backend.src.auth.exceptions import UserExistedCheck, InvalidPassword, InvalidUser, PostNotFound
from backend.src.auth.models import User, Token_Blacklist, Post, Refresh_Token
from backend.src.auth.schemas import UserCreate, UserUpdate, UserResponse, PostCreate, PostUpdate
from backend.src.auth.services import get_password_hash, verify_password, create_access_token, create_refresh_token
from backend.src.auth.dependencies import get_current_user, oauth2_scheme

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

####     USER ROUTE     #####
get_user_route = APIRouter(
    tags=["Get_user"]
)

@get_user_route.get('/me')
async def get_user(current_user: UserResponse = Depends(get_current_user)):
    return current_user

@get_user_route.put('/update-user')
async def update_user(update_request: UserUpdate,
                      db: AsyncSession = Depends(get_db),
                      current_user: UserResponse = Depends(get_current_user)):
    result = await db.execute(select(User).where(User.user_id == current_user.user_id))
    curr_user = result.scalars().first()
    update_data = update_request.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    for key, value in update_data.items():
        setattr(curr_user, key, value)
    await db.commit()
    await db.refresh(curr_user)
    return {"message": "User updated successfully !"}
####     END USER ROUTE     #####

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
    update_data = update_request.dict(exclude_unset=True)
    if not post:
        raise PostNotFound()
    for key, value in update_data.dict().items():
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

@post_route.get('/my-posts')
async def get_my_posts(db: AsyncSession = Depends(get_db),
                       current_user: UserResponse = Depends(get_current_user)):
    result = await db.execute(select(Post).where(Post.post_owner == current_user.user_id))
    posts = result.scalars().all()
    return posts
####     END POST ROUTE     ####

#---------------------------------------------------------------#