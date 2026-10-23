import json
from typing import List, Optional
from fastapi import APIRouter, Query, HTTPException
from backend.config import settings

router = APIRouter(prefix="/api/faculty", tags=["Faculty Directory"])

def load_faculty() -> List[dict]:
    fac_path = settings.KB_DIR / "faculty.json"
    if fac_path.exists():
        with open(fac_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@router.get("", response_model=List[dict])
async def get_faculty(
    department: Optional[str] = Query(None, description="Filter by department (e.g. 'Computer Science', 'Mechanical', 'Basic Science')"),
    query: Optional[str] = Query(None, description="Search by faculty name or designation"),
    hod_only: Optional[bool] = Query(False, description="Filter to show only Heads of Departments (HODs)")
):
    """
    Search and retrieve verified AIET faculty members.
    Students can look up HODs, professors in specific departments, and access official profile PDFs.
    """
    faculty = load_faculty()
    
    if department:
        dept_clean = department.strip().lower()
        faculty = [f for f in faculty if dept_clean in f.get("department", "").lower()]
        
    if hod_only:
        faculty = [f for f in faculty if f.get("is_head_of_department")]
        
    if query:
        q_clean = query.strip().lower()
        faculty = [
            f for f in faculty
            if q_clean in f.get("name", "").lower()
            or q_clean in f.get("designation", "").lower()
            or q_clean in f.get("department", "").lower()
        ]
        
    return faculty

@router.get("/departments", response_model=List[str])
async def get_departments_list():
    """Returns a list of all distinct departments represented in the faculty directory."""
    faculty = load_faculty()
    depts = sorted(list(set(f.get("department") for f in faculty if f.get("department"))))
    return depts
