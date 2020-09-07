@echo off
if not defined %SISTEM_GAJI_ENV% call env

call start_docker

docker stop %BACKEND_NAME%
docker container rm %BACKEND_NAME%
docker run --name %BACKEND_NAME% -p 80:%BACKEND_PORT% %BACKEND_NAME%