@echo off
echo ========================================
echo Terabox API - Git Deployment Script
echo ========================================
echo.

REM Check if git is installed
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Git is not installed!
    echo.
    echo Please install Git from: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo [1/5] Checking git status...
git status

echo.
echo [2/5] Adding all files...
git add .

echo.
echo [3/5] Committing changes...
git commit -m "Update: CORS enabled for frontend, cookie-free API ready"

echo.
echo [4/5] Pushing to GitHub...
git push origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo SUCCESS! Deployment pushed to GitHub
    echo ========================================
    echo.
    echo Render will automatically detect the changes
    echo and redeploy your API in 2-3 minutes.
    echo.
    echo Check deployment status at:
    echo https://dashboard.render.com
    echo.
) else (
    echo.
    echo ========================================
    echo ERROR: Push failed!
    echo ========================================
    echo.
    echo Possible reasons:
    echo 1. Not connected to GitHub repository
    echo 2. No internet connection
    echo 3. Authentication required
    echo.
    echo To setup GitHub:
    echo   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
    echo   git branch -M main
    echo   git push -u origin main
    echo.
)

pause
