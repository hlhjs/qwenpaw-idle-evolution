@echo off
chcp 65001 >nul
echo ========================================
echo QwenPaw 闲时进化系统 - 任务计划安装
echo ========================================

REM 获取脚本所在目录
set "SCRIPT_DIR=%~dp0.."

REM 删除旧任务（如果存在）
schtasks /delete /tn "QwenPawIdleEvolution" /f 2>nul

REM 获取 Python 路径
set PYTHON_PATH=
for %%i in (pythonw.exe python.exe) do (
    where %%i 2>nul > temp_path.txt
    set /p PYTHON_PATH=<temp_path.txt
    del temp_path.txt 2>nul
    if defined PYTHON_PATH goto :found_python
)

:found_python
if not defined PYTHON_PATH (
    echo [错误] 未找到 Python，请先安装 Python
    pause
    exit /b 1
)

echo 找到 Python: %PYTHON_PATH%

REM 创建任务计划
echo.
echo 创建任务计划...
schtasks /create /tn "QwenPawIdleEvolution" ^
    /tr "\"%PYTHON_PATH%\" \"%SCRIPT_DIR%\idle_evolution.py\" --run" ^
    /sc minute /mo 10 /f

if %errorlevel% equ 0 (
    echo.
    echo ✅ 任务创建成功！
    echo.
    echo 任务详情:
    schtasks /query /tn "QwenPawIdleEvolution" /fo LIST
) else (
    echo.
    echo ❌ 任务创建失败
)

echo.
pause
