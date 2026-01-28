# RLS 정책 오류 해결 가이드

"new row violates row-level security policy" 오류가 발생하면 다음 단계를 따라하세요.

---

## 🔧 해결 방법

### 1단계: Supabase Dashboard 접속

1. [Supabase Dashboard](https://supabase.com/dashboard) 접속
2. 프로젝트 선택

### 2단계: SQL Editor 열기

1. 왼쪽 메뉴에서 **SQL Editor** 클릭
2. **New query** 버튼 클릭

### 3단계: RLS 정책 수정 SQL 실행

`backend/fix_rls_policies.sql` 파일 내용을 복사하여 SQL Editor에 붙여넣고 **Run** 버튼 클릭.

또는 아래 SQL을 직접 실행:

```sql
-- 기존 정책 삭제
DROP POLICY IF EXISTS "Allow anon insert news_searches" ON news_searches;
DROP POLICY IF EXISTS "Allow anon insert chat_messages" ON chat_messages;

-- INSERT 정책 생성
CREATE POLICY "Allow anon insert news_searches"
  ON news_searches
  FOR INSERT
  TO anon
  WITH CHECK (true);

CREATE POLICY "Allow anon insert chat_messages"
  ON chat_messages
  FOR INSERT
  TO anon
  WITH CHECK (true);
```

### 4단계: 정책 확인

SQL Editor에서 다음 쿼리 실행:

```sql
SELECT 
  tablename,
  policyname,
  cmd,
  roles
FROM pg_policies
WHERE tablename IN ('news_searches', 'chat_messages');
```

**예상 결과:**
- `news_searches` 테이블에 `Allow anon insert news_searches` 정책 (cmd: INSERT, roles: {anon})
- `chat_messages` 테이블에 `Allow anon insert chat_messages` 정책 (cmd: INSERT, roles: {anon})

---

## ✅ 완료 확인

1. 웹 앱에서 뉴스 검색
2. DB 저장 로그 영역에서 **"검색 결과를 DB에 저장했습니다"** 메시지 확인
3. Supabase Dashboard > Table Editor에서 데이터 확인

---

## 🔍 문제가 계속되면

### 방법 1: RLS 비활성화 (개발용, 보안 주의)

```sql
ALTER TABLE news_searches DISABLE ROW LEVEL SECURITY;
ALTER TABLE chat_messages DISABLE ROW LEVEL SECURITY;
```

> ⚠️ **주의**: 프로덕션 환경에서는 사용하지 마세요!

### 방법 2: service_role key 사용 (서버 전용)

`.env`에 `SUPABASE_SERVICE_ROLE_KEY` 추가하고 `db.py`에서 사용:

```python
# config.py
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

# db.py
if SUPABASE_SERVICE_ROLE_KEY:
    client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
```

> ⚠️ **주의**: service_role key는 서버에서만 사용하고 클라이언트에 노출하지 마세요!

---

## 📚 참고

- [Supabase RLS 문서](https://supabase.com/docs/guides/database/postgres/row-level-security)
- [RLS 정책 생성 가이드](https://supabase.com/docs/guides/database/postgres/row-level-security#creating-policies)
