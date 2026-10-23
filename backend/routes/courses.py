import json
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from backend.config import settings

router = APIRouter(prefix="/api/courses", tags=["Courses & Departments"])

def load_courses() -> List[dict]:
    courses_path = settings.KB_DIR / "courses.json"
    if courses_path.exists():
        with open(courses_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@router.get("", response_model=List[dict])
async def get_courses(
    level: Optional[str] = Query(None, description="Filter by level: UG or PG"),
    query: Optional[str] = Query(None, description="Search term in course name or department")
):
    """Returns all verified engineering and postgraduate courses offered at AIET."""
    courses = load_courses()
    
    if level:
        level_clean = level.strip().lower()
        courses = [c for c in courses if level_clean in c.get("level", "").lower()]
        
    if query:
        q_clean = query.strip().lower()
        courses = [
            c for c in courses 
            if q_clean in c.get("course_name", "").lower() 
            or q_clean in c.get("short_name", "").lower()
            or q_clean in c.get("department", "").lower()
        ]
        
    return courses

@router.get("/{course_id}", response_model=dict)
async def get_course_detail(course_id: str):
    """Returns detailed information for a specific course by ID."""
    courses = load_courses()
    for c in courses:
        if c.get("id") == course_id:
            return c
    raise HTTPException(status_code=404, detail=f"Course with ID '{course_id}' not found")
