"""Supabase 연동. SUPABASE_URL, SUPABASE_ANON_KEY 설정 시 검색/채팅 로그 저장."""

from config import SUPABASE_ANON_KEY, SUPABASE_URL

_client = None


def _get_client():
    global _client
    if _client is not None:
        return _client
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        return None
    try:
        from supabase import create_client

        _client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        return _client
    except ImportError:
        return None
    except Exception as e:
        # 디버깅: 예외 정보 포함
        print(f"Supabase client 생성 실패: {e}")
        return None


def log_search(keyword: str, sort: str, total: int) -> dict:
    """뉴스 검색 로그 저장. 반환: {"success": bool, "message": str}"""
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        return {"success": False, "message": "Supabase 미설정 (URL 또는 KEY 없음)"}
    client = _get_client()
    if not client:
        return {"success": False, "message": "Supabase 클라이언트 생성 실패 (패키지 설치 확인 필요)"}
    try:
        client.table("news_searches").insert(
            {"keyword": keyword, "sort": sort, "total": total}
        ).execute()
        return {"success": True, "message": "검색 결과를 DB에 저장했습니다"}
    except Exception as e:
        err_msg = str(e)
        if "row-level security" in err_msg.lower() or "violates" in err_msg.lower():
            return {"success": False, "message": "DB 저장 실패: RLS 정책 오류. fix_rls_policies.sql을 Supabase Dashboard에서 실행하세요"}
        return {"success": False, "message": f"DB 저장 실패: {err_msg[:80]}"}


def log_chat(keyword: str, role: str, message: str) -> dict:
    """채팅 메시지 로그 저장. 반환: {"success": bool, "message": str}"""
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        return {"success": False, "message": "Supabase 미설정 (URL 또는 KEY 없음)"}
    client = _get_client()
    if not client:
        return {"success": False, "message": "Supabase 클라이언트 생성 실패 (패키지 설치 확인 필요)"}
    try:
        client.table("chat_messages").insert(
            {"keyword": keyword or "", "role": role, "message": message}
        ).execute()
        return {"success": True, "message": f"{role} 메시지를 DB에 저장했습니다"}
    except Exception as e:
        err_msg = str(e)
        if "row-level security" in err_msg.lower() or "violates" in err_msg.lower():
            return {"success": False, "message": "DB 저장 실패: RLS 정책 오류. fix_rls_policies.sql을 Supabase Dashboard에서 실행하세요"}
        return {"success": False, "message": f"DB 저장 실패: {err_msg[:80]}"}
