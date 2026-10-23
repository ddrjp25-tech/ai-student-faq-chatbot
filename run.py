import os
import sys

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.config import settings
import uvicorn

if __name__ == "__main__":
    port = int(os.getenv("PORT", str(settings.PORT)))
    host = os.getenv("HOST", settings.HOST)
    print("=================================================================")
    print(">> Starting Akash Institute of Engineering & Technology (AIET)")
    print("   AI Voice Assistant & College FAQ System")
    print(f"   Server running at: http://{host}:{port}")
    print(f"   Swagger API Docs at: http://{host}:{port}/docs")
    print("=================================================================")
    uvicorn.run("backend.main:app", host=host, port=port, reload=False)

