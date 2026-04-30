@echo off
chcp 65001 >nul
echo ========================================
echo   QwenPaw Idle Evolution 快速安装
echo ========================================
echo.

:: 直接从 GitHub 下载安装脚本并执行
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/hlhjs/qwenpaw-idle-evolution/main/install.cmd' -OutFile '%TEMP%\qwenpaw_install.cmd'; Start-Process '%TEMP%\qwenpaw_install.cmd' -Wait"

pause
