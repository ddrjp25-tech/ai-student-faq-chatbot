import os
import shutil
import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import pypdf
from bs4 import BeautifulSoup
from backend.config import settings
from backend.services.vector_store import VectorStoreService

class KnowledgeManager:
    def __init__(self):
        self.vector_store = VectorStoreService.get_instance()
        self.upload_dir = settings.UPLOAD_DIR
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def extract_text_from_pdf(self, file_path: Path) -> str:
        """Extracts plain text from a PDF file using pypdf."""
        reader = pypdf.PdfReader(str(file_path))
        text_content = []
        for idx, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text_content.append(page_text.strip())
        return "\n\n".join(text_content)

    def extract_text_from_html_or_txt(self, file_path: Path) -> str:
        """Extracts text from text or HTML documents."""
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        if file_path.suffix.lower() in [".html", ".htm"]:
            soup = BeautifulSoup(content, "html.parser")
            for s in soup(["script", "style", "noscript"]):
                s.decompose()
            return soup.get_text(separator="\n").strip()
        return content.strip()

    def preview_document(self, file_path: Path) -> Dict[str, Any]:
        """Extracts text and generates preview snippets without indexing."""
        if file_path.suffix.lower() == ".pdf":
            text = self.extract_text_from_pdf(file_path)
        else:
            text = self.extract_text_from_html_or_txt(file_path)
            
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        preview = "\n".join(lines[:30])
        char_count = len(text)
        word_count = len(text.split())

        return {
            "filename": file_path.name,
            "char_count": char_count,
            "word_count": word_count,
            "preview_snippet": preview[:1200]
        }

    def ingest_document(
        self,
        title: str,
        category: str,
        content: str,
        source_url: str,
        source_type: str = "Admin Verified Document",
        academic_year: str = "2025-2026"
    ) -> Dict[str, Any]:
        """Creates an indexed document chunk in ChromaDB."""
        today = datetime.date.today().isoformat()
        doc_id = f"custom_{category.lower()[:4]}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        self.vector_store.add_custom_document(
            doc_id=doc_id,
            title=title,
            category=category,
            content=content,
            source_url=source_url,
            academic_year=academic_year
        )
        return {
            "status": "success",
            "document_id": doc_id,
            "title": title,
            "indexed_date": today
        }

    def delete_document(self, doc_id: str) -> bool:
        """Removes a document from the vector store."""
        return self.vector_store.delete_document(doc_id)

    def rebuild_index(self) -> Dict[str, Any]:
        """Re-indexes all official JSON files from knowledge_base directory."""
        self.vector_store.index_all_knowledge_base()
        return {
            "status": "success",
            "message": "AIET Knowledge Base rebuilt successfully",
            "total_documents": self.vector_store.collection.count()
        }

    def list_documents(self) -> List[Dict[str, Any]]:
        """Lists all currently indexed knowledge records."""
        return self.vector_store.list_indexed_documents()
