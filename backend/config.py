import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Supabase (로컬 Supabase 또는 Cloud 모두 사용 가능)
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")
