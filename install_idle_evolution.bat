@echo off
chcp 65001 >nul
echo ========================================
echo   安装空闲进化服务开机自启
echo ========================================
echo.

set SCRIPT_DIR=%~dp0
set IDLE_SCRIPT=%SCRIPT_DIR%scripts\idle_evolution.py
set STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set BAT_FILE=%STARTUP_DIR%\CopawIdleEvolution.bat

:: 创建启动脚本
echo @echo off > "%BAT_FILE%"
echo python "%IDLE_SCRIPT%" >> "%BAT_FILE%"
echo exit >> "%BAT_FILE%"

echo.
echo [完成] 空闲进化服务已设置为开机自启
echo.
echo 启动路径: %BAT_FILE%
echo.
echo 卸载命令: del "%BAT_FILE%"
echo.
pause
