@echo off
title Stop PocketLaw Servers
echo Stopping PocketLaw Backend (Port 5001) and Frontend (Port 3000)...

powershell -NoProfile -Command ^
  "$p5001 = (Get-NetTCPConnection -LocalPort 5001 -ErrorAction SilentlyContinue).OwningProcess; if ($p5001) { Stop-Process -Id $p5001 -Force; Write-Host 'Stopped backend on port 5001' };" ^
  "$p3000 = (Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue).OwningProcess; if ($p3000) { Stop-Process -Id $p3000 -Force; Write-Host 'Stopped frontend on port 3000' };"

echo Done.
pause
