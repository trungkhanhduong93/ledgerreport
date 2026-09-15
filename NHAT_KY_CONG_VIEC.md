# NHẬT KÝ CÔNG VIỆC — LedgerReport

> Toàn bộ những gì đã làm với **LedgerReport**, và **vì sao**. Đọc file này trước khi sửa tiếp.
> Kiến trúc, ma trận báo cáo, phương án backup: [CLAUDE.md](CLAUDE.md).
> Mổ xẻ sâu sự cố + 4 bài học: [SU_CO_15082026.md](SU_CO_15082026.md).
> Phiên gần nhất: **15/09/2026** · EXE hiện hành: **iPOS_Accounting_Report v1.10.5**

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

### v1.10.5 — BC007 xuất Excel MỘT file nhiều sheet *(14/09/2026)*

**Người dùng báo:** xuất sổ nhật ký chung ra CSV, mở bằng Excel thì *"vẫn bị giới hạn số dòng"*.

**Truy ra — file CSV không thiếu dòng nào.** Đo trên bản xuất kỳ T08/2026: 317 MB, **2.851.224 dòng**,
dòng cuối đúng 31/08. Chỗ cắt nằm ở **Excel**: trần cứng **1.048.576 dòng/sheet**, là giới hạn kiến
trúc của định dạng bảng tính chứ không phải cấu hình nên không có cách nâng. Dòng thứ 1.048.576 rơi
vào 12/08 ⇒ mở file bằng Excel chỉ thấy tới 12/08, **mất 63% dữ liệu mà không báo lỗi gì rõ ràng**.

**Đã làm:**
- Thêm nhánh `format=xlsx` cho BC007 trong `/api/report_export_csv`. Dùng **CHUNG** `sql`/`params`/
  `headers` với nhánh CSV ngay phía trên ⇒ hai định dạng không thể lệch số.
- `_write_xlsx_to_disk` / `_start_export_job` nhận thêm tham số `sheet_limit`, kèm kẹp cứng
  `min(sheet_limit, 1048575)`: truyền sai cỡ nào cũng không sinh ra được file Excel mở không nổi.
- Nâng mặc định `sheet_limit` **500.000 → 1.000.000**, áp dụng cả 7 tab Danh sách (mốc 500k cũ cắt
  dày gấp đôi mức cần thiết, file nhiều sheet hơn mà không được lợi gì).
- Ô ngày và ô tiền ghi bằng **kiểu thật** (`datetime` / `float`) thay vì chuỗi như CSV ⇒ Excel cộng,
  lọc, sắp xếp được ngay.
- Modal BC007 thêm mục chọn định dạng Excel/CSV; câu cảnh báo đổi theo lựa chọn đang chọn.

**Đo trên dữ liệu thật T08/2026:**

| | |
|---|---|
| Số sheet | 3 — 1.000.000 + 1.000.000 + 851.224 |
| Tổng dòng | 2.851.224 — bằng đúng bản CSV |
| Tổng PS Nợ = Tổng PS Có | 303.164.989.646 — khớp từng đồng |
| Ranh giới giữa các sheet | liền mạch, không nuốt và không lặp dòng |
| Dung lượng | 115 MB so với 317 MB của CSV — **nhẹ hơn 2,75 lần** |

⚠️ **Đừng lặp lại lỗi đếm dòng này:** `wc -l` trên file CSV ra 2.851.240, lệch 16 dòng so với
2.851.224. KHÔNG phải mất dòng — có **15 bút toán bị gõ Enter xuống dòng ngay trong ô Diễn giải**.
Trình đọc CSV đúng chuẩn (Access, Excel, module `csv` của Python) nối lại thành một bản ghi; đếm thô
theo ký tự xuống dòng thì thừa ra. Tổng tiền khớp tuyệt đối là bằng chứng.

