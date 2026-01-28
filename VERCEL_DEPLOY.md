# Vercel 배포 가이드

GitHub에 올린 소스코드를 **Vercel**을 통해 배포하는 상세 가이드입니다.

---

## 📋 사전 준비

1. **Vercel 계정**
   - [Vercel](https://vercel.com) 가입/로그인
   - GitHub 계정으로 연동 권장

2. **GitHub 저장소 확인**
   - 저장소가 공개되어 있거나 Vercel과 연동된 경우
   - 현재 저장소: `https://github.com/im011x/skku-news.git`

---

## 1단계: Vercel 설정 파일 생성

프로젝트 루트에 `vercel.json` 파일을 생성합니다. 이 파일은 Vercel이 FastAPI 앱을 어떻게 실행할지 알려줍니다.

### vercel.json 구조

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

**참고**: `api/index.py`는 Vercel serverless 함수 handler로, `backend/main.py`의 FastAPI 앱을 import합니다.

---

## 2단계: CORS 설정 업데이트

Vercel 배포 후 도메인을 허용하도록 `backend/main.py`의 CORS 설정을 업데이트해야 합니다.

**현재 설정:**
```python
allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"]
```

**Vercel 배포용으로 변경:**
```python
allow_origins=["*"]  # 또는 특정 Vercel 도메인만 허용
```

또는 환경 변수로 관리:
```python
import os
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
allow_origins=ALLOWED_ORIGINS
```

---

## 3단계: Vercel 대시보드에서 프로젝트 연결

### 방법 1: GitHub 연동 (권장)

1. [Vercel Dashboard](https://vercel.com/dashboard) 접속
2. **Add New...** → **Project** 클릭
3. **Import Git Repository** 선택
4. GitHub 저장소 `im011x/skku-news` 선택
5. **Import** 클릭

### 방법 2: Vercel CLI 사용

```powershell
# Vercel CLI 설치
npm install -g vercel

# 프로젝트 디렉토리로 이동
cd c:\2999.edu\SKKU\Track4\chatbot2

# Vercel 로그인
vercel login

# 배포
vercel

# 프로덕션 배포
vercel --prod
```

---

## 4단계: 프로젝트 설정

Vercel 대시보드에서 프로젝트를 연결한 후:

### 기본 설정

1. **Framework Preset**: `Other` 선택
2. **Root Directory**: (비워둠 - 프로젝트 루트 사용)
3. **Build Command**: (비워둠 - Vercel이 자동으로 `requirements.txt`를 인식)
4. **Output Directory**: (비워둠)
5. **Install Command**: (비워둠 - 자동 인식)

### 환경 변수 설정

**Settings** → **Environment Variables**에서 다음 변수 추가:

| 변수명 | 값 | 설명 |
|--------|-----|------|
| `GEMINI_API_KEY` | `your_gemini_api_key_here` | Gemini API 키 (필수) |
| `SUPABASE_URL` | `https://xxxxx.supabase.co` | Supabase URL (선택) |
| `SUPABASE_ANON_KEY` | `eyJ...` | Supabase anon key (선택) |

**참고**: Python 버전은 Vercel이 자동으로 감지합니다. 명시적으로 설정하려면 `PYTHON_VERSION` 환경 변수를 추가할 수 있습니다.

**⚠️ 중요**: 
- 환경 변수는 **Production**, **Preview**, **Development** 각각 설정 가능
- 민감한 정보는 절대 코드에 포함하지 말고 환경 변수로만 관리

---

## 5단계: 배포 실행

### 자동 배포 (GitHub 연동 시)

1. GitHub에 코드 푸시
2. Vercel이 자동으로 감지하여 배포 시작
3. 배포 완료 후 URL 제공

### 수동 배포

Vercel 대시보드에서:
1. **Deployments** 탭
2. **Redeploy** 클릭

---

## 6단계: 배포 확인

### 배포 URL 확인

배포 완료 후 Vercel이 제공하는 URL:
- 예: `https://skku-news.vercel.app`
- 또는 커스텀 도메인 설정 가능

### 테스트

1. **웹 UI**: `https://your-app.vercel.app/` 접속
2. **API 문서**: `https://your-app.vercel.app/docs`
3. **뉴스 검색**: `https://your-app.vercel.app/api/news?keyword=테스트&sort=date`

---

## 7단계: 커스텀 도메인 설정 (선택)

1. Vercel 대시보드 → **Settings** → **Domains**
2. 도메인 추가
3. DNS 설정 안내에 따라 도메인 제공업체에서 설정

---

## 🔧 문제 해결

### 문제 1: 모듈을 찾을 수 없음

**에러**: `ModuleNotFoundError: No module named 'xxx'`

**해결**:
- `requirements.txt`에 모든 의존성이 포함되어 있는지 확인
- Vercel이 자동으로 `requirements.txt`를 인식하여 설치

### 문제 2: 정적 파일을 찾을 수 없음

**에러**: CSS/JS 파일이 로드되지 않음

**해결**:
- `backend/main.py`에서 `STATIC_DIR` 경로 확인
- Vercel 배포 시 경로가 올바르게 설정되었는지 확인

### 문제 3: CORS 오류

**에러**: `Access to fetch at '...' from origin '...' has been blocked by CORS policy`

**해결**:
- `backend/main.py`의 CORS 설정 업데이트
- Vercel 도메인을 `allow_origins`에 추가

### 문제 4: 환경 변수가 로드되지 않음

**에러**: API 키가 작동하지 않음

**해결**:
- Vercel 대시보드에서 환경 변수 확인
- 변수명이 정확한지 확인 (대소문자 구분)
- 배포 후 재배포 필요할 수 있음

---

## 📝 배포 후 체크리스트

- [ ] 웹 UI가 정상적으로 로드됨
- [ ] 뉴스 검색 기능 작동
- [ ] Gemini API 요약 기능 작동 (API 키 설정 시)
- [ ] 채팅 기능 작동
- [ ] Supabase 로그 저장 작동 (설정 시)
- [ ] API 문서 (`/docs`) 접근 가능
- [ ] CORS 오류 없음

---

## 🔄 지속적 배포 (CI/CD)

GitHub에 푸시할 때마다 자동으로 배포되도록 설정:

1. Vercel 대시보드 → **Settings** → **Git**
2. **Production Branch**: `main` 설정
3. 이후 `main` 브랜치에 푸시하면 자동 배포

---

## 📚 참고 자료

- [Vercel 공식 문서](https://vercel.com/docs)
- [Vercel Python 런타임](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python)
- [FastAPI 배포 가이드](https://fastapi.tiangolo.com/deployment/)

---

## ⚠️ 주의사항

1. **환경 변수 보안**
   - 절대 코드에 API 키를 하드코딩하지 마세요
   - Vercel 환경 변수로만 관리

2. **무료 플랜 제한**
   - Vercel 무료 플랜은 제한이 있습니다
   - 사용량 확인: Vercel 대시보드 → **Usage**

3. **Cold Start**
   - Serverless 함수는 첫 요청 시 지연될 수 있습니다
   - 프로덕션에서는 Keep-alive 설정 고려

---

## 🎉 완료!

배포가 완료되면 GitHub에 푸시할 때마다 자동으로 Vercel에 배포됩니다!
