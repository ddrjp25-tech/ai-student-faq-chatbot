import os
import sys
import types
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Ensure project root and backend directory are always in sys.path
_current_dir = Path(__file__).resolve().parent
_project_root = _current_dir.parent

for _p in [str(_project_root), str(_current_dir)]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

# Support running directly within backend directory (e.g. Render root dir = backend)
if "backend" not in sys.modules:
    try:
        import backend
    except ModuleNotFoundError:
        _backend_pkg = types.ModuleType("backend")
        _backend_pkg.__path__ = [str(_current_dir)]
        sys.modules["backend"] = _backend_pkg

from backend.config import settings
from backend.services.vector_store import VectorStoreService
from backend.models.schemas import HealthResponse

# Routers
from backend.routes.chat import router as chat_router
from backend.routes.courses import router as courses_router
from backend.routes.faculty import router as faculty_router
from backend.routes.fees import router as fees_router
from backend.routes.scholarships import router as scholarships_router
from backend.routes.infrastructure import router as infrastructure_router
from backend.routes.sources import router as sources_router
from backend.routes.admin import router as admin_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize VectorStore on startup
    print("Initializing AIET Vector Store...")
    vs = VectorStoreService.get_instance()
    total = vs.collection.count()
    print(f"AIET Vector Store Ready with {total} indexed knowledge chunks.")
    yield
    print("AIET Assistant shutting down.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Official AI Voice Assistant and Knowledge Retrieval API for Akash Institute of Engineering and Technology (AIET), Devanahalli, Bengaluru.",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(chat_router)
app.include_router(courses_router)
app.include_router(faculty_router)
app.include_router(fees_router)
app.include_router(scholarships_router)
app.include_router(infrastructure_router)
app.include_router(sources_router)
app.include_router(admin_router)

# Health Check
@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    vs = VectorStoreService.get_instance()
    llm_enabled = bool(settings.LLM_API_KEY and len(settings.LLM_API_KEY) > 5 and not settings.LLM_API_KEY.startswith("your_"))
    return HealthResponse(
        status="healthy",
        college=settings.COLLEGE_NAME,
        version=settings.VERSION,
        vector_database=f"ChromaDB (Collection: {vs.collection_name})",
        total_chunks_indexed=vs.collection.count(),
        llm_enabled=llm_enabled
    )

# Static Frontend mounting
frontend_dir = settings.BASE_DIR.parent / "frontend"
if not frontend_dir.exists():
    frontend_dir = Path("frontend").resolve()
if not frontend_dir.exists():
    frontend_dir = Path("../frontend").resolve()

if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

    @app.get("/", tags=["Frontend"])
    async def serve_index():
        index_file = frontend_dir / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
        return {"message": "Frontend index.html not found"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", settings.PORT))
    host = os.getenv("HOST", settings.HOST)
    uvicorn.run("backend.main:app", host=host, port=port, reload=False)
