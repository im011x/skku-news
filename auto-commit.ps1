# 자동 커밋 및 푸시 스크립트
# 사용법: .\auto-commit.ps1 "커밋 메시지"

param(
    [Parameter(Mandatory=$false)]
    [string]$Message = "자동 커밋: 소스 코드 업데이트"
)

$ErrorActionPreference = "Stop"

Write-Host "🔄 자동 커밋 및 푸시 시작..." -ForegroundColor Cyan

# Git 상태 확인
Write-Host "`n📋 변경사항 확인 중..." -ForegroundColor Yellow
$status = git status --porcelain

if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "✅ 커밋할 변경사항이 없습니다." -ForegroundColor Green
    exit 0
}

# 변경된 파일 표시
Write-Host "`n📝 변경된 파일:" -ForegroundColor Yellow
git status --short

# 모든 변경사항 추가
Write-Host "`n➕ 변경사항 스테이징 중..." -ForegroundColor Yellow
git add .

# 커밋
Write-Host "`n💾 커밋 중..." -ForegroundColor Yellow
git commit -m $Message

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 커밋 실패!" -ForegroundColor Red
    exit 1
}

# GitHub에 푸시
Write-Host "`n🚀 GitHub에 푸시 중..." -ForegroundColor Yellow
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ 자동 커밋 및 푸시 완료!" -ForegroundColor Green
} else {
    Write-Host "`n⚠️  푸시 실패. 수동으로 확인해주세요: git push" -ForegroundColor Yellow
    exit 1
}
