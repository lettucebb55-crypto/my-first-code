@echo off
chcp 65001 >nul
echo ========== 打包烟雾报警服务为 exe ==========
echo.

REM 检查/安装 PyInstaller
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo 正在安装 PyInstaller...
    pip install pyinstaller
    echo.
)

echo 正在打包（单文件 + 黑窗口）...
pyinstaller --onefile --console --name smoke_alarm_server smoke_alarm_server.py

echo.
if exist "dist\smoke_alarm_server.exe" (
    echo ========== 打包成功 ==========
    echo 输出文件: dist\smoke_alarm_server.exe
    echo.
    explorer dist
) else (
    echo 打包可能失败，请检查上方报错信息
)
pause
