# 구글 뉴스 챗봇 백엔드 실행
Set-Location $PSScriptRoot

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python이 설치되어 있지 않습니다."
    exit 1
}

# 의존성 설치 (없으면)
python -c "import fastapi" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "패키지 설치 중..."
    python -m pip install -r requirements.txt
}

Write-Host "서버 시작: http://localhost:8000"
Write-Host "API 문서: http://localhost:8000/docs"
python -m uvicorn main:app --reload
