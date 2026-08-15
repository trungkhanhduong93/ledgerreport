# NHẬT KÝ CÔNG VIỆC — LedgerReport

> Toàn bộ những gì đã làm với **LedgerReport**, và **vì sao**. Đọc file này trước khi sửa tiếp.
> Kiến trúc, ma trận báo cáo, phương án backup: [CLAUDE.md](CLAUDE.md).
> Mổ xẻ sâu sự cố + 4 bài học: [SU_CO_15082026.md](SU_CO_15082026.md).
> Phiên gần nhất: **15–16/08/2026** · EXE hiện hành: **iPOS_Accounting_Report v1.8.5**

---

## 0. LedgerReport là gì

**Sinh ra RIÊNG cho `IACC_CHULONG`** — mang cả luật nghiệp vụ đặc thù của Chú Long.
LedgerStudio là bản song song cho **DB iPOS chung chung** của khách khác.

| | LedgerReport (thư mục này) | LedgerStudio |
|---|---|---|
| DB đích | **`IACC_CHULONG`** | DB iPOS chung chung |
| EXE | `dist\iPOS_Accounting_Report.exe` | `dist\iPOS_Ledger_Studio.exe` |
| File build | **`BuildEXE-LedgerReport.bat`** | `BuildEXE-LedgerStudio.bat` |
| Git | **Có** — repo con `ledgerreport\` → GitHub `trungkhanhduong93/ledgerreport` | **KHÔNG có** |
| Phát hành | Push `main` → Actions tự build EXE + tạo Release | Đưa thẳng file EXE |

**5 báo cáo chỉ LedgerReport có:** `BC001`–`BC004` (KQKD) và `BC011` LCTT gián tiếp Chú Long.
Chúng chạy qua `_calc_results()` map **cứng** bộ mã danh mục riêng của Chú Long — bê sang DB khác
thì mọi chỉ tiêu về 0 mà không báo lỗi.

⚠️ **Mã BC cùng số khác nghĩa:** ở đây `BC011` = LCTT Chú Long, `BC013` = công nợ, `BC014` = bảng kê
bán ra. Ở Studio thì `BC011` = công nợ, `BC013` = bảng kê. Nhìn nhầm là sửa nhầm báo cáo.

---

## 1. Sự cố 15/08 — 8 lỗi làm chết báo cáo

Một agent AI được giao "khôi phục BC001–BC014" đã **nối 505 dòng vào cuối `server.py`** mà không đọc
phần đã có (commit `b90bdc9`). Build vẫn xanh, EXE vẫn đóng gói được. Người dùng: *"bấm là văng ra
khỏi phần mềm"*.

| # | Triệu chứng | Nguyên nhân |
|---|---|---|
| 1 | Bấm Xem báo cáo là văng về màn hình đăng nhập | `session["logged_in"]` **được đọc ở 3 endpoint nhưng không bao giờ được gán** → luôn trả 401 |
| 2 | BC009/BC010 lỗi 500 | `_calc_results` **định nghĩa 2 lần**, bản nối thêm che bản trên → `KeyError: 'expense_class'` |
| 3 | BC002/BC004 lỗi 500 | `SELECT L.EXPENSE_NAME` — LEDGER không có cột đó |
| 4 | BC011 lỗi 500 | Gọi `_compute_cdkt()` — hàm đã bị mất |
| 5 | Nút xuất CSV của BC014 báo lỗi | Frontend đổi mã BC013→BC014, backend còn khoá `"BC013"` |
| 6 | BC001/BC003 mất các dòng tổng | Điều kiện lọc dòng bằng 0 bỏ mất danh sách giữ lại mã `09`–`18` |
| 7 | Tab "Doanh thu chờ phân bổ" chết | `SELECT RECEIVE_DATE` — cột không tồn tại |
| 8 | **Không có triệu chứng** — nhưng **CĐKT không cân** | 5 báo cáo + 7 tab gộp cả đơn vị ngoài cây `'00'` |

**Chi tiết đầy đủ + cách phát hiện từng lỗi: [SU_CO_15082026.md](SU_CO_15082026.md).**

---

## 2. Việc đã làm — theo thứ tự

### v1.8.1 — Sửa 5 lỗi làm BC001–BC004, BC009–BC011 không xem được

- `session['logged_in']` → `session.get('db_config')` ở 3 endpoint
- Xoá bản `_calc_results` trùng tên; trả `cf_data` của `/api/cash_flow` về đủ key.
  **Fuzz 4.000 ca** so hai bản: `r['13']` và `r['07']` lệch 0 → BC009/BC010 giữ nguyên số
- `E.EXPENSE_NAME` + `ISNULL(L.JOB_ID,'')` — khôi phục đúng câu SQL gốc
- `report_export_csv` nhận cả `BC014` lẫn `BC013`
- Khôi phục điều kiện giữ dòng tổng `09`–`18` của BC001/BC003

### v1.8.2 — Khôi phục đúng bản `_compute_cdkt` gốc

**Lỗi của chính tôi:** ở v1.8.1 tôi **tự viết lại** `_compute_cdkt` trong khi **bản gốc vẫn còn
nguyên** trong `git show b6553f6:server.py`. Bản tự viết:
- lọc đơn vị bằng `ORGANIZATION_ID IN` thay vì `_org_filter_sql` → **ra số khác**
- thiếu hẳn phần tách `1311/1312` và `421A/421B`

Đã thay bằng nguyên văn bản gốc, chỉ đổi 2 điểm có chủ đích: thêm `WITH (NOLOCK)` cho đồng bộ, và
thay `calc_sub_131` `O(N²)` bằng bản `O(N)` đã tối ưu sẵn trong BC005 (**fuzz 3.000 ca: lệch 0**).

> **Bài học lớn nhất phiên này: hàm bị mất thì TÌM trong git, đừng VIẾT LẠI.**

### v1.8.3 — Mặc định BC001, định dạng Excel, tối ưu tốc độ

- **Mặc định mở tab Báo cáo vào BC001** thay vì BC005
- **Định dạng file `.xls`:** ô tiền đã đúng từ trước (value `1000000`, hiển thị `1,000,000`) —
  rà lại toàn bộ ô có `formatNum`, không sót ô nào. **Chỗ thật sự sai là cột phần trăm:** ô giữ
  nguyên chuỗi `"15.54%"` nên Excel coi là **text, không tính được**. Nay value `0.1554`, hiển thị
  `15.54%` (class `xpct0`–`xpct4`). Test 13 ca bằng Node, đúng cả 13
- **`index.html` chưa từng được nén** — `send_from_directory` bật `direct_passthrough` khiến
  `get_data()` ném lỗi rồi bị `except` nuốt im lặng. Sau khi sửa: **577.400 → 83.554 bytes (−86%)**
- **Xuất CSV bị middleware gzip nuốt trọn generator vào RAM** → mất sạch tác dụng streaming.
  Nay bỏ qua `response.is_streamed`
- **Bỏ ping `SELECT 1` trước mọi request** — 50 request liên tiếp giảm từ 49 lần ping xuống **0**
- Thêm tài liệu backup 4 tầng + script `Sync-And-Backup.ps1`

### v1.8.4 — Thống nhất bộ lọc đơn vị + gỡ tab không thuộc về đây

**Đây là đợt sửa quan trọng nhất về số liệu.**

BC005, BC006, BC007, BC008, BC013, đường xuất CSV và 7 tab danh sách **không loại đơn vị ngoài cây
`'00'`** (đơn vị `66` — CPMCL-HCM-SEVEN AM), trong khi BC001–BC004, BC009–BC011, BC014 thì có.
Hậu quả: các báo cáo **không tie được với nhau**, và CĐKT lệch **3.252.634.439** — đúng bằng số dư
TK 6411 chưa kết chuyển của đơn vị 66, thứ không có chỗ nào trên CĐKT.

Nay **29 chỗ đều đi qua `_org_filter_sql`**, không còn chỗ nào tự dựng `ORGANIZATION_ID IN`.
Chỗ quyết định của BC005 là hàm `run_ledger` **lồng bên trong** — đó mới là truy vấn sinh ra số dư
thật, không phải `org_where` ở ngoài.

**Chốt an toàn:** DB không có đơn vị gốc `'00'` thì `reaches_root()` trả False cho **mọi** đơn vị →
`NOT IN (tất cả)` → mọi báo cáo trả 0 dòng **không báo lỗi**. Nay không thấy `'00'` ⇒ không lọc gì
+ ghi cảnh báo vào log.

**Gỡ hẳn tab "Doanh thu chờ phân bổ"** — vốn của LedgerStudio, bị copy nhầm sang, và chết hoàn toàn
trên `IACC_CHULONG` vì cột `RECEIVE_DATE` không tồn tại. Gỡ 325 dòng `server.py` (3 route, 6 hằng,
6 hàm) + 258 dòng `index.html`. Còn **0 tham chiếu treo** ở cả hai file.

### v1.8.5 — Tách build + dọn repo

- **Hai file build tên khác hẳn nhau**, xoá `BuildEXE.bat` chung ở cả hai bên (mục 3)
- **Dọn repo 68 → 40 file** (mục 4)

---

## 3. Tách file build — không thể build nhầm

**Vấn đề:** cả hai project đều có `BuildEXE.bat` **cùng tên**, tự gọi PyInstaller và **đoán** tên EXE
theo thư mục đang đứng. Bản nằm trong chính thư mục *LedgerReport* lại build ra `iPOS_Ledger_Studio`
(di sản copy nhầm), và thiếu `--add-data version.txt`.

| Project | File build | Ra EXE |
|---|---|---|
| LedgerReport | **`BuildEXE-LedgerReport.bat`** | `iPOS_Accounting_Report.exe` |
| LedgerStudio | **`BuildEXE-LedgerStudio.bat`** | `iPOS_Ledger_Studio.exe` |

**Ba lớp chống nhầm:**
1. **Tên file khác hẳn** — nhìn là biết đang chạy cái nào
2. **Ghim cứng `APP_NAME`** trong `.bat`, truyền thẳng `python build_exe.py %APP_NAME%`.
   `build_exe.py` chỉ nhận đúng 2 tên hợp lệ, sai là `exit 1`. Chạy trần không tham số vẫn đoán
   như cũ **nhưng in cảnh báo to**
3. **Chặn theo đường dẫn** — `.bat` nằm trong thư mục của project kia thì **dừng, exit 1**.
   Đã test thật: copy `BuildEXE-LedgerStudio.bat` vào thư mục tên `…LedgerReport` rồi chạy →
   `[DUNG] Ban dang dung trong thu muc LedgerReport`, exit 1

> ⚠️ File `.bat` phải lưu **CRLF, KHÔNG BOM**. Ghi LF thì `cmd.exe` cắt câu lệnh loạn xạ, báo
> `'ILD' is not recognized as an internal or external command`. Đã vấp thật.

---

## 4. Dọn repo — 68 → 40 file

**Gốc rễ mớ lẫn lộn:** commit thứ hai của repo GitHub `ledgerreport` là
`27d5e98 "Initial commit: LedgerStudio project codebase"` — repo mang tên *ledgerreport* vốn được
**dựng lên từ chính codebase của LedgerStudio**. Hai project chung một gốc lịch sử, chung nhánh
`main`. Đó là lý do `CLAUDE.md` trong LedgerReport từng mô tả LedgerStudio, và tab `income_alloc`
của Studio lại nằm ở đây — **không phải copy nhầm, mà vốn là một repo**.

**Đã `git rm` 29 file:**
- Của Studio: `iPOS_Ledger_Studio.spec`, `patch_server_studio.py`, `patch_modal_progress_studio.py`
- Script one-off đã dùng xong: `fix_*.py` (7), `patch_*.py` (8), `inject_*.py` (2),
  `insert_endpoints.py`, `find_reports.py`, `read_docx.py`, `update_titles.py`, `test_jsx.py`,
  `extract.py`
- Dump/spec thừa: `temp.jsx` (300 KB), `server.spec`, `headers.txt`

**Chuyển 7 tài liệu cũ vào `docs-cu/`** (`README.md`, `skill.md`, `KIEN_TRUC_TOAN_TAP.md`,
`HANDOFF_*.md`, `HUONG_DAN_BC007_BC010.md`, `FIX_OFFLINE_FILTERS.md`). Chính mớ tài liệu này gây ra
cảnh "3 tài liệu mô tả 3 kiến trúc".

**Tài liệu LIVE còn đúng 5 file:** `CLAUDE.md` · `START_HERE.md` · `GEMINI.md` · `AGENTS.md` ·
`SU_CO_15082026.md` (+ file này).

Đã kiểm: `.github/workflows/release.yml` **không dùng file `.spec` nào** (gọi thẳng PyInstaller với
`--add-data`), và mọi file nó cần vẫn còn.

**Ngắt LedgerStudio khỏi repo này:** thư mục Studio từng có `.git` với `origin` trỏ **đúng repo này**,
cùng nhánh `main`. Một lệnh `git push` nhầm là đè code Studio lên `main` của Report. Đã chạy
`git remote remove origin` bên Studio.

> Lịch sử repo trên GitHub **vẫn còn** commit `27d5e98` chứa codebase Studio. Muốn xoá hẳn phải
> `git filter-repo` + force-push — **phá huỷ, không đảo ngược**. Chưa làm, chờ quyết định.

---

## 5. Verify — đạt M4 trên DB thật

`IACC_CHULONG`: **18.516.886 dòng LEDGER**, 02/12/2025 → 01/10/2026, 83 đơn vị có phát sinh,
`BALANCE_VIEW` **trống 0 dòng** (nên mọi số dư đầu kỳ phải dồn từ LEDGER — lý do BC005/BC011 nặng).
SQL Server 2025 Express, `compatibility_level = 170`, `AUTO_SHRINK`/`AUTO_CLOSE` đã tắt sẵn.

### Các đẳng thức kế toán — đều khớp

Kỳ **01/07–31/07/2026**:

| Kiểm tra | Kết quả |
|---|---|
| BC005 Tổng tài sản = Tổng nguồn vốn | **165.309.773.349** ✅ CÂN (trước: lệch 3,25 tỷ) |
| BC006 Nợ = Có (dư đầu / phát sinh / dư cuối) | ✅ cân cả 3 cột |
| BC006 phát sinh vs SQL thô có lọc đơn vị | **331.164.100.304** khớp |
| BC001 = BC002 = BC009 = BC010 = BC011 (LN trước thuế) | **4.054.883.218** |
| Tổng mã 13 của 82 công việc = tổng chung | ✅ BC002 không thất thoát dòng |
| **BC005 mã 110 Tiền = BC009 mã 70 Tiền cuối kỳ** | **8.217.295.888** ✅ |
| Xuất CSV BC007/BC008/BC012/BC014 | chạy thật, BC007 ra 448.765 dòng |

Luỹ kế **01/01–31/07/2026**: LN trước thuế `24.098.362.724`, doanh thu thuần `238.964.073.603`,
tổng phát sinh `2.262.469.808.105`. BC005 vẫn cân `165.309.773.349`.

> Chênh lệch **hợp lệ**, đừng tưởng là lỗi: BC006 dư cuối Nợ (`165.173.074.702`) thấp hơn BC005 tổng
> tài sản (`165.309.773.349`) đúng `136.698.647`. BC006 bù trừ Nợ/Có trong cùng tài khoản, còn CĐKT
> phải **tách tài khoản lưỡng tính theo từng đối tượng**. Nên CĐKT luôn ≥ và chênh đúng phần tách ra.

### Thời gian chạy thật

| Báo cáo | Thời gian | | Báo cáo | Thời gian |
|---|---:|---|---|---:|
| BC011 LCTT Chú Long | 114–150 s | | BC009/BC010 | 10 s |
| BC005 CĐKT | 103–117 s | | BC007 | 8 s |
| BC002 KQKD công việc | 31 s | | BC013 | 8 s |
| BC006 CĐ phát sinh | 28 s | | BC012 | 1 s |
| BC001 KQKD tháng | 25 s | | BC008 / BC014 | < 1 s |

BC005 và BC011 nặng vì phải dựng lại số dư luỹ kế **từ 01/01**; BC011 còn gọi chính engine của BC005
rồi quét LEDGER thêm lần nữa.

---

## 6. Bốn lỗi tôi tự gây ra trong lúc sửa — và bị bắt thế nào

Ghi lại vì chúng đều **lọt qua `ast.parse`** và chỉ lộ khi chạy thật:

| Lỗi | Bị bắt bởi |
|---|---|
| Tự viết lại `_compute_cdkt` trong khi bản gốc còn trong git → ra số khác | Đối chiếu với `git show b6553f6` |
| `org_params_open` của BC005 còn dùng `org_ids` (rỗng) trong khi SQL đã có `NOT IN (?)` | Chạy thật → `2 parameter markers, but 1 parameters were supplied` |
| `report_export_csv` sửa `org_where` mà quên `org_where_l`/`org_where_lv` → xuất CSV BC007 chết | Test riêng đường xuất CSV |
| Ghi file `.bat` bằng LF → `cmd.exe` cắt lệnh loạn | Chạy thử file `.bat` |

**Ba trong bốn lỗi là Bẫy 5 — lệch số tham số bind.** Sửa bộ lọc dùng chung thì phải quét lại
**SAU KHI** sửa hết, và **chạy thử từng đường**, kể cả đường xuất CSV.

---

## 7. Quy trình bắt buộc

```bash
# 1. Cú pháp (M1)
python -c "import ast; ast.parse(open('server.py',encoding='utf-8').read()); print('OK')"
node check_babel.js

