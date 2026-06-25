@echo off
setlocal

set "CHATGPT_EXE=%LOCALAPPDATA%\Programs\ChatGPT\ChatGPT.exe"

if not exist "%CHATGPT_EXE%" (
    echo ChatGPT.exe no se encontro en "%CHATGPT_EXE%".
    echo Ajusta la ruta dentro de RestartChatGPT.bat si lo instalaste en otro lugar.
    pause
    exit /b 1
)

set "WAS_RUNNING=0"
tasklist /FI "IMAGENAME eq ChatGPT.exe" /NH | find /I "ChatGPT.exe" >nul
if not errorlevel 1 (
    set "WAS_RUNNING=1"
    taskkill /IM ChatGPT.exe /F >nul 2>&1
    timeout /T 1 /NOBREAK >nul
)

start "" "%CHATGPT_EXE%"
if errorlevel 1 (
    echo Hubo un problema al iniciar ChatGPT.
    pause
    exit /b 1
)

if "%WAS_RUNNING%"=="1" (
    echo ChatGPT reiniciado.
) else (
    echo ChatGPT iniciado.
)

endlocal
