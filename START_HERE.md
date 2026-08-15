# 👉 ĐỌC FILE NÀY ĐẦU TIÊN (cho Gemini / dev mới tiếp nhận)

Đây là dự án **iPOS Accounting Ledger Report** — báo cáo kế toán iPOS ACC.
Backend Python (Flask) `server.py` + frontend single-file React `index.html`, đóng gói EXE.

## Đọc theo thứ tự này để hiểu toàn bộ:

1. **`README.md`** — đọc đầu tiên. Nắm toàn bộ: kiến trúc, cách chạy/build, bảng API, 2 bẫy nghiệp vụ, bản đồ file. Riêng file này là đủ để hiểu tổng thể.
2. **`skill.md`** — đọc khi cần đào sâu: chuẩn UI, quy trình 4 bước thêm báo cáo mới, vibe-guard (lỗi React/JSX/SQL hay gặp).
3. **`claude-memory/*.md`** — 2 bẫy ĐÃ TỪNG làm hỏng app, đọc trước khi sửa báo cáo KQKD hoặc query LEDGER:
   - `bc-report-calc-results-restore.md` — logic `_calc_results` (BC001–004), đừng xóa nhầm.
   - `ledger-tran-date-type.md` — `TRAN_DATE` là `smalldatetime`, KHÔNG phải VARCHAR.
4. **`FIX_OFFLINE_FILTERS.md`** — chỉ khi máy đích lỗi màn hình trắng / không có Internet cho CDN.

Code chính: **`server.py`** (backend + toàn bộ API) và **`index.html`** (frontend) — đọc trực tiếp khi cần sửa.

## ⚠️ 2 điều TUYỆT ĐỐI nhớ trước khi sửa code:

- **`_calc_results` trong `server.py`** = bộ não phân loại chỉ tiêu KQKD BC001–004. Cột `ITEM_CLASS1_ID` / `EXPENSE_CLASS_ID` lấy qua JOIN `DM_ITEM` / `DM_EXPENSE` (KHÔNG có sẵn trong LEDGER). Đừng tưởng cột không tồn tại mà xóa — đã từng hỏng form vì lý do này.
- **`dbo.LEDGER.TRAN_DATE` là `smalldatetime`**, không phải VARCHAR. Dùng `MONTH()/YEAR()/CONVERT(...,103)`, KHÔNG dùng `SUBSTRING` (văng lỗi 8116).

## Chạy thử nhanh & Quy trình bàn giao:
- Dev: cần Python 3.9+ → chạy `RunReport.bat` → mở `http://localhost:5050`.
- Chạy EXE: `dist/iPOS_Accounting_Report.exe` (cần ODBC Driver 17 for SQL Server + Internet cho CDN).
- Build lại EXE: chạy `python build_exe.py` (hoặc `BuildEXE.bat`).
- ⚡ **BẮT BUỘC ĐỒNG BỘ & GIT PUSH:** Mỗi khi sửa xong và build EXE ở `LedgerReport` (`D:\IACC HCM\iPOS ACC\ACC PMKT\LedgerReport`), **bắt buộc đồng bộ toàn bộ** sang thư mục con `ledgerreport` (`D:\IACC HCM\iPOS ACC\ACC PMKT\LedgerReport\ledgerreport`), sau đó tự động commit và push git vào nhánh `main` của repo [trungkhanhduong93/ledgerreport](https://github.com/trungkhanhduong93/ledgerreport).

