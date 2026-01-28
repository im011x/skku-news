# GitHub 버전 관리 설정 가이드

프로젝트를 GitHub에 올리고 버전 관리를 시작하는 방법입니다.

---

## 📋 사전 준비

1. **Git 설치 확인**
   ```powershell
   git --version
   ```
   설치되어 있지 않으면: [Git 다운로드](https://git-scm.com/download/win)

2. **GitHub 계정**
   - [GitHub](https://github.com) 가입/로그인

---

## 1단계: Git 저장소 초기화

프로젝트 루트에서 실행:

```powershell
cd c:\2999.edu\SKKU\Track4\chatbot2

# Git 초기화
git init

# 현재 상태 확인
git status
```

---

## 2단계: 첫 커밋

```powershell
# 모든 파일 추가 ( .gitignore에 제외된 파일은 자동 제외)
git add .

# 커밋 메시지와 함께 첫 커밋
git commit -m "Initial commit: 구글 뉴스 챗봇 프로젝트

- 구글 뉴스 RSS 검색 기능
- Gemini API를 이용한 요약 및 채팅
- Supabase Cloud 연동
- 웹 UI (HTML/CSS/JS)
- FastAPI 백엔드"
```

---

## 3단계: GitHub 저장소 생성

1. [GitHub](https://github.com) 접속
2. 오른쪽 상단 **+** → **New repository** 클릭
3. 저장소 정보 입력:
   - **Repository name**: `news-chatbot` (또는 원하는 이름)
   - **Description**: "구글 뉴스 검색 및 Gemini 기반 챗봇"
   - **Visibility**: Public 또는 Private 선택
   - **Initialize this repository with**: 체크하지 않기 (이미 로컬에 파일 있음)
4. **Create repository** 클릭

---

## 4단계: GitHub에 연결 및 푸시

GitHub에서 생성된 저장소 페이지에 표시된 명령어를 사용하거나:

```powershell
# GitHub 저장소 URL (예시)
# https://github.com/your-username/news-chatbot.git

# 원격 저장소 추가 (your-username과 저장소 이름을 실제 값으로 변경)
git remote add origin https://github.com/your-username/news-chatbot.git

# 기본 브랜치 이름을 main으로 설정
git branch -M main

# GitHub에 푸시
git push -u origin main
```

**인증:**
- GitHub에서 Personal Access Token 사용 (권장)
- 또는 GitHub Desktop 사용

---

## 5단계: Personal Access Token 생성 (필요 시)

GitHub에서 인증이 필요하면:

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. **Generate new token (classic)** 클릭
3. **Note**: "news-chatbot" 등 설명 입력
4. **Expiration**: 원하는 기간 선택
5. **Scopes**: `repo` 체크
6. **Generate token** 클릭
7. **토큰 복사** (한 번만 표시됨!)

**푸시 시:**
- Username: GitHub 사용자명
- Password: Personal Access Token (비밀번호 아님!)

---

## 🔄 이후 작업 흐름

### 변경사항 커밋 및 푸시

```powershell
# 변경된 파일 확인
git status

# 변경사항 추가
git add .

# 또는 특정 파일만
git add backend/main.py

# 커밋
git commit -m "기능 추가: DB 저장 로그 표시"

# GitHub에 푸시
git push
```

### 커밋 메시지 예시

```
feat: Supabase 연동 추가
fix: RLS 정책 오류 수정
docs: README 업데이트
style: CSS 스타일 개선
refactor: 코드 리팩토링
```

---

## 📁 커밋하지 말아야 할 파일

`.gitignore`에 포함된 파일은 자동으로 제외됩니다:

- ✅ `.env` - API 키 포함 (절대 커밋 금지!)
- ✅ `__pycache__/` - Python 캐시
- ✅ `*.pyc` - 컴파일된 파일

**확인:**
```powershell
git status
```

`.env` 파일이 목록에 나타나지 않아야 합니다!

---

## 🔍 유용한 Git 명령어

```powershell
# 상태 확인
git status

# 변경 이력 확인
git log

# 원격 저장소 확인
git remote -v

# 브랜치 목록
git branch

# 최근 커밋 취소 (파일은 유지)
git reset --soft HEAD~1

# 특정 파일 커밋에서 제거 (파일은 유지)
git reset HEAD 파일명
```

---

## ⚠️ 주의사항

1. **`.env` 파일 절대 커밋 금지**
   - API 키가 노출되면 보안 위험
   - `.gitignore`에 포함되어 있지만 확인 필수

2. **민감한 정보 확인**
   ```powershell
   # 커밋 전 확인
   git diff
   ```

3. **대용량 파일**
   - 100MB 이상 파일은 Git LFS 사용 고려

---

## 🆘 문제 해결

### 이미 `.env`를 커밋한 경우

```powershell
# Git 히스토리에서 .env 제거
git rm --cached backend/.env
git commit -m "Remove .env from repository"
git push
```

그리고 GitHub에서 `.env` 파일을 삭제하거나, API 키를 재발급하세요.

### 푸시 거부 오류

```powershell
# 원격 저장소 강제 업데이트 (주의: 다른 사람과 협업 시 사용 금지)
git push -f origin main
```

---

## 📚 참고 자료

- [Git 공식 문서](https://git-scm.com/doc)
- [GitHub 가이드](https://docs.github.com)
- [Git 커밋 메시지 컨벤션](https://www.conventionalcommits.org)
