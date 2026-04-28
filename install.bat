@echo off
chcp 65001 >nul
echo ========================================
echo   CoPaw Awesome Starter 安装程序
echo ========================================
echo.

:: 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未安装 Python，请先安装 Python 3.10+
    pause
    exit /b 1
)

:: 检查 pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未安装 pip
    pause
    exit /b 1
)

echo [1/5] 检查 QwenPaw...
pip show qwenpaw >nul 2>&1
if errorlevel 1 (
    echo     安装 QwenPaw...
    pip install qwenpaw
) else (
    echo     QwenPaw 已安装
)

echo.
echo [2/5] 创建配置文件目录...
set USERPROFILE=%USERPROFILE%
set COPAW_DIR=%USERPROFILE%\.copaw
set WORKSPACE_DIR=%COPAW_DIR%\workspaces\default

if not exist "%COPAW_DIR%" mkdir "%COPAW_DIR%"
if not exist "%WORKSPACE_DIR%" mkdir "%WORKSPACE_DIR%"
if not exist "%WORKSPACE_DIR%\skills" mkdir "%WORKSPACE_DIR%\skills"
if not exist "%WORKSPACE_DIR%\memory" mkdir "%WORKSPACE_DIR%\memory"

echo.
echo [3/5] 复制配置文件模板...
set SCRIPT_DIR=%~dp0
if not exist "%WORKSPACE_DIR%\agent.json" (
    copy "%SCRIPT_DIR%config\agent.json.template" "%WORKSPACE_DIR%\agent.json"
    echo     请编辑 %WORKSPACE_DIR%\agent.json 填入你的 API keys
) else (
    echo     agent.json 已存在，跳过
)

echo.
echo [4/5] 复制 Skills...
xcopy /E /Y "%SCRIPT_DIR%skills\*" "%WORKSPACE_DIR%\skills\" >nul 2>&1
echo     Skills 复制完成

echo.
echo [5/5] 启用 Skills...
cd /d "%COPAW_DIR%"
python enable_skills.py 2>nul

echo.
echo ========================================
echo   安装完成！
echo ========================================
echo.
echo 下一步：
echo   1. 编辑 %WORKSPACE_DIR%\agent.json 填入 API keys
echo   2. 运行 copaw 启动
echo   3. 输入 "help" 查看可用命令
echo.
echo 详细文档请查看 README.md
echo.
pause
