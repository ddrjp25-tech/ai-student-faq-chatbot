import json
from typing import List, Optional
from fastapi import APIRouter, Query
from backend.config import settings

router = APIRouter(prefix="/api/scholarships", tags=["Scholarships & Financial Aid"])

def load_scholarships() -> List[dict]:
    sch_path = settings.KB_DIR / "scholarships.json"
    if sch_path.exists():
        with open(sch_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@router.get("", response_model=List[dict])
async def get_scholarships(
    category: Optional[str] = Query(None, description="Filter by scholarship type (e.g. 'Institutional', 'Government', 'Girls')")
):
    """Returns verified state, national, and college-specific scholarship schemes."""
    scholarships = load_scholarships()
    if category:
        c_clean = category.strip().lower()
        scholarships = [
            s for s in scholarships 
            if c_clean in s.get("scheme_name", "").lower() 
            or c_clean in s.get("offered_by", "").lower()
            or c_clean in s.get("applicable_to", "").lower()
        ]
    return scholarships
