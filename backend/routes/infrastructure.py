import json
from typing import List
from fastapi import APIRouter
from backend.config import settings

router = APIRouter(prefix="/api/infrastructure", tags=["Campus Infrastructure"])

def load_infrastructure() -> List[dict]:
    infra_path = settings.KB_DIR / "infrastructure.json"
    if infra_path.exists():
        with open(infra_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@router.get("", response_model=List[dict])
async def get_infrastructure():
    """Returns verified details of all campus infrastructure and student amenities."""
    return load_infrastructure()
