@echo off
setlocal EnableExtensions EnableDelayedExpansion

cd /d "%~dp0"

if not exist "input" mkdir "input"
if not exist "output" mkdir "output"
if not exist "data" mkdir "data"

set "INPUT_FILE="
set "INPUT_NAME="
set /a FILE_COUNT=0

for %%F in ("input\*.xlsx") do (
    if exist "%%~fF" (
        set /a FILE_COUNT+=1
        set "INPUT_FILE=%%~fF"
        set "INPUT_NAME=%%~nF"
    )
)

if !FILE_COUNT! EQU 0 (
    echo.
    echo No XLSX file found in the input folder.
    echo Put one XLSX file into the input folder and run this file again.
    echo.
    pause
    exit /b 1
)

if !FILE_COUNT! GTR 1 (
    echo.
    echo More than one XLSX file was found in the input folder.
    echo Leave exactly one XLSX file and run this file again.
    echo.
    pause
    exit /b 1
)

echo.
echo Input: !INPUT_FILE!
echo Generating labels...
echo.

"barcode-labels.exe" --input "!INPUT_FILE!" --output "output\!INPUT_NAME!_with_barcodes.xlsx"

if errorlevel 1 (
    echo.
    echo Barcode Labels failed.
    echo.
    pause
    exit /b 1
)

echo.
echo Done.
echo Results are in the output folder.
echo.

start "" "output"
pause
