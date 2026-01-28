# GitHub 푸시 스크립트
# Git lock 파일 문제 해결 후 커밋 및 푸시

Write-Host "🔄 Git lock 파일 확인 및 제거..." -ForegroundColor Yellow

# Git lock 파일 제거 시도
$lockFile = ".git\index.lock"
if (Test-Path $lockFile) {
    Write-Host "⚠️  Lock 파일 발견. 제거 시도 중..." -ForegroundColor Yellow
    try {
        Remove-Item $lockFile -Force
        Write-Host "✅ Lock 파일 제거 완료" -ForegroundColor Green
        Start-Sleep -Seconds 2
    } catch {
        Write-Host "❌ Lock 파일 제거 실패. 다른 Git 프로세스가 실행 중일 수 있습니다." -ForegroundColor Red
        Write-Host "   다음을 확인하세요:" -ForegroundColor Yellow
        Write-Host "   1. VS Code, Cursor, Git GUI 등 모든 Git 관련 프로그램 종료" -ForegroundColor Yellow
        Write-Host "   2. 작업 관리자에서 git.exe 프로세스 확인" -ForegroundColor Yellow
        Write-Host "   3. 수동으로 lock 파일 제거: Remove-Item .git\index.lock -Force" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host "`n📋 변경사항 확인 중..." -ForegroundColor Cyan
git status

Write-Host "`n➕ 모든 변경사항 스테이징 중..." -ForegroundColor Yellow
git add .

Write-Host "`n💾 커밋 중..." -ForegroundColor Yellow
git commit -m "feat: Vercel 배포 설정 및 자동 커밋 기능 추가

- Vercel 배포 설정 완료 (api/index.py, vercel.json, requirements.txt)
- Cursor 자동 커밋 규칙 추가
- 자동 커밋 PowerShell 스크립트 추가
- CORS 설정 업데이트 (Vercel 환경 대응)
- 환경 변수 로딩 개선 (Vercel 환경 대응)"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 커밋 실패!" -ForegroundColor Red
    exit 1
}

Write-Host "`n🚀 GitHub에 푸시 중..." -ForegroundColor Yellow
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ GitHub 푸시 완료!" -ForegroundColor Green
} else {
    Write-Host "`n⚠️  푸시 실패. 네트워크 연결을 확인하세요." -ForegroundColor Yellow
    exit 1
}
