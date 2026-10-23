from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ChatMessage(BaseModel):
    role: str = Field(..., description="Role: 'user' or 'assistant'")
    content: str = Field(..., description="Message text")

class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000, description="The user's spoken or typed question")
    session_id: Optional[str] = Field(default="default_session", description="Unique session identifier for multi-turn conversation")
    history: Optional[List[ChatMessage]] = Field(default_factory=list, description="Recent conversation turns")
    language: Optional[str] = Field(default="en", description="Spoken/text language code (default 'en')")

class SourceCitation(BaseModel):
    title: str
    url: str
    category: str
    last_verified_date: str
    verification_status: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceCitation] = Field(default_factory=list)
    confidence: float = Field(default=0.95, description="Retrieval similarity confidence score (0.0 to 1.0)")
    needs_confirmation: bool = Field(default=False, description="True if official admissions confirmation is required (e.g. fees, deadlines)")
    confirmation_note: Optional[str] = None
    language: str = "en"
    intent: Optional[str] = None
    suggested_followups: List[str] = Field(default_factory=list)

class FacultyMember(BaseModel):
    id: str
    name: str
    designation: str
    department: str
    is_head_of_department: bool
    institution: str = "Akash Institute of Engineering and Technology"
    profile_pdf_url: Optional[str] = ""
    image_url: Optional[str] = ""
    source_url: str
    last_verified_date: str
    verification_status: str

class CourseInfo(BaseModel):
    id: str
    course_name: str
    short_name: str
    level: str
    duration: str
    degree_awarded: str
    department: str
    head_of_department: Optional[str] = None
    eligibility: str
    admission_routes: List[Dict[str, Any]]
    specialized_laboratories: Optional[List[str]] = None
    curriculum_highlights: Optional[str] = None
    career_pathways: Optional[str] = None
    source_url: str

class FeeInfo(BaseModel):
    id: str
    category: str
    title: str
    quota_type: Optional[str] = None
    academic_year: str
    fee_type: Optional[str] = None
    fee_range_inr: str
    official_guidance_rule: str
    mandatory_components: Optional[List[str]] = None
    admissions_contact: Optional[Dict[str, Any]] = None
    source_url: str
    last_verified_date: str

class ScholarshipInfo(BaseModel):
    id: str
    category: str
    scheme_name: str
    offered_by: str
    applicable_to: Optional[str] = None
    eligibility_criteria: Optional[str] = None
    benefit: Optional[str] = None
    benefit_amount: Optional[str] = None
    portal: Optional[str] = None
    application_portal: Optional[str] = None
    required_documents: Optional[List[str]] = None
    source_url: str
    last_verified_date: str

class AdminIngestDoc(BaseModel):
    title: str
    category: str
    content: str
    source_url: str
    source_type: str = "Admin Upload"
    academic_year: str = "2025-2026"
    last_verified_date: str

class AdminDocumentInfo(BaseModel):
    id: str
    title: str
    category: str
    chunk_count: int
    source_url: str
    last_verified_date: str
    indexed_date: str

class HealthResponse(BaseModel):
    status: str
    college: str
    version: str
    vector_database: str
    total_chunks_indexed: int
    llm_enabled: bool
