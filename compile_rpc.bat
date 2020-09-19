@echo off

if not defined %SISTEM_GAJI_ENV% call env

FOR /D %%p IN (%BACKEND_RPC%\*) DO rmdir "%%p" /s /q
del /s /q %BACKEND_RPC%\*
FOR /D %%p IN (%FRONTEND_RPC%\*) DO rmdir "%%p" /s /q
del /s /q %FRONTEND_RPC%\*

for %%f in (%RPC%\*) do thrift -r -out %BACKEND_RPC% --gen py:package_prefix=rpc.gen. %%f
for %%f in (%RPC%\*) do thrift -r -out %FRONTEND_RPC% --gen js:node,with_ns %%f