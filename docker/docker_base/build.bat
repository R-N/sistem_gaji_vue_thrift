@echo off
if not defined %SISTEM_GAJI_ENV% call ..\..\env

call start_docker

copy /y ..\..\%BACKEND%\requirements.txt .

docker image rm sistem_gaji_backend_base
docker build -t sistem_gaji_backend_base .