from fastapi import FastAPI,Request,status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router
from contextlib import asynccontextmanager
from .models import create_structure

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_structure()
    yield
    print("API OFF")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan
)


origins = ["http://localhost",'http://localhost:3000','http://localhost:3000/*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix=settings.API_V1_STR)