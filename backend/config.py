import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root if present
root_dir = Path(__file__).resolve().parent.parent
load_dotenv(root_dir / ".env")

class Settings:
    PROJECT_NAME: str = "AIET Voice Assistant & College Chatbot"
    VERSION: str = "1.0.0"
    COLLEGE_NAME: str = "Akash Institute of Engineering and Technology (AIET)"
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Security
    ADMIN_API_KEY: str = os.getenv("ADMIN_API_KEY", "aiet_admin_secret_2026")
    CORS_ORIGINS: list[str] = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",
        "http://localhost:5173",
        "*"
    ]
    
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent
    KB_DIR: Path = BASE_DIR / "knowledge_base"
    CHROMA_PERSIST_DIR: Path = BASE_DIR / "data" / "chroma"
    UPLOAD_DIR: Path = BASE_DIR / "data" / "uploads"
    
    # LLM Settings (Optional - fallback engine works fully offline if key is not set)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", os.getenv("OPENAI_API_KEY", ""))
    LLM_BASE_URL: str = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
    
    # Voice & Language
    DEFAULT_LANGUAGE: str = "en-IN"
    SUPPORTED_LANGUAGES: list[str] = ["en-IN", "en-US", "en-GB"]

settings = Settings()

# Ensure required directories exist
settings.CHROMA_PERSIST_DIR.mkdir(parents=True, exist_ok=True)
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
