# CLAUDE.md — NGUỒN SỰ THẬT DUY NHẤT CỦA **LedgerReport**

> Mọi agent AI (Claude Code, Gemini, Cursor, Copilot, Antigravity…) và mọi dev mới **đọc file này trước**.
> `GEMINI.md` và `AGENTS.md` chỉ là con trỏ về đây — đừng viết nội dung khác vào đó.
> Cập nhật gần nhất: **15/08/2026** · Bản EXE hiện hành: **iPOS_Accounting_Report v1.8.x**

---

## 0. ⛔ KHOÁ NGỮ CẢNH — ĐỌC TRƯỚC KHI GÕ DÒNG CODE ĐẦU TIÊN

Trong workspace `ACC PMKT/` có **hai project song song, kiến trúc giống hệt nhau nhưng phục vụ hai
mục đích khác nhau**:

| | LedgerReport (**file này**) | LedgerStudio |
|---|---|---|
| **Sinh ra để làm gì** | **Riêng cho `IACC_CHULONG`** — mang cả luật nghiệp vụ đặc thù của Chú Long | **DB iPOS chung chung** của khách khác |
| Thư mục | `D:\IACC HCM\iPOS ACC\ACC PMKT\LedgerReport` | `…\ACC PMKT\LedgerStudio` |
| EXE | `dist\iPOS_Accounting_Report.exe` | `dist\iPOS_Ledger_Studio.exe` |
| **Git** | **Có** — repo con `ledgerreport\` → [trungkhanhduong93/ledgerreport](https://github.com/trungkhanhduong93/ledgerreport) | **KHÔNG có git, KHÔNG push đi đâu** — chỉ nằm local |
| **Phát hành** | `Sync-And-Backup.ps1 -Commit` → Actions tự tạo Release | **Build EXE thẳng vào thư mục của chính nó.** Hết. |

⛔ **Làm ở LedgerStudio thì TUYỆT ĐỐI không `git add/commit/push`.**

### 0.0 Build EXE — MỖI PROJECT MỘT FILE `.bat` RIÊNG, TÊN KHÁC HẲN NHAU

| Project | File build | Ra EXE |
|---|---|---|
| LedgerReport | **`BuildEXE-LedgerReport.bat`** | `dist\iPOS_Accounting_Report.exe` |
| LedgerStudio | **`BuildEXE-LedgerStudio.bat`** | `dist\iPOS_Ledger_Studio.exe` |

**Không còn `BuildEXE.bat` chung — đã xoá ở cả hai bên.** Bản cũ tự gọi PyInstaller và *đoán*
tên EXE theo thư mục đang đứng; chính bản nằm trong thư mục **LedgerReport** lại build ra
`iPOS_Ledger_Studio` (di sản copy nhầm), và còn thiếu `--add-data version.txt`.

Cơ chế chống nhầm hiện nay — **ba lớp**:
1. **Tên file khác hẳn nhau** — nhìn là biết đang chạy cái nào.
2. **Ghim cứng tên EXE trong `.bat`** (`set "APP_NAME=..."`), truyền thẳng vào
   `python build_exe.py %APP_NAME%`. `build_exe.py` chỉ chấp nhận đúng 2 tên hợp lệ,
   sai là thoát ngay.
3. **Chặn theo đường dẫn** — `.bat` của Studio nằm trong thư mục có chữ `LedgerReport`
   (hoặc ngược lại) thì **dừng, exit 1**, không build. Đã test thật.

`build_exe.py` chạy trần không tham số vẫn đoán theo thư mục như cũ nhưng **in cảnh báo to** —
chỉ dùng khi biết rõ mình đang làm gì.

### 0.1 Khác biệt bản chất: báo cáo đặc thù Chú Long

**LedgerReport có, LedgerStudio KHÔNG có:**

| Mã | Tên | Vì sao đặc thù |
|---|---|---|
| BC001 | KQKD theo tháng | Phân loại chỉ tiêu theo `ITEM_CLASS1_ID` (CF, THUCAN, MC, TA, CB…) và `EXPENSE_CLASS_ID` (THTT, TTTM, CPVH, TL, BH…) — **bộ mã danh mục riêng của Chú Long**, DB khác không có |
| BC002 | KQKD theo công việc | như trên, tách thêm theo `JOB_ID` |
| BC003 | KQKD theo tháng (tuỳ chỉnh) | như BC001 + dòng phụ VH.PHH / VH.PQC |
| BC004 | KQKD theo công việc (tuỳ chỉnh) | như BC002 |
| BC011 | **LCTT gián tiếp (Chú Long)** | Mẫu riêng theo yêu cầu Chú Long, không phải B03-DN chuẩn |

Bốn báo cáo KQKD chạy qua engine `_calc_results()` — engine này **map cứng** bộ mã danh mục của
Chú Long vào ~40 chỉ tiêu. Bê sang DB khác thì mọi chỉ tiêu về 0 mà không báo lỗi.

**Phần còn lại (BC005–BC010, BC012–BC014 và 6 tab danh sách) là chuẩn kế toán VN, hai bên dùng chung.**

### 0.2 Luật nghiệp vụ riêng của Chú Long — cẩn thận khi bê qua lại

- **Loại đơn vị ngoài cây `'00'`**: `IACC_CHULONG` có đúng 1 đơn vị mồ côi (`66` — CPMCL-HCM-SEVEN AM)
  phải loại khỏi mọi báo cáo mặc định. `_get_external_org_ids()` suy ra bằng cách lần `PARENT_ORGANIZATION_ID`
  về gốc `'00'`.
  ⚠️ **DB không có đơn vị gốc `'00'` thì mọi đơn vị bị coi là "ngoài cây" → báo cáo trả 0 dòng, không
  báo lỗi.** Đã có chốt an toàn trong `_get_external_org_ids()` (không thấy `'00'` ⇒ không lọc gì).
- **Mã CĐKT `1311`/`1312`** tách theo nhóm đơn vị `{42, 51, 36, 65, 18, 31}` — danh sách cứng của Chú Long.
- `BALANCE_VIEW` của `IACC_CHULONG` **trống 0 dòng**, số dư đầu kỳ phải dồn từ `LEDGER` kể từ 01/01.
  DB khác có thể có `BALANCE_VIEW` thật — đừng giả định là trống.

### 0.3 Luật cứng

**Đang làm ở LedgerReport thì CHỈ sửa LedgerReport.** Được phép ĐỌC LedgerStudio để tham chiếu,
**cấm edit** — trừ khi người dùng yêu cầu rõ ràng làm việc bên đó.

⚠️ **Mã BC0xx cùng số nhưng khác nghĩa giữa hai bên.** Ở LedgerReport:
`BC011` = LCTT gián tiếp (Chú Long), `BC013` = Tổng hợp phát sinh công nợ.
Ở LedgerStudio thì `BC011` = công nợ. Nhìn nhầm là sửa nhầm báo cáo.

> Lịch sử: file CLAUDE.md cũ trong chính thư mục này lại mô tả **LedgerStudio** — đã gây nhầm lẫn thật.
> Tab "Doanh thu chờ phân bổ" cũng bị copy nhầm từ Studio sang Report rồi chết vì cột `RECEIVE_DATE`
> không tồn tại — đã gỡ 15/08/2026.
> Nếu thấy tài liệu nào mâu thuẫn với file này, **file này thắng**, và sửa file kia ngay.

📄 **Sự cố 15/08/2026 và 8 lỗi đã trả giá: xem [SU_CO_15082026.md](SU_CO_15082026.md)** — đọc trước
khi được giao bất kỳ việc "khôi phục / dọn dẹp / viết lại" nào.

---

## 1. 🏗️ KIẾN TRÚC

```
Trình duyệt (Chrome --app)  ──HTTP──>  Flask (server.py, cổng 5050)  ──pyodbc──>  SQL Server
        index.html                          51 route                          IACC_CHULONG
   React + Babel standalone            connection pool 1/DB                (2025 Express)
   (biên dịch JSX ngay trong                gzip response
      trình duyệt, 1 file)
