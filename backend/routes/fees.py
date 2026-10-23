import json
from typing import List, Optional
from fastapi import APIRouter, Query
from backend.config import settings

router = APIRouter(prefix="/api/fees", tags=["Fees & Expenses"])

def load_fees() -> List[dict]:
    fees_path = settings.KB_DIR / "fees.json"
    if fees_path.exists():
        with open(fees_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@router.get("", response_model=List[dict])
async def get_fees(
    quota: Optional[str] = Query(None, description="Filter by admission quota: KCET, COMEDK, Management, or Hostel")
):
    """
    Returns official fee information and regulatory policies.
    Clearly notes fee components and highlights the requirement to confirm specific current amounts with admissions.
    """
    fees = load_fees()
    if quota:
        q_clean = quota.strip().lower()
        fees = [f for f in fees if q_clean in f.get("title", "").lower() or q_clean in f.get("quota_type", "").lower()]
    return fees
