from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.src.auth import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # try:
    #     async with engine.connect() as conn:
    #         await conn.run_sync(Base.metadata.create_all)
    # except Exception as e:
    #     print(f"Database setup failed: {e}")
    #     raise
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(CORSMiddleware, 
                   allow_origins=["http://127.0.0.1:5173"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(router.register_route)
app.include_router(router.login_route)
app.include_router(router.logout_route)
app.include_router(router.get_user_route)
app.include_router(router.post_route)