⚠️ **Cái tên "Bảng tổng hợp" trong modal KHÔNG gộp dòng** — cả hai lựa chọn dùng chung một câu SQL
không có `GROUP BY`, "tổng hợp" chỉ nghĩa là bớt 3 cột. Bấm vào vẫn ra đủ 2,85 triệu dòng. Sổ nhật ký
chung (S03a-DN) buộc phải liệt kê từng bút toán theo trình tự thời gian nên **không được gộp**.

**Verify: đạt M4** — người dùng xuất thật trên `IACC_CHULONG` và xác nhận khớp (14/09/2026).

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
6. **Nâng 3 GitHub Action lên bản chạy Node 24** (`checkout@v7`, `setup-python@v7`,
   `action-gh-release@v3`). GitHub đã báo Node 20 hết vòng đời, hiện đang **ép** chạy trên Node 24;
   khi gỡ hẳn cơ chế ép đó thì workflow gãy mà không báo trước. Đã tra version và đối chiếu breaking
   change (14/09/2026), không vướng cái nào — nhưng token đang dùng **thiếu scope `workflow`** nên cả
   `git push` lẫn REST API đều bị chặn. Bảng 3 dòng cần đổi + toàn bộ kết quả đo ghi ở
   [CLAUDE.md](CLAUDE.md) mục 5. **Để chủ repo xem và quyết.**
7. **Route `/api/version` đăng ký 2 lần** (`get_version` dòng 210 và `get_app_version_api` dòng 6715).
   Cái trên thắng nên hàm dưới là code chết, `is_frozen` không bao giờ tới frontend. Frontend không
   dùng `is_frozen` nên hiện vô hại.

---

## 9. 15/09/2026 — Bộ lọc "Loại CT": đổi nguồn sang danh mục, tách theo từng tab

**Triệu chứng Đại Ca nêu:** *"loại chứng từ nó đang lọc thiếu, nếu có 1 mã chứng từ mới phát sinh thì
phải hiện ra"*.

### Đo được gì

| Việc | Số đo trên `IACC_CHULONG` |
|---|---|
| Nguồn cũ `SELECT DISTINCT TRAN_ID FROM dbo.LEDGER` | **39 mã / 14,9 giây** |
| Danh mục gốc `dbo.SYS_TRAN` | **90 mã / 0,04 giây** (74 mã `ACTIVE=1`) |
| Mã `ACTIVE=1` chưa từng có bút toán ⇒ **không có trong bộ lọc** | **35 mã** — `SO`, `SOXU`, `TX`, `TX1`, `TX2`, `HBTL`, `NKHAU`, `NMSC`, `XCK`, `XKHOK`, `ADJUST`, `TS`, `VAT_BR`… |
| Nhánh dự phòng `/api/ledger` lại lấy `SYS_TRAN ACTIVE=1` | **74 mã** — cùng một `meta['tran_ids']` mà khác nội dung tuỳ đường vào |

Một dropdown dùng chung cho cả 5 tab, trong khi mỗi tab đọc một nguồn khác nhau — và
`SALE_VIEW`/`PURCHASE_VIEW` còn có sẵn `WHERE SYS_TRAN.IS_SALE = 1` trong định nghĩa view:

| Tab | Nguồn tab thực sự đọc | Mã dùng được | Bản cũ hiện |
|---|---|---|---|
| Chứng từ tiền | `VOUCHER` | **9** | 39 |
| Mua hàng | `PURCHASE_VIEW` | **5** | 39 |
| Bán hàng | `SALE_VIEW` | **8** | 39 |
| Kho | `WAREHOUSE_VIEW` | **24** | 39 |
| Tổng hợp | `LEDGER` | 39 | 39 |

### Đã sửa

