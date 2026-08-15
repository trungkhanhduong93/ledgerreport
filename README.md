# iPOS Accounting Ledger Report

Ứng dụng báo cáo kế toán cho hệ thống **iPOS ACC** (SQL Server). Một file backend Python (Flask) + một file frontend `index.html` (React qua CDN). Đóng gói thành `.exe` chạy độc lập trên Windows.

> **Đọc kèm:** `skill.md` là cẩm nang chi tiết (kiến trúc, chuẩn UI, quy trình thêm báo cáo, vibe-guard). README này là bản tóm tắt để bàn giao + những cảnh báo quan trọng nhất.

---

## 1. Kiến trúc

- **Backend — `server.py`** (~3.300 dòng): Flask + PyODBC.
  - Kết nối SQL Server bằng **connection pool** (`_conn_pool`), tránh mở/đóng mỗi request.
  - `global_db_lock` / decorator `@with_db_lock` đồng bộ luồng, tự reconnect khi mất kết nối (mã lỗi `HY000`, `08S01`).
  - Nén `gzip` JSON payload tự động cho bảng vài trăm ngàn dòng.
  - Hàm `kill_process_on_port(5050)` tự taskkill process cũ đang giữ port trước khi start.
  - Chạy ở **port 5050** (`APP_PORT = 5050`, `host=0.0.0.0`).
- **Frontend — `index.html`** (~327 KB, single-file): ReactJS + Babel standalone + TailwindCSS, **toàn bộ qua CDN** (unpkg.com, cdn.tailwindcss.com). Virtual Scroll + `useMemo` để render bảng lớn không crash RAM.
- **Đóng gói:** PyInstaller one-file → `dist/iPOS_Accounting_Report.exe`.

---

## 2. Chạy & Build

### Chạy ở chế độ dev (cần Python 3.9+)
```
RunReport.bat        # tắt server cũ + chạy "python server.py"
```
Mở trình duyệt: `http://localhost:5050`

Dependencies (`requirements.txt`): `flask==3.1.0`, `flask-cors==5.0.0`, `pyodbc==5.2.0`, `xlsxwriter==3.2.9` (build thêm `pyinstaller`, `pillow`).

### Build EXE
```
BuildEXE.bat
```
→ Tự cài deps, dọn build cũ, đóng gói one-file no-console kèm `index.html`, `install_driver.ps1`, `manifest.json`, `icon.svg`. Kết quả: `dist/iPOS_Accounting_Report.exe`.

### Yêu cầu máy đích
- Cài **ODBC Driver 17 for SQL Server** (app tự gợi ý qua `install_driver.ps1`).
- **Có Internet** để tải CDN (xem cảnh báo mục 5).
- Đăng nhập SQL qua form login (`/api/login`): nhập `server`, `database`, `user`, `password`, `driver`. Không hardcode credentials trong code.

---

## 3. API chính (`server.py`)

| Route | Chức năng |
|---|---|
| `/api/login`, `/api/logout` | Kết nối / ngắt SQL, lưu `db_config` vào session |
| `/api/metadata`, `/api/metadata/refresh` | Cache metadata (danh mục lọc) theo database |
| `/api/ledger` (+ `/count`, `/stream_csv`, `/export`) | Chứng từ tổng hợp (LEDGER) |
| `/api/purchase` (+ `/count`, `/stream_csv`) | Mua hàng |
| `/api/warehouse` (+ `/count`, `/stream_csv`) | Kho |
| `/api/balance_sheet` | Bảng cân đối kế toán (CDKT) |
| `/api/trial_balance` | Bảng cân đối phát sinh |
| `/api/journal`, `/api/account_details` | Sổ nhật ký / chi tiết tài khoản |
| `/api/report`, `/api/report_by_job` | **Báo cáo KQKD BC001–BC004** (xem mục 4) |
| `/api/export_excel_backend`, `/api/export/status`, `/api/export/cancel` | Xuất Excel phía backend |
| `/api/open_file`, `/api/open_folder` | Mở file/thư mục đã xuất |
| `/api/check_driver`, `/api/install_driver` | Kiểm tra / cài ODBC driver |

---

## 4. ⚠️ Logic nghiệp vụ quan trọng (đừng xóa nhầm)

### `_calc_results(data, thtt_expense_list, expense_classes)` trong `server.py`
Hàm phân loại chỉ tiêu cho **KQKD BC001–BC004** (`/api/report`, `/api/report_by_job`).
- Map `ITEM_CLASS1_ID` (CF, THUCAN, MC, TA, CB, ITEM_TYPE-*…) và `EXPENSE_CLASS_ID` (THTT, TTTM, TTTT, CPVH, TL, BH, TAX, CPKH, CPC) vào ~40 chỉ tiêu (011, 012, 081–089 + `_0XX_details`).
- `ITEM_CLASS1_ID` đến từ JOIN `dbo.DM_ITEM`; `EXPENSE_CLASS_ID` từ JOIN `dbo.DM_EXPENSE` — **KHÔNG có sẵn trong bảng LEDGER**.
- Quy ước: tổng phía CRD luôn loại trừ bút toán kết chuyển `911` (`not any(contra.startswith('911'))`).
- `get_report` trả `data` + `months` + `monthly` (key tháng `"{m}_{y}"`) + `month_list`. `get_report_by_job` trả `data` + `jobs` + `job_list`.

> **Lịch sử:** Hàm này từng bị handoff trước xóa nhầm (tưởng cột không tồn tại) → hỏng form. Đã tái dựng nguyên văn từ `server.pyc` của EXE cũ (fuzz 37.500 ca khớp tuyệt đối). **Nếu BC001–004 sai số/sai form → kiểm tra `_calc_results` còn nguyên không trước tiên.**

