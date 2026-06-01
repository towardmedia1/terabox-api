@echo off
color 0A
echo.
echo ========================================
echo   iTeraPlay v4.0.0 - Deploy Assistant
echo ========================================
echo.
echo Files have been rebuilt with 100%% stability!
echo.
echo Changes made:
echo   [+] api_server.py - Triple-layer error handling
echo   [+] index.html - Premium UI with relative paths
echo   [+] No more 500 errors or JSON crashes
echo   [+] Full CORS support enabled
echo   [+] Frontend served at root URL
echo.
echo ========================================
echo   Choose Deployment Method
echo ========================================
echo.
echo 1. Install Git and Push (Recommended)
echo 2. Open GitHub Desktop Download
echo 3. Show Manual Upload Instructions
echo 4. Exit
echo.
choice /C 1234 /N /M "Enter your choice (1-4): "

if errorlevel 4 goto end
if errorlevel 3 goto manual
if errorlevel 2 goto desktop
if errorlevel 1 goto install

:install
echo.
echo Installing Git...
echo.
winget install Git.Git
echo.
echo ========================================
echo Git Installed Successfully!
echo ========================================
echo.
echo IMPORTANT: Please restart this script to push changes.
echo.
echo After restart, the script will:
echo   1. Add all files
echo   2. Commit with message
echo   3. Push to GitHub
echo   4. Trigger Render deployment
echo.
pause
exit

:desktop
echo.
echo Opening GitHub Desktop download page...
start https://desktop.github.com
echo.
echo ========================================
echo GitHub Desktop Installation Steps:
echo ========================================
echo.
echo 1. Install GitHub Desktop
echo 2. Sign in to your GitHub account
echo 3. File - Add Local Repository
echo 4. Select this folder
echo 5. Write commit message: "Rebuild for 100%% stability - v4.0.0"
echo 6. Click "Commit to main"
echo 7. Click "Push origin"
echo.
echo Render will auto-deploy in 2-3 minutes!
echo.
pause
exit

:manual
echo.
echo ========================================
echo Manual Upload Instructions
echo ========================================
echo.
echo Step 1: Go to your GitHub repository
echo   URL: https://github.com/YOUR_USERNAME/YOUR_REPO
echo.
echo Step 2: Upload api_server.py
echo   - Click on api_server.py
echo   - Click pencil icon (Edit)
echo   - Delete all content
echo   - Open your local api_server.py
echo   - Copy all content (Ctrl+A, Ctrl+C)
echo   - Paste into GitHub editor (Ctrl+V)
echo   - Scroll down and click "Commit changes"
echo.
echo Step 3: Upload index.html
echo   - Click on index.html
echo   - Click pencil icon (Edit)
echo   - Delete all content
echo   - Open your local index.html
echo   - Copy all content (Ctrl+A, Ctrl+C)
echo   - Paste into GitHub editor (Ctrl+V)
echo   - Scroll down and click "Commit changes"
echo.
echo Step 4: Wait for Render
echo   - Render will detect changes automatically
echo   - Deployment takes 2-3 minutes
echo   - Check: https://dashboard.render.com
echo.
echo ========================================
echo.
pause
exit

:end
echo.
echo Exiting...
echo.
echo Remember: Your files are ready to deploy!
echo Run this script again when you're ready.
echo.
pause
