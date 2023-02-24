@echo off
@setlocal enableextensions
for /f "tokens=2 delims==" %%F in ('wmic nic where "NetConnectionStatus=2 and AdapterTypeId=0" get  NetConnectionID /format:list') do echo %%F
pause