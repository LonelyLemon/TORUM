from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy import select

from backend.src.auth import router
from backend.src.auth.models import User
from backend.src.auth.services import get_password_hash
from backend.src.config import get_settings
from backend.src.database import SessionLocal

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    async with SessionLocal() as session:
        if settings.ADMIN_EMAIL and settings.ADMIN_PASSWORD and settings.ADMIN_USERNAME:
            result = await session.execute(select(User).where(User.user_role == "admin"))
            admin = result.scalar_one_or_none()
            if not admin:
                hashed_pw = get_password_hash(settings.ADMIN_PASSWORD)
                admin_user = User(
                    username=settings.ADMIN_USERNAME,
                    email=settings.ADMIN_EMAIL,
                    hashed_password=hashed_pw,
                    user_role="admin",
                )
                session.add(admin_user)
                await session.commit()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(CORSMiddleware, 
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(router.register_route)
app.include_router(router.login_route)
app.include_router(router.logout_route)
app.include_router(router.refresh_token_route)
app.include_router(router.get_user_route)
app.include_router(router.post_route)
app.include_router(router.reading_documents_route)
app.include_router(router.search_route)