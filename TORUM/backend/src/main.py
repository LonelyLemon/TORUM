from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.src.auth import router

@asynccontextmanager
async def lifespan(app: FastAPI):
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