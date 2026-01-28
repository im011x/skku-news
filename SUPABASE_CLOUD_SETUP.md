# Supabase Cloud 사용하기 - 상세 가이드

로컬에서 웹 앱(`localhost:8000`)을 실행하면서 **Supabase Cloud**의 데이터베이스를 사용하는 방법입니다.

---

## ⚡ 빠른 시작 (5분)

1. **Supabase 프로젝트 생성** → [supabase.com](https://supabase.com) 가입/로그인
2. **API 키 복사** → 프로젝트 Settings > API
3. **`.env` 설정** → `SUPABASE_URL`, `SUPABASE_ANON_KEY` 추가
4. **스키마 실행** → Supabase Dashboard > SQL Editor에서 `supabase_schema.sql` 실행
5. **앱 실행** → `uvicorn main:app --reload`

**완료!** 로컬 앱이 Cloud Supabase DB에 데이터를 저장합니다.

---

## 1단계: Supabase 프로젝트 생성

### 1.1 Supabase 가입/로그인

1. [Supabase](https://supabase.com) 접속
2. **Sign Up** 또는 **Sign In**
3. GitHub, Google 등으로 간편 가입 가능

### 1.2 새 프로젝트 생성

1. Dashboard에서 **New Project** 클릭
2. **Organization** 선택 (없으면 새로 생성)
3. 프로젝트 정보 입력:
   - **Name**: 프로젝트 이름 (예: `news-chatbot`)
   - **Database Password**: 강력한 비밀번호 설정 (기억해두세요!)
   - **Region**: 가장 가까운 리전 선택 (예: `Northeast Asia (Seoul)`)
   - **Pricing Plan**: Free 플랜 선택
4. **Create new project** 클릭

**프로젝트 생성에는 1-2분 소요됩니다.**

---

## 2단계: API 키 확인

프로젝트가 생성되면:

1. 왼쪽 메뉴에서 **Settings** (⚙️) 클릭
2. **API** 메뉴 선택
3. 다음 정보를 복사:

   - **Project URL**: `https://xxxxx.supabase.co` 형태
   - **anon public** key: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` 형태 (긴 문자열)

   > **참고**: 
   - `anon public` key: 클라이언트에서 사용 (우리 앱에서 사용)
   - `service_role` key: 서버 전용 (민감 정보, 사용 안 함)

---

## 3단계: 환경 변수 설정

`backend/.env` 파일에 Supabase 정보 추가:

```env
# 기존 설정
GEMINI_API_KEY=your_gemini_api_key_here

# Supabase Cloud 설정
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0
```

**예시:**
```env
SUPABASE_URL=https://abcdefghijklmnop.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0
```

> ⚠️ **보안**: `.env` 파일은 절대 Git에 커밋하지 마세요! `.gitignore`에 포함되어 있는지 확인하세요.

---

## 4단계: 데이터베이스 스키마 생성

### 4.1 Supabase Dashboard 접속

1. 프로젝트 Dashboard: `https://supabase.com/dashboard/project/your-project-id`
2. 왼쪽 메뉴에서 **SQL Editor** 클릭

### 4.2 스키마 실행

1. **New query** 버튼 클릭
2. `backend/supabase_schema.sql` 파일 내용을 복사
3. SQL Editor에 붙여넣기
4. **Run** 버튼 클릭 (또는 `Ctrl+Enter`)

**성공 메시지 확인:**
```
Success. No rows returned
```

### 4.3 테이블 확인

1. 왼쪽 메뉴에서 **Table Editor** 클릭
2. `news_searches`, `chat_messages` 테이블이 보이는지 확인

---

## 5단계: FastAPI 앱 실행

```powershell
cd backend

# 의존성 설치 (supabase 포함)
pip install -r requirements.txt

# 서버 실행
uvicorn main:app --reload
```

**앱 접속:**
- 웹 UI: `http://localhost:8000`
- API 문서: `http://localhost:8000/docs`

---

## 6단계: 테스트

1. **뉴스 검색 테스트**
   - 브라우저에서 `http://localhost:8000` 접속
   - 키워드 입력 후 검색
   - Supabase Dashboard > Table Editor > `news_searches`에서 데이터 확인

2. **채팅 테스트**
   - 검색 후 채팅 메시지 전송
   - Supabase Dashboard > Table Editor > `chat_messages`에서 데이터 확인

---

## 📊 데이터 확인 방법

### Supabase Dashboard (웹 UI)

1. [Supabase Dashboard](https://supabase.com/dashboard) 접속
2. 프로젝트 선택
3. **Table Editor** → 테이블 선택
4. 행(Row) 데이터 확인

### SQL 쿼리 (SQL Editor)

```sql
-- 최근 검색 10건
SELECT * FROM news_searches 
ORDER BY created_at DESC 
LIMIT 10;

-- 최근 채팅 메시지 20건
SELECT * FROM chat_messages 
ORDER BY created_at DESC 
LIMIT 20;

-- 키워드별 검색 통계
SELECT keyword, COUNT(*) as count 
FROM news_searches 
GROUP BY keyword 
ORDER BY count DESC;

-- 오늘 검색한 키워드
SELECT keyword, COUNT(*) as count, MAX(created_at) as last_search
FROM news_searches 
WHERE created_at::date = CURRENT_DATE
GROUP BY keyword 
ORDER BY count DESC;
```

---

## 🔧 문제 해결

### 연결 오류

**증상**: `Failed to connect to Supabase`

**해결:**
1. `.env`의 `SUPABASE_URL`이 `https://`로 시작하는지 확인
2. `SUPABASE_ANON_KEY`가 올바른지 확인 (Settings > API에서 재확인)
3. 인터넷 연결 확인
4. Supabase 프로젝트가 **Active** 상태인지 확인 (Dashboard에서 확인)

### RLS (Row Level Security) 오류

**증상**: `new row violates row-level security policy`

**해결:**
1. Supabase Dashboard > SQL Editor
2. 다음 쿼리 실행:

```sql
-- 정책 확인
SELECT * FROM pg_policies WHERE tablename IN ('news_searches', 'chat_messages');

-- 정책이 없으면 다시 생성
DROP POLICY IF EXISTS "Allow anon insert news_searches" ON news_searches;
CREATE POLICY "Allow anon insert news_searches"
  ON news_searches FOR INSERT TO anon WITH CHECK (true);

DROP POLICY IF EXISTS "Allow anon insert chat_messages" ON chat_messages;
CREATE POLICY "Allow anon insert chat_messages"
  ON chat_messages FOR INSERT TO anon WITH CHECK (true);
```

### 테이블이 보이지 않음

**해결:**
1. SQL Editor에서 스키마가 실행되었는지 확인
2. Table Editor에서 새로고침
3. 다음 쿼리로 테이블 존재 확인:

```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_name IN ('news_searches', 'chat_messages');
```

---

## 💰 무료 플랜 제한

Supabase Free 플랜 제한:

- **Database**: 500MB 저장 공간
- **API 요청**: 월 50,000 요청
- **Bandwidth**: 월 5GB
- **File Storage**: 1GB

**우리 앱 사용량:**
- 검색 1회 = 1 insert 요청
- 채팅 1회 = 2 insert 요청 (user + assistant)
- **예시**: 하루 검색 100회, 채팅 200회 = 약 500 요청/일 = 월 15,000 요청

→ **무료 플랜으로 충분합니다!**

---

## 🔐 보안 권장사항

1. **`.env` 파일 보호**
   - `.gitignore`에 포함 확인
   - 절대 Git에 커밋하지 않기

2. **API 키 관리**
   - `anon public` key는 클라이언트 노출 가능 (RLS로 보호)
   - `service_role` key는 **절대** 클라이언트에 노출하지 않기

3. **RLS 정책**
   - 현재는 모든 anon 사용자가 insert 가능
   - 필요 시 더 세밀한 정책 추가 가능

---

## 📚 참고 자료

- [Supabase 공식 문서](https://supabase.com/docs)
- [Supabase Python 클라이언트](https://supabase.com/docs/reference/python)
- [Row Level Security 가이드](https://supabase.com/docs/guides/database/postgres/row-level-security)

---

## 🆚 로컬 vs Cloud 비교

| 항목 | 로컬 Supabase | Cloud Supabase |
|------|--------------|----------------|
| **설정** | Docker + CLI 필요 | 웹 대시보드만 |
| **비용** | 무료 | 무료 플랜 있음 |
| **인터넷** | 불필요 | 필요 |
| **데이터** | 로컬에만 저장 | 클라우드 저장 |
| **속도** | 매우 빠름 | 네트워크 의존 |
| **용도** | 개발/테스트 | 프로덕션/개발 모두 |

**이 가이드는 Cloud Supabase 사용법입니다.**  
로컬 Supabase가 필요하면 `SUPABASE_LOCAL_SETUP.md`를 참고하세요.
