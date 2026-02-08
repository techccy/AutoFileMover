@echo off
title AutoFileMover 打包工具

echo ==========================================
echo AutoFileMover Windows可执行文件打包工具
echo ==========================================

REM 检查是否安装了PyInstaller
echo 检查PyInstaller...
python -c "import PyInstaller" >nul 2>&1
if %errorlevel% neq 0 (
    echo 安装PyInstaller...
    pip install pyinstaller
)

REM 使用PyInstaller打包程序
echo.
echo 开始打包程序...
pyinstaller --onefile --windowed ^
    --name AutoFileMover ^
    --add-data "config.yaml;." ^
    --add-data "icons;icons" ^
    --add-data "README.md;." ^
    --hidden-import tkinter ^
    --hidden-import tkinter.messagebox ^
    --hidden-import PIL ^
    --hidden-import yaml ^
    --hidden-import watchdog ^
    --hidden-import pystray ^
    start.py

REM 检查打包是否成功
if exist "dist\AutoFileMover.exe" (
    echo.
    echo ================================
    echo 打包成功！
    echo 可执行文件位置: dist\AutoFileMover.exe
    echo ================================
    
    REM 复制必要的文件到dist目录
    echo.
    echo 复制必要文件...
    copy /Y "start.bat" "dist\"
    copy /Y "test_functionality.py" "dist\"
    
    echo.
    echo 打包完成！请在dist目录中找到以下文件：
    echo - AutoFileMover.exe (主程序)
    echo - start.bat (启动脚本)
    echo - test_functionality.py (测试脚本)
) else (
    echo.
    echo ================================
    echo 打包失败！请检查错误信息。
    echo ================================
)

pause