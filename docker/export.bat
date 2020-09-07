@echo off

if not defined %SISTEM_GAJI_ENV% call env

docker save %BACKEND_NAME% -o %IMAGES%\%BACKEND_NAME%.tar
docker save %FRONTEND_NAME% -o %IMAGES%\%FRONTEND_NAME%.tar