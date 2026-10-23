import json
from typing import List
from fastapi import APIRouter
from backend.config import settings

router = APIRouter(prefix="/api/sources", tags=["Approved Sources"])

def load_sources() -> List[dict]:
    src_path = settings.KB_DIR / "sources.json"
    if src_path.exists():
        with open(src_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@router.get("", response_model=List[dict])
async def get_sources():
    """Returns the manifest of all official AIET and government sources used to train and ground the knowledge base."""
    return load_sources()
