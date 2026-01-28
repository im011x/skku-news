# 구글 뉴스 챗봇

키워드로 **구글 뉴스**를 검색해 최대 10건을 보여주고, **Gemini API**로 요약·대화를 지원합니다.

## 기능

- **뉴스 검색**: 구글 뉴스 RSS 검색 (최신순 / 인기순)
- **결과 요약**: Gemini로 검색 결과 10건 요약
- **뉴스 기반 대화**: 검색 결과를 바탕으로 Gemini와 대화

## 설정

1. **Gemini API 키**  
   [Google AI Studio](https://aistudio.google.com/apikey)에서 발급 후 `backend/.env`에 설정:

   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

2. **의존성 설치**

   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **서버 실행**

   ```bash
   cd backend
   uvicorn main:app --reload
   ```

- **웹 UI**: 브라우저에서 `http://localhost:8000` 접속 (검색·요약·채팅 화면)
- API 문서: `http://localhost:8000/docs`
- 뉴스 검색: `GET /api/news?keyword=키워드&sort=date|sim` (sort: `date`=최신순, `sim`=인기순)
- 대화: `POST /api/chat` Body: `{"message": "질문"}`

## 환경 변수

| 변수 | 설명 |
|------|------|
| `GEMINI_API_KEY` | Gemini API 키 (요약·채팅에 사용) |
| `SUPABASE_URL` | Supabase Project URL (선택, 로그 저장용) |
| `SUPABASE_ANON_KEY` | Supabase anon key (선택) |

GEMINI_API_KEY가 없으면 요약은 폴백 문구, 채팅은 키워드 매칭 폴백으로 동작합니다.

## Supabase Cloud 설정

로컬에서 웹 앱(`localhost:8000`)을 실행하면서 **Supabase Cloud**의 데이터베이스를 사용할 수 있습니다.

### 빠른 설정

1. [Supabase](https://supabase.com) 프로젝트 생성
2. Settings > API에서 **Project URL**과 **anon public key** 복사
3. `backend/.env`에 추가:
   ```env
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_ANON_KEY=eyJ...
   ```
4. Supabase Dashboard > SQL Editor에서 `backend/supabase_schema.sql` 실행
5. 앱 실행 → 뉴스 검색·채팅 시 자동으로 Cloud DB에 저장

**📖 상세 가이드**: [`SUPABASE_CLOUD_SETUP.md`](./SUPABASE_CLOUD_SETUP.md) 참고

> **참고**: 로컬 Supabase(Docker)를 사용하려면 `SUPABASE_LOCAL_SETUP.md`를 참고하세요.

## 버전 관리

GitHub에 프로젝트를 올리고 버전 관리를 시작하려면:

1. **Git 초기화**
   ```powershell
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **GitHub 저장소 생성** 후 연결
   ```powershell
   git remote add origin https://github.com/your-username/repo-name.git
   git push -u origin main
   ```

**📖 상세 가이드**: [`GIT_SETUP.md`](./GIT_SETUP.md) 참고

> ⚠️ **중요**: `.env` 파일은 절대 커밋하지 마세요! `.gitignore`에 포함되어 있습니다.
