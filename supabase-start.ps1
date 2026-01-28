# Supabase 로컬 시작 스크립트
Write-Host "Supabase 로컬 시작 중..." -ForegroundColor Cyan

# Supabase 초기화 (이미 되어 있으면 스킵)
if (-not (Test-Path "supabase")) {
    Write-Host "Supabase 초기화 중..." -ForegroundColor Yellow
    npx supabase init
}

# Supabase 시작
Write-Host "`nSupabase 시작 중 (Docker 필요)..." -ForegroundColor Yellow
npx supabase start

Write-Host "`n✅ Supabase가 시작되었습니다!" -ForegroundColor Green
Write-Host "`n다음 정보를 backend/.env에 추가하세요:" -ForegroundColor Cyan
Write-Host "  SUPABASE_URL=http://localhost:54321" -ForegroundColor White
Write-Host "  SUPABASE_ANON_KEY=(supabase status 명령으로 확인)" -ForegroundColor White
Write-Host "`n현재 상태 확인: npx supabase status" -ForegroundColor Gray
Write-Host "Studio (웹 UI): http://localhost:54323" -ForegroundColor Gray
