@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

echo ========================================
echo   QwenPaw Idle Evolution 一键安装
echo ========================================
echo.

set "REPO_URL=https://github.com/hlhjs/qwenpaw-idle-evolution.git"
set "INSTALL_DIR=%USERPROFILE%\.copaw-awesome"
set "QWENPAW_DIR=%USERPROFILE%\.copaw\workspaces\default"

:: 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Python 未安装，请先安装 Python 3.10+
    pause
    exit /b 1
)
echo [INFO] Python 已就绪

:: 检查 pip
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [INFO] pip 未安装，正在安装...
    python -m ensurepip --upgrade
)
echo [INFO] pip 已就绪

:: 检查 qwenpaw/copaw
python -c "import qwenpaw" >nul 2>&1
if errorlevel 1 (
    python -c "import copaw" >nul 2>&1
    if errorlevel 1 (
        echo [INFO] CoPaw/QwenPaw 未安装，正在安装...
        pip install qwenpaw
    )
)
echo [INFO] CoPaw 已就绪

:: 检查 git
where git >nul 2>&1
if errorlevel 1 (
    echo [错误] git 未安装，请先安装 git
    pause
    exit /b 1
)

:: 克隆模板
if exist "%INSTALL_DIR%" (
    echo [INFO] 模板已存在，正在更新...
    cd /d "%INSTALL_DIR%" && git pull
) else (
    echo [INFO] 正在克隆模板...
    git clone "%REPO_URL%" "%INSTALL_DIR%"
)

:: 初始化 CoPaw 工作空间
echo [INFO] 正在初始化 CoPaw...
if not exist "%QWENPAW_DIR%" (
    mkdir "%QWENPAW_DIR%"
    echo [INFO] 工作目录已创建
)

:: 复制模板文件
echo [INFO] 正在复制模板文件...

:: 复制配置模板
if exist "%INSTALL_DIR%\config\*.template" (
    copy /Y "%INSTALL_DIR%\config\*.template" "%QWENPAW_DIR%\" >nul 2>&1
    echo [INFO] 配置模板已复制
)

:: 复制 Skills
if exist "%INSTALL_DIR%\skills\*" (
    if not exist "%QWENPAW_DIR%\skills" mkdir "%QWENPAW_DIR%\skills"
    xcopy /E /Y /Q "%INSTALL_DIR%\skills\*" "%QWENPAW_DIR%\skills\" >nul 2>&1
    echo [INFO] Skills 已复制
)

:: 复制脚本
if exist "%INSTALL_DIR%\scripts\*" (
    if not exist "%QWENPAW_DIR%\scripts" mkdir "%QWENPAW_DIR%\scripts"
    xcopy /Y /Q "%INSTALL_DIR%\scripts\*" "%QWENPAW_DIR%\scripts\" >nul 2>&1
    echo [INFO] 脚本已复制
)

:: 创建 Windows 任务计划
echo.
echo [INFO] 是否创建 Windows 任务计划？(每10分钟自动运行)
echo [INFO] 按 Y 确认，其他键跳过...
choice /C YN /T 10 /D N >nul
if errorlevel 1 (
    echo.
    echo [INFO] 创建任务计划...
    schtasks /create /tn "QwenPawIdleEvolution" /tr "\"%%PYTHON_PATH%%pythonw.exe\" \"%QWENPAW_DIR%\scripts\idle_evolution.py\" --run" /sc minute /mo 10 /f >nul 2>&1
    if errorlevel 1 (
        echo [WARN] 任务计划创建失败，请手动创建
    ) else (
        echo [INFO] 任务计划创建成功！
    )
)

echo.
echo ========================================
echo   安装完成！
echo ========================================
echo.
echo 下一步：
echo   1. 编辑 %QWENPAW_DIR%\agent.json 填入 API keys
echo   2. 运行 'copaw' 启动
echo   3. 运行 'python %QWENPAW_DIR%\scripts\idle_evolution.py --status' 查看状态
echo.
pause
