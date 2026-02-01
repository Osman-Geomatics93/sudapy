@echo off
REM ============================================================
REM  SudaPy Portable Launcher
REM  Activates the bundled conda environment and runs sudapy CLI
REM ============================================================

setlocal

set "SUDAPY_ROOT=%~dp0.."
set "SUDAPY_ENV=%~dp0sudapy_env"

if not exist "%SUDAPY_ENV%\python.exe" (
    echo ERROR: Cannot find bundled Python at %SUDAPY_ENV%\python.exe
    echo Make sure you extracted the full zip archive.
    exit /b 1
)

REM Activate the conda environment
call "%SUDAPY_ENV%\Scripts\activate.bat"

REM Forward all arguments to sudapy CLI
python -m sudapy.cli.main %*

endlocal
