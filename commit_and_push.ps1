# PowerShell script to commit and push changes to GitHub
# Run: .\commit_and_push.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Git Commit and Push Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
$gitInstalled = Get-Command git -ErrorAction SilentlyContinue

if (-not $gitInstalled) {
    Write-Host "ERROR: Git is not installed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Git first:" -ForegroundColor Yellow
    Write-Host "  Option 1: winget install Git.Git" -ForegroundColor White
    Write-Host "  Option 2: Download from https://git-scm.com/download/win" -ForegroundColor White
    Write-Host ""
    Write-Host "After installation, restart PowerShell and run this script again." -ForegroundColor Yellow
    Write-Host ""
    
    # Ask if user wants to install Git now
    $install = Read-Host "Install Git now using winget? (y/n)"
    if ($install -eq "y" -or $install -eq "Y") {
        Write-Host "Installing Git..." -ForegroundColor Green
        winget install Git.Git
        Write-Host ""
        Write-Host "Git installed! Please restart PowerShell and run this script again." -ForegroundColor Green
    }
    
    pause
    exit 1
}

Write-Host "✓ Git is installed" -ForegroundColor Green
Write-Host ""

# Check if this is a git repository
if (-not (Test-Path ".git")) {
    Write-Host "This is not a Git repository yet." -ForegroundColor Yellow
    Write-Host ""
    $init = Read-Host "Initialize Git repository? (y/n)"
    
    if ($init -eq "y" -or $init -eq "Y") {
        Write-Host "Initializing Git repository..." -ForegroundColor Green
        git init
        git branch -M main
        Write-Host "✓ Git repository initialized" -ForegroundColor Green
        Write-Host ""
        
        # Ask for remote URL
        Write-Host "Enter your GitHub repository URL:" -ForegroundColor Yellow
        Write-Host "Example: https://github.com/username/repo.git" -ForegroundColor Gray
        $remoteUrl = Read-Host "URL"
        
        if ($remoteUrl) {
            git remote add origin $remoteUrl
            Write-Host "✓ Remote added: $remoteUrl" -ForegroundColor Green
        }
    } else {
        Write-Host "Exiting..." -ForegroundColor Yellow
        pause
        exit 0
    }
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Changes to be committed:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Show status
git status --short

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Commit Message" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Default commit message
$defaultMessage = "Serve frontend from API, update CORS, use relative URLs"
Write-Host "Default message: $defaultMessage" -ForegroundColor Gray
Write-Host ""
$customMessage = Read-Host "Enter commit message (or press Enter for default)"

if ([string]::IsNullOrWhiteSpace($customMessage)) {
    $commitMessage = $defaultMessage
} else {
    $commitMessage = $customMessage
}

Write-Host ""
Write-Host "Committing with message: $commitMessage" -ForegroundColor Green
Write-Host ""

# Add all changes
Write-Host "[1/3] Adding files..." -ForegroundColor Yellow
git add .

# Commit
Write-Host "[2/3] Committing..." -ForegroundColor Yellow
git commit -m $commitMessage

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Commit failed!" -ForegroundColor Red
    Write-Host "This might mean there are no changes to commit." -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

# Push
Write-Host "[3/3] Pushing to GitHub..." -ForegroundColor Yellow
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "SUCCESS! Changes pushed to GitHub" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "✓ Files committed and pushed" -ForegroundColor Green
    Write-Host "✓ GitHub will notify Render" -ForegroundColor Green
    Write-Host "✓ Render will auto-deploy in 2-3 minutes" -ForegroundColor Green
    Write-Host ""
    Write-Host "Check deployment status at:" -ForegroundColor Cyan
    Write-Host "https://dashboard.render.com" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "ERROR: Push failed!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Possible reasons:" -ForegroundColor Yellow
    Write-Host "1. Not connected to GitHub repository" -ForegroundColor White
    Write-Host "2. No internet connection" -ForegroundColor White
    Write-Host "3. Authentication required" -ForegroundColor White
    Write-Host "4. Branch doesn't exist on remote" -ForegroundColor White
    Write-Host ""
    Write-Host "To setup GitHub remote:" -ForegroundColor Yellow
    Write-Host "  git remote add origin https://github.com/USERNAME/REPO.git" -ForegroundColor White
    Write-Host "  git push -u origin main" -ForegroundColor White
    Write-Host ""
    Write-Host "Or use GitHub Desktop (easier):" -ForegroundColor Yellow
    Write-Host "  https://desktop.github.com" -ForegroundColor White
    Write-Host ""
}

Write-Host ""
pause