- Thêm `_build_tran_catalog()` + `_load_tran_usage()` trong [server.py](server.py): nguồn là
  **`dbo.SYS_TRAN`**, **chỉ lấy mã `ACTIVE = 1`** cho gọn (bỏ 16 mã đã ngưng dùng: `PO`, `SBO`, `SD`,
  `XKHO2`, `TSKH`, `VAT_DCT`…), hợp thêm mã thực sự có trong **view mà từng tab đọc** làm lưới an toàn.
  Ngoại lệ: mã `ACTIVE = 0` mà **còn chứng từ lịch sử** vẫn được giữ — có dữ liệu thì phải lọc ra được.
  Vẫn **đọc hết bảng** (không `WHERE ACTIVE=1`) để lấy TÊN cho mọi mã; bản cũ lọc `ACTIVE=1` ngay lúc
  lấy tên nên mã ngưng dùng hiện trơ mã, không có tên chứng từ.
- Phạm vi từng tab theo `OUTPUT_FORM` + `IS_SALE` (chính là mệnh đề của 2 view kia).
- Bỏ hẳn `SELECT DISTINCT TRAN_ID FROM dbo.LEDGER`; nhánh dự phòng bỏ `ACTIVE=1` cho đồng nguồn.
- `/api/metadata` khi trúng cache vẫn **đọc lại `SYS_TRAN` mỗi lần (0,04s)** → mã chứng từ mới khai
  báo là thấy ngay, **không cần bấm nút "Danh mục" hay khởi động lại EXE**.
- [index.html](index.html): thêm `tranItemsFor(tab)`, 5 dropdown "Loại CT" dùng danh sách riêng của
  tab mình; mã đang được chọn ở tab khác vẫn hiện ra để còn bỏ chọn được.

### Kết quả

| | Bản cũ | Bản mới |
|---|---|---|
| Nạp danh mục lần đầu | ~15s (riêng DISTINCT LEDGER 14,9s) | **7,4s** |
| Nạp lại (cache nóng) | 0s nhưng **danh sách đứng im cả phiên** | **0,04s, luôn tươi** |
| Tab Chứng từ tiền | 39 lựa chọn / 9 dùng được | **11 / 9** |
| Tab Mua hàng | 39 / 5 | **9 / 5** |
| Tab Bán hàng | 39 / 8 | **10 / 8** |
| Tab Kho | 39 / 24 | **46 / 24** |
| Tab Tổng hợp | 39 / 39 | **74 / 39** |
| Mã mới lập chưa có bút toán | **không hiện** | **hiện ngay** |

**Đã cân nhắc và bỏ:** lấy **chỉ mã đang có chứng từ thật** (Tổng hợp còn 39, Kho 24, Bán 8, Mua 5)
— gọn hơn nhưng mã mới phát sinh phải bấm nút "Danh mục" mới thấy, vì phần quét dữ liệu mất ~6 giây
nên buộc phải cache. Chọn `ACTIVE=1` để giữ đúng yêu cầu gốc: **mã mới khai báo là hiện ngay**.

**Verify — đạt M3** (Flask `test_client` in-process theo Bẫy 6, rồi build EXE chạy thật):
- Nghiệm thu "không tab nào thiếu mã": đối chiếu dropdown với `DISTINCT TRAN_ID` của đúng nguồn từng
  tab ⇒ **thiếu 0 mã ở cả 5 tab**.
- Lọc thật `/api/voucher?tran_ids=KT_PC` → 212 dòng, `TRAN_NAME` = "Phiếu chi".
- Smoke 12 endpoint (8 tab danh sách + BC001/BC005/BC011) → **200 hết, không cái nào 500/401**.
- M3: build `iPOS_Accounting_Report.exe` **v1.10.6**, chạy thật, bind cổng 5050, `/api/version` trả
  đúng phiên bản. M4 không áp dụng — đây là bộ lọc, không phải số liệu sổ sách.

Ba bẫy ghi vào [CLAUDE.md](CLAUDE.md): **Bẫy 14** (dựng bộ lọc từ dữ liệu phát sinh), **Bẫy 15**
(`SALE_VIEW`/`PURCHASE_VIEW` lọc `IS_SALE=1`), **Bẫy 16** (dropdown lọc `ACTIVE=1` — đã quyết để nguyên).
