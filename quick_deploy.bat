@echo off
echo ========================================
echo Quick Deploy Script
echo ========================================
echo.

REM Check if git is installed
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Git is NOT installed!
    echo.
    echo Please choose an option:
    echo.
    echo 1. Install Git now (recommended)
    echo 2. Use GitHub Desktop
    echo 3. Manual upload instructions
    echo.
    choice /C 123 /N /M "Enter your choice (1, 2, or 3): "
    
    if errorlevel 3 goto manual
    if errorlevel 2 goto desktop
    if errorlevel 1 goto install
)

:gitpush
echo Git is installed!
echo.
echo Adding files...
git add .

echo.
echo Committing...
git commit -m "Fix parameter extraction"

echo.
echo Pushing to GitHub...
git push origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo SUCCESS! Changes pushed to GitHub
    echo ========================================
    echo.
    echo Render will auto-deploy in 2-3 minutes
    echo Check: https://dashboard.render.com
) else (
    echo.
    echo Push failed! See error above.
)
goto end

:install
echo.
echo Installing Git...
winget install Git.Git
echo.
echo Git installed! Please restart this script.
goto end

:desktop
echo.
echo Opening GitHub Desktop download page...
start https://desktop.github.com
echo.
echo After installing:
echo 1. Open GitHub Desktop
echo 2. File - Add Local Repository
echo 3. Select this folder
echo 4. Commit and Push
goto end

:manual
echo.
echo Manual Upload Instructions:
echo ========================================
echo 1. Go to your GitHub repository
echo 2. Click on api_server.py
echo 3. Click Edit (pencil icon)
echo 4. Copy content from your local file
echo 5. Paste and commit
echo ========================================
goto end

:end
echo.
pause
