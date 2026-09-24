# NHẬT KÝ CÔNG VIỆC — LedgerReport

> Toàn bộ những gì đã làm với **LedgerReport**, và **vì sao**. Đọc file này trước khi sửa tiếp.
> Kiến trúc, ma trận báo cáo, phương án backup: [CLAUDE.md](CLAUDE.md).
> Mổ xẻ sâu sự cố + 4 bài học: [SU_CO_15082026.md](SU_CO_15082026.md).
> Phiên gần nhất: **24/09/2026 (chiều)** · ✅ Đã phát hành **v1.12.0** — `main` = `1e5dee9`,
> Actions `success`, Release là `Latest`.
> 🔑 Phiên này chốt được **luật nghiệp vụ gốc**: iPOS **tự sinh** phiếu nhập `NDCNB` khi phiếu xuất
> `XDCNB` ghi sổ — đổi hẳn cách đọc tab đối chiếu điều chuyển. Xem mục 24/09 ở cuối file.
> 🔴 **Đã phát hành KHI CHƯA đủ tài khoản nhân viên trên Google Sheet** — Đại Ca chốt chấp nhận,
> làm phân quyền sau. Đây là **rủi ro đang chạy**, xem việc số 3.
> Apps Script trên Google: **Version 5** (21/09/2026 19:33), mã bản `2026-09-21c` — **đã triển khai**.
>
> 📌 **Việc còn treo gom ở ngay dưới: [§ VIỆC CẦN LÀM](#-việc-cần-làm--cập-nhật-21092026).**

---

## 📌 VIỆC CẦN LÀM — *cập nhật 24/09/2026*

> Gom hết việc còn treo về một chỗ. Nhận việc mới thì **đọc mục này trước**.
> Trạng thái: **v1.12.2** đã build local, đạt M3, chờ push. Trên GitHub `Latest` là **v1.12.1**.
> ⚠️ Commit tài liệu sau đó **cố ý giữ ở local** — push file `.md` là Actions build lại, thay asset,
> và SHA256 của EXE trên máy Đại Ca vừa khớp xong sẽ lệch ngay. Gộp kèm lần sửa code tiếp theo.

### 🔴 Ưu tiên 1 — làm sớm, càng để lâu càng rủi ro

| # | Việc | Vì sao gấp |
|---|---|---|
| 1 | **Đổi mật khẩu tài khoản `admin`** | Đã lộ trong khung chat ngày 21/09 để chạy phép thử cuối. Đổi ngay trong tab Phân quyền → ô tài khoản → Đổi mật khẩu |
| 2 | ~~Push + phát hành~~ ✅ **XONG 21/09/2026** | Đã push `phanquyen`, gộp `main` (fast-forward, 8 commit), Actions chạy **1m18s** → Release **v1.11.9**. **Tầng 1 và tầng 2 của [backup 4 tầng](#2--phương-án-backup--phục-hồi) nay đều đã có** |
| 3 | 🔴 **TẠO TÀI KHOẢN NHÂN VIÊN TRÊN GOOGLE SHEET — rủi ro ĐANG CHẠY** | Mục này trước đây là *chốt chặn trước khi gộp `main`*. **Đã gộp và phát hành ngày 21/09 khi chưa đủ tài khoản** — Đại Ca được báo trước và chốt "phân quyền sau". Hệ quả **đang có hiệu lực ngay bây giờ**: máy nhân viên ở v1.10.7 mở app là hiện nút cập nhật; bấm xong thì bản v1.11.9 **bỏ hẳn chế độ file**, không có tài khoản trên Sheet là **đăng nhập không được**. Đo 21/09: Sheet mới có **2 tài khoản**. Lùi lại phải tự tải EXE cũ từ trang Releases. ⇒ Càng để lâu càng nhiều người vấp |

### 🟡 Ưu tiên 2 — Đại Ca tự làm được trên giao diện

| # | Việc | Ghi chú |
|---|---|---|
| 4 | **Tick 2 tab mới cho các chức vụ thật** (`KT`, `XSX`, `TM`…) | Cột `dcnb_reconcile` / `po_list` **đã có sẵn trên Sheet** (tạo 21/09). Chỉ cần vào tab Phân quyền tick là ăn. Chức vụ `ADMIN` khỏi cần — app tự tính đủ |
| 5 | **Hỏi Chú Long / iPOS**: nhập mua hàng có bắt buộc bấm từ phiếu PO không? | Quyết định việc có làm được đối chiếu PO ↔ phiếu nhập hay không. Chi tiết 7 khoá đã đo: [Bẫy 20](CLAUDE.md) |
| 6 | **Tắt `AUTO_SHRINK` + `AUTO_CLOSE`** trên SQL Server | Việc **rẻ nhất, hiệu quả nhất** còn treo ở phía máy chủ. `AUTO_CLOSE` đúng là triệu chứng "lúc nhanh lúc chậm". Script `Tat_AutoShrink_AutoClose.sql` trong skill `chulong-db-perf` |

### 🟢 Ưu tiên 3 — việc code, chưa chặn ai

| # | Việc | Ghi chú |
|---|---|---|
| 7 | **Bộ lọc Đơn vị của tab điều chuyển nội bộ** áp cho phía **XUẤT** | Hệ quả: tài khoản chỉ được xem đơn vị cửa hàng **không thấy hàng chuyển đến mình** (bên xuất là kho tổng `01`). Đại Ca dùng tài khoản toàn quyền nên chưa vướng. Mở cho cửa hàng thì phải đổi sang lọc OR cả hai phía — **cần Đại Ca chốt** |
| 8 | **Xoá file rác**: `phanquyen.json` (972 B, 4 tài khoản test) + `dist/phanquyen.json.cu` (1.002 B) | Vô dụng từ khi bỏ chế độ file 21/09. Cả hai đã `.gitignore` nên không lộ, chỉ là rác |
| 9 | Màn đăng nhập **chưa bắt buộc** điền Tài khoản ứng dụng | Để trống thì phải chờ Google **4–7 giây** mới báo lỗi, thay vì chặn ngay tại chỗ |
| 10 | Dropdown lọc **Đơn vị** vẫn hiện tên đơn vị ngoài quyền | Chọn vào ra 0 dòng — **lộ tên, không lộ số** |
| 12 | ~~Hàng chip tụt về 0 khi bấm chọn một chip~~ ✅ **XONG 24/09/2026** | Sửa cả **ba** tab (`dcnb_reconcile`, `btp_reconcile`, **`po_list`** — tab này cũng dính, phát hiện lúc sửa). Cờ `bo_trang_thai` + `so_dong` tách theo trạng thái. Đối chứng trước/sau: **không chậm đi** |
| 15 | ~~Bấm chip chậm gấp ~4 lần~~ ✅ **XONG 24/09/2026** | Dựng `DC` ra bảng tạm `#dc` một lần. Chip `Đã nhận đủ` **42,9s → 7,9s**, trang 2 **50,1s → 6,6s**, đổi cột sắp xếp **45,9s → 7,3s**. Đánh đổi: ô tìm mã hàng chậm thêm ~2s |
| 13 | ~~Phiếu `POSTED` mà 0 dòng `WAREHOUSE` bị tab giấu~~ ✅ **ĐÓNG 24/09/2026 — KHÔNG phải lỗi** | Đo cả năm 2026: chỉ **5/20.089** `XDCNB` · **4/19.479** `NDCNB` · **2/21.848** `XKHOSXBTP` · **1/21.561** `NSP` (≤0,02%), và **cả 12 phiếu đều có số lượng = 0** — phiếu rỗng. Phiếu rỗng thì không có gì để đối chiếu ⇒ giấu đi là **đúng**. Không sửa dòng code nào |
| 14 | ~~Hai chip tên gần giống nhau nằm cách xa~~ ✅ **XONG 24/09/2026** | Đã đưa `Không thấy phiếu xuất` lên ngay sau `Không thấy phiếu nhập` — hai chiều ngược của cùng một việc thì để cạnh nhau |
| 11 | **Nâng 3 GitHub Action lên bản chạy Node 24** | Kẹt vì token `gh` thiếu scope `workflow`. Đại Ca chạy `gh auth refresh -h github.com -s workflow` hoặc sửa thẳng trên web GitHub. Tiện tay thêm `paths-ignore` — [chi tiết](#-việc-còn-treo--nâng-3-action-lên-bản-chạy-node-24) |

### ⚠️ Giới hạn thiết kế — KHÔNG phải lỗi, đừng "sửa giúp"

| Giới hạn | Vì sao cố ý |
|---|---|
| **Thu hồi quyền chỉ có hiệu lực khi người đó đăng nhập lại** | Quyền chốt MỘT LẦN lúc đăng nhập. Gọi Google ở mọi request thì mỗi cú bấm chờ 1–3 giây |
| **Mất mạng vẫn vào được 7 ngày bằng mật khẩu cũ** trên máy khác | Bản cache offline — cùng mô hình credential-cached như Windows domain. Nút "Tải lại" chỉ làm mới phiên của **chính mình** |
| **Khởi động lại app là phải đăng nhập lại** | Kho phiên nằm trong RAM. Đổi lại là quay về [Bẫy 17](CLAUDE.md) — mật khẩu SQL nằm đọc được trong cookie |
| Tab điều chuyển nội bộ **6–8,5 giây/tháng** | Dựng lại toàn bộ CTE mỗi lần gọi, ngang `btp_reconcile`. Nút thắt gốc là RAM của SQL Express, không phải code |
| `PO.EMPLOYEE_ID` **trống** ⇒ cột Người lập luôn rỗng | iPOS không ghi. Giữ cột phòng sau này có |

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
7. ~~**Route `/api/version` đăng ký 2 lần**~~ — **ĐÃ XỬ LÝ 19/09/2026.** Đã xoá hàm chết
   `get_app_version_api` (Flask khớp rule đăng ký trước nên `get_version` luôn thắng). Kiểm lại sau
   khi xoá: **không còn route trùng, không còn hàm trùng tên**, `url_map` chỉ còn 1 rule
   `/api/version` → `get_version`, `test_client` GET `/api/version` trả **200**
   `{"status":"ok","version":...}`. Frontend chưa từng đọc `is_frozen` từ endpoint này nên không
   ảnh hưởng gì; `/api/check_update` vẫn tự trả `is_frozen` riêng, giữ nguyên.

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

### Phát hành

Commit `4cc22af` → push thẳng `main` (`e11d2af..4cc22af`), 6 file / +290 −19. Actions chạy **1 phút
6 giây, thành công**; Release [**v1.10.7**](https://github.com/trungkhanhduong93/ledgerreport/releases/tag/v1.10.7)
tự tạo, đính `iPOS_Accounting_Report.exe` (13.056.524 bytes) + bản `.zip`.

⚠️ QA trước push phải chạy **bằng tay**: **skill `pre-push-qa` mà mục 3.5 của [CLAUDE.md](CLAUDE.md)
bắt chạy KHÔNG tồn tại trên máy này** — không có `.claude/skills` ở cả repo lẫn user dir (kiểm
15/09/2026). Đã chạy thay bằng: M1 `ast.parse` + `check_babel.js` → quét trùng tên hàm/route → quét
secret 290 dòng thêm mới (sạch) → smoke 12 endpoint in-process → kiểm không có `.exe` bị stage.

### 🔑 Chốt lại quy trình phát hành — không cần ai duyệt

| Kiểm | Kết quả thật (15/09/2026) |
|---|---|
| Quyền tài khoản đang dùng | `push=true`, `admin=false`, `maintain=false` |
| Branch protection trên `main` | **KHÔNG CÓ** — API trả `404 Not Found` |
| Workflow cần approval? | Không — `release.yml` không khai `environment:` |
| Release sinh ra | `draft=false`, `prerelease=false` → công khai ngay |

⇒ **Sửa code → QA → push `main` → xong.** Actions tự build EXE trên `windows-latest` rồi đính vào
Release, **không cần tự build EXE để phát hành** (bản build ở máy chỉ để đạt M3 tại chỗ).

**Máy khác nhận update:** app mở lên **sau 1 giây tự gọi** `/api/check_update` → đọc
`api.github.com/.../releases/latest` (timeout 3 giây), so semver, lớn hơn thì hiện banner;
**người dùng phải bấm** mới tải + ghi đè. Máy không vào được `api.github.com` thì im lặng bỏ qua.

⚠️ **`version.txt` quyết định tag** — quên tăng version mà vẫn push thì `action-gh-release` ghi đè
lên Release cũ cùng tag, máy khác không thấy bản mới. `BuildEXE-LedgerReport.bat` tự tăng file này,
**nhớ commit kèm**.


---

## 19/09/2026 — Phân quyền: PBKDF2 + tab Phân quyền + quyền theo đơn vị (nhánh `phanquyen`, CHƯA push)

> Chi tiết đầy đủ ở nhật ký ngoài repo (Ngày 7). Đây là bản tóm tắt trong repo.

**Bước ngoặt:** iPOS **mã hoá 2 chiều (AES-128)**, KHÔNG băm — bằng chứng: `SEC_USER.USER_PASSWORD` có 2
độ dài (24/44 ký tự) tùy độ dài mật khẩu (hash thì cố định độ dài). ⇒ **bỏ mật khẩu iPOS**, tool tự quản
mật khẩu riêng bằng **PBKDF2**.

**Đã làm (code + M1/M2/M3-lite + build EXE `v1.11.0`):**
1. **Khung quyền theo mục** — 24 mục (7 tab + BC001..016 + `perm_admin`). Guard `_perm_guard`
   (`@app.before_request`) trả **403** (né Bẫy 1). 3 endpoint dùng chung guard theo tham số `report=`;
   `/api/cash_flow` cắt `direct`/`indirect` theo quyền. `/api/my_perms` + ẩn menu FE.
2. **Đăng nhập PBKDF2** — `_pbkdf2_hash/verify`, `_load_phanquyen` (file cạnh EXE ưu tiên, không có →
   ADMIN bootstrap), `/api/login` xác thực tài khoản tool trước, mật khẩu KHÔNG lưu session. Màn đăng
   nhập thêm "Tài khoản ứng dụng".
3. **Tab "Phân quyền"** (chỉ ADMIN) — `PermAdminPanel`: CRUD user, lưới chống mất admin cuối. Quyền lưu
   **theo từng user** (`items` = tick 24 mục), nhóm chỉ còn là nhãn.
4. **Quyền theo ĐƠN VỊ (row-level)** — `_current_allowed_orgs()` ép tập trung trong `_org_filter_sql`
   (điểm DUY NHẤT). Sửa 7 builder tab + vá 2 lỗ (btp dựng IN thẳng; cache `cash_book` thiếu allowed_orgs
   trong key). Form tick đơn vị, mặc định tất cả. Verify DB thật: giới hạn 1 đơn vị chỉ thấy đơn vị đó,
   chọn ngoài quyền → 0 dòng.

**Đang bàn dở (phiên sau):** nơi lưu tài khoản dùng chung nhiều máy → **chốt hướng Google Sheet** (mỗi user
1 hàng, quyền theo cột, hash mật khẩu; đăng nhập băm-lại-so). Nút thắt: cần Đại Ca tạo **Service Account +
key** trên Google Cloud (agent không tự làm). Đánh đổi: cần internet để đăng nhập.

**Chưa làm / điểm mù:** `secret_key` cứng (cookie giả mạo được / phiên cũ sống qua rebuild); dropdown lọc
Đơn vị vẫn hiện tên đơn vị ngoài quyền (chọn vào 0 dòng); xoá 4 tài khoản test trước khi phát hành; CHƯA
commit/push (main vẫn v1.10.7).

**File test:** `phanquyen.json` (đã .gitignore) — `admin1/admin@123`, `tonghop1/th@123`, `ketoan1/kt@123`,
`xuong1/xsx@123`. Mở EXE bằng double-click/Start-Process (mở qua terminal bị dọn theo phiên).

---

## 20/09/2026 — Tài khoản dùng chung trên Google Sheet (nhánh `phanquyen`, CHƯA push)

Chốt bỏ hướng Service Account, chuyển sang **Apps Script Web App**: không phải phát key JSON, không
thêm `google-api-python-client` (~18 MB vào EXE), `server.py` gọi bằng `urllib` đã có sẵn từ trước.

### Bốn quyết định của Đại Ca

1. **Apps Script tự kiểm mật khẩu** — bảng hash không bao giờ rời khỏi Sheet, app chỉ nhận về quyền.
2. **Mất mạng vẫn đăng nhập được 7 ngày** bằng bản cache trên máy, có banner vàng "Chạy offline".
3. **CHỨC VỤ quyết định toàn bộ quyền** — bỏ tick riêng 24 mục cho từng người (khác bản trước).
   Riêng **đơn vị được xem vẫn theo từng người** (cùng chức vụ nhưng khác chi nhánh là chuyện thường).
4. 24 cột quyền đánh dấu `x`, xếp theo nhóm DANH SÁCH / BÁO CÁO / QUẢN TRỊ.

### Băm 2 tầng — vì Apps Script chậm hơn Python 2.500 lần

Bản đầu để Google quay 10.000 vòng: **đăng nhập mất 15 giây**. Đo ra ~0,9ms mỗi vòng HMAC
(Python 200.000 vòng hết 74ms, Apps Script 10.000 vòng hết 9 giây).

Đẩy phần nặng về máy khách: `_dan_xuat_dk()` trong [server.py](server.py) quay **200.000 vòng
(95ms)** với salt `"TOOL_CHULONG|<tài khoản>"` rồi gửi **chuỗi đã băm**; Google băm tiếp 1.000 vòng
với salt ngẫu nhiên riêng. Kết quả: **đăng nhập còn 4–7 giây**, Google không bao giờ thấy mật khẩu
gốc, mà kẻ trộm được cả Sheet vẫn phải trả 201.000 vòng cho mỗi lần đoán.

⚠️ Hệ quả phải chấp nhận: **gõ mật khẩu thẳng trên Sheet không dùng được nữa** (Apps Script quay
200.000 vòng mất ~3 phút). `onEdit` nay tự xoá ô và báo "đặt trong app". Tiện thể hết luôn chuyện
mật khẩu nằm lại trong Version history của Google.

### Ba lỗi chỉ lòi ra khi CHẠY THẬT

| Lỗi | Nguyên nhân | Đã sửa |
|---|---|---|
| `The parameters (number[],String) don't match the method signature` | `Utilities.computeHmacSha256Signature` chỉ nhận **(String,String)** hoặc **(Byte[],Byte[])**, cấm trộn | thêm `_byteCuaChuoi()` |
| `Cannot call SpreadsheetApp.getUi() from this context` | chạy `khoiTao()` lúc không mở bảng tính — 3 sheet **đã dựng xong** rồi mới chết ở dòng cuối, dễ tưởng hỏng | bọc `try/catch` |
| Google kiểm "mật khẩu ≥ 6 ký tự" thành vô nghĩa | nó chỉ còn nhận chuỗi băm 44 ký tự | chuyển phép kiểm về `server.py` |

**Bài test đầu tiên của tôi KHÔNG bắt được lỗi thứ nhất** vì shim Node viết dễ dãi hơn API thật.
Đã siết shim ném lỗi đúng như Google khi trộn kiểu — giờ mới đúng là bài test.

### Gõ tay hash vào ô là sai

Thử đặt lại mật khẩu admin bằng cách gõ 2 ô `PW_HASH`/`SALT` → **đăng nhập vẫn hỏng**: base64 có
`I` hoa và `l` thường nhìn y hệt nhau. Bỏ hẳn cách đó, thêm hằng `ADMIN_DK_BOOTSTRAP` để **chính
Apps Script tự sinh** dòng admin. Không còn chỗ cho sai sót.

### Verify — đạt M3

| Mức | Nội dung |
|---|---|
| M1 | `ast.parse` + `node check_babel.js` + quét trùng tên hàm → sạch |
| Thuật toán | hàm băm Apps Script **4/4 khớp** `hashlib.pbkdf2_hmac`, kể cả mật khẩu tiếng Việt có dấu và mật khẩu rỗng |
| Cache offline | **6/6** — sai mật khẩu chặn, máy lạ chặn, **quá 7 ngày hết hiệu lực**, file không chứa mật khẩu thường |
| M2 | smoke 10/10 ở chế độ Google, không endpoint nào 500 |
| **M3 — Sheet thật** | **7/7**: ping `iter=1000` · admin đăng nhập 24/24 mục · **gửi mật khẩu gốc bị chặn** (chứng minh cơ chế 2 tầng có hiệu lực) · tạo `ketoan1` chức vụ KT01 → đúng **5 mục**, không có `perm_admin` · xoá lại sạch |
| Tầng app | **8/8**: sai mật khẩu chặn trước khi đụng SQL · đúng mật khẩu qua Google rồi mới chết ở SQL · **mất mạng vẫn vào được bằng cache mà vẫn chặn mật khẩu sai** |

M4 không áp dụng — đây là phân quyền, không phải số liệu sổ sách.

### Còn treo
> 🕘 *Ảnh chụp lúc đó — nhiều mục dưới đây nay đã xong. Danh sách còn treo THẬT ở [§ VIỆC CẦN LÀM](#-việc-cần-làm--cập-nhật-21092026).*

- **CHƯA commit/push.** `main` vẫn v1.10.7.
- Thu hồi quyền chỉ có hiệu lực khi người đó **đăng nhập lại** (quyền chốt 1 lần lúc đăng nhập để
  mỗi request không phải chờ Google 2 giây).
- Cột `DON_VI` **để trống = xem tất cả**, không phải "không xem gì" — bỏ tick hết đơn vị trong app
  sẽ thành "xem tất cả"; muốn khoá thì bỏ tick *Cho phép đăng nhập*.
- `secret_key` vẫn ghi cứng trong `server.py`.
- Dropdown lọc Đơn vị vẫn hiện tên đơn vị ngoài quyền (chọn vào ra 0 dòng — lộ tên, không lộ số).
- Tài khoản `admin`/`admin@123` còn nguyên mật khẩu khởi tạo — **phải đổi trước khi phát hành**.

---

## 20/09/2026 (chiều) — Thông báo lỗi nói tiếng người + 3 lỗi lòi ra theo

Đại Ca gặp lỗi đăng nhập, màn hình quăng nguyên cục `('08001', '[08001] [Microsoft][ODBC SQL
Server Driver][DBNETLIB]SQL Server does not exist or access denied...` và yêu cầu ghi cho dễ hiểu.
Lần theo thì ra **bốn** việc, không phải một.

### 1. Dịch lỗi ODBC sang tiếng Việt — `_loi_ket_noi_de_hieu()`

Phân 6 loại: không tới được máy chủ · máy chủ trả lời chậm · sai User/Password SQL · sai tên
database · chưa cài driver · lỗi lạ. Nguyên văn **vẫn giữ**, nằm sau nút *"+ Chi tiết kỹ thuật"*.

⚠️ **Thứ tự xét quan trọng hơn tưởng.** Driver 17 khi không tới được máy chủ trả về CẢ HAI chuỗi
`Login timeout expired` lẫn `Server is not found or not accessible`. Bản đầu xét "timeout" trước
nên báo *"máy chủ quá tải, thử lại sau"* — **dẫn người dùng đi sai hướng**, ngồi chờ thay vì đi bật
VPN. Đã đảo lại: xét "không tới được" trước, "trả lời chậm" sau.

### 2. Apps Script chập chờn thật — phải thử lại

Đo trên máy mạng tốt (0,2s ra google.com): cùng lệnh `ping` lúc 5s, lúc 10,4s, lúc **19,7s rồi trả
HTTP 404**. 404 đó không phải sai URL, là lỗi nhất thời phía Google.

Timeout cũ 15 giây + không thử lại ⇒ **nhân viên sẽ ngẫu nhiên đăng nhập hỏng**, lại còn bị báo
nhầm thành "mất mạng". Nay: timeout **45 giây**, **thử lại 3 lần** (giãn 1,5s → 3s). Đo lại: **5/5
lần thành công, 3,4–5,7 giây**. Thử lại an toàn vì mọi hành động hiện có đều lặp lại vô hại —
thêm hành động mới không chịu được gọi hai lần thì phải bỏ qua vòng lặp đó.

### 3. Báo sai bản chất lúc mất mạng

Cũ: *"Máy này chưa từng đăng nhập thành công"* — không nhắc gì tới Google, người đọc không hiểu
tại sao hôm qua vẫn vào được. Nay nói rõ **"Không kết nối được tới Google (nơi lưu danh sách tài
khoản), và …"**. `_cache_kiem()` thêm cờ thứ 3 để **sai mật khẩu thì không đổ cho mạng**.

### 4. App mặc định dùng driver đời 2000 → mỗi lần lỗi chờ 21 giây

| Driver | Thời gian báo lỗi |
|---|---|
| `SQL Server` (mặc định cũ) | **21,1 giây** — không tôn trọng `timeout=5` |
| `ODBC Driver 17` | **5,2 giây** |

`/api/check_driver` vốn đã trả về danh sách driver có thật trên máy nhưng frontend vứt đi không
dùng. Nay: lấy danh sách đó, **chỉ liệt kê driver có thật**, tự chọn theo thứ tự ưu tiên
17 → 13 → SQL Server, và **nhớ lựa chọn** vào localStorage (trước đây mở lại app là quên).

⛔ **Cố ý KHÔNG tự chọn ODBC Driver 18** — nó mặc định bật mã hoá TLS, máy chủ không có chứng chỉ
hợp lệ là nối không được. Ai cần thì tự chọn trong danh sách.

### Verify — đạt M3 (nhìn tận mắt trên giao diện EXE thật)

- Dịch lỗi: **4/4** phân loại đúng, kể cả phân biệt *máy chủ chết* với *máy chủ sống nhưng chậm*.
- Thử lại + thông báo offline: **3/3**.
- **Trên EXE v1.11.4, mở bằng trình duyệt, điền form và bấm nút thật:** hiện đúng câu
  *"Không kết nối được tới máy chủ 171.244.129.176,9001. Kiểm tra lần lượt: đã bật VPN…"*, nút
  *"+ Chi tiết kỹ thuật"* bung ra nguyên văn lỗi. Nguyên văn ghi `[ODBC Driver 17 for SQL Server]`
  ⇒ chứng minh phần tự chọn driver đã chạy.

Ghi vào CLAUDE.md: thông báo lỗi cho người dùng phải là tiếng Việt dễ hiểu, nguyên văn giấu sau
nút "Chi tiết" — xem [thong-bao-loi-phai-noi-tieng-nguoi] trong bộ nhớ agent.

---

## 21/09/2026 — TỔNG KẾT NGÀY (đọc mục này trước, 7 mục chi tiết nằm dưới)

Một ngày dài, **7 mục**. Tóm tắt để khỏi phải đọc hết:

| # | Việc | Kết quả |
|---|---|---|
| 1 | Tách tab Phân quyền thành **Quản lý tài khoản** / **Quản lý chức vụ** | M2 · bấm thật trên trình duyệt |
| 2 | 🔴 **Mật khẩu SQL nằm đọc được trong cookie** — cookie Flask chỉ được KÝ, không mã hoá | Đã bịt: cookie chỉ còn `sid`, db_config nằm RAM máy chủ. `secret_key` → ngẫu nhiên mỗi lần chạy. **14/14** |
| 3 | **Bỏ hẳn chế độ file** — Google Sheet là nguồn duy nhất | Thiếu cấu hình = **chặn đăng nhập**, thay vì mở toang 24 mục. **24/24** |
| 4 | **Ghim cứng URL + TOKEN** vào `server.py` ⇒ chỉ phát **một file EXE** | Kèm **rate limit** trong Code.gs (khoá 15 phút sau 8 lần sai). **15/15** |
| 5 | 🔴 **Đổi mật khẩu trong tab Phân quyền không có tác dụng** | `_apiLuuUser` chỉ ghi mật khẩu khi TẠO MỚI. Đã sửa. **14/14** |
| 6 | **Ô tài khoản ở header** + nhân viên tự đổi mật khẩu (mẫu SYNA AI PORTAL) | M2 · bấm thật **5/5 ca** |
| 7 | **Triển khai Code.gs lên Google** | **Version 4**, `ping` trả `ban: 2026-09-21b` ✓ |

### Trạng thái tại thời điểm đó *(giữa ngày 21/09 — ngày còn chạy tiếp sau mục này)*

> 🕘 *Ảnh chụp lúc đó, **không** phải trạng thái hiện hành. Bản mới nhất xem đầu file
> + [§ VIỆC CẦN LÀM](#-việc-cần-làm--cập-nhật-21092026).*

| | |
|---|---|
| EXE local | **v1.11.7** (`dist\iPOS_Accounting_Report.exe`) → *sau đó lên **v1.11.9*** |
| Apps Script trên Google | **Version 4** · mã bản `2026-09-21b` → *sau đó lên **Version 5** · `2026-09-21c`* |
| URL + TOKEN | **không đổi** — mọi EXE đã phát vẫn nối được *(vẫn đúng tới giờ)* |
| Git | ⛔ CHƯA commit, CHƯA push → *sau đó **đã commit 5 lần**, vẫn chưa push* |
| Mật khẩu `admin` | vẫn là mật khẩu cũ → *⚠️ nay **đã lộ trong chat**, xem việc số 1 ở § VIỆC CẦN LÀM* |

### Hai sự cố trong ngày — đọc kỹ

1. **Đổi mật khẩu không ăn** (mục 5). Nguyên nhân nằm ở Google chứ không ở EXE, nên build lại EXE
   bao nhiêu lần cũng vô ích. Trường `ban` thêm trong `ping` **bắt được ngay lần dùng đầu tiên**.
2. **Suýt xoá mất TOKEN thật** (mục 7). Dán thẳng `Code.gs` từ repo công khai lên Google ⇒ ghi đè
   token bằng chuỗi giữ chỗ. Cứu được **chỉ vì** lúc đó chưa bấm Triển khai.
   ➡️ Từ nay dùng `python phanquyen_gas/chuan_bi_deploy.py`. Xem **Bẫy 19** trong CLAUDE.md.

### Còn treo sang phiên sau
> 🕘 *Ảnh chụp lúc đó — nhiều mục dưới đây nay đã xong. Danh sách còn treo THẬT ở [§ VIỆC CẦN LÀM](#-việc-cần-làm--cập-nhật-21092026).*


- ⛔ **Chưa commit/push.** Khi push, lệnh quét secret **sẽ báo động ở `_GS_URL_GHIM`/`_GS_TOKEN_GHIM`**
  — đó là **báo đúng**, không phải báo nhầm (Đại Ca đã chốt chấp nhận, xem Bẫy 18).
- **Đổi mật khẩu `admin`** trước khi phát cho nhân viên.
- `phanquyen.json` ở thư mục gốc và `dist/phanquyen.json.cu` nay vô dụng — xoá được.
- `ADMIN_DK_BOOTSTRAP` trên Google nay là chuỗi giữ chỗ (vô hại, xem mục 7).
- Chưa đạt M3 đầy đủ: chưa đăng nhập bằng SQL + tài khoản thật trên EXE v1.11.7.
- Màn đăng nhập chưa bắt buộc điền Tài khoản ứng dụng ở frontend (để trống phải chờ Google 4–7 giây
  mới báo sai, thay vì chặn ngay).

---

## 21/09/2026 — Tab Phân quyền tách làm 2 tab con (nhánh `phanquyen`, CHƯA push)

Đại Ca xem ảnh màn hình iPOS (hai tab *Nhân viên* / *Chức vụ*) rồi yêu cầu tách y vậy: một tab
**Quản lý tài khoản**, một tab **Quản lý chức vụ**. Trước đó hai bảng nằm chồng nhau trong cùng
một trang, phải cuộn xuống mới thấy bảng Chức vụ.

**Đã làm** — chỉ sửa [index.html](index.html), 4 chỗ trong `PermAdminPanel`, **không đụng
`server.py`**:
1. Thêm state `tabCon` ('user' / 'role').
2. Thêm `tabHienTai` — chế độ file **ép cứng về `'user'`**.
3. Tiêu đề trang tách khỏi nút "+ Thêm người dùng"; thêm thanh tab con gạch chân, mỗi tab kèm
   số đếm (số tài khoản / số chức vụ).
4. Bảng tài khoản bọc trong `{tabHienTai === 'user' && (<>…</>)}`; khối chức vụ đổi điều kiện từ
   `{theoChucVu && …}` sang `{tabHienTai === 'role' && …}`.

**Vì sao chế độ file KHÔNG có tab Chức vụ** (Đại Ca chốt): không có `ketnoi.json` thì
`/api/perm/role` trả thẳng 400 *"Chức vụ chỉ sửa được khi dùng nguồn Google Sheet"* — bày ra một
tab bấm vào là báo lỗi thì thà ẩn. Chế độ file trông y hệt trước đây.

**Verify:**

| Mức | Nội dung |
|---|---|
| M1 | `node check_babel.js` → SUCCESSFUL · `ast.parse(server.py)` → OK |
| M3-lite | Dựng trang demo độc lập: **cắt nguyên văn 341 dòng `PermAdminPanel` từ chính `index.html`** (không gõ lại tay), stub `fetch('/api/perm/config')` để khỏi cần VPN + SQL + Google. Mở bằng trình duyệt thật, bấm nút thật |
| Kết quả | Thanh tab hiện đúng số đếm 4/4 · đổi tab đổi đúng bảng · trạng thái tab kiểm bằng `getComputedStyle` (tab đang chọn `rgb(79,70,229)` + viền dưới indigo, tab kia `rgb(148,163,184)` + viền trong suốt) · modal **Sửa chức vụ: KT01** mở đúng 5/24 mục · modal **Sửa: ketoan1** mở đúng chức vụ + 2/4 đơn vị · **chế độ file: thanh tab biến mất hẳn**, chỉ còn bảng Tài khoản |

**Chưa đạt M3 đầy đủ:** chưa build EXE và chưa bấm trên bản chạy thật có SQL + Google Sheet.
Thay đổi thuần bố cục hiển thị, không đụng luồng dữ liệu, nhưng vẫn nên bấm thử một lượt trên EXE
trước khi phát.

**Điểm mù ghi lại (có sẵn từ trước, không phải do lần sửa này):** biến `msg` ở cấp trang chỉ được
hiển thị bên trong hai modal và màn hình nhập mật khẩu. Lỗi từ `load()` (ví dụ *"Lỗi tải danh
sách"*, *"Lỗi kết nối"*) **không hiện ở đâu cả** — bảng chỉ đứng im. Sửa được bằng một dòng, để
lần sau.

---

## 21/09/2026 (tiếp) — Mật khẩu SQL nằm đọc được trong cookie (nhánh `phanquyen`, CHƯA push)

Đại Ca chốt tiêu chí: *"tuyệt đối không dò thấy được thông tin SQL dùng để kết nối"*.
Đi kiểm thì ra một lỗ thật, nằm đúng chỗ không ai ngờ.

### Lỗ — chứng minh bằng code, không phải suy đoán

`session['db_config'] = data` đặt nguyên **server / database / user / password** của SQL vào
cookie. Cookie Flask chỉ được **KÝ để chống sửa, KHÔNG MÃ HOÁ**. Giải ra **không cần
`secret_key`** — chỉ tách phần payload rồi base64 + unzip:

```
{"db_config":{"server":"171.244.129.176,9001","database":"IACC_CHULONG",
 "user":"sa","password":"MatKhauThatCuaSQL",...},"app_user":"ketoan1"}
```

Mở **F12 → Application → Cookies** là đọc được. Mượn máy đồng nghiệp một phút là lấy được
mật khẩu SQL của người đó.

Đi kèm lỗ thứ hai: `secret_key = 'IACC_SECRET_SUPREME_2026'` ghi cứng trong mã nguồn của
repo **CÔNG KHAI** ⇒ ai cũng **tự ký được cookie giả**, tự cấp `app_items` cho mình; và phiên
cũ sống xuyên qua mọi lần build lại. Hai điểm này đã ghi là điểm mù từ 19/09 nhưng chưa sửa.

### Quét hết các đường rò khác — sạch

| Đường | Kết quả |
|---|---|
| Ghi log ra file | không ghi file nào |
| Chỗ nào log `db_config` | không có |
| Endpoint trả `db_config` về trình duyệt | không có |
| `localStorage` | chỉ `iacc_server` / `iacc_db` / `iacc_driver` — **không có mật khẩu** |
| Frontend giữ mật khẩu trong biến | không |
| Thông báo lỗi ODBC (`_loi_ket_noi_de_hieu`) | chỉ dùng `str(e)`, không chạm chuỗi kết nối |
| **Cookie phiên** | ⚠️ **có — nguyên văn mật khẩu** |

⇒ Đúng **MỘT** đường rò, và đã bịt.

### Đã sửa — kho phiên phía máy chủ

- Cookie nay **chỉ còn mã phiên ngẫu nhiên `sid`**. Toàn bộ `db_config` nằm trong
  `_phien_db` (RAM tiến trình), truy cập qua `_db_cfg()` / `_dat_db_cfg()` / `_xoa_db_cfg()`.
- **32 chỗ** trong `server.py` đổi từ `session.get('db_config')` sang `_db_cfg()` — thay cơ học,
  mỗi mẫu đều kiểm đúng số lượng trước khi thay.
- `_dat_db_cfg()` **luôn sinh `sid` mới** mỗi lần đăng nhập ⇒ mã phiên cũ bị lộ không dùng
  lại được (chống session fixation).
- `secret_key` → `os.urandom(32)` mỗi lần khởi động ⇒ **hết đường giả cookie**.
- Ghi rõ `SESSION_COOKIE_HTTPONLY=True`, `SESSION_COOKIE_SAMESITE='Lax'`.
  ⛔ **Cố ý KHÔNG bật `SECURE`** — app chạy `http://localhost:5050`, bật lên là trình duyệt
  ngừng gửi cookie, đăng nhập xong vẫn bị coi là chưa đăng nhập.

### Verify — đạt M2

| Mount | Nội dung |
|---|---|
| M1 | `ast.parse` OK · quét trùng tên hàm: không trùng · không còn `session['db_config']` nào ngoài 2 ghi chú |
| **M2 — 14/14** | Đăng nhập bằng `test_client` (SQL giả), rồi **giải cookie đúng cách kẻ tấn công làm**: không còn mật khẩu, không còn user `sa`, không còn địa chỉ máy chủ, chỉ còn `sid` · app vẫn nhận ra phiên (`/api/my_perms` → 200) · đăng nhập lại đổi `sid`, `sid` cũ bị xoá · đăng xuất dọn sạch kho · sau đăng xuất gọi lại bị chặn 401 · `secret_key` là 32 byte ngẫu nhiên |

Chưa đạt M3 — chưa build EXE, chưa đăng nhập bằng SQL thật.

### ⚠️ Hệ quả vận hành phải báo cho người dùng

**Khởi động lại app là phải đăng nhập lại**, kể cả sau khi tự cập nhật. Trước đây cookie
mang sẵn thông tin kết nối nên app tự dựng lại kết nối mà người dùng không hề hay — tiện,
nhưng tiện đó chính là cái lỗ.

### Quyết định của Đại Ca trong phiên này

1. **Nhân viên VẪN tự gõ thông tin SQL** như hiện nay ⇒ không nhúng credential SQL vào app.
2. **Bỏ hẳn chế độ file** (`phanquyen.json`) — chỉ còn nguồn Google Sheet. Không có phân
   quyền = **không ai vào được**, thay vì mở toang 24 mục như hiện nay. *(chưa làm)*
3. **Nhúng URL + TOKEN vào EXE** để chỉ còn **một file** phát cho nhân viên. *(chưa làm —
   còn chờ Đại Ca chốt đặt token ở GitHub Secrets hay code cứng)*

### Vì sao token Apps Script lộ không đáng sợ (đã tra tận nơi)

Token chỉ được kiểm ở **đúng một chỗ** — cửa vào `doPost` của `Code.gs`. Qua được cửa đó thì
**7/8 lệnh còn đòi mật khẩu**: `nap` / `luu_user` / `xoa_user` / `dat_mat_khau` / `luu_chuc_vu` /
`xoa_chuc_vu` đều gọi `_doiAdmin()` ngay dòng đầu; `dang_nhap` đòi mật khẩu của chính người đó.
Chỉ `ping` là không đòi gì.

⇒ Kẻ cầm token **không đọc được danh sách tài khoản, không sửa được ai, không lấy được bảng
hash, và tuyệt nhiên không chạm được số liệu kế toán** (số liệu ở SQL Server sau VPN).
Cái mất thật sự: **`Code.gs` không có rate limit** nên người lạ đoán mật khẩu không giới hạn
số lần (thực tế ~1.800 lần/giờ vì mỗi lần phải quay 200.000 vòng + chờ Apps Script ~2s), và
có thể **spam cho cạn quota Apps Script** ⇒ nhân viên không đăng nhập được trong ngày.
⇒ Nếu chọn nhúng token vào EXE thì **phải thêm khoá tạm sau N lần sai** vào `Code.gs`.

---

## 21/09/2026 (tiếp) — Bỏ hẳn chế độ file: Google Sheet là nguồn DUY NHẤT

Đại Ca chốt: bỏ `phanquyen.json`, mọi máy đều đối chiếu tài khoản + quyền trên Google Sheet.

### Vì sao phải bỏ — không phải cho gọn mà vì một cái bẫy

Nhánh dự phòng cũ xếp thế này:

```
có ketnoi.json ? → hỏi Google Sheet
không         ? → có phanquyen.json ? → tra file
                   không             ? → app_group = 'ADMIN'   ← Ở ĐÂY
```

Dòng cuối nghĩa là: **máy nào chỉ có miền EXE là bất kỳ ai đăng nhập được SQL sẽ thấy đủ
24 mục, mọi đơn vị** — im lặng, không một dòng cảnh báo, nhìn bằng mắt thì y hệt bản đúng.
Quên chép cấu hình sang một máy = máy đó coi như không có phân quyền.

Nay: thiếu cấu hình ⇒ **chặn đăng nhập (503)** kèm câu tiếng Việt dễ hiểu, nguyên văn giấu
sau `chi_tiet` — xem `_loi_chua_cau_hinh()`.

### Đã bỏ khỏi `server.py`

| Thứ | Ghi chú |
|---|---|
| `_load_phanquyen` · `_app_users` · `_find_app_user` · `_effective_matrix` · `_save_phanquyen` · `_user_items` · `_has_active_admin` | 7 hàm chỉ phục vụ chế độ file |
| `PERM_MATRIX` · `PERM_GROUP_NAMES` | bảng nhóm quyền **ghi cứng trong code**. Chức vụ nay nằm trên Sheet ⇒ giữ lại là có **HAI nguồn sự thật mâu thuẫn nhau**, đúng loại bẫy đã gây tai nạn trước đây |
| nhánh `elif users:` trong `/api/login` | đường đăng nhập bằng file |
| nhánh chế độ file trong 4 endpoint quản trị | `perm_config` · `perm_save_user` · `perm_delete_user` · `perm_set_password` |

`_current_perms()` trước đây không có `app_items` thì rơi về file rồi cuối cùng về *'ADMIN = full'*
— tức là **phiên hỏng thì được toàn quyền**, đúng chiều ngược với cái cần. Nay trả tập **rỗng**.
`_current_group()` cũng bỏ mặc định `'ADMIN'`.

**Giữ lại:** `_pbkdf2_hash` / `_pbkdf2_verify` — nay chỉ còn phục vụ **bản cache offline 7 ngày**,
không còn dùng để đăng nhập.

### Đã bỏ khỏi `index.html`

State `nguon` · biến `theoChucVu` · 4 chỗ rẽ nhánh theo nó · toàn bộ **checklist tick riêng 24 mục
cho từng người** trong modal Sửa · hai hàm `applyPreset` / `toggleItem` (`applyPreset` vốn đã là
code chết, không ai gọi). Modal Sửa nay chỉ còn **dropdown chức vụ** + danh sách đơn vị.

### Verify — đạt M2

| Mức | Nội dung |
|---|---|
| M1 | `ast.parse` OK · `node check_babel.js` SUCCESSFUL · không còn tham chiếu treo nào |
| **M2 — 24/24** | (A) **thiếu cấu hình: 503, không cấp phiên, gọi `/api/ledger` vẫn bị chặn** · (B) có cấu hình: kế toán đăng nhập → đúng 5 mục / chức vụ KT01 / 2 đơn vị; mục ngoài quyền **403**; tab Phân quyền **403** · (C) sai tài khoản → 401, không lọt vào bằng ADMIN · (D) 7 hàm + 2 bảng ghi cứng đã biến mất, `PERM_ALL_ITEMS` vẫn đủ 24 |
| Giao diện | Mở trên trình duyệt thật: 2 tab con chạy đúng · modal Sửa **chỉ còn dropdown chức vụ**, checklist 24 mục đã biến mất |

Chưa đạt M3 — chưa build EXE, chưa đăng nhập bằng SQL + Google Sheet thật.

### Còn treo sau việc này
> 🕘 *Ảnh chụp lúc đó — nhiều mục dưới đây nay đã xong. Danh sách còn treo THẬT ở [§ VIỆC CẦN LÀM](#-việc-cần-làm--cập-nhật-21092026).*


- **Việc 3 chưa làm:** nhúng URL + TOKEN vào EXE để chỉ phát một file. ⚠️ **Giờ nó quan trọng
  hơn trước**: sau khi bỏ chế độ file, máy thiếu `ketnoi.json` là **không ai đăng nhập được**,
  chứ không phải "chạy như cũ" nữa.
- ⛔ **Chưa nhúng thì ĐừNG PHÁT bản này** — hoặc phải chép kèm `ketnoi.json` sang từng máy.
- `Code.gs` **không có rate limit** — phải thêm khoá tạm sau N lần sai TRƯỚC khi phát EXE
  có token công khai.
- `phanquyen.json` ở thư mục gốc và `dist/phanquyen.json.cu` nay **vô dụng** — xoá được.
  Giữ dòng `phanquyen.json` trong `.gitignore` cho chắc.
- Màn đăng nhập **chưa bắt buộc** điền Tài khoản ứng dụng ở phía frontend; để trống thì Google
  trả "Sai tài khoản hoặc mật khẩu" — đúng nhưng chậm hơn 4–7 giây so với chặn ngay tại chỗ.

---

## 21/09/2026 (tiếp) — Ghim cứng token + chống dò mật khẩu: chỉ còn MỘT file EXE

Đại Ca chốt: **code cứng URL + TOKEN vào `server.py`**, không phát kèm file cấu hình nào.

### Trước khi làm — gỡ một hiểu nhầm quan trọng

Đại Ca hỏi *"token này là token của Google Sheet đúng không"*. **Không.** Nó là chuỗi
**Đại Ca tự gõ** ở `const TOKEN` trong `Code.gs`, Google không biết nó là gì.

| | Token Google thật | `TOKEN` của app này |
|---|---|---|
| Ai cấp | Google | Đại Ca tự đặt |
| Cầm được thì vào được | **Drive, Gmail, mọi Sheet** | chỉ gõ cửa đúng một script |
| App này có không | ❌ **KHÔNG CÓ** | ✅ có |

Trong toàn bộ app **không có một mẩu credential Google nào** — đó chính là lý do 19/09 bỏ hướng
Service Account. Lộ `url` + `token` **không cho ai vào tài khoản Google của Đại Ca**.

⚠️ Ghi lại cho sòng phẳng: luật cũ của chính Đại Ca là *"không ghi credential vào bất kỳ file nào
trong repo"*. Việc này **đi ngược luật đó**, đã cảnh báo hai lần và Đại Ca chốt chấp nhận, vì
token Apps Script không mở vào dữ liệu. **Luật vẫn giữ nguyên cho mọi thứ khác — nhất là SQL.**

### Đã làm

**1. Ghim cứng vào `server.py`** — `_GS_URL_GHIM` / `_GS_TOKEN_GHIM`, kèm khối ghi chú dài giải
thích vì sao cố ý. Thứ tự ưu tiên trong `_gs_config()`:

```
1. ketnoi.json cạnh EXE      (để đổi gấp, khỏi build lại — gửi 1 file là xong)
2. ketnoi.json nhúng trong EXE
3. BẢN GHIM CỨNG             ← đường mặc định, dùng cho mọi máy bình thường
```

Tức là **file ĐÈ LÊN bản ghim**, không phải ngược lại. Bình thường không cần file nào.

**2. Chống dò mật khẩu trong `Code.gs`** — đây là phần **bắt buộc đi kèm**: token công khai nghĩa
là ai cũng gọi được API, mà trước đó `Code.gs` **không có giới hạn số lần thử nào**.

- Khoá tạm **15 phút** sau **8 lần sai** trong cửa sổ 15 phút. Đăng nhập đúng thì xoá bộ đếm.
- Áp cho **cả `_doiAdmin`** — dò mật khẩu admin là nguy nhất (vào được là đọc/sửa cả bảng).
- Dùng `CacheService`, không đụng Sheet ⇒ không làm chậm đăng nhập.
- **Đang bị khoá thì KHÔNG ghi log** — nếu không, mỗi lần kẻ lạ gõ là một dòng, sheet Nhật ký
  phình vô ích. Dòng báo khoá ghi đúng **một** lần lúc bắt đầu khoá.

⚠️ **Cố ý chỉ khoá THEO TỪNG TÀI KHOẢN, không khoá toàn cục.** Khoá toàn cục thì một kẻ rảnh rỗi
gõ bậy vài chục lần là **khoá được cả công ty** — đổi một lỗ nhỏ lấy một lỗ to hơn.

Hiệu quả đo được: không giới hạn thì dò ~1.800 lần/giờ; nay còn **32 lần/giờ mỗi tài khoản**
— giảm 56 lần.

### Verify — đạt M2

| Mức | Nội dung |
|---|---|
| M1 | `ast.parse` OK · URL/TOKEN ghim **khớp từng ký tự** với `ketnoi.json` đang chạy (kiểm bằng so sánh, không in giá trị ra màn hình) |
| Bản ghim | **4/4** — chạy từ thư mục **không có** `ketnoi.json`: vẫn lấy được cấu hình, url/token đúng, `/api/login` không còn bị chặn 503 |
| Rate limit | **15/15** bằng shim Node **siết sát API Google** (`get()` chỉ trả String, `put()` bắt buộc String, TTL ≤ 21600, hết hạn thì trả null): sai 7 lần chưa khoá · đăng nhập đúng xoá bộ đếm · chạm ngưỡng thì khoá và ghi **đúng 1** dòng log · đang khoá thì **gõ đúng mật khẩu vẫn bị chặn** · gõ thêm 20 lần **không ghi thêm dòng nào** · **người khác vẫn đăng nhập bình thường** · hết hạn vào lại được · admin chịu chung lưới · quá cửa sổ thì bộ đếm về 0 |

⚠️ Shim Node viết dễ dãi thì test vô dụng — bài học 20/09 (shim cũ không bắt được lỗi
`computeHmacSha256Signature` trộn kiểu). Shim lần này ném lỗi đúng như Google.

Chưa đạt M3 — chưa build EXE, và **`Code.gs` mới chưa được triển khai lên Google**.

### ⛔ Hai việc Đại Ca phải tự làm (agent không làm thay được)
> 🕘 *Ảnh chụp lúc đó — nhiều mục dưới đây nay đã xong. Danh sách còn treo THẬT ở [§ VIỆC CẦN LÀM](#-việc-cần-làm--cập-nhật-21092026).*


1. **Triển khai lại Apps Script**: mở Sheet → Extensions → Apps Script → dán `Code.gs` mới →
   Triển khai → **Quản lý bản triển khai** → bút chì → Phiên bản: **Mới** → Triển khai.
   ⛔ **ĐỪNG bấm "Triển khai mới"** — nó sinh URL khác và mọi EXE đã phát sẽ chết.
2. Quyết định có **đổi token mới** hay không. Token hiện tại sẽ công khai ngay khi push.
   Đổi hay không thì kết quả cuối cũng như nhau (token mới cũng công khai) — nêu ra để Đại Ca biết.

### Còn treo
> 🕘 *Ảnh chụp lúc đó — nhiều mục dưới đây nay đã xong. Danh sách còn treo THẬT ở [§ VIỆC CẦN LÀM](#-việc-cần-làm--cập-nhật-21092026).*

- **CHƯA build EXE, CHƯA commit/push.**
- Nếu `Code.gs` mới chưa lên Google mà đã phát EXE: app vẫn chạy bình thường, chỉ là **chưa có
  lưới chống dò** — không hỏng gì, nhưng mất đúng cái lớp bảo vệ vừa thêm.
  → ✅ **Đã triển khai cuối ngày 21/09 (Version 4)** — xem mục cuối file.
- `phanquyen.json` ở thư mục gốc và `dist/phanquyen.json.cu` nay vô dụng — xoá được.

### Build EXE v1.11.5 + chạy thật — đạt M3 (phần kiểm được)

Build qua `BuildEXE-LedgerReport.bat` (lớp chặn theo đường dẫn cho qua vì thư mục chứa chữ
`ledgerreport`). **v1.11.4 → v1.11.5.**

⚠️ **Một phép đo tôi làm SAI, ghi lại để đừng lặp:** tôi thử kiểm nội dung EXE bằng cách tìm
chuỗi thô (`_GS_TOKEN_GHIM`, `_phien_db`…) trong file `.exe`. **Vô hiệu** — PyInstaller nén
bytecode vào PYZ nên không chuỗi nào tìm thấy, kể cả thứ chắc chắn có. Kết quả "đã bị xoá → đạt"
cũng là đạt giả. **Muốn biết EXE chứa gì thì phải CHẠY nó.**

| Phép kiểm | Kết quả |
|---|---|
| Bẫy 10 — EXE mới hơn code | EXE **11:58** > `server.py` **11:46** ✓ |
| `/api/version` trên EXE thật | `{"status":"ok","version":"1.11.5"}` ✓ |
| **Bản ghim cứng có chạy không** | Tạm đổi tên `dist/ketnoi.json` → EXE **không còn file cấu hình nào**. Đăng nhập với tài khoản không tồn tại → **HTTP 401 sau 3,3 giây**, nội dung `"Sai tài khoản hoặc mật khẩu"` — **đúng câu Google trả về** |
| Không cấp phiên khi đăng nhập hỏng | `curl -c` không nhận được cookie nào ✓ |

**Vì sao 401-sau-3,3-giây là bằng chứng quyết định:** nếu bản ghim KHÔNG chạy thì `_gs_config()`
trả None ⇒ `_loi_chua_cau_hinh()` ⇒ **503 trả về tức thì (0 giây)**. Nhận được 401 kèm đúng câu
của Google nghĩa là app **đã gọi Apps Script thật** mà trong tay không có file cấu hình nào.
⇒ Ghim cứng hoạt động, và chế độ file đã bỏ hẳn (không rơi về `ADMIN`).

**Chưa kiểm được trên EXE thật** (cần VPN + SQL + tài khoản thật, không có trong phiên này):
đăng nhập thành công end-to-end · cookie không chứa mật khẩu SQL (đã đạt 14/14 ở M2) ·
tab Phân quyền 2 tab con · **rate limit** (vì `Code.gs` mới **chưa deploy lên Google**).

Đã trả lại tên `dist/ketnoi.json` sau khi test.

---

## 21/09/2026 (tiếp) — 🔴 Đổi mật khẩu trong tab Phân quyền KHÔNG có tác dụng

**Triệu chứng Đại Ca báo:** đổi mật khẩu `admin` trong tab Phân quyền → app báo lưu thành công →
**đăng nhập lại không vào được**, màn hình hiện *"Sai tài khoản hoặc mật khẩu"*.

### Nguyên nhân — `_apiLuuUser` trong Code.gs

```javascript
if (moi) {                                    // ← moi = TẠO MỚI
    if (!p.mat_khau) return {...};
    const kq = _doiMatKhauDong(b, soDong, p.mat_khau);
}
```

**Mật khẩu CHỈ được ghi khi tạo tài khoản mới.** Sửa tài khoản đã có thì `p.mat_khau` bị **vứt đi
trong im lặng** — không một dòng nào xử lý.

Mà ô *"Mật khẩu mới (để trống nếu giữ nguyên)"* trong modal **Sửa** đi đúng đường đó:
modal Sửa → `/api/perm/user` → `luu_user`. App báo "Lưu thành công", Sheet cập nhật tên/chức vụ/
đơn vị — **nhưng cột `PW_HASH` không hề đổi**. Gõ mật khẩu mới thì không khớp hash cũ.

✅ **May: mật khẩu CŨ vẫn còn nguyên hiệu lực** nên không mất tài khoản. Đại Ca vào lại bằng
`admin@123`.

⚠️ Endpoint `/api/perm/password` (đường đổi mật khẩu *đúng*, có xoá cache offline) vẫn nằm đó
trong `server.py` nhưng **không frontend nào gọi tới** — hôm 21/09 tôi đã thấy điều này và chỉ ghi
vào điểm mù, **không lần tiếp xem vậy thì đổi mật khẩu đi đường nào**. Nếu lần thì đã ra lỗi này
trước khi Đại Ca vấp.

### Lỗi thứ hai — bài test bắt được, chưa ai gặp

`_apiLuuUser` **ghi USER_ID / họ tên / chức vụ / đơn vị vào Sheet RỒI MỚI** kiểm *"tài khoản mới
phải có mật khẩu"*. Tạo tài khoản mà quên gõ mật khẩu ⇒ Sheet đã có một dòng **không có PW_HASH**
(tài khoản ma). Tệ hơn: lần lưu sau `moi` thành `false` nên **không còn bắt buộc mật khẩu nữa**.
Không đăng nhập được bằng dòng đó (`_xacThuc` đòi cả salt lẫn hash) nên không phải lỗ bảo mật,
nhưng là rác trên Sheet và làm người dùng tưởng đã tạo xong.

### Đã sửa

| Chỗ | Sửa gì |
|---|---|
| `Code.gs` · `_apiLuuUser` | Đặt mật khẩu **khi nào có gửi lên**, không chỉ lúc tạo mới. Để trống = giữ nguyên, **đúng như nhãn trên modal** |
| `Code.gs` · `_apiLuuUser` | Chuyển phép kiểm mật khẩu **LÊN TRƯỚC** khi ghi Sheet |
| `Code.gs` · log | Ghi rõ `· ĐỔI MẬT KHẨU` để còn truy vết |
| `Code.gs` · `ping` | Trả thêm `ban: BAN_CODE` + `co_ratelimit: true` — **để biết bản đang chạy trên Google có phải bản mới không**. Trước đây sửa xong quên Triển khai là ngồi đoán |
| `server.py` · `perm_save_user` | Đổi mật khẩu xong thì **xoá bản cache offline** của tài khoản đó (`_xoa_cache_uid`) |

⚠️ **Hạn chế còn lại của cache offline:** chỉ xoá được cache **trên máy đang thao tác**. Máy khác
đã từng đăng nhập bằng mật khẩu cũ thì vẫn giữ cache đó tới khi hết 7 ngày ⇒ **mất mạng vẫn vào
được bằng mật khẩu cũ**. Đây là hạn chế của mô hình "credential cached", giống hệt Windows domain.
Ghi ra để khỏi tưởng đã kín.

### Verify — đạt M2

**14/14** bằng shim Node (shim tầng Sheet, dùng `_apiLuuUser` / `_doiMatKhauDong` / `_xacThuc` /
`_apiDangNhap` **nguyên văn** từ Code.gs):
- Tái hiện đúng lỗi: sửa tài khoản + gửi mật khẩu → **PW_HASH đã đổi** (trước khi sửa thì y nguyên)
- Sau khi đổi: **vào được bằng mật khẩu MỚI, mật khẩu CŨ hết tác dụng**
- Để trống ô mật khẩu → PW_HASH giữ nguyên, **tên và đơn vị vẫn được cập nhật**
- Tạo mới không mật khẩu → bị từ chối **và không để lại dòng rác nào**
- Log ghi rõ `ĐỔI MẬT KHẨU`

Chạy lại hai bộ test cũ: rate limit **15/15**, bỏ chế độ file **24/24** — không vỡ gì.

**Build lại EXE v1.11.5 → v1.11.6.**

### ⛔ Việc Đại Ca phải làm

`Code.gs` sửa rồi nhưng **chưa lên Google** — phải Triển khai → Quản lý bản triển khai → bút chì →
Phiên bản **Mới**. Chừng nào chưa làm thì **đổi mật khẩu vẫn không có tác dụng**.
Sau khi deploy, kiểm bằng `ping`: kết quả phải có `"ban":"2026-09-21a"`.

> ✅ **ĐÃ XONG cuối ngày 21/09 — Version 4.** Lưu ý: mã bản cuối cùng là **`2026-09-21b`**
> (không phải `a` như viết lúc này) vì sau đó còn vá thêm lỗ rate limit ở `_apiDatMatKhau`.
> Và Đại Ca ĐÃ gặp đúng cảnh báo này: đổi mật khẩu vẫn không ăn trên EXE v1.11.6 vì chưa Triển khai.

---

## 21/09/2026 (tiếp) — Ô tài khoản ở header + tự đổi mật khẩu (mẫu SYNA AI PORTAL)

### Vì sao Google vẫn chạy bản cũ — và cách phát hiện

Đại Ca báo đổi mật khẩu **vẫn không ăn** trên EXE v1.11.6. Chạy `ping` thì rõ ngay:
kết quả **không có trường `ban`** ⇒ Google vẫn chạy `Code.gs` **bản cũ**.
`_apiLuuUser` chạy **trên Google**, không nằm trong EXE — build lại EXE bao nhiêu lần cũng vô ích
nếu chưa Triển khai.

✅ Trường `ban: BAN_CODE` thêm sáng nay **bắt được đúng việc này ngay lần dùng đầu tiên**.
Trước đây không có cách nào biết, sửa xong quên Triển khai là ngồi đoán.

### Vá thêm một lỗ trước khi mở giao diện đổi mật khẩu cho mọi người

`_apiDatMatKhau` khi mật khẩu cũ sai **chỉ trả lỗi, không đếm lần sai**. Mà `/api/perm/password`
nằm trong `PERM_PUBLIC` (miễn kiểm quyền) ⇒ ai đăng nhập được cũng gửi `user_id` của **người khác**
+ đoán mật khẩu **không giới hạn số lần** — **đường dò mật khẩu VÒNG QUA rate limit**.
Chưa nguy vì chưa giao diện nào gọi tới; mở ra thì thành nguy. Nay chịu chung lưới với `_apiDangNhap`.
⇒ `BAN_CODE` lên **`2026-09-21b`**.

### Ô tài khoản ở header — theo đúng mẫu Portal

Đọc `Zalo CRM ASSISTANT.html` (SYNA AI PORTAL) rồi làm theo:

| Luật của Portal | Áp vào đây |
|---|---|
| Ô tài khoản chỉ gánh **2 việc**: cho biết đang ở tài khoản nào, và đổi mật khẩu | Menu chỉ có **Đổi mật khẩu** |
| **KHÔNG đưa Đăng xuất vào menu** — nút đó đã nằm chỗ khác, bày hai chỗ chỉ tổ rối | Giữ nguyên nút Đăng xuất cạnh bên |
| Tên/email nằm **ngay cạnh** ảnh đại diện | Tên + chức vụ cạnh ô chữ cái đầu |
| Menu thả xuống có dòng đầu nhắc đang ở tài khoản nào | Có, kèm **"Được xem N mục · M đơn vị"** |

⚠️ **Bẫy z-index Portal đã trả giá** (ghi trong chính file đó): menu nằm trong thẻ cha có z-index
thì cha tạo một **tầng riêng**, số z-index của con chỉ tranh nhau trong tầng đó chứ **không vượt ra**
so với khối khác ⇒ dòng dưới của menu bị phủ, **nhìn thấy mà bấm không ăn**. Đặt z-index 5000 cho
riêng menu KHÔNG cứu được, phải nâng chính thanh cha.
➡️ Ở đây tránh hẳn bằng `createPortal` — đúng cách `DocumentTabDropdown` trong chính `index.html`
đã dùng. Header là `z-[1000]`, khối dưới `z-[900]` nên vốn không vướng, nhưng portal thì miễn nhiễm.

### Vì sao việc này cần, không chỉ là cho đẹp

Tab Phân quyền **chỉ ADMIN vào được** ⇒ nhân viên thường **không có bất kỳ cách nào tự đổi mật
khẩu**, phải nhờ Đại Ca đổi hộ từng người và gửi mật khẩu qua Zalo.
Phần khó vốn đã có sẵn: `/api/perm/password` hỗ trợ **chính chủ tự đổi** (kèm `old_password`,
KHÔNG cần tài khoản quản trị) và nằm trong danh sách miễn kiểm quyền. **Chỉ thiếu mỗi giao diện.**

Nhân tiện: `/api/my_perms` vốn đã trả về `name` / `group` / `allowed_orgs` từ lâu, nhưng frontend
chỉ lấy mỗi `items` rồi **vứt phần còn lại**. Nay dùng hết.

### Verify — đạt M2

| Mức | Nội dung |
|---|---|
| M1 | `node check_babel.js` SUCCESSFUL · `ast.parse` OK |
| Apps Script | rate limit **15/15** · đổi mật khẩu **14/14** — chạy lại sau khi vá, không vỡ gì |
| **Giao diện — bấm thật trên trình duyệt** | Cắt nguyên văn 136 dòng component từ `index.html`, stub `fetch`. Menu mở đúng: tên · `KETOAN1 · KT01` · *"Được xem 5 mục · 2 đơn vị"* · dòng **Đổi mật khẩu**. Modal: **5/5 ca** — mật khẩu mới < 6 ký tự bị chặn · hai ô gõ lại không khớp bị chặn · mật khẩu hiện tại sai thì **gọi server rồi báo "Mật khẩu hiện tại không đúng"** · lúc chờ nút đổi thành **"ĐANG ĐỔI..."** · đổi đúng thì hiện hộp xanh *"Đã đổi mật khẩu…"* và các ô nhập biến mất |

**Build EXE v1.11.6 → v1.11.7.**

### ⛔ Vẫn chờ Đại Ca: Triển khai `Code.gs`
> 🕘 *Ảnh chụp lúc đó — nhiều mục dưới đây nay đã xong. Danh sách còn treo THẬT ở [§ VIỆC CẦN LÀM](#-việc-cần-làm--cập-nhật-21092026).*


Chừng nào chưa Triển khai thì **cả đổi mật khẩu lẫn rate limit đều chưa có tác dụng** — dù EXE đã
là v1.11.7. Sau khi Triển khai, `ping` phải trả `"ban":"2026-09-21b"`.

---

## 21/09/2026 (tiếp) — Triển khai Code.gs lên Google, và một cú suýt chết

Đại Ca giao tôi triển khai luôn. Điều khiển **Chrome thật của Đại Ca** (đã đăng nhập Google sẵn) —
tôi không đăng nhập thay, chỉ dùng phiên có sẵn.

### 🔴 Sự cố: dán thẳng Code.gs lên Google = xoá mất TOKEN thật

Tôi dán nguyên `phanquyen_gas/Code.gs` vào editor rồi **Ctrl+S**, quên rằng repo này công khai nên
file trong repo cố ý để `TOKEN` là chuỗi giữ chỗ `DAN_TOKEN_NGAU_NHIEN_VAO_DAY`.
**Token thật trong editor đã bị ghi đè và đã lưu.**

✅ **Không thiệt hại** vì lúc đó chưa bấm Triển khai — bản đang chạy vẫn là Version 3 mang token
thật, app của Đại Ca vẫn sống bình thường suốt lúc tôi sửa.
❌ **Bấm Deploy sớm vài phút là cả công ty mất đăng nhập ngay lập tức.**

**Đã sửa:** nạp lại token thật từ `ketnoi.json`, dán đè lại, lưu, rồi xác minh bằng Ctrl+F tìm
`DAN_TOKEN_NGAU_NHIEN` → **"No results"**, và `BAN_CODE = '2026-09-21b'` → **1 of 1**.

**Không khôi phục được:** hằng `ADMIN_DK_BOOTSTRAP` nay là chuỗi giữ chỗ. Nó chỉ dùng một lần lúc
`khoiTao()` sinh admin đầu tiên; Sheet đã có admin nên vô hại. Cần dựng lại từ đầu thì phải tự điền.

**Để không lặp lại:** thêm `phanquyen_gas/chuan_bi_deploy.py` — đọc Code.gs, thay token thật từ
`ketnoi.json`, đưa vào clipboard, **không ghi ra file nào trong repo**. Và ghi **Bẫy 19** vào CLAUDE.md.

### Triển khai — đạt M3

| Bước | Kết quả |
|---|---|
| Deploy → **Quản lý bản triển khai** (⛔ KHÔNG phải "Triển khai mới") | Active = "Untitled", đang chạy **Version 3 (20/09)** |
| ✏️ → Phiên bản **Mới** + mô tả | **Deployment ID giữ nguyên** `AKfycbx8Zr…G5b7PEiFlk` ⇒ **URL không đổi** |
| Bấm Deploy | *"Deployment successfully updated"* — **Version 4 on Sep 21, 2026, 2:39 PM** |
| `ping` từ máy | `{"ok": true, "ban": "2026-09-21b", "co_ratelimit": true}` |

⇒ Bản mới đang chạy · lưới chống dò đã bật · **token cũ vẫn khớp nên mọi EXE đã phát vẫn nối được**.

Trước khi bấm Deploy tôi dừng lại xin Đại Ca xác nhận, kèm bằng chứng Deployment ID không đổi —
đúng cam kết đầu việc, và càng cần thiết sau cú suýt chết ở trên.

### Giờ Đại Ca thử được rồi

Trên EXE **v1.11.7**: đổi mật khẩu trong tab Phân quyền, hoặc dùng **ô tài khoản ở góc phải header**
→ *Đổi mật khẩu*. Cả hai đường giờ đều ăn thật.

---

## 21/09/2026 (tiếp) — Hai tab đối chiếu mới: điều chuyển nội bộ + danh sách PO

Đại Ca giao thêm danh sách xuất/nhập điều chuyển nội bộ và danh sách PO (yêu cầu thường xuyên) +
phiếu nhập mua hàng, **làm theo đúng nguyên tắc kiểm tra của tab đối chiếu BTP**.

### Khảo sát trước, code sau — và đó là chỗ cứu được cả việc

Không viết dòng code nào cho tới khi đo xong trên DB thật. Hai kết quả ngược hẳn nhau:

| | Điều chuyển nội bộ | PO ↔ phiếu nhập mua |
|---|---|---|
| Khoá nối | `PURCHASE.SALE_PR_KEY = SALE.PR_KEY` — **y hệt BTP** | **không có khoá nào đúng** |
| Độ phủ | 19.838 phiếu `NDCNB` → **19.828 nối được (99,95%)** | **99/4.217 PO = 2,3%**, `TX2` = **0%** |
| Kết luận | làm được ngay | **iPOS không ghi liên kết** |

**Đã thử 7 khoá cho PO, ghi đủ vào [CLAUDE.md](CLAUDE.md) Bẫy 20** để người sau khỏi đo lại.
Ca quyết định: PO `POCH2026/0001/T01` của đơn vị 44 đặt `LY-NH600` 22.000 CÁI, nhưng 12 dòng nhập
ghi tham chiếu **đúng số PO đó** lại toàn mã `KEA-*`. Hai gốc rễ: **số phiếu PO trùng 50 bản ở 50
đơn vị cùng ngày**, và `PURCHASE_DETAIL` — bảng DUY NHẤT có cột `PO_TRAN_NO` — chỉ chứa **3%** số
dòng hàng thật (phiếu `NM`: 11.434 dòng ở `WAREHOUSE` vs **340** ở `PURCHASE_DETAIL`), lại còn tắt
hẳn T02→T06/2026.

⚠️ **Suýt xây báo cáo trên khoá sai.** Khoá `PO_TRAN_NO + ORGANIZATION_ID` cho **669 khớp đúng 1,
0 nổ dòng** — nhìn số là tưởng ngon. Chỉ tới lúc soi một ca cụ thể mới thấy mã hàng hai bên không
liên quan gì. **Bài học: "khoá duy nhất" chưa chắc là "khoá đúng" — phải kiểm nội dung, không chỉ
kiểm độ duy nhất.**

➡️ Báo Đại Ca, Đại Ca chốt: **bỏ hẳn cột "đã có phiếu mua hàng chưa"**, chỉ làm danh sách PO đầy đủ.
Trên màn hình có ghi rõ một dòng vì sao không có cột đó — để người xem khỏi tưởng thiếu sót, và khỏi
ai đó "bổ sung" bằng một liên kết bịa.

### Tab `dcnb_reconcile` — đối chiếu `XDCNB` → `NDCNB`

Cùng khuôn `btp_reconcile`, nhưng **ba chỗ khác phải xử riêng**:

1. **Xuất và nhập ở hai đơn vị khác nhau** (kho tổng `01` xuất → cửa hàng `35`/`71`/`32`… nhận) ⇒
   bảng có **cả hai cột đơn vị**. BTP thì cùng đơn vị.
2. **`NDCNB` có `IS_SALE = 0`** ⇒ dính đúng **Bẫy 15**: nó *không hề* nằm trong `PURCHASE_VIEW`.
   Đọc qua view là ra 0 dòng mà không báo lỗi. Phải đọc thẳng `dbo.PURCHASE`.
3. **So thẳng `QUANTITY` là đúng** — KHÔNG bê mẹo "mốc gần hơn" của BTP sang. Mẹo đó chỉ sinh ra vì
   `JOB_QTY` của BTP ghi bằng 1 trong 2 đơn vị tuỳ người gõ; điều chuyển thì hai phía cùng ĐVT cơ bản.
   Đã đo cả năm 2026: khớp **133.348** · chưa nhận **4.603** · lệch **28**.

Nhánh phiếu nhập mồ côi giữ nguyên logic BTP và **bắt được việc thật**: tháng 5/2026 có 9 phiếu
`NGHI NHẬN TRÙNG — phiếu xuất đã có phiếu nhập khác`.

### Tab `po_list` — danh sách PO (`TX` / `TX1` / `TX2`)

Nguồn `dbo.PO` + `dbo.PO_DETAIL`. 2026: 4.217 phiếu / 3.384 dòng, chạy **~0,2s**.
Trạng thái dịch sang tiếng người (`APPROVED` → *Đã duyệt*…) theo đúng luật "thông báo phải nói
tiếng người". ⚠️ `dbo.PURCHASE_ORDER` **trống 0 dòng** — di sản, đừng đụng.

🔴 **Lỗi tự gây, ghi lại thành Bẫy 21:** viết câu PO phẳng không CTE nên
`ROW_NUMBER() OVER (ORDER BY DON_VI)` tham chiếu bí danh của chính câu `SELECT` ⇒
`Invalid column name 'DON_VI'`. Đáng chú ý: **`/count` vẫn xanh**, chỉ nhánh phân trang mới chết —
nhìn mỗi `/count` là tưởng xong. Đã bọc `WITH POL AS (…)` như BTP/ĐCNB.

### Verify — đạt M2, thêm một lớp M4 cho phần số liệu

| Mức | Nội dung |
|---|---|
| M1 | `ast.parse` OK · `node check_babel.js` SUCCESSFUL · **không có hàm trùng tên** (Bẫy 2) |
| Số cột | header / ô tìm kiếm / ô dữ liệu: **ĐCNB 19-19-19**, **PO 17-17-17** — khớp, cùng kiểu với BTP 21-21-21 |
| **M2** | **13/13 phép thử qua `test_client` in-process** (không qua cổng 5050, Bẫy 6): nạp trang · lọc từng trạng thái · lọc loại PO · tìm theo số phiếu · sắp xếp · phân trang · `/count` · tạo job xuất CSV |
| **Ép quyền** | **8/8 đúng** — không có quyền ⇒ 403; có `btp_reconcile` mà không có `dcnb_reconcile` ⇒ vẫn 403. Ép quyền **đơn vị**: tài khoản chỉ được xem đơn vị `99` ⇒ trả **0 dòng**, không lộ dữ liệu |
| **M4 (phần số)** | Mọi con số trong tài liệu đều đo trên `IACC_CHULONG` thật, không ước lượng |

⚠️ **Chưa đạt M4 đầy đủ**: chưa đối chiếu với form sổ sách/báo cáo gốc của iPOS, vì hai tab này là
**danh sách đối chiếu nội bộ**, không có mẫu gốc để tie.

### Điểm mù — phải biết trước khi dùng

- **Bộ lọc Đơn vị của tab điều chuyển áp cho phía XUẤT**, giống mọi tab khác. Hệ quả: tài khoản chỉ
  được xem đơn vị cửa hàng sẽ **không thấy hàng chuyển đến mình** (vì bên xuất là kho tổng `01`).
  Đại Ca dùng tài khoản toàn quyền nên không vướng — nhưng mở cho cửa hàng thì phải đổi.
- Hiệu năng tab điều chuyển **~6–8,5s/tháng**, ngang BTP. Kỳ dài sẽ chậm hơn.
- `PO.EMPLOYEE_ID` **trống trên dữ liệu thật** ⇒ cột Người lập luôn rỗng. Giữ cột vì iPOS có thể ghi
  về sau, không phải lỗi.
- Tên đơn vị nhận để trống khi một phiếu xuất đi tới nhiều đơn vị (mã vẫn hiện đủ dạng `35 + 71`).

---

## 21/09/2026 (tiếp) — "Lưu phân quyền không ăn": Google nuốt mã mới trong im lặng

Đại Ca thử hai tab mới xong báo 4 việc. Việc thứ 4 mới là gốc, ba việc kia là triệu chứng.

### 🔴 Gốc bệnh — và nó KHÔNG phải nút Lưu hỏng

`phanquyen_gas/Code.gs` **ghi cứng danh sách mã trong hằng `PERM`** (7 tab). Checklist trong app
lại dựng từ `DOC_TABS` **ở máy** — nên 2 tab mới hiện ra tick được. Bấm Lưu thì `_apiLuuChucVu`
lặp `PERM.forEach`, **không thấy 2 mã đó nên bỏ qua**, Sheet cũng không có cột để ghi.
⇒ App báo **lưu thành công**, Sheet không đổi gì.

**Đúng y hình dạng con bug đổi mật khẩu sáng nay** (`_apiLuuUser` chỉ ghi mật khẩu khi
`moi === true`). Hai lần trong một ngày, cùng một kiểu: **Google nhận rồi vứt, app báo OK.**
➡️ Ghi thành **Bẫy 22** trong CLAUDE.md.

### Đã sửa — ba tầng, thiếu tầng nào là bệnh quay lại

| Tầng | Sửa gì | Ở đâu |
|---|---|---|
| 1 | Google đọc mã quyền từ **hàng tiêu đề của Sheet**, không đọc hằng `PERM` | `_maQuyenTrenSheet()` — vá cả `_quyenChucVu`, `_apiNap`, `_apiLuuChucVu` |
| 2 | App gửi `tat_ca_muc` + `nhan_muc`; Google **tự tạo cột** cho mã lạ | `server.py` `/api/perm/role` + `_apiLuuChucVu` |
| 3 | Chức vụ **ADMIN tính đủ 100% mục ở phía app** | `_current_perms()` |

⇒ **Từ nay thêm tab mới vào app không phải sửa `Code.gs` rồi Triển khai lại nữa** — đúng cái
Đại Ca chốt.

⚠️ Tầng 3 dễ hiểu nhầm là quay lại lỗi cũ "phiên hỏng thì toàn quyền" (bản trước 21/09). Khác ở
chỗ: chỉ nhận đúng chuỗi `'ADMIN'` **do Google Sheet cấp**; chưa đăng nhập / phiên hỏng thì
`_current_group()` trả `''` ⇒ vẫn tập RỖNG. **Đã test riêng 6 ca cho đúng ranh giới này.**

### Ba việc còn lại Đại Ca nêu

- **Nút "Tải lại"** ở header — app chạy Chrome `--app` nên không có thanh địa chỉ, không có F5.
  Nút này nạp lại quyền + danh mục + dữ liệu tab đang mở, **không mất phiên đăng nhập**.
  ⚠️ Giới hạn: quyền của NGƯỜI KHÁC vẫn chốt lúc họ đăng nhập (cố ý — gọi Google ở mọi request
  thì mỗi cú bấm chờ 1–3 giây). Sửa quyền cho ai thì người đó vẫn phải đăng nhập lại.
- **Trạng thái chờ cho nút Lưu** — mỗi lệnh ghi đi vòng qua Google mất **4–7 giây**; nút đứng yên
  nên tưởng hỏng rồi bấm lại ⇒ ghi hai lần. Nay hiện *"Đang lưu lên Google..."* + vòng xoay, và
  **khoá không cho bấm lần hai**. Áp cho cả Xoá tài khoản / Xoá chức vụ.
- **Lưới an toàn `kiemMucBiVutBo`** — sau khi lưu, app đọc lại từ Google và đối chiếu. Mã nào bị
  vứt thì **giữ hộp thoại lại kèm cảnh báo nói rõ mã nào**, không đóng im lặng.
  Đây là thứ lẽ ra phải có từ đầu: cả hai con bug hôm nay đều sống được vì app tin lời Google.

### Verify

| Mức | Kết quả |
|---|---|
| M1 | `ast.parse` OK · `check_babel` SUCCESSFUL · `node --check` cho `Code.gs` OK |
| **Logic Apps Script** | **18/18 ca** bằng **sheet giả** dựng trong Node (stub `SpreadsheetApp`): tạo cột mới · ghi tick · **bỏ tick phải xoá thật** · không đụng chức vụ khác · **chặn mã bậy không làm bẩn tiêu đề** · `_apiNap` đọc đúng · **tương thích ngược khi app cũ không gửi `tat_ca_muc`** |
| **Ranh giới ADMIN** | **6/6 ca**: ADMIN dù Sheet cấp 0 mục vẫn đủ 26/26 · nhóm thường đúng số mục · **phiên hỏng ⇒ 0 mục, 403** · **`admin` chữ thường ⇒ KHÔNG được toàn quyền** |
| M3 | build EXE v1.11.9 |

### ✅ Đã Triển khai — 21/09/2026 19:33, **Version 5**

| Bước | Kết quả |
|---|---|
| Deploy → **Quản lý bản triển khai** (⛔ không phải "Triển khai mới") | Active đang chạy Version 4 |
| ✏️ → Phiên bản **Mới** + mô tả | **Deployment ID giữ nguyên** ⇒ **URL không đổi** |
| Bấm Deploy | *"Deployment successfully updated"* — **Version 5 on Sep 21, 2026, 7:33 PM** |
| `ping` từ máy | `{"ok": true, "ban": "2026-09-21c", "co_ratelimit": true}` |

⇒ Bản mới đang chạy · token vẫn khớp nên **mọi EXE đã phát vẫn nối được** · lưới chống dò còn nguyên.

### 🔴 Suýt hỏng lần hai — clipboard làm nát tiếng Việt (Bẫy 23)

Dán bản đầu lên Apps Script thì **toàn bộ chữ tiếng Việt thành rác** (`Chá»n gá»­i…`).
Nguyên nhân: `chuan_bi_deploy.py` bơm UTF-8 vào stdin PowerShell, mà `[Console]::In` giải mã theo
**bảng mã ANSI của console** (cp1252). Không chỉ hỏng chú thích — **mọi chuỗi thông báo lỗi hiện
cho người dùng cũng hỏng**.

✅ **Bắt được chỉ vì nhìn màn hình trước khi Ctrl+S.** Ctrl+Z hai lần, nội dung gốc trở lại nguyên
vẹn, không mất gì. Lưu rồi Triển khai là cả công ty nhận thông báo lỗi rác.

➡️ Sửa **hai lớp** trong `chuan_bi_deploy.py`: đặt `[Console]::InputEncoding = UTF8` trước khi đọc
stdin, **và đọc ngược clipboard ra đối chiếu từng ký tự** — lệch là dừng, không cho dán.
Cùng tinh thần `Sync-And-Backup.ps1`: không tin lệnh copy, phải đối chiếu.

⚠️ Đây là **lần thứ hai trong ngày** cùng một họ lỗi với Bẫy 12 (PowerShell + tiếng Việt + bảng mã).

### Kiểm trước khi bấm Deploy — 4 điều kiện, đủ cả 4 mới bấm

| Kiểm | Kết quả |
|---|---|
| Ctrl+F `DAN_TOKEN_NGAU_NHIEN` | **No results** ⇒ token thật đã vào |
| Ctrl+F `2026-09-21c` | **1 of 1** ⇒ đúng bản cần triển khai |
| Ctrl+F `_maQuyenTrenSheet` | **1 of 5** ⇒ code mới có thật trong bản dán |
| Deployment ID vs URL trong `ketnoi.json` | **khớp** ⇒ URL sẽ không đổi |

### ✅ Chạy thật trên Google — 8/8, con bug đã chết

Đại Ca cấp mật khẩu quản trị để chạy nốt phép thử cuối (dùng đúng một lần, **không ghi vào file
nào**; Đại Ca đổi mật khẩu sau).

Cách thử **an toàn**: tạo một chức vụ thử `ZZTEST` rồi xoá — **không đụng chức vụ thật nào**.

| Bước | Kết quả |
|---|---|
| Đọc Sheet thật | 2 tài khoản · 9 chức vụ · **chưa chức vụ nào có 2 tab mới** (đúng, cột chưa tồn tại) |
| Lưu `ZZTEST` với `ledger` + 2 tab mới | Google báo **`cot_moi: ['dcnb_reconcile','po_list']`** — tự tạo cột thật trên Sheet · `da_ghi` đủ 3 mã |
| **Đọc ngược từ Sheet** | trả về **`['ledger','dcnb_reconcile','po_list']`** — **đủ 3, không mất mã nào** |
| Xoá `ZZTEST` | xoá sạch, về lại đúng 9 chức vụ |

⇒ **Đây mới là bằng chứng.** Trước đây app cũng báo "lưu thành công" — khác nhau ở chỗ giờ **đọc
ngược ra vẫn còn**. Hai cột `dcnb_reconcile` / `po_list` nay **nằm vĩnh viễn trên Sheet**, Đại Ca
tick cho chức vụ thật là ăn.

⏱️ Ghi nhận hiệu năng: đọc danh sách **10–14 giây**, lưu **6,6s**, xoá **8,3s**. Chậm vì mỗi lệnh
đi vòng qua Apps Script — đúng lý do phải có trạng thái chờ cho nút Lưu.

---

## 21/09/2026 (tiếp) — Hai tab đối chiếu: thêm trạng thái "chưa ghi sổ", và phát hiện tab đang đổ oan cho cửa hàng

Đại Ca giao: *"lấy trạng thái như Phiếu xuất kho chưa duyệt — các phiếu có status không phải
trạng thái đã ghi sổ"*, kèm bổ sung điều kiện kho xuất / kho nhập / thời gian xuất / SL + ĐVT.

### Khảo sát trước, code sau — 8 vòng đo, và vòng nào cũng đổi phương án

Không viết dòng code nào cho tới khi đo xong trên DB thật. Kết quả lật ngược cả hai phía:

| Đo được | Hệ quả |
|---|---|
| `STATUS` chỉ có 2 giá trị: `POSTED` / `DRAFT`. `REVIEW_STATUS` là thứ khác (29/19.887) | Đúng hướng Đại Ca chỉ |
| Phiếu `DRAFT` **không sinh dòng nào trong `WAREHOUSE`** (13 phiếu `XDCNB` → 0 dòng) | Tab **chưa từng nhìn thấy** phiếu nháp ⇒ thêm nhóm này là **thêm mới**, không bóc ra từ 219 |
| **211/218 phiếu "Chưa nhận hàng" T09 thực ra bên nhận ĐÃ lập phiếu, chỉ chưa ghi sổ** | 🔴 Phát hiện lớn hơn hẳn việc được giao |
| `SALE.WAREHOUSE_ID_RECEIVE` ghi đủ 19.887/19.887, khớp kho nhận thật 19.225/19.226 | Điền được **Kho nhập cho mọi dòng**, kể cả dòng đang hiện "—" |
| 4 cột ngày trên `SALE`/`PURCHASE`/`WAREHOUSE`: **0 dòng nào có giờ ≠ 00:00** | ❌ Không có "thời gian xuất kho". Đại Ca chốt bỏ cột giờ |

🔴 **Tab đang đổ oan cho cửa hàng.** Nhóm "Chưa nhận hàng" T09 có 218 phiếu thì **211 (96,8%)**
bên nhận đã lập phiếu nhập rồi, chỉ chưa bấm ghi sổ; cả năm 2026 là **605/631 (95,9%)**. Chỉ **7
phiếu** T09 là thật sự chưa ai lập phiếu. Báo Đại Ca, Đại Ca chốt **tách hẳn thành nhóm riêng**.

### 🔴 Lỗi của chính tôi — và Đại Ca bắt được

Tôi đo `SALE_DETAIL` bằng cách nối `SD.PR_KEY = S.PR_KEY`, ra **0 dòng cho CẢ phiếu đã ghi sổ**,
rồi kết luận *"phiếu nháp không có dòng hàng ở bất kỳ đâu"* và báo Đại Ca rằng cột mã hàng / SL /
ĐVT sẽ phải để trống. Đại Ca bác: *"thực tế nó có bảng đó… trong màn hình XDCNB có nút mở để hiển
thị toàn bộ chứng từ, xem có kiểm tra được bảng nào liên quan không"*.

Đúng. Trên mọi bảng `*_DETAIL` của iPOS thì **`PR_KEY` là khoá của chính dòng đó, `FR_KEY` mới
trỏ về phiếu cha** — điều mà [Bẫy 20](CLAUDE.md) đã ghi sẵn từ hôm trước (`PO_DETAIL.FR_KEY →
PURCHASE.PR_KEY`) mà tôi không đối chiếu. Nối lại bằng `FR_KEY`: **độ phủ 100%**, phiếu nháp có
đủ mã hàng, SL, ĐVT, kho.

**Bài học ghi vào Bẫy 24:** con số **0 ở chỗ chắc chắn phải có dữ liệu** (nhóm *đã ghi sổ*) là dấu
hiệu câu SQL sai, không phải dấu hiệu dữ liệu không tồn tại. Tôi đã đọc con số đó mà không dừng lại.

### Bẫy thứ hai suýt vấp: lấy nhầm cột số lượng

So `SALE_DETAIL` với `WAREHOUSE` trên phiếu đã ghi sổ: `QUANTITY` chỉ khớp **28%**,
`QUANTITY_EXTRA` **26%**, **`QUANTITY_WH` khớp 100%** (12.706/12.706). `QUANTITY` ghi theo ĐVT
nhập liệu, kho theo ĐVT cơ bản — `KEPC-PMR` ghi `10 BỊCH` còn kho là `7.000 G`, **sai gấp 700 lần**.
Cùng họ với bẫy `JOB_QTY` của tab BTP. 39 cặp lệch còn lại đều là **dòng SL = 0**, lọc đi là khít.

### Đã làm

**Tab điều chuyển nội bộ** — 2 trạng thái mới (`Phiếu nhập chưa ghi sổ`, `Phiếu xuất chưa ghi sổ`),
Kho nhập điền theo 3 mức ưu tiên nên **không còn để trống**, thêm cột Tên kho nhập vào file xuất,
thêm dropdown **Kho nhập** và ô tìm cho Kho nhập / ĐVT / SL xuất. Cột **Ghi chú** nói thẳng
*"Bên nhận ĐÃ lập phiếu nhập NNB0001/T09 nhưng chưa bấm ghi sổ"* — đọc là biết phải bảo ai làm gì.

**Tab BTP** — cùng khuôn. ⚠️ Nhưng `XKHOSXBTP`/`NSP` **chưa từng có một phiếu nháp nào trong cả
lịch sử DB** (100% `POSTED`) nên hai nhóm này **hiện luôn bằng 0**; giữ để mai kia quy trình đổi
thì bắt được ngay.

**Bỏ cột giờ xuất kho** — iPOS không ghi. Giờ thật chỉ có trong `dbo.LOGGING` nhưng
`LOGGING.PR_KEY` không phải khoá phiếu (0 dòng trùng với `SALE`), phải dò chuỗi tự do, quét 1
tháng mất **8,95s**, và LOGGING chỉ còn từ **17/05/2026**. Ghi vào Bẫy 24 để người sau khỏi đo lại.

### Verify — M2, có thêm một lớp đối chứng trước/sau

| Mức | Nội dung |
|---|---|
| M1 | `ast.parse` OK · `node check_babel.js` SUCCESSFUL · **không có hàm trùng tên** (Bẫy 2) · số cột **ĐCNB 19-19-19**, **BTP 21-21-21** |
| **M2** | **ĐCNB 35/35** và **BTP 14/14** qua `test_client` in-process (Bẫy 6): dựng CTE · **số dấu `?` khớp số params** (Bẫy 5) · lọc từng trạng thái · 3 bộ lọc mới · sắp xếp · phân trang · `/count` · job xuất CSV chạy tới file thật |
| **Đối chứng trước/sau** | Chạy **bản git HEAD** và bản mới cạnh nhau trên cùng kỳ T09/2026. **Tab BTP: mọi con số y hệt.** Tab ĐCNB: `Đã nhận đủ` 1.502 và `Lệch` 3 **không đổi**, tiền 83.387 **không đổi**, và **7 + 211 = 218** đúng bằng nhóm "Chưa nhận hàng" cũ — không mất phiếu nào, chỉ tách ra |
| **Kiểm nhánh chưa có dữ liệu** | Nhánh nháp của BTP không có phiếu thật để thử ⇒ chạy đúng công thức đó lên phiếu **đã ghi sổ**: `SALE_DETAIL` khớp `WAREHOUSE` **10.094/10.094** (cả SL lẫn `JOB_QTY`), `PURCHASE_DETAIL` **4.149/4.149**, lệch 0 |
| Hiệu năng | ĐCNB **5,6s** · BTP **6,5s** cho kỳ 1 tháng — không xấu đi (nhánh nháp đo riêng: 0,42s và 0,18s) |

⚠️ **Chưa đạt M3** — **chưa build lại EXE** vì Đại Ca đang dùng app trên cổng 5050, và luật cấm
tắt/build lại khi Đại Ca đang dùng (đã gây "Failed to fetch" thật ngày 12/08/2026).

### Điểm mù — phải biết trước khi dùng

- **Nhóm "Chưa nhận hàng" tụt từ 218 xuống 7.** Ai đang theo dõi con số cũ sẽ thấy hụt — tổng
  không mất, chỉ chuyển sang nhóm "Phiếu nhập chưa ghi sổ".
- Bộ lọc **Kho nhập** dùng `IN`, an toàn vì đo được **0/133.607 nhóm** đi tới nhiều kho. Nếu về sau
  có phiếu đi nhiều kho thì `KHO_NHAP` thành chuỗi gộp `"A + B"` và lọc sẽ trượt dòng đó.
- Ô tìm **SL xuất** là so khớp đầu chuỗi trên số (gõ `1000` ra mọi dòng bắt đầu bằng 1000) — thô.
  Cần lọc khoảng từ–đến thì phải làm riêng.
- `SALE.WAREHOUSE_ID_RECEIVE` có **1 ca lệch** với kho nhận thật trong cả năm 2026. Dòng đã nhận
  vẫn lấy kho thật nên ca đó không bị ảnh hưởng; chỉ dòng **chưa** nhận mới dùng kho dự kiến.
- **Bộ lọc Đơn vị vẫn áp cho phía XUẤT** — việc còn treo số 7 ở mục VIỆC CẦN LÀM, chưa động tới.

---

## 21/09/2026 (cuối ngày) — Phát hành **v1.11.9**, và cái bẫy số hiệu trùng nhau

### Đã phát hành thật

Đại Ca chốt *"phát hành luôn"* sau khi được báo rõ rủi ro tài khoản Google Sheet.

| Bước | Kết quả |
|---|---|
| Đẩy nhánh `phanquyen` | `origin/phanquyen` = `aea3bb9`, 8 commit. **Actions KHÔNG chạy** — workflow chỉ kích hoạt trên `main` + tag `v*` |
| Gộp `main` | **fast-forward sạch** (`4cc22af..aea3bb9`), không xung đột |
| Actions | `success` trong **1m18s** |
| Release | **v1.11.9** — `iPOS_Accounting_Report.exe` 13.100.698 B + bản `.zip` 12.898.119 B |

Trước khi bấm đã kiểm đủ 3 điều kiện an toàn: remote đúng **GitHub** (không phải GitLab),
tag `v1.11.9` **chưa tồn tại** (nên là Release mới thật, không đè bản cũ), và quét secret trên
bản đã stage — **sạch**.

### 🔴 Bẫy tự gây: hai file khác nhau mang CÙNG số hiệu `1.11.9`

Phát hành xong mới lòi ra: **máy Đại Ca sẽ không bao giờ nhận được bản mới.**

| | Số hiệu | Kích thước | SHA256 |
|---|---|---|---|
| EXE trên máy Đại Ca (build local 16:16) | **1.11.9** | 14.712.220 B | `21ef4e6f…` |
| EXE trên GitHub Release (CI build 22:26) | **1.11.9** | 13.100.698 B | `b3ad2a60…` |

App so phiên bản bằng **`has_update = latest > current`** (`server.py`, hàm `check_github_update`)
— **lớn hơn hẳn** mới báo. `1.11.9` không lớn hơn `1.11.9` ⇒ app im lặng, Đại Ca chạy mãi bản cũ
thiếu 2 trạng thái mới, mà **không có dấu hiệu gì báo là đang chạy bản cũ**.

**Gốc rễ:** `version.txt` chỉ được tăng khi chạy `build_exe.py` ở máy. Phiên này sửa code nhưng
**không build local** (Đại Ca đang dùng app, luật cấm build đè) ⇒ số hiệu đứng yên trong khi nội
dung đã đổi. Máy nhân viên không dính vì họ ở **v1.10.7**, thấp hơn thật nên vẫn được báo.

➡️ **Luật rút ra — ghi để lần sau khỏi vấp:** *sửa code mà không build local thì phải TĂNG
`version.txt` bằng tay trước khi gộp `main`.* Không thì mọi máy đang ở đúng số hiệu đó sẽ kẹt lại
bản cũ vĩnh viễn. Triệu chứng rất khó thấy: app chạy bình thường, chỉ là thiếu tính năng.

---

## 24/09/2026 — Đưa máy Đại Ca về đúng bản đã phát hành, đạt **M3**

Đại Ca chọn phương án **lấy đúng file đã phát hành về** (thay vì tăng số rồi build lại) — chạy
cùng một binary với nhân viên, không sinh thêm số hiệu lạ.

| Bước | Kết quả |
|---|---|
| Sao lưu bản cũ | `dist\iPOS_Accounting_Report_v1.11.9_build_local_2109.exe.bak` |
| Tải bản phát hành | `gh release download v1.11.9` |
| **Đối chiếu SHA256** | `b3ad2a60…` — **khớp từng ký tự** với digest GitHub công bố ⇒ đúng file nhân viên nhận |
| Chạy thử | cổng 5050 LISTENING, **48 MB RAM** (không phải ~10 MB của bootloader bị chặn ở [Bẫy 13](CLAUDE.md)) |
| **Kiểm nội dung EXE** | **11/11 xanh** — đủ 2 trạng thái mới, mã lọc `nhap_chua_gs`/`xuat_chua_gs`, dropdown Kho nhập, `wh_nhap_ids`, ô tìm `s_dvt`/`s_sl_xuat`, cột `TEN_KHO_NHAP`, và **câu giải thích cũ đã bị thay** |
| gzip | 730.575 ký tự → **109.916 byte** trên đường truyền |
| `check_update` | đang chạy `1.11.9` · mới nhất `v1.11.9` · **`has_update: False`** — đúng như phân tích ở trên |

⇒ **Đạt M3**: chạy đúng EXE đã phát hành, gọi API thật, nội dung đúng.

⚠️ **Mẹo vận hành:** mở EXE bằng `Start-Process` trong một lệnh PowerShell thì **app tự tắt ngay
khi lệnh kết thúc** (tiến trình con bị kết thúc theo). Cổng 5050 lên rồi tắt trong vòng một phút,
nhìn tưởng app crash. Phải chạy ở **chế độ nền tách hẳn** thì mới sống qua nhiều lượt.

### Còn thiếu để đạt M4

Chưa đăng nhập được vào app đang chạy — mật khẩu SQL và mật khẩu tài khoản ứng dụng đều do Đại Ca
giữ (`config.json` đã xoá ngay sau khi đo xong 21/09). Đại Ca đăng nhập rồi vào
**Danh sách → Đối chiếu điều chuyển nội bộ**, kỳ **2026 – Tháng 9**, đối chiếu hàng chip với số đã đo:

**Chưa nhận hàng 7** · **Phiếu nhập chưa ghi sổ 211** · **Phiếu xuất chưa ghi sổ 13** ·
Lệch số lượng 3 · Đã nhận đủ 1.502.

(Con số cũ 219 tách thành 7 + 211 = 218; chênh 1 phiếu là do bộ lọc đơn vị loại đơn vị ngoài
cây `'00'` — phép đo bằng SQL thô không có bộ lọc đó.)

---

## 24/09/2026 (chiều) — Luật nghiệp vụ gốc lộ ra, tab đối chiếu điều chuyển đổi hẳn cách đọc · **v1.12.0**

Việc nhận ban đầu chỉ là đóng nốt **M4** cho tab điều chuyển (Đại Ca đã đăng nhập). Đóng xong,
nhưng thứ đáng giá lại nằm ở một câu Đại Ca nói giữa chừng.

### 🔑 Câu nói đổi hết mọi thứ

> *"Khi phiếu xuất điều chuyển ghi sổ, thì phiếu nhập điều chuyển **tự động sinh ra** và ở trạng
> thái chưa ghi sổ, người dùng cần phải kiểm tra để duyệt ghi sổ để nhập vào kho."*

Trước đó tab ghi trong cột Ghi chú: *"**Bên nhận ĐÃ lập phiếu nhập** NNB.../T09 nhưng chưa bấm ghi
sổ"*. **Sai người** — bên nhận không lập gì cả, máy tự sinh. Cùng một con số, hai cách đọc ngược nhau.

Đo lại trên DB thật để xác nhận, không tin mỗi lời kể. **Đúng: 1.906/1.915 phiếu xuất đã ghi sổ
T09/2026 có phiếu nhập trỏ về — 99,53%.**

### Giả thuyết của tôi sai — và nói thẳng ra là sai

Tôi nghi phiếu tự sinh mà chưa ai mở thì `QUANTITY_WH = 0`, bị điều kiện lọc của app vứt mất, nên
rơi nhầm xuống nhóm "Chưa nhận hàng". Đo: **187/187 phiếu `DRAFT` đều có dòng hàng với
`QUANTITY_WH > 0`.** App thấy hết, không sót phiếu nào. Điều kiện lọc không có lỗi.

Bác xong giả thuyết thì nhóm 11 phiếu kia mới lộ ra là **bất thường thật**, chứ không phải lỗi app.

### Tách được hai loại trong cùng một nhóm

Màn hình hiện **11 phiếu** mà SQL đếm **9**. Nguyên nhân: app ghép cặp theo **phiếu × mã hàng**,
nên một phiếu có mã đã nhận và mã chưa nhận sẽ nằm ở cả hai nhóm. Tách ra:

| Loại | Phiếu | Dòng | Bản chất |
|---|---|---|---|
| Không có phiếu nhập nào | **8** | 12 | Phiếu tự sinh bị xoá, hoặc chưa từng sinh |
| **Có phiếu nhập, ĐÃ ghi sổ, nhưng thiếu đúng một mã hàng** | **3** | 3 | 🔴 Nguy hiểm hơn — bên nhận nhìn thấy phiếu "đã xong" |

**Ca soi tận nơi:** `XNB00373/T09` ngày 08/09, Kho Tổng xuất **13 mã** cho ĐV `04`. Phiếu nhập
`NNB0009/T09` **đã ghi sổ**, có **12 mã, khớp từng mã từng số một**. Riêng **`COC` (Trái cóc)
2.000 G không có trên phiếu nhập** — hàng rời Kho Tổng, không vào kho nào, không ai biết.
Hai ca còn lại y hệt: `XNB00941/T09` thiếu Nước Cốt Dừa 9.600 G · `XNB01050/T09` thiếu Chanh tươi 500 G.

### Đã sửa

| # | Việc | Chỗ |
|---|---|---|
| 1 | Câu Ghi chú: bỏ *"Bên nhận ĐÃ lập phiếu nhập… nhưng chưa bấm ghi sổ"* → **"Phiếu nhập NNB0009/T09 chưa duyệt ghi sổ"** | `server.py` `GHI_CHU` |
| 2 | Chú thích chip: *"bên nhận đã lập phiếu rồi"* → **"phiếu nhập đã tự sinh, chưa duyệt ghi sổ"** | `index.html` |
| 3 | **Đổi tên nhóm** `Chưa nhận hàng` → **`Không tìm thấy phiếu nhập`** (Đại Ca chốt) — 4 chỗ: hằng, nhãn chip, chú thích, **điều kiện tô màu dòng** | cả hai file |
| 4 | **Ghi chú mới cho loại "thiếu mã hàng"**: *"Phiếu nhập NNB0009/T09 CÓ nhưng thiếu mã hàng này"* — CTE `NP` dùng lại CTE `P`, **không quét thêm bảng** | `server.py` |

⚠️ Mã lọc trên URL **giữ nguyên** (`chua`) — đổi mã là gãy link cũ và gãy cả bộ lọc đang lưu.
Chỉ đổi chuỗi hiển thị. Nhớ sửa **cả điều kiện tô màu** `row.TRANG_THAI === …`, quên là dòng đỏ mất màu.

### Verify

| Mức | Nội dung |
|---|---|
| M1 | `ast.parse` OK · `node check_babel.js` SUCCESSFUL · không có hàm trùng tên · **0 chỗ còn sót chữ cũ** trong cả 2 file |
| M2 | `test_client` in-process (Bẫy 6): phân bố T09 đúng · `status=chua` trỏ đúng nhóm đã đổi tên · **3 dòng có ghi chú mới / 12 dòng không** đúng như đo bằng SQL thô · ghi chú cũ còn nguyên · **xuất CSV chạy tới file thật**, job `done` 15/15, mở file đọc lại đủ 15 dòng |
| **M3** | Build **v1.12.0** (14.715.374 B), EXE mới hơn cả `server.py` lẫn `index.html` (Bẫy 10), chạy **tách hẳn** bằng `Win32_Process.Create`, cổng 5050 LISTENING, 41 MB (không phải ~10 MB của Bẫy 13), lấy `index.html` từ chính server đang chạy: **10/10 xanh**, `check_update` trả `current_version 1.12.0` · `is_frozen true` |
| **M4** | **11 phiếu / 15 dòng** — khớp **ba chiều**: màn hình EXE Đại Ca chụp · SQL thô chạy độc lập · code in-process. Thêm `Phiếu nhập chưa ghi sổ` = **187** khớp đúng số phiếu `NDCNB STATUS='DRAFT'`, `Phiếu xuất chưa ghi sổ` = **12** khớp `XDCNB DRAFT` |

⚠️ Giữa hai lần đo, số dịch 2 phiếu (Đã nhận đủ 1.719→1.721, chưa ghi sổ 187→185) — **người dùng
thật vừa bấm duyệt trên hệ thống**, không phải tôi làm lệch. Tổng dòng đứng yên 14.110.

### Hai việc phát hiện thêm — CHƯA sửa, Đại Ca chưa chốt

1. 🐛 **Hàng chip tụt về 0 khi bấm chọn một chip.** `_dcnb_summary()` dùng chung `where_sql` vốn đã
   có `TRANG_THAI = ?`, nên chọn một trạng thái là mọi chip khác về 0 — "Đã nhận đủ · 0" trông như
   cả tháng không ai nhận hàng. **Tab BTP dính y hệt.** Tạm thời: bấm chip **TẤT CẢ** mới ra phân bố thật.
2. 🐛 **Phiếu `POSTED` mà không có dòng nào trong `WAREHOUSE` thì tab giấu hẳn.** `XNB00001/T09`
   ngày 03/09 đơn vị `10`: `STATUS = POSTED`, có 1 dòng `SALE_DETAIL`, **0 dòng kho**. Nhánh `X` đọc
   `WAREHOUSE` nên phiếu này không hiện ở bất kỳ nhóm nào. Đây là lý do SQL đếm 9 mà tab ra 8.
   Chưa đo cả năm.

### Điểm mù

- Hai chip nay tên gần giống nhau: **KHÔNG THẤY PHIẾU NHẬP** và **KHÔNG THẤY PHIẾU XUẤT**, chỉ khác
  một chữ và nằm cách xa nhau trên hàng chip. Đã đề xuất đưa cạnh nhau, Đại Ca chưa chốt.
- **Cộng các chip lại KHÔNG ra tổng số phiếu** — ghép cặp theo phiếu × mã hàng nên một phiếu đếm ở
  nhiều nhóm.
- Nhóm `Không tìm thấy phiếu nhập` giờ đúng ở **mức dòng** (mã hàng này không có phiếu nhập), nhưng
  ở **mức phiếu** thì 3 ca loại 2 vẫn có phiếu nhập — chính vì thế mới phải thêm cột Ghi chú.

### ✅ Đã phát hành — v1.12.0

| Bước | Kết quả |
|---|---|
| Push | `aea3bb9..1e5dee9` — **2 commit** (của phiên này + `ec4cce8` phiên trước vốn chưa push) |
| Actions | run `35957485959` · **`success`** |
| Release | **v1.12.0** · là `Latest` · `.exe` + `.zip`. ⚠️ **Không ghi cứng digest ở đây** — xem mục dưới |

Trước khi bấm đã kiểm đủ 4 điều kiện: remote đúng **GitHub**, tag `v1.12.0` **chưa tồn tại**
(nên là Release mới thật), quét secret trên diff **sạch**, `config.json` **không nằm trong git**.

### ⚠️ Lại hai file cùng số hiệu — nhưng lần này VÔ HẠI, đừng nhầm với vụ 21/09

| | Kích thước | SHA256 |
|---|---|---|
| EXE build local lúc 11:43 | 14.715.374 B | `aa85a24a…` |
| EXE trên Release (CI build) | ~13,1 MB | đổi mỗi lần build — xem mục dưới |

Khác byte, **cùng số hiệu `1.12.0`** — y hệt hình dạng cái bẫy ngày 21/09. **Nhưng khác bản chất:**
lần đó bản local build từ mã **CŨ** (thiếu 2 trạng thái mới) nên Đại Ca kẹt lại bản thiếu tính năng.
Lần này **cả hai build từ ĐÚNG một commit `1e5dee9`** — `server.py` sửa lần cuối 11:41:15,
`index.html` 11:36:45, build lúc 11:43:16, sau đó chỉ đụng file `.md`
(**không** nằm trong `--add-data`). ⇒ **Nội dung giống hệt nhau, không thiếu gì.**

Hệ quả thật sự: máy Đại Ca **sẽ không hiện nút cập nhật** cho `v1.12.0` (`1.12.0 > 1.12.0` là sai)
— **không cần**, vì đang chạy đúng nội dung. Bản `v1.12.1` trở đi sẽ báo bình thường.
Chỉ khi muốn **SHA256 khớp digest GitHub** thì mới phải tải bản CI về thay.

➡️ **Cách phân biệt cho người sau:** thấy hai file cùng số hiệu thì đừng vội kết luận. Hỏi đúng một
câu: *bản local có build SAU commit cuối cùng đụng vào `server.py` / `index.html` không?* Có thì
vô hại, không thì đúng là bẫy 21/09.

### ✅ Đã đổi EXE trên máy sang đúng file CI phát hành

Đại Ca chốt lấy bản CI về cho khớp SHA256, chạy cùng một binary với nhân viên.

| Bước | Kết quả |
|---|---|
| Sao lưu bản local | `dist\iPOS_Accounting_Report_v1.12.0_build_local.exe.bak` |
| Tải asset từ Release | `gh release download v1.12.0` |
| **Đối chiếu SHA256** | **khớp từng ký tự** với digest GitHub công bố |
| Thay vào `dist\` + chạy lại | cổng 5050 LISTENING, **48,5 MB** (không phải ~10 MB của [Bẫy 13](CLAUDE.md)) |
| Kiểm nội dung EXE | **5/5** — tên nhóm mới, điều kiện tô màu, 2 chú thích mới, **0 chỗ còn tên nhóm cũ** |
| `check_update` | `current 1.12.0` · `latest v1.12.0` · `has_update False` · `is_frozen True` |

### ⚠️ Vòng lặp tự gây: ghi digest vào tài liệu rồi push tài liệu là digest hết đúng

Commit `1e5dee9` phát hành ra asset `c723e541…` (13.101.382 B). Push tiếp commit **docs**
`8183dd9` — chỉ sửa 2 file `.md` — Actions **build lại toàn bộ** và **thay asset** thành
`686fe061…` (13.101.994 B). Nghĩa là **chính commit ghi lại digest đã làm digest đó sai.**

Gốc rễ là việc treo số 11: workflow **chưa có `paths-ignore`** nên push file `.md` cũng kích hoạt
build EXE đầy đủ. Mỗi lần build ra một binary khác SHA (PyInstaller không tái lập bit-for-bit).

➡️ **Luật rút ra:** **đừng ghi cứng digest / kích thước asset vào tài liệu.** Cần kiểm thì lấy
digest **hiện tại** ngay lúc kiểm:
```bash
gh release view v1.12.0 --json assets --jq '.assets[] | select(.name|endswith(".exe")) | .digest'
```
Cho tới khi thêm được `paths-ignore`, con số ghi trong tài liệu chỉ đúng cho tới lần push kế tiếp.

---

## 24/09/2026 (cuối ngày) — Sửa lỗi hàng chip tụt về 0 · **v1.12.1**

Đại Ca chốt: *"sửa lỗi chip tụt về 0 luôn đi"*.

### Lúc sửa mới thấy: ba tab dính, không phải hai

Tôi báo ban đầu là 2 tab (`dcnb_reconcile`, `btp_reconcile`). Đọc code để sửa thì thấy **`po_list`
cũng dính** — bộ lọc trạng thái nằm ngay trong CTE `POL`, mà `_polist_summary()` cũng chạy trên
chính CTE đó. Cùng một con bug thì sửa một lượt, để sót một tab là nửa vời.

### Gốc bệnh

Phần tóm tắt (hàng chip) và phần dữ liệu **dùng chung một `where_sql`**, mà `where_sql` đã kẹp sẵn
`TRANG_THAI = ?`. Bấm một chip ⇒ `GROUP BY TRANG_THAI` chỉ còn đúng một nhóm ⇒ **mọi chip khác
hiện 0**. Người dùng nhìn "Đã nhận đủ · 0" sẽ tưởng cả tháng không ai nhận hàng.

### Đã sửa

| Chỗ | Thay đổi |
|---|---|
| `_build_dcnb_where` · `_build_btp_where` · `_build_polist_where` | Thêm cờ **`bo_trang_thai=False`**. Bật lên thì bỏ riêng mệnh đề trạng thái, **giữ nguyên mọi bộ lọc khác** |
| `_dcnb_summary` · `_btp_summary` · `_polist_summary` | Phơi thêm **`so_dong` tách theo từng trạng thái**. Câu SQL vốn đã `COUNT(*)` sẵn — trước giờ gộp hết vào `tong_dong` rồi vứt đi |
| 3 endpoint | Tóm tắt dựng bằng WHERE **không có trạng thái**; số dòng phân trang lấy `so_dong[trạng thái đang chọn]` |

⚠️ Nhờ `so_dong` mà **không tốn thêm câu SQL nào** — vẫn đúng một lượt quét như trước.

⚠️ **Phải sửa cả `total_rows`, không chỉ hàng chip.** Bỏ trạng thái khỏi tóm tắt mà vẫn lấy
`summary["tong_dong"]` làm số dòng phân trang thì **phân trang loạn ngay** (hiện tổng của cả kỳ
trong khi bảng chỉ có một nhóm). Đây mới là chỗ dễ chết, không phải hàng chip.

### Verify

| Mức | Nội dung |
|---|---|
| M1 | `ast.parse` OK · không hàm trùng tên |
| **Cấu trúc** (không cần DB) | **21 phép, đạt hết** trên 3 tab: có chọn → SQL **có** mệnh đề; `bo_trang_thai=True` → **không còn**, và cho ra kết quả **giống hệt** trường hợp không chọn trạng thái; `params` chỉ khác **đúng một phần tử**, mọi params khác **giữ nguyên thứ tự**; **số `?` = số params** trên cả 6 nhánh (Bẫy 5) |
| **M2** (DB thật) | **14 phép, đạt hết** trên 3 tab: bấm chip thì **mọi chip giữ nguyên số** · `total_rows` khớp đúng nhóm đang chọn · dữ liệu trả về **chỉ có** trạng thái đã chọn · **bộ lọc khác vẫn ăn vào hàng chip** (lọc mã `COC` làm tổng tụt 14.215 → 376 và hàng chip đổi theo) |
| **Đối chứng trước/sau** | Chạy **bản git HEAD** và bản mới cạnh nhau: không chọn chip **7,8s / 7,9s**, bấm chip **29,2s / 29,5s**, `total_rows` **12.630 y hệt** — chỉ khác đúng một chỗ: chip hiện **1** trạng thái (cũ) so với **5** (mới) |
| **M3** | Build **v1.12.1** (14.716.141 B), EXE mới hơn cả 2 file nguồn, chạy tách hẳn: cổng 5050 LISTENING, **41,6 MB**, `check_update` trả `current 1.12.1` · `is_frozen True` |

✅ **M4 — Đại Ca bấm thử trên giao diện ngày 24/09/2026, xác nhận đúng.** Phần sửa nằm ở backend
nên không kiểm được qua `index.html`, mà phiên đăng nhập của app nằm trong RAM nên không gieo từ
ngoài vào được — chỉ Đại Ca mới đóng được mức này. Kiểm trên **đúng binary đã phát hành**
(SHA256 khớp digest GitHub), không phải bản build local.

### 🐢 Lộ ra một vấn đề CÓ SẴN, không phải do lần sửa này

Bấm chip **chậm gấp ~4 lần** không chọn chip: **7,8s → 29,2s** (T09/2026, `page_size=200`).
Đối chứng bản git HEAD ra **đúng con số đó** ⇒ có sẵn từ trước. Nguyên nhân: mệnh đề
`TRANG_THAI = ?` lọc trên một cột **`CASE` dựng trong CTE**, làm kế hoạch thực thi xấu đi.
Ghi thành việc số 15, chưa đào.

### Bẫy nhỏ suýt báo động nhầm: đếm dấu `?` mà không bỏ comment

Phép kiểm "số dấu `?` khớp số params" (Bẫy 5) báo **thừa 1** ở `dcnb` và `btp`. Không phải lỗi
code — dấu `?` đó nằm trong **comment SQL tiếng Việt**: `-- Số chứng từ xuất ghi trên phiếu nhập
giờ còn dẫn tới phiếu nào không?`. Phải bỏ dòng `--` trước khi đếm:

```python
re.sub(r"--.*$", "", dong)   # bỏ comment rồi mới .count("?")
```

⚠️ Các phiên trước có dùng phép đếm này mà **không bỏ comment**, nên con số ghi trong nhật ký cũ
lệch 1 mà không ai để ý. Bản thân phép kiểm vẫn đúng hướng — chỉ là phải đếm cho sạch.

### ✅ Đã phát hành v1.12.1 + đổi EXE trên máy sang bản CI

Push `8183dd9..2a7e7fb` (2 commit) · Actions run `35962369740` **`success`** · Release **v1.12.1**
là `Latest`. Sau đó đổi EXE trên máy sang đúng asset CI: sao lưu bản local thành
`dist\iPOS_Accounting_Report_v1.12.1_build_local.exe.bak`, tải về, **SHA256 khớp từng ký tự** với
digest GitHub, chạy lại — cổng 5050 LISTENING, **48,2 MB**, nội dung **5/5**, `check_update` trả
`current 1.12.1` · `latest v1.12.1` · `has_update False` · `is_frozen True`.

⚠️ **Commit tài liệu ghi lại việc này CỐ Ý giữ ở local.** Push nó là Actions build lại, thay asset,
SHA vừa khớp xong lại lệch — đúng vòng lặp đã mô tả ở mục trên. Gộp kèm lần sửa code tiếp theo.

---

## 24/09/2026 (tối) — Dọn nốt 3 việc treo: 13, 14, 15 · **v1.12.2**

Đại Ca chốt *"làm luôn đi"*. Việc 11 (nâng GitHub Action + `paths-ignore`) vẫn kẹt vì cần sửa
trên web GitHub, việc 7 cần Đại Ca quyết — nên phiên này làm 13, 14, 15.

### Việc 13 — hoá ra KHÔNG phải lỗi, đóng bằng phép đo

Nghi phiếu `POSTED` mà không có dòng nào trong `WAREHOUSE` đang bị tab giấu mất. Đo cả năm 2026:

| Loại phiếu | POSTED | Không dòng kho | Trong đó **SL > 0** |
|---|---|---|---|
| `XDCNB` | 20.089 | 5 (0,02%) | **0** |
| `NDCNB` | 19.479 | 4 (0,02%) | **0** |
| `XKHOSXBTP` | 21.848 | 2 (0,01%) | **0** |
| `NSP` | 21.561 | 1 (0,00%) | **0** |

**Cả 12 phiếu đều là phiếu rỗng** — có dòng chứng từ nhưng số lượng bằng 0. Phiếu rỗng thì không
có gì để đối chiếu ⇒ tab giấu đi là **đúng**. Không sửa dòng code nào. Đây là kết cục tốt nhất
của một việc treo: **đóng nó bằng số liệu, không phải bằng code.**

### Việc 15 — đào ra gốc, sửa được 5–7 lần

Đo tách từng phần mới thấy nghi ngờ ban đầu ("mệnh đề lọc đắt") là **sai**:

| Phép đo | Thời gian |
|---|---|
| CTE + `COUNT(*)`, **không** lọc | 2,0s |
| CTE + `COUNT(*)`, **có** lọc | 4,0s → **bộ lọc chỉ tốn +1,9s** |
| CTE + phân trang, **không** lọc | 3,6s |
| CTE + phân trang, **có** lọc | 27,1s → **+23,5s** |

⇒ Chỗ đắt không phải bộ lọc, mà là **lọc CỘNG VỚI `ROW_NUMBER` + danh sách cột đầy đủ**.

Thử `ORDER BY … OFFSET/FETCH` (31,9s) và `OPTION (RECOMPILE)` (28,8s) — **cả hai không ăn thua**.
Cách ăn thua: **dựng `DC` ra bảng tạm `#dc` một lần**, rồi cả tóm tắt lẫn phân trang đọc từ đó.

Đo T08/2026, `page_size=50`:

| Thao tác | Trước | Sau | |
|---|---|---|---|
| Không chọn chip | 9,7s | **6,6s** | |
| Chip `Không thấy phiếu nhập` | 31,5s | **7,8s** | 4,0× |
| Chip `Đã nhận đủ` | 42,9s | **7,9s** | 5,4× |
| **Trang 2** | 50,1s | **6,6s** | 7,6× |
| **Đổi cột sắp xếp** | 45,9s | **7,3s** | 6,3× |
| Lọc kho nhập | 8,1s | **5,8s** | |
| **Ô tìm mã hàng** | 7,8s | **9,5s** | ⚠️ chậm đi |

⚠️ **Đánh đổi có thật, không giấu:** ô tìm mã hàng **chậm thêm ~2s** — điều kiện đó vốn đẩy sâu
xuống bảng gốc được, `SELECT INTO` chặn mất. Đo 3 lần mỗi bên để chắc không phải nhiễu.

⚠️ **Chỉ `dcnb_reconcile` dùng `#dc`.** `btp_reconcile` bấm chip 7,5s (bằng lúc không bấm) và
`po_list` 0,2s — không có bệnh thì không sửa.

### Việc 14 — hai chip "Không thấy…" nay nằm cạnh nhau

`Tất cả` · **`Không thấy phiếu nhập`** · **`Không thấy phiếu xuất`** · `Phiếu nhập chưa ghi sổ` ·
`Phiếu xuất chưa ghi sổ` · `Lệch số lượng` · `Đã nhận đủ`.

### 🔴 Tôi làm hỏng `server.py` — và cách bắt được

Để thay một khối trong `get_dcnb_reconcile`, tôi dò **theo số dòng**: tìm dòng bắt đầu bằng
`sql = f"{cte} SELECT`. Chuỗi đó **cũng có ở endpoint BTP phía trên**, còn mốc kết thúc lại khớp
ở dcnb ⇒ vùng thay trải từ BTP sang dcnb, **xoá mất 574 dòng** mà script vẫn báo "đã viết" bình thường.

Bắt được ngay vì `ast.parse` fail. Cứu được **chỉ vì** đã commit sạch trước đó:
`git checkout -- server.py` → đếm lại **162 hàm / 69 route**, đúng nguyên. Không mất gì.

➡️ Ghi thành **Bẫy 26**: sửa `server.py` phải **khớp nguyên khối bằng chuỗi + `assert count == 1`**,
tuyệt đối không dùng chỉ số dòng; và **commit trước khi làm việc lớn**.

### Bẫy 25 — bảng tạm chết ngay khi câu lệnh có tham số kết thúc

pyodbc chạy câu **có tham số** qua `sp_executesql` ⇒ `#dc` tạo trong scope con, hết câu lệnh là
mất. Tách hai lượt `execute` là `Invalid object name '#dc'`.

⚠️ Thử nhanh bằng câu **không tham số** (`SELECT 1 INTO #t`) thì thấy bảng tạm sống bình thường —
suýt kết luận sai. Phải gộp tất cả vào **một** `execute`, duyệt bằng `cursor.nextset()`.
Lợi thêm: hết batch `#dc` tự biến mất, không phải dọn.

### Verify

| Mức | Nội dung |
|---|---|
| M1 | `ast.parse` OK · Babel SUCCESSFUL · không hàm trùng tên · **164 hàm** (162 + 2 hàm mới) · **69 route** không đổi |
| **M2 — đối chứng trước/sau** | Chạy bản git HEAD và bản mới trên **10 tổ hợp** (không lọc · 4 chip khác nhau · trang 2 · ô tìm mã hàng · ô tìm + chip · đổi cột sắp xếp · lọc kho nhập), kỳ **T08/2026** đã đóng nên dữ liệu không trôi: **`data` + `summary` + `pagination` giống HỆT nhau 10/10** |
| M2 | Bộ 14 phép của lần trước chạy lại trên code cuối: **đạt hết** trên cả 3 tab |
| **M3** | Build **v1.12.2** (14.718.356 B), EXE mới hơn cả 2 file nguồn, chạy tách hẳn: cổng 5050 LISTENING, **41,7 MB**, `current_version 1.12.2` · `is_frozen True`, thứ tự chip trong EXE **đúng** |

⚠️ Phép kiểm thứ tự chip lúc đầu báo SAI — **lỗi của phép đo**: nó bắt nhầm khối chip của tab BTP
nằm trước trong file. Phải neo bằng chuỗi **chỉ có ở tab DCNB** (`'chua', 'Không thấy phiếu nhập'`).
Cùng họ với Bẫy 26: **tìm chuỗi mà không kiểm tính duy nhất.**
