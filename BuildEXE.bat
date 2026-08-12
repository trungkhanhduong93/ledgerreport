@echo off
setlocal enabledelayedexpansion
title iPOS Accounting Report - EXE Builder

REM Chuyen ve thu muc chua file .bat (de chay tu Explorer cung dung)
cd /d "%~dp0"

echo =======================================================
echo  iPOS Accounting Report - One-File EXE Builder
echo =======================================================
echo.

REM ---------- 1. Kiem tra Python ----------
where python >nul 2>&1
if errorlevel 1 (
    echo [LOI] Khong tim thay Python trong PATH.
    echo Hay cai Python 3.9+ tu https://www.python.org/downloads/
    echo va tich vao "Add Python to PATH" khi cai dat.
    
    exit /b 1
)
python --version

REM ---------- 2. Kiem tra cac file nguon bat buoc ----------
if not exist "server.py"           (echo [LOI] Khong tim thay server.py & exit /b 1)
if not exist "index.html"          (echo [LOI] Khong tim thay index.html & exit /b 1)
if not exist "install_driver.ps1"  (echo [LOI] Khong tim thay install_driver.ps1 & exit /b 1)
if not exist "manifest.json"       (echo [LOI] Khong tim thay manifest.json & exit /b 1)
if not exist "icon.svg"            (echo [LOI] Khong tim thay icon.svg & exit /b 1)

echo.
echo -------------------------------------------------------
echo  [1/3] Cai dat / cap nhat dependencies
echo -------------------------------------------------------
python -m pip install --upgrade pip
python -m pip install --upgrade pyinstaller flask flask-cors pyodbc pillow xlsxwriter
if errorlevel 1 (
    echo [LOI] pip install that bai. Kiem tra ket noi mang.
    
    exit /b 1
)

REM ---------- Sinh icon.ico bang Pillow neu chua co ----------
if not exist "icon.ico" (
    echo Dang tao icon.ico...
    python make_icon.py 2>nul
    if not exist "icon.ico" echo [Canh bao] Khong tao duoc icon.ico - se build khong co icon.
)

echo.
echo -------------------------------------------------------
echo  [2/3] Don dep build cu
echo -------------------------------------------------------
if exist "build"                          rmdir /s /q "build"            2>nul
if exist "dist"                           rmdir /s /q "dist"             2>nul
if exist "iPOS_Ledger_Studio.spec"    del   /f /q "iPOS_Ledger_Studio.spec"
if exist "iPOS_Ledger_Studio.spec"        del   /f /q "iPOS_Ledger_Studio.spec"
if exist "LedgerReport_ChuLong.spec"      del   /f /q "LedgerReport_ChuLong.spec"

echo.
echo -------------------------------------------------------
echo  [3/3] Dong goi EXE (One-File, No Console)
echo -------------------------------------------------------
echo Vui long cho 1-3 phut...
echo.

REM Co icon.ico thi dung, khong co thi bo qua
set ICON_ARG=
if exist "icon.ico" set ICON_ARG=--icon icon.ico

python -m PyInstaller ^
    --noconsole ^
    --onefile ^
    --clean ^
    --noconfirm ^
    --name "iPOS_Ledger_Studio" ^
    %ICON_ARG% ^
    --add-data "index.html;." ^
    --add-data "install_driver.ps1;." ^
    --add-data "manifest.json;." ^
    --add-data "icon.svg;." ^
    --collect-submodules flask ^
    --collect-submodules flask_cors ^
    --collect-submodules pyodbc ^
    --hidden-import pyodbc ^
    --hidden-import flask ^
    --hidden-import flask_cors ^
    server.py

if errorlevel 1 (
    echo.
    echo [LOI] PyInstaller that bai. Xem log o tren.
    
    exit /b 1
)

REM Don dep cache sau khi build
if exist "build"                          rmdir /s /q "build"            2>nul
if exist "iPOS_Ledger_Studio.spec"    del   /f /q "iPOS_Ledger_Studio.spec"

echo.
echo =======================================================
echo  THANH CONG!
echo =======================================================
echo File EXE: %CD%\dist\iPOS_Ledger_Studio.exe
echo.

REM Hien size file
for %%A in ("dist\iPOS_Ledger_Studio.exe") do (
    set /a size_mb=%%~zA / 1024 / 1024
    echo Dung luong: !size_mb! MB
)

echo.
echo Ban co the chay truc tiep file EXE tren bat ky may Windows 10/11 nao.
echo Yeu cau may dich: cai ODBC Driver 17 for SQL Server (app se goi y tu cai).
echo =======================================================

endlocal
