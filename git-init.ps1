# Git 초기화 및 첫 커밋 스크립트

Write-Host "Git 저장소 초기화 중..." -ForegroundColor Cyan

# Git 설치 확인
try {
    $gitVersion = git --version
    Write-Host "Git 버전: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Git이 설치되어 있지 않습니다." -ForegroundColor Red
    Write-Host "다운로드: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# 현재 디렉토리 확인
$currentDir = Get-Location
Write-Host "`n작업 디렉토리: $currentDir" -ForegroundColor Gray

# Git 초기화 (이미 있으면 스킵)
if (Test-Path ".git") {
    Write-Host "`n이미 Git 저장소가 초기화되어 있습니다." -ForegroundColor Yellow
} else {
    git init
    Write-Host "`nGit 저장소 초기화 완료" -ForegroundColor Green
}

# .gitignore 확인
if (-not (Test-Path ".gitignore")) {
    Write-Host "WARNING: .gitignore 파일이 없습니다." -ForegroundColor Yellow
}

# 상태 확인
Write-Host "`n현재 상태:" -ForegroundColor Cyan
git status

Write-Host "`n다음 단계:" -ForegroundColor Yellow
Write-Host "1. git add ." -ForegroundColor White
Write-Host "2. git commit -m 'Initial commit'" -ForegroundColor White
Write-Host "3. GitHub에서 저장소 생성 후:" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/username/repo.git" -ForegroundColor Gray
Write-Host "   git push -u origin main" -ForegroundColor Gray
