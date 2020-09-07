@echo off
if not defined %SISTEM_GAJI_ENV% call env

call start_docker

docker image rm %BACKEND_NAME%
docker build -t %BACKEND_NAME% ..\%BACKEND%