# 2. Quét trùng tên hàm — cấm nối code vào cuối file
python -c "import ast,collections;t=ast.parse(open('server.py',encoding='utf-8').read());c=collections.Counter(n.name for n in t.body if isinstance(n,ast.FunctionDef));print({k:v for k,v in c.items() if v>1} or 'khong trung')"

# 3. Đổi bộ lọc đơn vị? quét lại SAU KHI sửa hết
grep -n "list(org_ids)\|+ org_ids" server.py     # phải rỗng

# 4. Chạy thật trên DB (M2/M4) — test_client in-process, KHÔNG qua cổng 5050
# 5. Ép các đẳng thức kế toán ở mục 5 — bước duy nhất bắt được lỗi loại 8
# 6. Chạy skill pre-push-qa
# 7. Build
BuildEXE-LedgerReport.bat
# 8. Đồng bộ + push
powershell -File Sync-And-Backup.ps1 -Commit -Message "fix: ..."
```

---

## 8. Còn treo

1. **Lịch sử repo vẫn còn commit `27d5e98` chứa codebase Studio** — muốn xoá phải `git filter-repo`
   + force-push, phá huỷ và không đảo ngược. Chưa làm.
2. **Định dạng `%` trong file `.xls` chưa mở bằng Excel xác nhận.** Nếu Excel không ăn
   `mso-number-format` thì ô **vẫn đúng value `0.1554`**, chỉ hiển thị thành `0.1554` thay vì `15.54%`.
3. **BC002 từng đo 692 giây một lần rồi 31 giây hai lần sau** — biến động phía SQL Server, không tái
   hiện được, chưa truy ra nguyên nhân.
4. **Phân trang vẫn dùng `ROW_NUMBER()`** (chọn cố ý để tương thích SQL Server 2008). DB CHULONG là
   SQL 2025 `compatibility_level = 170` nên `OFFSET/FETCH` dùng được — nhưng chưa đo nên chưa đổi.
5. **Đổi mật khẩu tài khoản DB** đã dùng để kiểm tra trong phiên 15–16/08.
