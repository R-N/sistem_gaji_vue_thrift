@echo on
setlocal enabledelayedexpansion

git submodule foreach --recursive "echo Submodule: $name && git status"

:: Check if a commit message is provided
if "%1"=="" (
    echo Please provide a commit message.
    echo Usage: push_sub.bat "Your commit message"
    pause
    exit /b 1
)

:: Store the commit message
set "COMMIT_MESSAGE=%1"

:: Log file
set LOG_FILE=debug_log.txt
echo Debugging started... > "%LOG_FILE%"

:: Pull updates, add changes, commit, and push in each submodule
git submodule foreach --recursive "git pull origin $(git rev-parse --abbrev-ref HEAD) >> \"debug_log.txt\" 2>&1 && git add . >> \"debug_log.txt\" 2>&1 && git commit -m \"!COMMIT_MESSAGE!\" >> \"debug_log.txt\" 2>&1 && git push >> \"debug_log.txt\" 2>&1 || echo Failed to push changes for the submodule: $name >> \"debug_log.txt\""

:: Final message
echo All submodules have been processed. >> "%LOG_FILE%"
pause
endlocal
