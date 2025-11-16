@echo off
REM Build executable with PyInstaller
REM Usage: build_exe.bat gui OR build_exe.bat cli

set TARGET=%1
if "%TARGET%"=="" set TARGET=gui

IF NOT DEFINED PYINSTALLER (
    pip install pyinstaller
)

REM Clean up
rmdir /S /Q build >NUL 2>&1
rmdir /S /Q dist >NUL 2>&1
del /Q *.spec >NUL 2>&1

set BASEWD=%~dp0\..
cd /d %BASEWD%

if "%TARGET%"=="gui" (
    set ENTRY=gui\vrp_gui.py
    set WINDOWED=--windowed
    set NAME=projectVRP-GUI
) else (
    set ENTRY=cli\solve_cvrp.py
    set WINDOWED=
    set NAME=projectVRP-CLI
)

set ADDDATA="data;data" "config.yaml;."

pyinstaller --noconfirm --onefile %WINDOWED% --name %NAME% --add-data %ADDDATA% %ENTRY%

echo Build finished. Check dist\%NAME%.exe
pause
