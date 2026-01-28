import os
from pathlib import Path

from dotenv import load_dotenv

# Vercel 배포 환경에서는 .env 파일이 없을 수 있으므로
# 파일이 존재할 때만 로드 (로컬 개발용)
env_path = Path(__file__).resolve().parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

# 환경 변수는 Vercel에서 자동으로 설정됨
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Supabase (로컬 Supabase 또는 Cloud 모두 사용 가능)
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")