### `dbo.LEDGER.TRAN_DATE` là `smalldatetime` (KHÔNG phải VARCHAR)
- Dùng `MONTH(L.TRAN_DATE)`, `YEAR(L.TRAN_DATE)`, `CONVERT(VARCHAR(10), L.TRAN_DATE, 103)`.
- **KHÔNG dùng `SUBSTRING`** trên cột này (văng lỗi 8116).
- Truyền tham số ngày từ Python bằng `.strftime('%Y%m%d')` (so sánh implicit với smalldatetime — đã chứng minh đúng).
- Cursor trả về object `date/datetime`, hiển thị bằng `.strftime("%d/%m/%Y")`.

> Handoff doc cũ ghi SAI rằng TRAN_DATE là chuỗi 'YYYYMMDD' → từng làm hỏng BC001–BC004.

---

## 5. Khắc phục sự cố thường gặp

- **Màn hình trắng / bộ lọc không chạy:** Máy đích mất Internet hoặc firewall chặn CDN (`unpkg.com`, `cdn.tailwindcss.com`, `fonts.googleapis.com`). Mở F12 → Network xem file `.js`/`.css` nào đỏ. Giải pháp lâu dài: inline CDN vào HTML (xem `FIX_OFFLINE_FILTERS.md`).
- **`Communication link failure` / `HY000` / `08S01`:** Mất session SQL. Backend tự reconnect nhờ `@with_db_lock`; user chỉ cần bấm tìm kiếm lại.
- **`Address already in use` (port 5050):** Process cũ chưa tắt. `kill_process_on_port(5050)` xử lý tự động; nếu vẫn lỗi, dùng `RunReport.bat` (đã `taskkill` các exe/python cũ).

---

## 6. Bản đồ file

**Cốt lõi (cần để chạy/build):**
- `server.py` — backend Flask, toàn bộ API.
- `index.html` — frontend SPA (bản đang dùng). `index.html.bak` là bản cũ.
- `RunReport.bat`, `BuildEXE.bat` — chạy dev / build EXE.
- `install_driver.ps1`, `manifest.json`, `icon.svg`/`icon.ico` — tài nguyên nhúng vào EXE.
- `requirements.txt`, `CREATE_INDEXES.sql` (index tối ưu query).
- `dist/` — EXE đã build.

**Tài liệu:**
- `skill.md` — cẩm nang chi tiết (đọc cái này khi cần đào sâu).
- `FIX_OFFLINE_FILTERS.md` — cách làm bản offline không cần CDN.
- `README.md` — file này.

**Tham chiếu báo cáo (mẫu Excel):** `BCDPS.xlsx`, `CDKT T1.xlsx`, `BESReportViewer.pdf`, `headers.txt`.

**Đồ nghề reverse-engineering / phụ trợ (KHÔNG cần khi chạy app, có thể bỏ khi nén để giảm dung lượng):**
- `LedgerReport.rar` (~57 MB), `iPOS_Accounting_Report.exe_extracted/`, `temp_backup/`, `node_modules/`, `__pycache__/`.
- `server_dis.txt`, `get_report_*.txt`, `all_strings.txt`, `search_out.txt`, `out.txt` — output disassemble/extract từ EXE cũ.
- `extract.py`, `dump_pyc.py`, `recover.js`, `insert_reports.py`, `patch*.py`, `fix_*.py`, `check_schema.py`, `test*.py` — script một lần dùng để dựng lại/patch, không phải runtime.

> **Khi nén bàn giao cho Gemini:** chỉ cần nhóm "Cốt lõi" + "Tài liệu" là đủ để chạy & phát triển tiếp. Có thể loại `LedgerReport.rar`, `node_modules/`, `__pycache__/`, `*_extracted/`, `temp_backup/` và các `*.txt` disassemble để giảm mạnh dung lượng (từ ~58 MB xuống vài MB).

---

## 7. Lưu ý cho người tiếp nhận (Gemini / dev mới)

1. **Đừng tin handoff doc cũ về kiểu dữ liệu** — verify schema thật trên DB (`TRAN_DATE` = smalldatetime; `ITEM_CLASS1_ID`/`EXPENSE_CLASS_ID` lấy qua JOIN DM_ITEM/DM_EXPENSE).
2. **Trước khi sửa `_calc_results` hay query LEDGER** — đọc lại mục 4. Đây là 2 chỗ đã từng bị hỏng do hiểu nhầm.
3. **Khi sửa `index.html`** — tuân chuẩn UI premium + vibe-guard trong `skill.md` (escape JSX, dọn event listener, truyền props đầy đủ, parse date bằng `dateString.replace(' ', 'T')`).
4. **Thêm báo cáo mới** — theo quy trình 4 bước ở `skill.md` mục 4 (API backend → state/fetch frontend → table+virtual scroll → tích hợp export Excel).
5. **⚡ QUY TẮC ĐỒNG BỘ & GIT PUSH BẮT BUỘC:** Mỗi khi sửa xong và build EXE ở `LedgerReport` (`D:\IACC HCM\iPOS ACC\ACC PMKT\LedgerReport`), **bắt buộc đồng bộ toàn bộ** sang thư mục con `ledgerreport` (`D:\IACC HCM\iPOS ACC\ACC PMKT\LedgerReport\ledgerreport`), sau đó tự động commit và push git vào nhánh `main` của repo [trungkhanhduong93/ledgerreport](https://github.com/trungkhanhduong93/ledgerreport).

