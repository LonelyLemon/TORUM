import asyncio
import uuid

from fastapi import Depends, APIRouter, UploadFile, File, Query
from fastapi.params import Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.sql import text, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from jose import JWTError

from backend.src.database import get_db
from backend.src.auth.exceptions import UserExistedCheck, InvalidPassword, InvalidUser, PostNotFound, FileUploadFailed, FileDeletionFailed, DocumentNotFound, PresignedURLFailed, PermissionException, SizeTooLarge, EmptyQueryException, CredentialException
from backend.src.auth.models import User, Post, Reading_Documents
from backend.src.auth.schemas import UserCreate, UserUpdate, UserResponse, PostCreate, PostUpdate, Reading_Documents_Response
from backend.src.auth.services import get_password_hash, verify_password, create_access_token, create_refresh_token, decode_token
from backend.src.auth.dependencies import require_role
from backend.src.auth.utils import upload_file_to_s3, delete_file_from_s3, generate_presigned_url

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
    if not user:
        raise InvalidUser()
    if not verify_password(login_request.password, user.hashed_password):
        raise InvalidPassword()
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
####     END LOGIN ROUTE     #####

#---------------------------------------------------------------#

####     REFRESH TOKEN ROUTE     #####
refresh_token_route = APIRouter(
    tags=["Refresh_Token"]
)

@refresh_token_route.post('/refresh')
async def refresh_token(refresh_token: str):
    try:
        payload = decode_token(refresh_token)
        email: str = payload.get("sub")
        token_type: str = payload.get("type")
        if not email or token_type != "refresh":
            raise CredentialException()
    except JWTError:
        raise CredentialException()
    
    access_token = create_access_token(data={"sub": email})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
####     END REFRESH TOKEN ROUTE     #####

#---------------------------------------------------------------#

####     LOGOUT ROUTE     #####
logout_route = APIRouter(
    tags=["Logout"]
)

@logout_route.post('/logout')
async def logout():
    return {"message": "Logout Successfully"}
####     END LOGOUT ROUTE     #####

#---------------------------------------------------------------#

####     USER ROUTE     #####
get_user_route = APIRouter(
    tags=["Get_user"]
)

@get_user_route.get('/me')
async def get_user(current_user: UserResponse = Depends(require_role(["user", "moderator", "admin"]))):
    return current_user

@get_user_route.get('/users', response_model=List[UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db), 
                        current_user: UserResponse = Depends(require_role(["user", "moderator", "admin"]))):
    if current_user.user_role != "admin":
        raise PermissionException()
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

@get_user_route.put('/update-user')
async def update_user(update_request: UserUpdate,
                      db: AsyncSession = Depends(get_db),
                      current_user: UserResponse = Depends(require_role(["user", "moderator", "admin"]))):
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

@get_user_route.put('/update-user-role/{user_id}')
async def update_user_role(user_id: str, 
                           new_role: str, 
                           db: AsyncSession = Depends(get_db), 
                           current_user: UserResponse = Depends(require_role(["user", "moderator", "admin"]))):
    if current_user.user_role != "admin":
        raise PermissionException()
    result = await db.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise InvalidUser()
    user.user_role = new_role
    await db.commit()
    await db.refresh(user)
    return user
####     END USER ROUTE     #####

#---------------------------------------------------------------#

####     POST ROUTE     ####
post_route = APIRouter(
    tags=["Posts"]
)

@post_route.post('/create-post')
async def create_post(post: PostCreate, 
                      db: AsyncSession = Depends(get_db), 
                      current_user: UserResponse = Depends(require_role(["user", "moderator", "admin"]))):
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
                      current_user: UserResponse = Depends(require_role(["user", "moderator", "admin"]))):
    if current_user.user_role == "admin":
        result = await db.execute(select(Post).where(Post.post_id == id))
    else:
        result = await db.execute(select(Post).where(Post.post_id == id, Post.post_owner == current_user.user_id))
    post = result.scalar_one_or_none()
    update_data = update_request.model_dump(exclude_unset=True)
    if post is None:
        raise PostNotFound()
    for key, value in update_data.items():
        if hasattr(post, key):
            setattr(post, key, value)
    await db.commit()
    await db.refresh(post)
    return post

@post_route.delete('/delete-post/{id}')
async def delete_post(id: str, 
                      db: AsyncSession = Depends(get_db), 
                      current_user: UserResponse = Depends(require_role(["user", "moderator", "admin"]))):
    if current_user.user_role in ["moderator", "admin"]:
        result = await db.execute(select(Post).where(Post.post_id == id))
    else:
        result = await db.execute(select(Post).where(Post.post_id == id, Post.post_owner == current_user.user_id))
    post = result.scalar_one_or_none()
    if post is None:
        raise PostNotFound()
    await db.delete(post)
    await db.commit()
    return {"message": "Post deleted successfully !"}

