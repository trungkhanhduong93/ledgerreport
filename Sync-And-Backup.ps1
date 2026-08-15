<#
    Sync-And-Backup.ps1 — đồng bộ thư mục làm việc sang repo git rồi sao lưu.

    VÌ SAO CÓ FILE NÀY
    Thư mục làm việc D:\IACC HCM\iPOS ACC\ACC PMKT\LedgerReport và repo git con
    ledgerreport\ là HAI BẢN COPY RIÊNG. Trước đây đồng bộ bằng cách copy tay từng
    file — sót một file là mất vĩnh viễn nếu ổ đĩa hỏng, vì chỉ repo con mới được
    push lên GitHub. Script này copy theo danh sách cố định, không dựa vào trí nhớ.

    CÁCH DÙNG
      .\Sync-And-Backup.ps1                 # đồng bộ + kiểm tra, KHÔNG commit
      .\Sync-And-Backup.ps1 -Commit         # đồng bộ + commit + push GitHub
      .\Sync-And-Backup.ps1 -Commit -Message "fix: ..."
      .\Sync-And-Backup.ps1 -ZipTo "E:\Backup"   # kèm tạo file zip toàn bộ mã nguồn

    KHÔNG đụng tới: dist\, build\, node_modules\, __pycache__\, *.rar, *.zip
#>
[CmdletBinding()]
param(
    [switch]$Commit,
    [string]$Message = "",
    [string]$ZipTo   = ""
)

$ErrorActionPreference = 'Stop'
$Src = Split-Path -Parent $MyInvocation.MyCommand.Definition
$Dst = Join-Path $Src 'ledgerreport'

if (-not (Test-Path $Dst)) { throw "Khong tim thay repo con: $Dst" }

# ── Danh sách file BẮT BUỘC đồng bộ ────────────────────────────────────────────
# Thêm file mới vào đây NGAY khi tạo, đừng để tới lúc build mới nhớ.
$Files = @(
    'server.py',
    'index.html',
    'version.txt',
    'version_info.txt',
    'build_exe.py',
    'requirements.txt',
    'icon.ico',
    'icon.svg',
    'manifest.json',
    'iPOS_Accounting_Report.spec',
    'BuildEXE-LedgerReport.bat',
    'RunReport.bat',
    'check_babel.js',
    'check_schema.py',
    'install_driver.ps1',
    'CREATE_INDEXES.sql',
    'CREATE_INDEXES_SALE.sql',
    'test.py',
    'test_sql.py',
    # --- Tài liệu LIVE (chỉ 5 file này, xem docs-cu/ cho bản cũ) ---
    'CLAUDE.md',
    'GEMINI.md',
    'AGENTS.md',
    'START_HERE.md',
    'SU_CO_15082026.md',
    'NHAT_KY_CONG_VIEC.md',
    'Sync-And-Backup.ps1'
)

# 16/08/2026 — repo đã dọn 29 file rác (di sản LedgerStudio + script one-off) và chuyển
# README.md / skill.md / KIEN_TRUC_TOAN_TAP.md / HANDOFF_*.md / HUONG_DAN_* / FIX_OFFLINE_*
# vào docs-cu/. ĐỪNG thêm lại chúng vào $Files — thêm là script copy đè ngược từ thư mục cha
# và làm sống lại đúng mớ tài liệu mâu thuẫn đã gây ra sự cố 15/08.

Write-Output "=== DONG BO: $Src  ->  $Dst ==="
$changed = @()
foreach ($f in $Files) {
    $s = Join-Path $Src $f
    if (-not (Test-Path $s)) { Write-Output ("  BO QUA (khong co): {0}" -f $f); continue }
    $d = Join-Path $Dst $f
    $hashS = (Get-FileHash $s).Hash
    $hashD = if (Test-Path $d) { (Get-FileHash $d).Hash } else { '' }
    if ($hashS -ne $hashD) {
        Copy-Item -Path $s -Destination $d -Force
        $changed += $f
        Write-Output ("  DA COPY : {0}" -f $f)
    } else {
        Write-Output ("  giong roi: {0}" -f $f)
    }
}

