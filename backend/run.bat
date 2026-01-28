@echo off
chcp 65001 >nul
cd /d "%~dp0"

python -c "import fastapi" 2>nul || (
    echo Installing packages...
    python -m pip install -r requirements.txt
)

echo.
echo Server: http://localhost:8000
echo API docs: http://localhost:8000/docs
echo.
python -m uvicorn main:app --reload
pause
