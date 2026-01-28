"""
Vercel serverless function handler for FastAPI app
"""
import sys
from pathlib import Path

# backend 디렉토리를 Python 경로에 추가
backend_path = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_path))

# FastAPI 앱 import
from main import app

# Vercel이 ASGI 앱을 인식하도록 app을 export
__all__ = ["app"]