# ── Kiểm tra lại bằng hash, không tin lệnh copy ────────────────────────────────
Write-Output "`n=== DOI CHIEU HASH ==="
$bad = 0
foreach ($f in $Files) {
    $s = Join-Path $Src $f; $d = Join-Path $Dst $f
    if (-not (Test-Path $s)) { continue }
    if (-not (Test-Path $d)) { Write-Output ("  THIEU O REPO: {0}" -f $f); $bad++; continue }
    if ((Get-FileHash $s).Hash -ne (Get-FileHash $d).Hash) {
        Write-Output ("  LECH: {0}" -f $f); $bad++
    }
}
if ($bad -gt 0) { throw "$bad file chua dong bo dung — DUNG LAI, dung push." }
Write-Output "  Tat ca khop."

# ── Cảnh báo file .py/.html mới chưa nằm trong danh sách ───────────────────────
$tracked = $Files | ForEach-Object { $_.ToLower() }
# -Include chi hoat dong khi co -Recurse hoac duong dan wildcard -> loc bang Where-Object.
$skipLike = @('fix_*', 'patch_*', 'test*', 'check_*', 'scratch*', '*.bak*', 'index_check.html',
              'dump_pyc.py', 'extract.py', 'recover.js', '_time_voucher.py', 'add_contra_cols.py',
              'insert_reports.py', 'rename_and_remove.py', 'inject_*', 'find_*', 'read_docx.py',
              'update_titles.py', 'insert_endpoints.py')
$orphan = Get-ChildItem -Path $Src -File |
          Where-Object { $_.Extension -in '.py', '.html' } |
          Where-Object { $tracked -notcontains $_.Name.ToLower() } |
          Where-Object { $n = $_.Name; -not ($skipLike | Where-Object { $n -like $_ }) }
if ($orphan) {
    Write-Output "`n=== CANH BAO: file nay KHONG duoc dong bo (chua co trong `$Files) ==="
    $orphan | ForEach-Object { Write-Output ("  {0}" -f $_.Name) }
}

# ── Zip toàn bộ mã nguồn (tuỳ chọn) ───────────────────────────────────────────
if ($ZipTo) {
    if (-not (Test-Path $ZipTo)) { New-Item -ItemType Directory -Force -Path $ZipTo | Out-Null }
    $stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
    $zip = Join-Path $ZipTo "LedgerReport_src_$stamp.zip"
    $tmp = Join-Path $env:TEMP "lr_zip_$stamp"
    New-Item -ItemType Directory -Force -Path $tmp | Out-Null
    foreach ($f in $Files) {
        $s = Join-Path $Src $f
        if (Test-Path $s) { Copy-Item $s (Join-Path $tmp $f) -Force }
    }
    Compress-Archive -Path (Join-Path $tmp '*') -DestinationPath $zip -Force
    Remove-Item $tmp -Recurse -Force
    Write-Output ("`n=== DA TAO ZIP: {0} ({1:N0} KB) ===" -f $zip, ((Get-Item $zip).Length / 1KB))
}

# ── Commit + push ──────────────────────────────────────────────────────────────
if ($Commit) {
    Push-Location $Dst
    try {
        $remote = (git remote get-url origin)
        Write-Output "`n=== REMOTE: $remote ==="
        if ($remote -match 'gitlab') { throw "Remote la GitLab — CAM push. Chi push GitHub." }

        $st = git status --short
        if (-not $st) { Write-Output "Khong co gi de commit."; return }
        Write-Output $st

        git add -A
        if ($Message) { $msg = $Message }
        else { $msg = "chore: dong bo tu thu muc lam viec $(Get-Date -Format 'yyyy-MM-dd HH:mm')" }
        git commit -m $msg
        if ($?) {
            git push origin main
            if ($?) { Write-Output "`n=== DA PUSH. GitHub Actions se tu dong goi EXE va tao Release. ===" }
        }
    } finally { Pop-Location }
}

Write-Output "`nXong. File da doi lan nay: $(if ($changed) { $changed -join ', ' } else { '(khong co)' })"
