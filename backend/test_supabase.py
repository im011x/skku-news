"""Supabase 설정 확인 스크립트"""

import os
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 직접 로드 (config.py와 동일한 방식)
env_path = Path(__file__).resolve().parent / ".env"
print(f"\n.env 파일 경로: {env_path}")
print(f"   파일 존재: {'OK' if env_path.exists() else 'FAIL'}")

if env_path.exists():
    load_dotenv(env_path, override=True)
    print("   .env 파일 로드 완료")
    
    # .env 파일 내용 직접 확인 (디버깅)
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"\n.env 파일 내용 (첫 10줄):")
            for i, line in enumerate(lines[:10], 1):
                if line.strip() and not line.strip().startswith('#'):
                    # 값은 일부만 표시
                    if '=' in line:
                        key, val = line.split('=', 1)
                        if len(val.strip()) > 20:
                            print(f"   {i}. {key.strip()}={val.strip()[:20]}...")
                        else:
                            print(f"   {i}. {key.strip()}={val.strip()}")
    except Exception as e:
        print(f"   .env 파일 읽기 오류: {e}")
else:
    print("   WARNING: .env 파일을 찾을 수 없습니다")

# 환경 변수 직접 확인
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")

print("=" * 50)
print("Supabase 설정 확인")
print("=" * 50)

print(f"\n1. SUPABASE_URL: {SUPABASE_URL[:30] + '...' if SUPABASE_URL and len(SUPABASE_URL) > 30 else SUPABASE_URL}")
print(f"   설정됨: {'OK' if SUPABASE_URL else 'FAIL'}")

print(f"\n2. SUPABASE_ANON_KEY: {SUPABASE_ANON_KEY[:30] + '...' if SUPABASE_ANON_KEY and len(SUPABASE_ANON_KEY) > 30 else SUPABASE_ANON_KEY}")
print(f"   설정됨: {'OK' if SUPABASE_ANON_KEY else 'FAIL'}")

if SUPABASE_URL and SUPABASE_ANON_KEY:
    print("\n3. Supabase 패키지 확인...")
    try:
        from supabase import create_client
        print("   OK: supabase 패키지 설치됨")
        
        print("\n4. 클라이언트 생성 테스트...")
        client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        print("   OK: 클라이언트 생성 성공")
        
        print("\n5. 테이블 존재 확인...")
        try:
            # news_searches 테이블 확인
            result = client.table("news_searches").select("id").limit(1).execute()
            print("   OK: news_searches 테이블 접근 가능")
        except Exception as e:
            err_msg = str(e)
            print(f"   WARNING: news_searches 테이블 접근 실패")
            print(f"      오류: {err_msg[:150]}")
            if "10061" in err_msg or "connection" in err_msg.lower():
                print("      -> 네트워크 연결 문제. Supabase URL이 올바른지 확인하세요")
            elif "permission" in err_msg.lower() or "policy" in err_msg.lower():
                print("      -> RLS 정책 문제. supabase_schema.sql의 정책을 확인하세요")
            else:
                print("      -> supabase_schema.sql을 Supabase Dashboard에서 실행했는지 확인하세요")
        
        try:
            # chat_messages 테이블 확인
            result = client.table("chat_messages").select("id").limit(1).execute()
            print("   OK: chat_messages 테이블 접근 가능")
        except Exception as e:
            err_msg = str(e)
            print(f"   WARNING: chat_messages 테이블 접근 실패")
            print(f"      오류: {err_msg[:150]}")
            if "10061" in err_msg or "connection" in err_msg.lower():
                print("      -> 네트워크 연결 문제. Supabase URL이 올바른지 확인하세요")
            elif "permission" in err_msg.lower() or "policy" in err_msg.lower():
                print("      -> RLS 정책 문제. supabase_schema.sql의 정책을 확인하세요")
            else:
                print("      -> supabase_schema.sql을 Supabase Dashboard에서 실행했는지 확인하세요")
            
    except ImportError:
        print("   FAIL: supabase 패키지가 설치되지 않음")
        print("   -> pip install supabase 실행 필요")
    except Exception as e:
        print(f"   FAIL: 클라이언트 생성 실패: {str(e)[:100]}")
        print("   -> SUPABASE_URL과 SUPABASE_ANON_KEY가 올바른지 확인하세요")
else:
    print("\nWARNING: SUPABASE_URL 또는 SUPABASE_ANON_KEY가 설정되지 않았습니다.")
    print("   -> backend/.env 파일에 설정하세요")

print("\n" + "=" * 50)
