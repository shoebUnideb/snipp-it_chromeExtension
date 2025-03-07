@echo off
echo Installing Screenshot to PDF dependencies...
echo.

:: Check if pip is installed
where pip >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: pip is not installed or not in PATH.
    echo Please install Python with pip and try again.
    pause
    exit /b 1
)

:: Install requirements
echo Installing required packages...
pip install -r requirements.txt

if %ERRORLEVEL% neq 0 (
    echo.
    echo Error: Failed to install dependencies.
    echo Please check your internet connection and try again.
) else (
    echo.
    echo Dependencies installed successfully!
    echo You can now run the server using start_screenshot_server.bat
)

echo.
pause