# AGENTS.md — Context cho MỌI AI agent (Cursor, Copilot, Codex, Cline, GPT, Gemini, Claude…)

> **File này là điểm vào chung.** Bất kỳ agent nào (không riêng Claude Code) đọc hết file này là hiểu
> đủ ngữ cảnh để bắt đầu làm việc an toàn. Muốn hiểu SÂU (business logic KQKD, schema DB, chi tiết từng
> báo cáo, các sự cố đã gặp) → đọc tiếp **`KIEN_TRUC_TOAN_TAP.md`** trong cùng thư mục (nguồn tham chiếu đầy đủ).
>
> **Ngôn ngữ:** code + UI + trả lời đều bằng **tiếng Việt**. Trả lời ngắn gọn, sửa targeted — không rewrite
> toàn bộ file trừ khi được yêu cầu.

---

## 1. Đây là gì?

**2 ứng dụng desktop "anh em"** cho kế toán chuỗi F&B (iPOS), nằm cạnh nhau trong `ACC PMKT/`:

| | LedgerReport | LedgerStudio |
|---|---|---|
| Thư mục | `LedgerReport/` | `LedgerStudio/` |
| EXE | `dist/iPOS_Accounting_Report.exe` | `dist/iPOS_Ledger_Studio.exe` |
| Báo cáo | BC001→BC014 | BC005→BC012 |

⚠️ **Mã báo cáo KHÔNG đồng nhất giữa 2 app** (vd "BC011" khác nghĩa). Khi port qua lại phải kiểm mã trống ở app đích.
Sửa gì thường phải **sửa SONG SONG cho cả 2 app** (code gần giống nhưng đã phân nhánh — không copy mù, phải đọc code từng bên).

## 2. Kiến trúc (mỗi app)

- **`server.py`** — Flask + `pyodbc` (fallback `pymssql`), ~4000 dòng. Toàn bộ REST API. Nối **SQL Server** (DB kế toán iPOS).
- **`index.html`** — 1 file duy nhất ~450KB: **React + Babel standalone + Tailwind, TẤT CẢ qua CDN**, 1 `<script type="text/babel">` khổng lồ. **Không có build step JS** (Babel biên dịch JSX ngay trong trình duyệt).
- Đóng gói **1 file EXE** bằng **PyInstaller** (one-file, no-console), nhúng kèm `index.html`.
- Chạy: server bind `0.0.0.0:5050`, tự mở trình duyệt. Đăng nhập SQL Server qua `POST /api/login` (KHÔNG hardcode credential; lưu vào `session`).
- **Cần Internet** (CDN unpkg/tailwind/google-fonts). Mất mạng → màn hình trắng (xem `FIX_OFFLINE_FILTERS.md`).

Sửa **backend** → `server.py`; sửa **UI/báo cáo** → `index.html`.

## 3. Lệnh chuẩn

```bash
# Syntax-check Python:
python -c "import ast; ast.parse(open('server.py',encoding='utf-8').read()); print('OK')"

# Build EXE (CHUẨN — chạy trong thư mục app; tự nhận tên app, tự tăng version.txt):
python build_exe.py
#   ⚠️ build_exe.py in "[SUCCESS]" VÔ ĐIỀU KIỆN. PHẢI verify mtime dist/*.exe sau build.
#   ⚠️ Nếu EXE đang chạy → khóa file, build không đè được (vẫn in SUCCESS). Tắt tiến trình trước:
#      tasklist | grep -i iPOS   (đóng app nếu còn)
```
`BuildEXE.bat` có `pause` → **treo** ở môi trường non-interactive; ưu tiên `build_exe.py`.

## 4. TEST ĐÚNG CÁCH (quan trọng — hay sai)

**KHÔNG** test bằng `python server.py` + curl → dễ dính **"ghost server"** (process/EXE cũ còn giữ port 5050 trả code cũ).
**Luôn** test bằng Flask **`test_client` in-process**:
```bash
export PYTHONIOENCODING=utf-8   # tránh UnicodeEncodeError tiếng Việt trên Windows
python -c "
import server
c = server.app.test_client()
c.post('/api/login', json={'server':'171.244.129.176,9001','database':'IACC_CHULONG','user':'ipchulong','password':'iP0So@\$\$','driver':'ODBC Driver 17 for SQL Server'})
print(c.get('/api/cash_book?from_date=01/01/2026&to_date=31/01/2026&acc_ids=111&page=1').get_json()['pagination'])
"
```
DB test: `171.244.129.176,9001` / user `ipchulong` / pass `iP0So@$$` / db `IACC_CHULONG` (dữ liệu 2026-01 → 2026-10).

⚠️ **Test bằng CẢ driver `'SQL Server'`** (mặc định của form login — thứ user thật sự dùng), không chỉ
`ODBC Driver 17`: driver cũ trả `CONVERT(DATE,...)` thành **chuỗi** → `.strftime()` văng lỗi 500 trên máy user
dù test bằng Driver 17 pass sạch (đã dính ở BC014). Ép SQL trả chuỗi `CONVERT(VARCHAR(8),col,112)` cho chắc.
Chi tiết: `KIEN_TRUC_TOAN_TAP.md` mục 9.5.

