@echo off
setlocal enabledelayedexpansion

:: Store the commit message
set "COMMIT_MESSAGE=%1"

:: Pull updates, add changes, commit, and push in each submodule
git submodule foreach --recursive "git pull origin $(git rev-parse --abbrev-ref HEAD) && git add -A && git commit -am \"!COMMIT_MESSAGE!\" && git push || echo Failed to push changes for the submodule: $name"

:: Final message
echo All submodules have been processed.
pause
endlocal
