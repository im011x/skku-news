# 로컬에서 Supabase 사용하기 - 상세 가이드

로컬 개발 환경에서 **Supabase Local**을 사용해 PostgreSQL, Auth, Storage 등을 Docker로 실행하는 방법입니다.

---

## ⚡ 빠른 시작 (5분)

```powershell
# 1. Docker Desktop 실행 확인

# 2. Supabase 시작
.\supabase-start.ps1

# 3. 상태 확인 및 .env 자동 설정
.\supabase-status.ps1

# 4. Supabase Studio에서 스키마 실행
# http://localhost:54323 접속 → SQL Editor → supabase_schema.sql 실행

# 5. FastAPI 실행
cd backend
uvicorn main:app --reload
```

**완료!** 이제 뉴스 검색·채팅 시 데이터가 Supabase에 저장됩니다.

---

---

## 📋 사전 요구사항

1. **Docker Desktop** (또는 Rancher Desktop, Podman, OrbStack)
   - [Docker Desktop 다운로드](https://www.docker.com/products/docker-desktop/)
   - 설치 후 실행 확인: `docker --version`

2. **Node.js 20+** (Supabase CLI 필요)
   - [Node.js 다운로드](https://nodejs.org/)
   - 설치 확인: `node --version`

---

## 1단계: Supabase CLI 설치

### Windows (PowerShell)

```powershell
# npm으로 전역 설치
npm install -g supabase

# 설치 확인
supabase --version
```

### 또는 npx로 실행 (설치 없이)

```powershell
# 프로젝트별로 사용 (권장)
npx supabase --version
```

---

## 2단계: 프로젝트 초기화

프로젝트 루트에서 실행:

```powershell
cd c:\2999.edu\SKKU\Track4\chatbot2

# Supabase 초기화 (supabase 폴더 생성)
npx supabase init
```

이 명령은 다음을 생성합니다:
- `supabase/` 폴더
  - `config.toml` - Supabase 설정
  - `migrations/` - DB 마이그레이션
  - `seed.sql` - 초기 데이터 (선택)

---

## 3단계: 로컬 Supabase 시작

```powershell
# Docker로 Supabase 로컬 스택 시작 (PostgreSQL, Auth, Storage 등)
npx supabase start
```

**처음 실행 시** Docker 이미지를 다운로드하므로 시간이 걸립니다 (5-10분).

**성공 시 출력 예시:**
```
Started supabase local development setup.

         API URL: http://localhost:54321
     GraphQL URL: http://localhost:54321/graphql/v1
          DB URL: postgresql://postgres:postgres@localhost:54322/postgres
      Studio URL: http://localhost:54323
    Inbucket URL: http://localhost:54324
      JWT secret: super-secret-jwt-token-with-at-least-32-characters-long
        anon key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0
service_role key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU
```

**중요 정보:**
- **API URL**: `http://localhost:54321` ← 이것을 `SUPABASE_URL`에 사용
- **anon key**: `eyJ...` ← 이것을 `SUPABASE_ANON_KEY`에 사용

---

## 4단계: 환경 변수 설정

`backend/.env` 파일에 로컬 Supabase 정보 추가:

```env
# 기존 설정
GEMINI_API_KEY=your_gemini_api_key_here

# 로컬 Supabase 설정 (supabase start 출력에서 복사)
SUPABASE_URL=http://localhost:54321
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0
```

> **참고**: `supabase start` 출력의 **anon key**를 그대로 복사하세요. 위 예시는 데모용이며 실제 키는 다릅니다.

---

## 5단계: 데이터베이스 스키마 생성

### 방법 A: Supabase Studio (웹 UI)

1. **Supabase Studio 열기**
   ```
   http://localhost:54323
   ```
   브라우저에서 위 URL 접속 (Studio는 로컬 Supabase 관리 UI)

2. **SQL Editor 열기**
   - 왼쪽 메뉴에서 **SQL Editor** 클릭
   - **New query** 클릭

3. **스키마 실행**
   - `backend/supabase_schema.sql` 파일 내용을 복사
   - SQL Editor에 붙여넣기
   - **Run** 버튼 클릭

### 방법 B: Supabase CLI (터미널)

```powershell
# 마이그레이션 파일로 생성
npx supabase migration new create_news_tables

# 생성된 파일 (supabase/migrations/xxxxx_create_news_tables.sql)에
# supabase_schema.sql 내용 복사

# 마이그레이션 실행
npx supabase migration up
```

### 방법 C: 직접 psql 연결

```powershell
# PostgreSQL에 직접 연결
npx supabase db reset

# 또는 psql 직접 사용
psql postgresql://postgres:postgres@localhost:54322/postgres -f backend/supabase_schema.sql
```

---

## 6단계: 테이블 확인

### Supabase Studio에서 확인

1. `http://localhost:54323` 접속
2. 왼쪽 메뉴 **Table Editor** 클릭
3. `news_searches`, `chat_messages` 테이블이 보이는지 확인

### 또는 SQL로 확인

```sql
-- Supabase Studio > SQL Editor에서 실행
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';
```

---

## 7단계: FastAPI 앱 실행 및 테스트

```powershell
cd backend

# 의존성 설치 (supabase 포함)
pip install -r requirements.txt

# 서버 실행
uvicorn main:app --reload
```

**테스트:**
1. 브라우저에서 `http://localhost:8000` 접속
2. 키워드로 뉴스 검색
3. 채팅 메시지 전송
4. Supabase Studio (`http://localhost:54323`) > Table Editor에서 데이터 확인

---

## 📊 데이터 확인 방법

### Supabase Studio

1. `http://localhost:54323` 접속
2. **Table Editor** → `news_searches` 또는 `chat_messages` 선택
3. 행(Row) 데이터 확인

### SQL 쿼리

```sql
-- 최근 검색 10건
SELECT * FROM news_searches ORDER BY created_at DESC LIMIT 10;

-- 최근 채팅 메시지 20건
SELECT * FROM chat_messages ORDER BY created_at DESC LIMIT 20;

-- 키워드별 검색 통계
SELECT keyword, COUNT(*) as count 
FROM news_searches 
GROUP BY keyword 
ORDER BY count DESC;
```

---

## 🔧 유용한 명령어

### CLI 명령어

```powershell
# Supabase 상태 확인
npx supabase status

# Supabase 중지 (Docker 컨테이너 종료)
npx supabase stop

# Supabase 재시작
npx supabase restart

# 로그 확인
npx supabase logs

# DB 리셋 (모든 데이터 삭제)
npx supabase db reset

# DB 백업
npx supabase db dump -f backup.sql

# DB 복원
npx supabase db restore backup.sql
```

### 편의 스크립트 (프로젝트 루트에 포함)

```powershell
# Supabase 시작
.\supabase-start.ps1

# Supabase 중지
.\supabase-stop.ps1

# 상태 확인 및 .env 자동 업데이트
.\supabase-status.ps1
```

---

## 🐛 문제 해결

### Docker가 실행되지 않음

```powershell
# Docker Desktop 실행 확인
docker ps

# Docker 재시작 후
npx supabase start
```

### 포트 충돌

`supabase start`가 실패하면 포트가 이미 사용 중일 수 있습니다.

```powershell
# 사용 중인 포트 확인 (Windows)
netstat -ano | findstr :54321
netstat -ano | findstr :54322
netstat -ano | findstr :54323

# config.toml에서 포트 변경 가능
# supabase/config.toml 편집
```

### 테이블이 보이지 않음

1. SQL Editor에서 스키마가 실행되었는지 확인
2. Table Editor에서 새로고침
3. `npx supabase db reset` 후 재실행

### 연결 오류

- `.env`의 `SUPABASE_URL`이 `http://localhost:54321`인지 확인
- `supabase status`로 현재 anon key 확인 후 `.env` 업데이트

---

## 📝 로컬 vs Cloud 비교

| 항목 | 로컬 (Local) | Cloud |
|------|-------------|-------|
| **설정** | Docker + CLI 필요 | 웹 대시보드만 |
| **비용** | 무료 | 무료 플랜 있음 |
| **인터넷** | 불필요 | 필요 |
| **데이터** | 로컬에만 저장 | 클라우드 저장 |
| **속도** | 매우 빠름 | 네트워크 의존 |
| **용도** | 개발/테스트 | 프로덕션 |

---

## 🚀 다음 단계

로컬에서 테스트 완료 후, 프로덕션 배포 시:

1. [Supabase Cloud](https://supabase.com) 프로젝트 생성
2. Cloud 프로젝트의 URL·anon key를 `.env`에 설정
3. 동일한 스키마(`supabase_schema.sql`)를 Cloud SQL Editor에서 실행
4. 코드 변경 없이 Cloud Supabase 사용 가능

---

## 📚 참고 자료

- [Supabase Local Development 공식 문서](https://supabase.com/docs/guides/local-development)
- [Supabase CLI 문서](https://supabase.com/docs/reference/cli)
- [Supabase Python 클라이언트](https://supabase.com/docs/reference/python)