@post_route.get('/my-posts')
async def get_my_posts(db: AsyncSession = Depends(get_db),
                       current_user: UserResponse = Depends(require_role(["user", "moderator", "admin"]))):
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
async def upload_reading_documents(docs_title: str = Form(...), 
                                   docs_description: str = Form(...), 
                                   docs_tags: str = Form(...),
                                   file: UploadFile = File(...),
                                   db: AsyncSession = Depends(get_db), 
                                   current_user: UserResponse = Depends(require_role(["user", "moderator", "admin"]))):
    MAX_FILE_SIZE = 20 * 1024 * 1024
    if file.size > MAX_FILE_SIZE:
        raise SizeTooLarge()
    
    s3_key = f"{current_user.user_id}/{uuid.uuid4()}_{file.filename}"
    try:
        upload_result = await upload_file_to_s3(file.file, s3_key, file.content_type)
        if upload_result is None:
            raise FileUploadFailed()
    finally:
        await file.close()

    new_doc = Reading_Documents(
        docs_owner = current_user.user_id,
        docs_title = docs_title,
        docs_description = docs_description,
        docs_tags = docs_tags,
        docs_file_path = s3_key,
    )
    db.add(new_doc)
    await db.commit()
    await db.refresh(new_doc)
    return new_doc

@reading_documents_route.get('/download-document/{doc_id}')
async def download_document(doc_id: str, 
                            db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Reading_Documents).where(Reading_Documents.docs_id == doc_id))
    document = result.scalar_one_or_none()

    if document is None:
        raise DocumentNotFound()
    
    presigned_url = await generate_presigned_url(document.docs_file_path)
    if presigned_url is None:
        raise PresignedURLFailed()
    
    return {"url": presigned_url}

@reading_documents_route.get('/my-reading-documents')
async def get_my_documents(db: AsyncSession = Depends(get_db), 
                           current_user: UserResponse = Depends(require_role(["user", "moderator", "admin"]))):
    result = await db.execute(select(Reading_Documents).where(Reading_Documents.docs_owner == current_user.user_id))
    docs = result.scalars().all()
    return docs

@reading_documents_route.delete('/delete-reading-document/{doc_id}')
async def delete_document(doc_id: str, 
                          db: AsyncSession = Depends(get_db), 
                          current_user: UserResponse = Depends(require_role(["user", "moderator", "admin"]))):
    if current_user.user_role in ["moderator", "admin"]:
        result = await db.execute(select(Reading_Documents).where(Reading_Documents.docs_id == doc_id))
    else:
        result = await db.execute(select(Reading_Documents).where(Reading_Documents.docs_id == doc_id, Reading_Documents.docs_owner == current_user.user_id))
    document = result.scalar_one_or_none()

    if document is None:
        raise DocumentNotFound()
    
    deleted = await delete_file_from_s3(document.docs_file_path)
    if not deleted:
        raise FileDeletionFailed()
    
    await db.delete(document)
    await db.commit()

    return {"message": "Document deleted successfully !"}
####     READING DOCUMENTS ROUTE     ####

#---------------------------------------------------------------#

####     SEARCH ROUTE     ####

search_route = APIRouter(
    tags = ["Search"]
)

@search_route.get("/search")
async def search(query: str = Query(..., min_length=1, max_length=100),
                 offset: int = Query(0, ge=0),
                 limit: int = Query(10, ge=1, le=100),
                 db: AsyncSession = Depends(get_db)):
    if not query.strip():
        raise EmptyQueryException()
    tsquery = func.plainto_tsquery('english', f"{query}:*")

    post_query = select(Post, func.ts_rank(Post.search_vector, tsquery).label('rank')
                        ).where(Post.search_vector.op('@@')(tsquery)
                        ).order_by(text('rank DESC')).offset(offset).limit(limit)
    
    document_query = select(Reading_Documents, func.ts_rank(Reading_Documents.search_vector, tsquery).label('rank')
                            ).where(Reading_Documents.search_vector.op('@@')(tsquery)
                            ).order_by(text('rank DESC')).offset(offset).limit(limit)
    
    post_result, document_result = await asyncio.gather(
        db.execute(post_query),
        db.execute(document_query)
    )
    
    return {
        "post_result": post_result.scalars().all(),
        "document_result": document_result.scalars().all()
    }

####     END SEARCH ROUTE     ####