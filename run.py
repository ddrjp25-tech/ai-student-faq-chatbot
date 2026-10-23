import os
import sys

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.config import settings
import uvicorn

if __name__ == "__main__":
    print("=================================================================")
    print(">> Starting Akash Institute of Engineering & Technology (AIET)")
    print("   AI Voice Assistant & College FAQ System")
    print(f"   Server running at: http://localhost:{settings.PORT}")
    print(f"   Swagger API Docs at: http://localhost:{settings.PORT}/docs")
    print("=================================================================")
    uvicorn.run("backend.main:app", host=settings.HOST, port=settings.PORT, reload=False)
