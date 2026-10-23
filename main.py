import os
import sys
from pathlib import Path

# Ensure root directory is in sys.path
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from backend.main import app
from backend.config import settings

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", settings.PORT))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run("main:app", host=host, port=port, reload=False)
