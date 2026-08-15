@echo off
setlocal
title BUILD LedgerReport  (iPOS_Accounting_Report.exe)

REM =====================================================================
REM  BUILD CHO **LEDGERREPORT** — ra file iPOS_Accounting_Report.exe
REM
REM  File nay CHI dung cho LedgerReport. Ban cua LedgerStudio ten khac:
REM      BuildEXE-LedgerStudio.bat   -> iPOS_Ledger_Studio.exe
REM
REM  VI SAO PHAI TACH LAM 2 FILE TEN KHAC NHAU:
REM  Truoc day chi co mot "BuildEXE.bat" chung, ten EXE thi doan theo thu muc
REM  dang dung. Chay nham thu muc la ra sai ten EXE ma khong bao gi. Trong
REM  chinh thu muc LedgerReport da ton tai mot BuildEXE.bat build ra
REM  "iPOS_Ledger_Studio" — di san copy nham tu Studio.
REM  Nay: ten file khac nhau + ghim cung ten EXE + chan neu dung sai thu muc.
REM =====================================================================

cd /d "%~dp0"

set "APP_NAME=iPOS_Accounting_Report"
set "MUST_HAVE=CLAUDE.md"

echo =======================================================
echo  BUILD LEDGERREPORT  -^>  %APP_NAME%.exe
echo  Thu muc: %CD%
echo =======================================================
echo.

REM ---------- Chan chay nham thu muc ----------
echo %CD% | find /i "LedgerStudio" >nul
if not errorlevel 1 (
    echo [DUNG] Ban dang dung trong thu muc LedgerStudio.
    echo        File nay chi danh cho LedgerReport.
    echo        Hay chay: BuildEXE-LedgerStudio.bat
    exit /b 1
)
echo %CD% | find /i "LedgerReport" >nul
if errorlevel 1 (
    echo [DUNG] Duong dan hien tai khong chua "LedgerReport".
    echo        Thu muc: %CD%
    echo        Khong build de tranh ra sai ten EXE.
    exit /b 1
)

where python >nul 2>&1
if errorlevel 1 (
    echo [LOI] Khong tim thay Python trong PATH. Cai Python 3.9+ va tich "Add Python to PATH".
    exit /b 1
)
python --version

if not exist "server.py"    (echo [LOI] Khong tim thay server.py    & exit /b 1)
if not exist "index.html"   (echo [LOI] Khong tim thay index.html   & exit /b 1)
if not exist "build_exe.py" (echo [LOI] Khong tim thay build_exe.py & exit /b 1)

echo.
echo [1/3] Cap nhat dependencies
python -m pip install --upgrade pip
python -m pip install --upgrade pyinstaller flask flask-cors pyodbc pillow xlsxwriter
if errorlevel 1 (echo [LOI] pip install that bai. Kiem tra ket noi mang. & exit /b 1)

echo.
echo [2/3] Dong EXE cu dang chay (PyInstaller khong ghi de duoc file dang mo)
taskkill /F /IM %APP_NAME%.exe /T >nul 2>&1

echo.
echo [3/3] Dong goi (One-File, No Console) — cho 1-3 phut
REM Truyen THANG ten EXE, khong de build_exe.py doan theo thu muc
python build_exe.py %APP_NAME%
if errorlevel 1 (echo. & echo [LOI] Build that bai. Xem log o tren. & exit /b 1)

echo.
echo =======================================================
echo  THANH CONG
echo =======================================================
if exist "version.txt" (set /p VER=<version.txt) else (set VER=?)
echo Phien ban: %VER%
echo File EXE : %CD%\dist\%APP_NAME%.exe
for %%A in ("dist\%APP_NAME%.exe") do echo Dung luong: %%~zA bytes
echo.
echo Nho: sua xong nho chay Sync-And-Backup.ps1 -Commit de day len GitHub.
