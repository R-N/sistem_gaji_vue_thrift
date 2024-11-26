@echo off
setlocal enabledelayedexpansion

:: Store the commit message
set "COMMIT_MESSAGE=%1"

:: Check if a commit message is provided
if "%1"=="" (
    echo Please provide a commit message.
    echo Usage: push_sub.bat "Your commit message"
    pause
    exit /b 1
)

:: Pull updates, add changes, commit, and push in each submodule
git submodule foreach --recursive "git pull origin $(git rev-parse --abbrev-ref HEAD) && git add -A && git commit -am \"!COMMIT_MESSAGE!\" || echo Failed to push changes for the submodule: $name"

:: Final message
echo All submodules have been processed.
pause
endlocal