```

- **Backend** — [server.py](server.py) (~5.900 dòng, Python 3.12 + Flask 3 + pyodbc). Một file duy nhất.
- **Frontend** — [index.html](index.html) (~575 KB, một file duy nhất). React + Babel standalone + Tailwind CDN.
  Không có bước build; sửa file là chạy được ngay.
- **Đóng gói** — PyInstaller one-file no-console qua [build_exe.py](build_exe.py) → `dist\iPOS_Accounting_Report.exe`.
  `index.html`, `version.txt`, `icon`, `manifest.json` được nhúng vào EXE bằng `--add-data`.
- **Phiên đăng nhập** — chỉ lưu `session['db_config']`. **KHÔNG có khoá `session['logged_in']`** (xem Bẫy 1).
- **Cache** — `_meta_cache[db_name]` giữ danh mục (đơn vị, TK, hàng hoá, MCP, công việc…) để khỏi JOIN bảng dimension.

### 1.1 Màn hình

**8 tab dữ liệu thô** (đều virtual-scroll, lọc theo cột, xuất CSV stream):
`ledger` (chứng từ tổng hợp) · `sale` · `purchase` · `warehouse` · `warehouse_balance` (tồn kho thực tế) ·
`voucher` (chứng từ tiền) · `income_alloc` (doanh thu chờ phân bổ) · `report`.

### 1.2 Ma trận báo cáo — **BC001 → BC014**

| Mã | Tên | Endpoint | Nguồn |
|---|---|---|---|
| BC001 | KQKD theo tháng | `/api/report` | LEDGER ⋈ DM_ITEM ⋈ DM_EXPENSE |
| BC002 | KQKD theo công việc | `/api/report_by_job` | như trên + `JOB_ID` |
| BC003 | KQKD theo tháng (tuỳ chỉnh) | `/api/report` | như BC001 |
| BC004 | KQKD theo công việc (tuỳ chỉnh) | `/api/report_by_job` | như BC002 |
| BC005 | Bảng cân đối kế toán (TT200, B01-DN) | `/api/balance_sheet` | BALANCE_VIEW + LEDGER |
| BC006 | Bảng cân đối phát sinh (B09-DN) | `/api/trial_balance` | BALANCE_VIEW + LEDGER |
| BC007 | Sổ nhật ký chung (S03a-DN) | `/api/journal` | LEDGER ⋈ DM_ORGANIZATION |
| BC008 | Sổ chi tiết tài khoản (S38-DN) | `/api/account_details` | BALANCE_VIEW + LEDGER |
| BC009 | LCTT trực tiếp (B03-DN) | `/api/cash_flow` | LEDGER theo TK đối ứng |
| BC010 | LCTT gián tiếp (B03-DN) | `/api/cash_flow` | LEDGER theo TK đối ứng |
| BC011 | **LCTT gián tiếp (Chú Long)** | `/api/cash_flow_cl` | `_compute_cdkt` (engine BC005) + LEDGER |
| BC012 | Sổ tiền mặt & tiền ngân hàng | `/api/cash_book` | VOUCHER_VIEW |
| BC013 | **Tổng hợp phát sinh công nợ** | `/api/debt_summary` | BALANCE_VIEW + LEDGER |
| BC014 | 6.2 — Bảng kê hoá đơn bán ra | `/api/vat_sales_report` | VAT_TRANSACTION_VIEW (`DEBIT_CREDIT='CRD'`) |

Engine dùng chung — **sửa một chỗ, ảnh hưởng nhiều báo cáo**:
- `_calc_results()` — phân loại chỉ tiêu KQKD. Dùng bởi BC001–BC004, **và cả BC009/BC010/BC011** (lấy `r['13']` LN trước thuế, `r['07']` chi phí lãi vay). Chỉ được có **MỘT** định nghĩa trong file.
- `_calc_cdkt_balances()` / `_map_account_to_cdkt()` — mã chỉ tiêu CĐKT. Dùng bởi BC005 và `_compute_cdkt` (BC011).
- `_org_filter_sql()` — lọc đơn vị, mặc định **loại đơn vị ngoài cây `'00'`** khi người dùng không chọn.

---

## 2. 💾 PHƯƠNG ÁN BACKUP & PHỤC HỒI

> Phần này sinh ra sau sự cố 15/08/2026: một agent "khôi phục" báo cáo bằng cách nối code vào cuối
> `server.py`, làm chết BC001–BC004 + BC009–BC011. Cứu được **chỉ vì** còn bản git đầy đủ để đối chiếu.

### 2.1 Bốn tầng backup — thiếu tầng nào là có ngày mất

| Tầng | Cái gì | Ở đâu | Ai làm |
|---|---|---|---|
| 1 | **Mã nguồn** | repo con `ledgerreport\` → push GitHub `main` | `.\Sync-And-Backup.ps1 -Commit` |
| 2 | **Bản build EXE** | [GitHub Releases](https://github.com/trungkhanhduong93/ledgerreport/releases) | GitHub Actions tự chạy khi push `main` |
| 3 | **Dữ liệu kế toán** | file `.bak` của SQL Server, chép sang ổ khác / NAS / cloud | job SQL Agent hoặc tay (mục 2.4) |
| 4 | **Bản đối chiếu khi nghi mất code** | git history + EXE cũ trong Releases | mục 2.3 |

### 2.2 ⚠️ Rủi ro cấu trúc PHẢI biết

Thư mục làm việc `LedgerReport\` và repo con `LedgerReport\ledgerreport\` là **HAI BẢN COPY RIÊNG**.
**Chỉ repo con mới được push lên GitHub.** File sửa ở thư mục cha mà quên đồng bộ thì:
GitHub không có, và ổ D hỏng là mất vĩnh viễn.

Git của **thư mục cha** đứng ở commit cũ (bản Vercel 04/07/2026) và có hàng chục file chưa commit —
**đừng tin `git status` ở thư mục cha**, nó không phản ánh cái gì đã được sao lưu.

➡️ **Luật cứng: sửa xong là chạy [`Sync-And-Backup.ps1`](Sync-And-Backup.ps1). Không copy tay từng file.**

```powershell
.\Sync-And-Backup.ps1                          # đồng bộ + đối chiếu hash, chưa commit
.\Sync-And-Backup.ps1 -Commit -Message "fix: ..."   # đồng bộ + commit + push GitHub
.\Sync-And-Backup.ps1 -ZipTo "E:\Backup"       # kèm zip mã nguồn ra ổ khác
```

Script tự: đối chiếu **hash từng file** (không tin lệnh copy), **chặn push nếu remote là GitLab**,
và **cảnh báo file `.py`/`.html` mới chưa nằm trong danh sách đồng bộ**.
Tạo file mới → thêm tên vào mảng `$Files` **ngay lúc đó**, đừng đợi tới lúc build.

### 2.3 Khi nghi ngờ "mất code / báo cáo biến mất"

**Đừng viết lại. Tìm trong lịch sử trước** — lần trước viết lại đã cho ra số sai.

```bash
cd ledgerreport
git log --oneline                       # commit b6553f6 (04/07/2026) là bản ĐẦY ĐỦ đã chạy thật
git show b6553f6:server.py  > /tmp/head_server.py
git show b6553f6:index.html > /tmp/head_index.html
```

Rồi **đối chiếu theo TỪNG HÀM**, đừng diff cả file (file đã tiến hoá nhiều, diff toàn phần vô dụng).
Và luôn so **danh sách hàm + route** giữa hai bản để phát hiện thứ bị xoá mất:

```python
python -c "
import ast
def names(p):
    t=ast.parse(open(p,encoding='utf-8').read())
    fn={n.name for n in t.body if isinstance(n,ast.FunctionDef)}
    rt={d.args[0].value for n in ast.walk(t) if isinstance(n,ast.FunctionDef)
        for d in n.decorator_list
        if isinstance(d,ast.Call) and getattr(d.func,'attr','')=='route' and d.args}
    return fn,rt
