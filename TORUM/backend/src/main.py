from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.database import Base, engine
from src.auth import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI(lifespan=lifespan)

# @app.on_event("startup")
# async def startup_event():
#     async with engine.connect() as conn:
#         await conn.run_sync(Base.metadata.drop_all)     # Only use in dev/test phase, disable when deploy. 
#         await conn.run_sync(Base.metadata.create_all)

app.include_router(router.register_route)
app.include_router(router.login_route)
app.include_router(router.logout_route)
app.include_router(router.get_user_route)