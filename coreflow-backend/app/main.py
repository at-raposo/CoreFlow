from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import missions, sync, editais, study

# Import all models to ensure SQLAlchemy registry finds relationships like 'Tag'
import app.models.user
import app.models.taxonomy
import app.models.mission

from contextlib import asynccontextmanager
from app.core.scheduler import start_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    start_scheduler()
    yield
    # Shutdown logic if needed

app = FastAPI(
    title="CoreFlow API",
    description="Backend for the CoreFlow ADHD-Aware Productivity Platform",
    version="0.1.0",
    lifespan=lifespan
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(missions.router, prefix="/api", tags=["missions"])
app.include_router(sync.router, prefix="/api/sync", tags=["sync"])
app.include_router(editais.router, prefix="/api/editais", tags=["editais"])
app.include_router(study.router, prefix="/api/study", tags=["study"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the CoreFlow API. Engine is ready."}

