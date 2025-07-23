from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .database import Base, engine
from .auth import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)     #Only for development phase
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(CORSMiddleware, 
                   allow_origins=["http://localhost:5173"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(router.register_route)
app.include_router(router.login_route)
app.include_router(router.logout_route)
app.include_router(router.get_user_route)
app.include_router(router.post_route)