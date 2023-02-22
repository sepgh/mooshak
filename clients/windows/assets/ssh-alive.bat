@echo off
@setlocal enableextensions
Title TUNNEL
:start
plink.exe -ssh %2 -D 6060 -l %1 -P %3 -no-antispoof -pw %4 -T while true; do echo 0; sleep 30s; done
timeout /t 2
goto :start
