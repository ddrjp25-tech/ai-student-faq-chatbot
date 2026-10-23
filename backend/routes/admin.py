import os
import shutil
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Header, UploadFile, File, Form, Depends
from backend.config import settings
from backend.services.knowledge_manager import KnowledgeManager
from backend.models.schemas import AdminIngestDoc

router = APIRouter(prefix="/api/admin", tags=["Knowledge Base Administration"])
km = KnowledgeManager()

def verify_admin_key(x_admin_key: Optional[str] = Header(None)):
    """Validates the administrative secret key."""
    if not x_admin_key or x_admin_key != settings.ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid or missing admin API key")
    return True

@router.get("/documents")
async def list_documents(authorized: bool = Depends(verify_admin_key)):
    """Lists all indexed knowledge base records with metadata and dates."""
    docs = km.list_documents()
    # Check for outdated documents (older than 1 year)
    current_year = "2026"
    for d in docs:
        d["is_potentially_outdated"] = not d.get("last_verified_date", "").startswith(current_year)
    return {"total_count": len(docs), "documents": docs}

@router.post("/upload-and-preview")
async def upload_and_preview(
    file: UploadFile = File(...),
    authorized: bool = Depends(verify_admin_key)
):
    """Uploads a PDF or text document and returns an extracted text preview before indexing."""
    filename = file.filename or "upload.txt"
    dest_path = settings.UPLOAD_DIR / filename
    
    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    preview_data = km.preview_document(dest_path)
    return preview_data

@router.post("/ingest")
async def ingest_document(
    doc: AdminIngestDoc,
    authorized: bool = Depends(verify_admin_key)
):
    """Indexes an approved document into ChromaDB."""
    result = km.ingest_document(
        title=doc.title,
        category=doc.category,
        content=doc.content,
        source_url=doc.source_url,
        source_type=doc.source_type,
        academic_year=doc.academic_year
    )
    return result

@router.delete("/documents/{doc_id}")
async def delete_document(
    doc_id: str,
    authorized: bool = Depends(verify_admin_key)
):
    """Deletes an outdated or incorrect document from the knowledge base."""
    success = km.delete_document(doc_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Document with ID '{doc_id}' not found or could not be deleted")
    return {"status": "success", "message": f"Document '{doc_id}' deleted successfully"}

@router.post("/rebuild")
async def rebuild_knowledge_base(authorized: bool = Depends(verify_admin_key)):
    """Rebuilds the entire ChromaDB index from baseline verified official JSON files."""
    result = km.rebuild_index()
    return result