hf,hr=names('/tmp/head_server.py'); cf,cr=names('server.py')
print('HAM BI MAT  :', sorted(hf-cf) or '(khong)')
print('ROUTE BI MAT:', sorted(hr-cr) or '(khong)')
"
```

Nếu git cũng không có: **tải EXE cũ từ GitHub Releases**, giải nén bằng `pyinstxtractor`, dịch ngược
`server.pyc` — đã làm thật ngày 15/06/2026 để dựng lại `_calc_results`. Các file `*_dis.txt`,
`get_report_full.txt` trong thư mục này là sản phẩm của lần đó, **giữ lại, đừng xoá**.

### 2.4 Backup dữ liệu kế toán (SQL Server)

DB `IACC_CHULONG` ~10,6 GB, recovery model **SIMPLE** (không có log backup → chỉ phục hồi được về
thời điểm bản `.bak` gần nhất). Backup tay khi sắp làm việc gì rủi ro:

```sql
BACKUP DATABASE IACC_CHULONG
TO DISK = N'E:\Backup\IACC_CHULONG_20260815.bak'
WITH COMPRESSION, INIT, STATS = 5;
```

Luật: **chép file `.bak` sang ổ vật lý khác hoặc cloud** — để cùng ổ với DB thì ổ hỏng là mất cả hai.

---

## 3. 🧭 NGUYÊN TẮC LÀM VIỆC

1. **Khoá ngữ cảnh trước** (mục 0).
2. **Sửa targeted** — đọc file trước khi sửa, không rewrite cả file. Rewrite xoá mất comment và code người khác vừa thêm.
3. **Verify 4 mức, nói rõ đạt mức nào:**
   - **M1 Compile** — `ast.parse(server.py)` + `node check_babel.js` (JSX).
   - **M2 Test repo** — Flask `test_client` in-process (**không** qua cổng 5050, xem Bẫy 6).
   - **M3 Chạy thật** — build EXE, chạy, gọi API thật.
   - **M4 Khớp nguồn sự thật** — **số liệu khớp form sổ sách**. Báo cáo kế toán chỉ được bàn giao ở M4.
4. **Test fail thì tìm nguyên nhân gốc**, không sửa test cho pass.
5. **Trước khi commit/push** thay đổi có logic → chạy skill `pre-push-qa`.
6. **Chỉ push GitHub, cấm push GitLab.** Sự cố sau push thì `git revert`, cấm force-reset.
7. **Báo cáo trung thực:** 🎯 Mục tiêu → ✅ Đã sửa → 🧪 Verify (ghi rõ M1–M4) → 📦 Git → 🔍 Điểm mù.
8. **Cấm đẩy `.exe` vào git.** Bản build phát hành qua GitHub Releases.

---

## 4. 🐛 BẪY ĐÃ TRẢ GIÁ

### Bẫy 1 — `session['logged_in']` KHÔNG TỒN TẠI *(15/08/2026)*
`/api/login` chỉ gán `session['db_config']`. Endpoint nào kiểm `session.get("logged_in")` sẽ **luôn trả 401**,
frontend gặp 401 là `setIsLoggedIn(false)` → **user bị đá về màn hình đăng nhập ngay khi bấm Xem báo cáo**.
Đã giết BC001–BC004 + BC011. Triệu chứng người dùng: *"bấm là văng ra khỏi phần mềm"*.
➡️ Kiểm đúng: `session.get('db_config')`. Nghe báo triệu chứng đó thì `grep -n "logged_in" server.py` đầu tiên.

### Bẫy 2 — Nối code vào cuối `server.py` sinh hàm trùng tên *(15/08/2026)*
Python lấy định nghĩa **sau cùng**. Một bản `_calc_results` nối thêm ở cuối che mất bản ở trên →
`KeyError: 'expense_class'` ở BC009/BC010. Trước khi thêm hàm, luôn quét trùng tên:
```bash
python -c "import ast,collections;t=ast.parse(open('server.py',encoding='utf-8').read());c=collections.Counter(n.name for n in t.body if isinstance(n,ast.FunctionDef));print({k:v for k,v in c.items() if v>1} or 'khong trung')"
```

### Bẫy 3 — SELECT cột không tồn tại → crash 500 + ngắt pool
`L.EXPENSE_NAME` không có trên bảng `LEDGER` (phải JOIN `DM_EXPENSE` lấy `E.EXPENSE_NAME`).
Tương tự `ORGANIZATION_NAME`. **Đừng đoán tên cột** — introspect `INFORMATION_SCHEMA.COLUMNS`
hoặc tra trong code đã chạy.

### Bẫy 4 — `TRAN_DATE` kiểu `smalldatetime`
Cấm `SUBSTRING(TRAN_DATE, …)` (lỗi 8116). Dùng `CONVERT(VARCHAR(8), TRAN_DATE, 112)` hoặc `MONTH()/YEAR()`.
Tham số ngày từ Python luôn `.strftime('%Y%m%d')`.

### Bẫy 5 — Lệch thứ tự tham số bind
Mảng `params` truyền vào pyodbc phải **đúng thứ tự dấu `?` xuất hiện trong chuỗi SQL**.
`_org_filter_sql` hay được chèn giữa mệnh đề WHERE nhưng params lại `append()` ở cuối → **trả 0 dòng, không báo lỗi**.

### Bẫy 6 — "Ghost server" cổng 5050
Sửa code mà test vẫn ra kết quả cũ vì còn tiến trình `python.exe` / `.exe` cũ giữ cổng.
➡️ **Luôn test bằng `test_client` in-process**, không qua cổng.

### Bẫy 7 — Lọc đa tài khoản
`ACCOUNT_ID LIKE '111,112%'` trả 0 dòng. Dùng `_acc_like_sql("111,112", "ACCOUNT_ID")`.

### Bẫy 8 — `<colgroup>` làm vỡ layout file `.xls`
`exportReportXls()` phải `clone.querySelectorAll('colgroup').forEach(cg => cg.remove())` trước khi ghi file.

### Bẫy 9 — Xuất Excel báo cáo phân trang bị thiếu dòng
DOM chỉ có trang hiện tại. Dùng helper `exportFullXls` (backend nhận `page_size=0` trả toàn bộ).
Backend phải chặn `ZeroDivisionError` khi `page_size=0`.

### Bẫy 10 — EXE đang chạy thì PyInstaller không ghi đè được
Build báo SUCCESS nhưng file `dist\*.exe` không đổi. `taskkill /F /IM iPOS_Accounting_Report.exe /T` trước khi build.
**Luôn so mtime của EXE với `server.py` / `index.html` sau khi build.**

### Bẫy 11 — Middleware gzip nuốt response stream *(15/08/2026)*
`after_request` gọi `response.get_data()` trên response `stream_with_context` sẽ **nuốt trọn generator
vào RAM**, xoá sạch tác dụng streaming của các endpoint xuất CSV. Phải `if response.is_streamed: return response`.
Ngược lại, `send_from_directory` bật `direct_passthrough` khiến `get_data()` ném lỗi bị `except` nuốt →
`index.html` 575 KB **chưa từng được nén**. Phải xử nhánh `direct_passthrough` **trước** nhánh `is_streamed`.

### Bẫy 12 — PowerShell 5.1 đọc `.ps1` không BOM là ANSI
File `.ps1` có tiếng Việt mà lưu UTF-8 không BOM → PowerShell parse hỏng, báo `Unexpected token`.
Luôn lưu `.ps1` bằng **UTF-8 CÓ BOM**. Tương tự: `Set-Content` mặc định ANSI → luôn `-Encoding utf8`.

---

## 5. 🛠️ QUY TRÌNH DEV → RELEASE

```bash
# B1 — Cú pháp (M1)
python -c "import ast; ast.parse(open('server.py',encoding='utf-8').read()); print('PYTHON_OK')"
node check_babel.js

