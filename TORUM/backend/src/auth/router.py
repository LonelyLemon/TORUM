import asyncio

from fastapi import Depends, APIRouter, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.src.database import get_db
from backend.src.auth.exceptions import UserExistedCheck, InvalidPassword, InvalidUser, PostNotFound, FileUploadFailed, DocumentNotFound, PresignedURLFailed
from backend.src.auth.models import User, Token_Blacklist, Post, Refresh_Token, Reading_Documents
from backend.src.auth.schemas import UserCreate, UserUpdate, UserResponse, PostCreate, PostUpdate, Reading_Documents_Upload, Reading_Documents_Response
from backend.src.auth.services import get_password_hash, verify_password, create_access_token, create_refresh_token
from backend.src.auth.dependencies import get_current_user, oauth2_scheme
from backend.src.auth.utils import upload_file_to_s3, generate_presigned_url

#---------------------------------------------------------------#

####     REGISTER ROUTE     #####
register_route = APIRouter(
    tags=["Register"]
)

@register_route.post('/register', response_model=UserResponse)
async def register(user: UserCreate, 
                   db: AsyncSession = Depends(get_db)):
    existed_user = await db.execute(select(User).where((User.email == user.email)))
    if existed_user.scalar_one_or_none():
        raise UserExistedCheck()
    hashed_pw = get_password_hash(user.password)
    new_user = User(
        username = user.username,
        email = user.email,
        hashed_password = hashed_pw,
        user_role = "user"
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
    user = result.scalar_one_or_none()
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
    refresh_token = result.scalar_one_or_none()
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
    curr_user = result.scalar_one_or_none()
    update_data = update_request.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    for key, value in update_data.items():
        setattr(curr_user, key, value)
    await db.commit()
    await db.refresh(curr_user)
    return curr_user
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
    viewing_post = result.scalar_one_or_none()
    if viewing_post is None:
        raise PostNotFound()
    return viewing_post

@post_route.put('/update-post/{id}')
async def update_post(id: str, 
                      update_request: PostUpdate, 
                      db: AsyncSession = Depends(get_db), 
                      current_user: UserResponse = Depends(get_current_user)):
    result = await db.execute(select(Post).where(Post.post_id == id, Post.post_owner == current_user.user_id))
    post = result.scalar_one_or_none()
    update_data = update_request.model_dump(exclude_unset=True)
    if post is None:
        raise PostNotFound()
    for key, value in update_data.dict().items():
        setattr(post, key, value)
    await db.commit()
    await db.refresh(post)
    return post

@post_route.delete('/delete-post/{id}')
async def delete_post(id: str, 
                      db: AsyncSession = Depends(get_db), 
                      current_user: UserResponse = Depends(get_current_user)):
    result = await db.execute(select(Post).where(Post.post_id == id, Post.post_owner == current_user.user_id))
    post = result.scalar_one_or_none()
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

####     READING DOCUMENTS ROUTE     ####
reading_documents_route = APIRouter(
    tags=["Reading_Documents"]
)

@reading_documents_route.post('/upload-reading-documents', response_model=Reading_Documents_Response)
async def upload_reading_documents(docs: Reading_Documents_Upload,
                                   file: UploadFile = File(...),
                                   db: AsyncSession = Depends(get_db), 
                                   current_user: UserResponse = Depends(get_current_user)):
    s3_key = f"{current_user.user_id}/{file.filename}"
    upload_result = upload_file_to_s3(file.file, s3_key, file.content_type)

    if upload_result is None:
        raise FileUploadFailed()
    
    new_doc = Reading_Documents(
        docs_owner = current_user.user_id,
        docs_title = docs.docs_title,
        docs_description = docs.docs_description,
        docs_tags = docs.docs_tags,
        docs_file_path = s3_key,
    )
    db.add(new_doc)
    await db.commit()
    await db.refresh(new_doc)
    return new_doc

@reading_documents_route.get('/download-document/{doc_id}')
async def download_document(doc_id: str, 
                            db: AsyncSession = Depends(get_db),
                            current_user: UserResponse = Depends(get_current_user)):
    result = await db.execute(select(Reading_Documents).where(Reading_Documents.docs_id == doc_id, Reading_Documents.docs_owner == current_user.user_id))
    document = result.scalar_one_or_none()

    if not document:
        raise DocumentNotFound()
    
    presigned_url = generate_presigned_url(document.docs_file_path)
    if not presigned_url:
        raise PresignedURLFailed()
    
    return {"url": presigned_url}

@reading_documents_route.get('/my-reading-documents')
async def get_my_documents(db: AsyncSession = Depends(get_db), 
                           current_user: UserResponse = Depends(get_current_user)):
    result = await db.execute(select(Reading_Documents).where(Reading_Documents.docs_owner == current_user.user_id))
    docs = result.scalars().all()
    return docs
####     READING DOCUMENTS ROUTE     ####

#---------------------------------------------------------------#

####     SEARCH ROUTE     ####

search_route = APIRouter(
    tags = ["Search"]
)

@search_route.get("/search")
async def search(query: str,
                 db: AsyncSession = Depends(get_db)):
    post_query = select(Post).where(Post.post_title.ilike(f"%{query}%"))
    document_query = select(Reading_Documents).where(Reading_Documents.docs_title.ilike(f"%{query}%"))
    
    post_result, document_result = await asyncio.gather(
        db.execute(post_query),
        db.execute(document_query)
    )

    return {
        "post_result": post_result.scalars().all(),
        "document_result": document_result.scalars().all()
    }

####     END SEARCH ROUTE     ####