## 5. Quy ước KẾT XUẤT (mới nhất 2026-07-08)

- **Danh sách chứng từ** (ledger/purchase/warehouse/sale/voucher) — nút "Xuất Excel", mode "1 file" → luôn **CSV** server-side (endpoint `/api/*/stream_csv` fname `.csv`), **không giới hạn dòng** (`SERVER_STREAM_THRESHOLD=0`). Mode "mỗi đơn vị 1 sheet" → xlsx client (SheetJS).
- **Báo cáo bảng DOM** (mọi BC trừ 007/008/012) — hàm `exportReportXls()` xuất **.xls dạng HTML-mso** (KHÔNG dùng SheetJS biff8 — bản community không ghi được style): clone `.report-table`, nội tuyến computed-style → Excel render **giống web 100%**; kèm khối tiêu đề công ty/mẫu/kỳ; ô cột giá trị lưu **số thật** + format `#,##0`. Nút nhãn "Excel".
- BC007/BC008 (dữ liệu lớn) → CSV/xlsx backend riêng. BC012 → `/api/cash_book/export_csv` stream. **Giữ nguyên.**

## 6. BẪY chí mạng (đọc kỹ trước khi sửa `server.py`)

- **`LEDGER.TRAN_DATE` là `smalldatetime`** (KHÔNG phải VARCHAR). Dùng `MONTH()/YEAR()/CONVERT(...,103)`, **KHÔNG `SUBSTRING`** (lỗi 8116). Truyền tham số ngày từ Python bằng `.strftime('%Y%m%d')`.
- **Thứ tự tham số SQL phải khớp thứ tự mệnh đề.** Bộ lọc đơn vị mặc định (`_org_filter_sql`) trả clause KHÔNG rỗng (`NOT IN external orgs`) → sai thứ tự bind → **trả 0 dòng** dù logic đúng.
- **⚠️ KIỂM TRA BÁO CÁO PHẢI LOẠI ĐƠN VỊ NGOÀI CÂY TỔNG CÔNG TY `'00'`** (hiện là org `'66'`). Báo cáo mặc định đã loại (`_org_filter_sql` → `NOT IN`), nên **query thô `FROM LEDGER` sẽ KHÔNG khớp báo cáo** vì gồm cả org ngoài → dễ tưởng nhầm là bug. Đã dính: TK 6411 chưa kết chuyển tổng 421.242.631 nhưng BC005 chỉ lệch 24.384.900 — chênh 396.857.731 là của org `'66'`. Danh sách đơn vị ngoài tính **động theo cây** (`_get_external_org_ids`), **đừng hardcode `'66'`**. Chi tiết: `KIEN_TRUC_TOAN_TAP.md` mục 2.4.
- **`_calc_results()`** = bộ não phân loại KQKD (BC001–BC004). Từng bị handoff cũ xóa nhầm → hỏng form. Sửa KQKD sai → kiểm hàm này còn nguyên trước tiên.
- **Đừng để công cụ "auto thêm WITH (NOLOCK)"** chạy lên `server.py` — đã từng làm hỏng SQL hàng loạt (nhân đôi hint, tách alias → lỗi 8180). Chi tiết cách phát hiện/sửa ở `KIEN_TRUC_TOAN_TAP.md` mục 9.4.
- **`@with_db_lock`** bọc mọi route DB (đồng bộ luồng + tự reconnect). Route mới phải có decorator này + try/except + `invalidate_pool()` khi lỗi.
- **Frontend**: mọi state của `App` phải truyền xuống `ReportTab` qua **props** (thiếu → `ReferenceError` vỡ app). Mỗi `loadReportData` tạo `AbortController` MỚI (dùng chung ref cũ → hủy nhau giữa `r.json()` → "Unexpected end of JSON input").

## 7. Sau khi sửa BẤT KỲ thứ gì

1. `syntax-check` → `test_client` (mục 4) → `python build_exe.py` + verify mtime EXE trong `dist/`.
2. **⚡ BẮT BUỘC ĐỒNG BỘ & GIT PUSH:** Mỗi khi sửa xong và build EXE ở `LedgerReport` (`D:\IACC HCM\iPOS ACC\ACC PMKT\LedgerReport`), **bắt buộc đồng bộ toàn bộ** sang thư mục con `ledgerreport` (`D:\IACC HCM\iPOS ACC\ACC PMKT\LedgerReport\ledgerreport`), sau đó tự động commit và push git vào nhánh `main` của repo [trungkhanhduong93/ledgerreport](https://github.com/trungkhanhduong93/ledgerreport).
3. Cập nhật tài liệu LIVE: `KIEN_TRUC_TOAN_TAP.md` / `GEMINI.md` / `CLAUDE.md`.
4. Nếu thay đổi áp dụng cả 2 app → làm cho **cả LedgerReport và LedgerStudio**.

---

📖 **Chi tiết đầy đủ:** `KIEN_TRUC_TOAN_TAP.md` (schema DB, từng báo cáo BC, tối ưu hiệu năng, quy trình thêm báo cáo, lịch sử sự cố).