# B2 — Test in-process (M2). KHÔNG chạy qua cổng 5050.
python -c "
import server; c = server.app.test_client()
c.post('/api/login', json={'server':'<SERVER>','database':'IACC_CHULONG','user':'<USER>','password':'<PASS>','driver':'ODBC Driver 17 for SQL Server'})
print(c.get('/api/report?from_date=01/01/2026&to_date=31/01/2026&org_ids=&job_ids=').status_code)
"

# B3 — QA trước khi push (thay đổi có logic)
#      chạy skill pre-push-qa

# B4 — Build EXE (M3)
taskkill /F /IM iPOS_Accounting_Report.exe /T
python build_exe.py            # tự tăng version.txt, sinh version_info.txt

# B5 — Đồng bộ + push (Actions tự tạo Release)
powershell -File Sync-And-Backup.ps1 -Commit -Message "fix: ..."
```

`build_exe.py` chọn tên EXE **theo thư mục đang đứng**: đường dẫn chứa `ledgerreport` →
`iPOS_Accounting_Report`, ngược lại → `iPOS_Ledger_Studio`. **Chạy sai thư mục là ra sai tên EXE.**

CI: [.github/workflows/release.yml](.github/workflows/release.yml) — push `main` là build EXE trên
`windows-latest` rồi tạo Release theo `version.txt`.

---

## 6. 📎 GHI CHÚ HIỆU NĂNG

Nút thắt gốc **không nằm ở code**: DB 10,6 GB / buffer pool 1.410 MB (trần cứng của SQL Express) ≈ **7,7 : 1**
→ phần lớn truy vấn phải đọc đĩa. Index không nâng được trần RAM.

Đã đo và **đừng làm lại**: `IX_LEDGER_ACC_DATE` là có lợi (giảm 95% số trang đọc) — **không drop**;
thêm INCLUDE dài cho `SALE_DETAIL` là lỗ; nâng cấu hình IIS không cứu được nghẽn SQL.
Chi tiết đầy đủ ở skill `chulong-db-perf`.

**Việc rẻ nhất và hiệu quả nhất hiện còn treo ở phía máy chủ:** tắt `AUTO_SHRINK` + `AUTO_CLOSE`
(script `Tat_AutoShrink_AutoClose.sql` trong skill đó). `AUTO_CLOSE` khiến DB đóng lại khi hết kết nối,
người vào sau phải chờ mở lại cả DB — đúng triệu chứng "lúc nhanh lúc chậm".
