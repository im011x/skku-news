# Supabase 상태 확인 및 .env 업데이트 도우미
Write-Host "Supabase 상태 확인 중..." -ForegroundColor Cyan
Write-Host ""

$status = npx supabase status 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host $status -ForegroundColor Green
    
    # API URL 추출
    $apiUrl = ($status | Select-String -Pattern "API URL:\s+(.+)").Matches.Groups[1].Value
    $anonKey = ($status | Select-String -Pattern "anon key:\s+(.+)").Matches.Groups[1].Value
    
    if ($apiUrl -and $anonKey) {
        Write-Host "`n📋 backend/.env에 추가할 내용:" -ForegroundColor Yellow
        Write-Host "SUPABASE_URL=$apiUrl" -ForegroundColor White
        Write-Host "SUPABASE_ANON_KEY=$anonKey" -ForegroundColor White
        
        $update = Read-Host "`n.env 파일을 자동으로 업데이트하시겠습니까? (y/n)"
        if ($update -eq "y" -or $update -eq "Y") {
            $envFile = "backend\.env"
            if (Test-Path $envFile) {
                $content = Get-Content $envFile -Raw
                
                # SUPABASE_URL 업데이트 또는 추가
                if ($content -match "SUPABASE_URL=") {
                    $content = $content -replace "SUPABASE_URL=.*", "SUPABASE_URL=$apiUrl"
                } else {
                    $content += "`nSUPABASE_URL=$apiUrl"
                }
                
                # SUPABASE_ANON_KEY 업데이트 또는 추가
                if ($content -match "SUPABASE_ANON_KEY=") {
                    $content = $content -replace "SUPABASE_ANON_KEY=.*", "SUPABASE_ANON_KEY=$anonKey"
                } else {
                    $content += "`nSUPABASE_ANON_KEY=$anonKey"
                }
                
                Set-Content -Path $envFile -Value $content.Trim()
                Write-Host "✅ .env 파일이 업데이트되었습니다!" -ForegroundColor Green
            } else {
                Write-Host "⚠️  backend/.env 파일이 없습니다. 수동으로 추가해주세요." -ForegroundColor Yellow
            }
        }
    }
} else {
    Write-Host "❌ Supabase가 실행 중이지 않습니다." -ForegroundColor Red
    Write-Host "   먼저 '.\supabase-start.ps1' 또는 'npx supabase start'를 실행하세요." -ForegroundColor Yellow
}
