# CLAUDE.md — NGUỒN SỰ THẬT DUY NHẤT CỦA **LedgerReport**

> Mọi agent AI (Claude Code, Gemini, Cursor, Copilot, Antigravity…) và mọi dev mới **đọc file này trước**.
> `GEMINI.md` và `AGENTS.md` chỉ là con trỏ về đây — đừng viết nội dung khác vào đó.
> Cập nhật gần nhất: **26/09/2026** · **Bản mới nhất: `v2.0.2`** — vá lỗi nhân viên thường không xuất được Excel Báo cáo TC
> (Bẫy 30, có từ v2.0.0) + việc 9, 10, 23. Kết quả: mục nhật ký *26/09/2026 — Phát hành v2.0.2*.
> · v2.0.1: thông báo có bản mới kiểu mới (hộp thoại + nút cam + thẻ nhắc, việc 37) + "Có gì mới" đọc từ `CO_GI_MOI.md`.
> · Bản trước: **`v2.0.0` = GIAO DIỆN MỚI `DATA REPORT`** (Đại Ca chốt lên Ver 2)
> — push `main` 25/09/2026 tối, Actions tự tạo Release. Gồm: giao diện mới (GĐ0–GĐ5, đăng nhập nhanh, tab Phân quyền,
> thanh lọc 9 màn, cột bảng, lọc 2 chiều tab điều chuyển) + Báo cáo TC xuất `.xlsx` thật chữ 11pt (việc 35–36)
> + vá việc 31 (ô Số chứng từ BC012) + việc 34 (bảng chỉ vẽ ~87 dòng, Bẫy 29). Nhánh `giaodien` đã gộp hết vào `main`.
> Kết quả Actions + đối chiếu EXE trên máy với file CI: xem mục nhật ký *25/09/2026 — Phát hành v2.0.0*.
> · Lên số hiệu đời mới thì `python build_exe.py iPOS_Accounting_Report X.Y.Z` (tham số 2 — thêm 25/09/2026);
> không truyền thì script tự tăng như cũ
> · Tab đối chiếu điều chuyển **đã đạt M4** — Đại Ca bấm thử trên giao diện, đúng
> · Apps Script: **Version 5** (`ban 2026-09-21c`)
> ⚠️ **Đừng ghi cứng digest/kích thước của asset vào tài liệu** — mỗi lần push (kể cả push mỗi
> file `.md`) là Actions build lại và **thay asset bằng binary khác SHA**. Xem việc treo số 11.
> ✅ Tài khoản nhân viên trên Google Sheet + đổi mật khẩu `admin` + tick quyền 2 tab mới: **Đại Ca
> báo đã làm xong 25/09/2026** (việc 1, 3, 4 trong nhật ký).
>
> 📌 **VIỆC CẦN LÀM đang treo: [NHAT_KY_CONG_VIEC.md § Việc cần làm](NHAT_KY_CONG_VIEC.md#-việc-cần-làm--cập-nhật-21092026)** — đọc trước khi nhận việc mới.

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

📄 **Nhật ký công việc đầy đủ: [NHAT_KY_CONG_VIEC.md](NHAT_KY_CONG_VIEC.md)** — mọi thứ đã làm và vì sao.
📄 **Sự cố 15/08/2026 và 8 lỗi đã trả giá: [SU_CO_15082026.md](SU_CO_15082026.md)** — đọc trước khi
được giao bất kỳ việc "khôi phục / dọn dẹp / viết lại" nào.

---

## 1. 🏗️ KIẾN TRÚC

```
Trình duyệt (Chrome --app)  ──HTTP──>  Flask (server.py, cổng 5050)  ──pyodbc──>  SQL Server
        index.html                          48 route                          IACC_CHULONG
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

#### 🗣️ Thông báo lỗi đăng nhập — **đúng HAI tiêu đề, đừng trộn** *(chốt 24/09/2026)*

Màn hình đăng nhập có **hai nhóm ô khác hẳn nhau**: thông tin SQL Server, và tài khoản ứng dụng.
Người dùng phải liếc **dòng đầu** là biết phải sửa nhóm nào:

| Hỏng ở đâu | Dòng đầu (hằng trong `server.py`) |
|---|---|
| Tài khoản / mật khẩu **ứng dụng** | **`Mật khẩu hoặc tài khoản không đúng`** — `_LOI_SAI_TAI_KHOAN` |
| Thông tin **SQL Server** | **`Lỗi kết nối máy chủ`** — `_LOI_KET_NOI` |

Hướng dẫn cụ thể nằm ở **dòng thứ hai**, nguyên văn lỗi ODBC nằm sau nút **"Chi tiết"**.

⛔ **Đừng bỏ dòng hướng dẫn để cho gọn.** Nó sinh ra sau sự cố 20/09/2026: báo sai hướng là người
dùng ngồi chờ thay vì đi bật VPN. Tiêu đề ngắn **thêm vào trước**, không thay thế.

⛔ **Đừng gộp mọi lỗi tài khoản thành "sai mật khẩu".** Lệnh `dang_nhap` của Google trả về **ba**
loại: sai mật khẩu · **tạm khoá N giây** do gõ sai nhiều lần · **tài khoản đã bị khoá**. Chỉ ca
đầu mới đổi chữ — nói "sai mật khẩu" với người đang bị khoá là họ gõ lại tiếp, càng khoá lâu.
Xem nhánh `if not kq.get('ok')` trong `login()`.

Hai đường online (Google) và offline (bản cache trên máy) **dùng chung một câu** — người dùng
không cần biết lúc đó có mạng hay không.
- **Cache** — `_meta_cache[db_name]` giữ danh mục (đơn vị, TK, hàng hoá, MCP, công việc…) để khỏi JOIN bảng dimension.

### 1.1 Màn hình

**10 tab dữ liệu thô** (đều virtual-scroll, lọc theo cột, xuất CSV stream):
`ledger` (chứng từ tổng hợp) · `sale` · `purchase` · `warehouse` · `warehouse_balance` (tồn kho thực tế) ·
`voucher` (chứng từ tiền) · `btp_reconcile` (đối chiếu xuất SX BTP – nhập TP) ·
`dcnb_reconcile` (đối chiếu điều chuyển nội bộ) · `po_list` (danh sách PO) · `report`.

> Tab `income_alloc` (doanh thu chờ phân bổ) đã **gỡ hẳn 16/08/2026** — nó vốn của LedgerStudio,
> bị copy nhầm sang đây và chết hoàn toàn trên `IACC_CHULONG` vì cột `RECEIVE_DATE` không tồn tại.

#### 🧭 Điều hướng 2 tầng *(GĐ3 — 25/09/2026, phát hành trong v2.0.0)*

Cột navy bên trái = **phân hệ** · màn hình của phân hệ nằm ở cột (mở rộng) hoặc hàng tab ngang (thu gọn).
**Kiểu 06C** (Đại Ca chốt 25/09/2026 tối, phác thảo mục 06 của canvas): cột **có tên, 216px**, mục đang chọn
nền `#1d4ed8` (hằng `CPH`). Phân hệ nhiều màn (Mua & bán, Kho) hiện sẵn màn con,
bấm tên nhóm = đóng/mở; phân hệ 1 màn bấm tên là vào thẳng. **Màu nền = đúng tấm navy màn đăng nhập `#172554`**
— bản nhạt 1 bậc `#1e3a8a` Đại Ca thấy *"lạt tông"*, đã bỏ (25/09). Mở rộng thì hàng tab ngang của màn danh sách thành
**dòng đường dẫn** (`HangTab` prop `duongDan`); Báo cáo TC / Phân quyền / Trang chủ vẫn có tab riêng. Nút
**Thu gọn cột** ⇒ 64px icon như GĐ3, hàng tab ngang quay lại. Nhớ trên máy: `lr_cot_phan_he_gon`,
`lr_nhom_phan_he_dong`. ⚠️ Mở rộng ăn thêm 152px chiều ngang: ở 1280px, BC012 (4 ô lọc) ô bị ép còn 113px —
vẫn một hàng, không cắt chữ (đo 25/09). Tên hiển thị: **`DATA REPORT`** (`APP_NAME`). Khai báo ở `PHAN_HE` trong `index.html`:
Tổng hợp (`ledger`) · Tiền (`voucher`) · Mua & bán (`sale`, `purchase`, `po_list`) ·
Kho (`warehouse`, `warehouse_balance`, `btp_reconcile`, `dcnb_reconcile`) · **Báo cáo TC**.
Phân quyền nằm **sát đáy cột**; ô tài khoản (có Đăng xuất) ở **góc phải trên cùng**, sau nút Tải lại
(Đại Ca chốt 25/09/2026 tối — menu mở xuống, mép phải thẳng nút).

**Trang chủ** *(GĐ4, 25/09/2026)* — nút **đầu** cột, `activeTab = 'home'`, component `TrangChu`. Mở app hoặc
đăng nhập xong là vào đây. Hiện **chỉ lời chào + thẻ phân hệ** — Đại Ca chốt *"tạm thời lên mẫu, chưa lấy
số liệu"* ⇒ trang này **không gọi truy vấn SQL nào**. Thẻ = đúng các phân hệ người đó thấy ở cột trái
(+ Phân quyền nếu có quyền); số trên thẻ đếm từ `PHAN_HE` / `REPORT_TYPES` theo quyền. Mô tả + màu thẻ
khai ở `PHAN_HE` (`mo_ta`, `mau`, `ten_day`) — thêm phân hệ mới thì điền luôn, thiếu thì thẻ ra màu xám.
⏭️ Khi thêm khối số liệu ("Việc cần xử lý" trong phác thảo): **kỳ = tháng hiện tại** (Đại Ca chốt), mỗi ô
là truy vấn 6–8 giây ⇒ **tải ngầm**, đừng bắt trang chờ.

**Tab Phân quyền** *(giao diện mới 25/09/2026)* — hai màn **Tài khoản / Chức vụ** nằm trên hàng tab ngang
(`tabPhanQuyen` ở App ⇒ prop `tabCon` của `PermAdminPanel`; số trên tab báo lên qua `onDem`). Mỗi màn =
danh sách bên trái + **khung sửa bên phải 460px** (thay hộp thoại giữa màn). Đại Ca chốt: **không ma trận**
cho chức vụ · khung sửa tài khoản **không** có hộp tóm tắt quyền · ô mật khẩu ẩn sau dòng **"Đặt lại mật
khẩu"** (admin đặt mk mới, không cần mk cũ; tài khoản MỚI luôn có ô) · đơn vị = danh sách tick + dòng
"Tất cả đơn vị" (= `orgs: null`, thấy cả đơn vị mở sau này). Sửa dở mà bấm dòng khác / Huỷ / ✕ ⇒ **hỏi trước**.
⛔ Giữ nguyên `kiemMucBiVutBo` (Bẫy 22): khung sửa chức vụ **chỉ đóng khi Google nhận đủ mã**, thiếu mã là
giữ khung + cảnh báo. Chức vụ `ADMIN`: không có ô tick (app tự tính đủ), **không xoá được**.

**Thông báo có bản mới** *(Đại Ca chốt 26/09/2026 — phương án B + C, mục 07 bản phác thảo; thay dải mỏng 36px cũ)*:
app hỏi GitHub **1 giây sau khi mở, rồi mỗi 2 giờ** (`KIEM_CAP_NHAT_MS`, hook `useAutoUpdate`). Lần hỏi **lúc mở app** thấy bản
mới ⇒ **hộp thoại giữa màn** `HopThoaiCapNhat` (lúc đó gần như luôn ở màn đăng nhập). Thấy bản mới **giữa ngày** ⇒ ⛔ **KHÔNG**
bật hộp thoại đè lên việc đang làm, chỉ **nút cam** `NutCoBanMoi` trên thanh trên (không tắt được) + **thẻ nhắc** `TheNhacCapNhat`
góc phải. "Để lần sau" / "Nhắc lại sau 2 giờ" / ✕ ⇒ thẻ quay lại **đúng 2 giờ sau**. Màn đăng nhập sau khi bấm "Để lần sau":
nhãn cam *Có bản vX* cạnh số phiên bản, bấm là mở lại hộp thoại.
Mục **"Có gì mới"** đọc từ **`CO_GI_MOI.md` tại tag của bản mới** trên GitHub (`_doc_co_gi_moi` / `_tach_co_gi_moi` trong
`server.py`), gộp mọi bản nằm giữa bản đang chạy và bản mới, bỏ dòng trùng, tối đa 8 dòng. ⛔ **Chỉ ghi TÍNH NĂNG người dùng
thấy**; thay đổi hệ thống / code / cách thông báo ⇒ đúng một dòng `- Cập nhật hệ thống` (Đại Ca chốt 26/09/2026). Không đọc được ⇒ mục đó tự ẩn, **không** làm hỏng
việc báo cập nhật. ⚠️ Ghi chú Release trên GitHub **không dùng được** — đó là đoạn văn cố định trong `release.yml`.
⚠️ Máy đang ở bản cũ báo cập nhật bằng **code của bản cũ** ⇒ đổi giao diện thông báo chỉ có tác dụng từ **lần cập nhật sau đó**.

**Báo cáo TC — KHÔNG chia nhóm** (Đại Ca chốt 25/09/2026, theo mẫu iPOS Inventory): vào là thấy
**trang liệt kê 16 thẻ** (`DanhSachBaoCao`, mỗi thẻ = mã + `ten` + `mo_ta` trong `REPORT_TYPES`).
Đang xem mà muốn đổi thì bấm **ô chọn ở đầu hàng điều kiện** (`ChonBaoCao`, có ô tìm, gõ không dấu
được). Ô chọn + nút kiểu xem ở **trái**, Thời gian + ô lọc + nút phễu ở **phải**. Hàng tab: `Tất cả báo cáo` ·
`BCxxx · tên` — tab thứ hai **chỉ hiện khi đang xem báo cáo**, ở trang liệt kê thì ẩn (Đại Ca chốt). ⚠️ `ReportTab` **chỉ bị ẩn, không bị tháo** khi về trang liệt kê
— tháo ra là mất số liệu đang xem và hộp xuất file đang chạy.

⛔ **Thêm tab danh sách mới thì gắn vào `PHAN_HE`.** Quên thì nó tự rơi vào phân hệ **"Khác"** — cố
ý để lộ ra, đừng "dọn" nhánh đó đi (cùng bài học Bẫy 22). Báo cáo mới thì chỉ cần thêm vào
`REPORT_TYPES` (nhớ `ten` + `mo_ta`), trang liệt kê tự hiện.
**Hàng điều kiện báo cáo = ô "Thời gian" gộp + tối đa 3 ô lọc + nút phễu "Bộ lọc nâng cao" + nút
tải xuống** (Đại Ca chốt 25/09/2026). Ô **Thời gian** (`OThoiGian`) gộp Kỳ + Từ ngày + Đến ngày, luôn
ở ngoài. Bấm vào: cột trái **chỉ 5 chế độ** Chọn ngày · tuần · tháng · quý · năm (**không có phím tắt**
kiểu "Hôm nay", "Tháng này" — Đại Ca đã bỏ), bên phải 2 lịch cạnh nhau. Chọn tháng/quý/năm thì
`period` được đặt **đúng loại** vì 9 màn danh sách dùng chung `period`; còn lại là `custom`. Số tuần
theo **ISO 8601** (`TG.tuan`). Bảng nổi là portal `position:fixed`, đặt sát dưới ô nhưng **không đè
cột phân hệ**. Hai nút Excel + PDF gộp thành **`NutXuat`** (icon tải xuống, xổ ra chọn kiểu).
Các ô khác khai ở **`O_LOC_BAO_CAO`**: mặc định ô nào đứng trước thì ra ngoài trước, tới đủ
**`TOI_DA_O_NGOAI` = 4** (tính cả Thời gian); còn lại vào bảng nâng cao. Người dùng bật/tắt + kéo đổi
thứ tự, **nhớ riêng từng báo cáo trên máy** (`localStorage` khoá `lr_loc_ngoai_BCxxx`).
⛔ **Số trên nút phễu = số ô ĐANG CÓ GIÁ TRỊ mà bị giấu trong bảng — đừng bỏ.** Ô lọc bị giấu mà
vẫn áp dụng thì người xem tưởng số liệu là toàn bộ.
⛔ Thêm ô lọc cho báo cáo thì khai vào `O_LOC_BAO_CAO`, **đừng viết thẳng vào hàng điều kiện**.
⚠️ Lớp nổi gắn vào `body` bằng portal (lịch của `IOSDatePicker`) phải mang **`data-lop-noi`** — không
thì bấm vào nó bị tính là "bấm ra ngoài" và bảng Thời gian / Bộ lọc nâng cao tự đóng.

**9 màn danh sách — thanh lọc mới** *(25/09/2026, theo mẫu iPOS "Đặt mua hàng")*: một hàng dồn phải —
ô **Thời gian** + các ô khác: **tối đa 4 ô, mặc định hiện 3** (cả hai tính cả Thời gian — Đại Ca chốt 25/09
tối; `TOI_DA_O_NGOAI_DS` / `MAC_DINH_O_NGOAI_DS`) + phễu **Bộ lọc nâng cao** + nút **"Lọc"** navy đặc (thay
TRUY VẤN) + nút **Cấu hình cột** + Excel (ô icon). *Kết quả N dòng · Hiển thị* nằm ở **chân bảng, góc trái**
(`veKetQuaDs`, thay chữ chìm PROOFTRAIL; ô chọn số dòng mở LÊN). ⚠️ Khối chứa ô lọc phải `flex-1` — bỏ đi
là ô nào cũng bị ép xuống mức sàn 120px dù hàng còn thừa chỗ (đo 1366/1280px: 4 ô đủ 160px, một hàng). Ô lọc khai ở **`oLocDs(tab)`** trong App — thêm ô lọc cho danh sách thì khai
ở đó. Nhớ cấu hình ô ngoài: `lr_loc_ngoai_ds_<tab>`. 3 màn đối chiếu giữ hàng chip trạng thái ngay dưới.

**Cột của 9 bảng — ẩn/hiện + kéo giãn** *(25/09/2026, việc 28)*: khai ở **`COT_BANG`** (khoá, nhãn, độ
rộng gốc, khoá cột file xuất). ⛔ **Thứ tự `COT_BANG` phải đúng thứ tự cột trên bảng** — ẩn cột làm bằng
CSS `:nth-child` theo vị trí; thêm/bớt/đổi chỗ cột trên bảng mà quên sửa `COT_BANG` là **ẩn nhầm cột**.
Dòng gom nhóm (`.dong-nhom`) và dòng tổng tính lại `colSpan` qua `hienCot` / `nhipCot` — viết dòng
tổng mới thì dùng hai hàm đó, đừng ghi `colSpan` cứng. Kéo mép phải tiêu đề = đổi độ rộng, bấm đúp mép =
về gốc; bảng vẫn **tự nở theo nội dung** nên kéo hẹp chỉ tới mức vừa chữ (cố ý, không cắt số liệu).
Tiêu đề cột **không gãy dòng**. Nhớ `lr_cot_<tab>`. **Excel xuất đúng cột đang hiện**: xuất 1 file đi
qua máy chủ (tham số `an_cot` ⇒ `_loc_cot_xuat` trong `server.py`), chia sheet theo đơn vị lọc ở trình
duyệt. Cột chỉ có trong file (Địa chỉ, MST… của Bán hàng) không ẩn được ⇒ luôn xuất.

⚠️ Hàng lọc của 9 màn danh sách: cụm nút phải là **`shrink-0`** — bỏ đi là trên màn 1366px nút
**Xuất Excel bị cắt 56–62px** (đo trên hàng lọc cũ; thanh lọc mới 25/09 đo lại: 9/9 màn một hàng ở 1366 và 1280px). Ô lọc ngoài của báo cáo có **mức sàn `min-w`** — bỏ đi là ô
bị bóp tới gãy chữ (đã đo: ô Kỳ cũ còn 106px, *"2026 - Tháng 1"* gãy 2 dòng). Máy Đại Ca 2048px nên
sẽ không thấy các lỗi này — **đo ở 1366px và 1280px**.

#### `btp_reconcile` — đối chiếu xuất kho SX BTP → nhập kho thành phẩm *(thêm 28/08/2026)*

Nằm trong nhóm "Danh sách" nhưng **không phải danh sách thô**: mỗi dòng là kết quả ghép
`SALE` (phiếu xuất `XKHOSXBTP`) + `WAREHOUSE` (dòng nguyên liệu) + `PURCHASE` (phiếu nhập `NSP`).
Endpoint `/api/btp_reconcile` (+ `/count`, `/stream_csv`).

**Luật nghiệp vụ Chú Long xác nhận:** nhập kho thành phẩm **bắt buộc bấm ngay trên phiếu xuất SX**.
Chỉ khi đó `PURCHASE.SALE_PR_KEY` mới được ghi trỏ về phiếu xuất. Tạo hai phiếu độc lập ⇒
**không có cách nào đối chiếu**.
- Nối phiếu **CHỈ** bằng `PURCHASE.SALE_PR_KEY = SALE.PR_KEY`, thêm tầng hai theo mã BTP.
- ⛔ **Cấm nối theo số phiếu**: số phiếu trùng giữa các đơn vị, và cặp (đơn vị + số phiếu) cũng
  không duy nhất (35 ca trùng trong 2026).
- 1 phiếu = cùng (đơn vị + ngày + số phiếu + kho xuất) — đã kiểm: duy nhất trên cả 19.423 phiếu.

**Ba trường số lượng, đừng lẫn:** `JOB_QTY` = SL bán thành phẩm sản xuất (duy nhất theo cặp
phiếu × BTP) · `QUANTITY` dòng xuất = SL nguyên liệu dùng · `QUANTITY` dòng nhập = SL thành phẩm
nhập kho. ⚠️ `JOB_QTY` ghi theo **ĐVT cơ bản HOẶC ĐVT nhập liệu** tuỳ người gõ (202 BỊCH =
202.000 G) ⇒ phải so với mốc gần hơn giữa `QUANTITY` và `QUANTITY_EXTRA`. So thẳng `JOB_QTY`
với `QUANTITY` cho ra **1.091 ca "sai" hoàn toàn giả** (đã đo trên DB thật).

**6 trạng thái** kể từ 21/09/2026: `Đã nhập đủ` · `Chưa nhập kho BTP` · `Phiếu nhập chưa ghi sổ` ·
`Phiếu xuất chưa ghi sổ` · `Lệch số lượng` · `Không tìm thấy phiếu xuất
liên quan` (chiều ngược — phiếu nhập không truy được về phiếu xuất; cột **Ghi chú** nói rõ là
*làm tay* / *phiếu xuất đã xoá* / *liên kết đứt do lập lại* / *nghi nhập trùng*).

⚠️ **Hai nhóm "chưa ghi sổ" ở tab này HIỆN LUÔN BẰNG 0** — `XKHOSXBTP` (21.588 phiếu) và `NSP`
(21.298 phiếu) **100% `POSTED`, chưa từng có một phiếu nháp nào trong cả lịch sử DB**. Giữ lại để
quy trình đổi thì bắt được ngay. Công thức vẫn được kiểm thật bằng cách chạy lên phiếu **đã** ghi
sổ: `SALE_DETAIL` khớp `WAREHOUSE` **10.094/10.094** (cả SL lẫn `JOB_QTY`), `PURCHASE_DETAIL` khớp
**4.149/4.149**, lệch 0. Đối chứng trước/sau với bản git: **mọi con số của tab giữ nguyên.**

⚠️ Hiệu năng: truy vấn dựng lại toàn bộ CTE mỗi lần gọi (~6–8s cho kỳ 1 tháng). Nhánh phiếu nhập
mồ côi **phải join một lượt**, đừng dùng `OUTER APPLY` tương quan — `SALE` 1 triệu dòng không có
index trên `TRAN_NO`, bản đầu viết kiểu đó làm tab tụt xuống 22–34 giây.

#### `dcnb_reconcile` — đối chiếu điều chuyển nội bộ `XDCNB` → `NDCNB` *(thêm 21/09/2026)*

Cùng khuôn `btp_reconcile`: nối **CHỈ** bằng `PURCHASE.SALE_PR_KEY = SALE.PR_KEY`.
Đo trên `IACC_CHULONG` 2026: **19.838 phiếu `NDCNB` → 19.828 nối được (99,95%), 10 mồ côi.**
**6 trạng thái**: `Đã nhận đủ` · **`Không tìm thấy phiếu nhập`** *(đổi tên 24/09/2026, trước là
"Chưa nhận hàng")* · **`Phiếu nhập chưa ghi sổ`** · **`Phiếu xuất chưa ghi sổ`** · `Lệch số lượng` ·
`Không tìm thấy phiếu xuất liên quan`. Bốn mã lọc trên URL **không đổi** (`du`, `chua`,
`nhap_chua_gs`, `xuat_chua_gs`, `lech`, `khonggoc`) — `chua` vẫn là nhóm đã đổi tên.

🔑 **LUẬT NGHIỆP VỤ GỐC — Chú Long xác nhận 24/09/2026: iPOS TỰ SINH phiếu nhập `NDCNB` (trạng
thái `DRAFT`) ngay khi phiếu xuất `XDCNB` được ghi sổ.** Bên nhận **không lập phiếu**, họ chỉ kiểm
rồi bấm duyệt ghi sổ. Đo T09/2026 xác nhận: **1.906/1.915 phiếu xuất đã ghi sổ có phiếu nhập trỏ
về = 99,53%**.

Hệ quả phải hiểu cho đúng, nếu không là **đọc ngược ý nghĩa cả tab**:

| Nhóm | Thực tế | Việc phải làm |
|---|---|---|
| `Phiếu nhập chưa ghi sổ` | Phiếu **tự sinh sẵn rồi**, đang chờ duyệt | Nhắc bấm duyệt. **Không mất hàng** — đây là hàng đợi bình thường của quy trình |
| `Không tìm thấy phiếu nhập` | Hàng **đã trừ kho** bên xuất mà **không phiếu nào ghi nhận vào kho** | 🔴 Lệch kho thật, phải đi truy |

⛔ **Đừng ghi "bên nhận đã lập phiếu" ở bất cứ đâu** — sai người, và đổ oan cho cửa hàng. Câu đó
từng nằm trong `GHI_CHU` và chú thích chip, đã gỡ 24/09/2026.

⚠️ **Nhóm `Không tìm thấy phiếu nhập` trộn HAI loại khác hẳn nhau** (đo T09/2026: 11 phiếu/15 dòng):
- **8 phiếu / 12 dòng** — không có phiếu nhập nào. Phiếu tự sinh bị xoá, hoặc chưa từng sinh.
- **3 phiếu / 3 dòng** — **CÓ phiếu nhập, đã ghi sổ hẳn hoi, nhưng thiếu đúng một mã hàng.**
  Loại này nguy hiểm hơn vì bên nhận nhìn thấy phiếu "đã xong". Ví dụ `XNB00373/T09` xuất 13 mã,
  `NNB0009/T09` đã ghi sổ chỉ có 12 — thiếu `COC` (Trái cóc) **2.000 G**. Cột **Ghi chú** nay nói
  thẳng *"Phiếu nhập NNB0009/T09 CÓ nhưng thiếu mã hàng này"* (CTE `NP`, dùng lại CTE `P` nên
  không quét thêm bảng).

⚠️ **App ghép cặp theo PHIẾU × MÃ HÀNG**, nên `COUNT(DISTINCT PR_KEY_XUAT)` của một nhóm **đếm cả
phiếu nằm ở nhóm khác** — một phiếu có mã đã nhận và mã chưa nhận sẽ hiện ở cả hai chip. Đó là lý
do 11 phiếu chứ không phải 9. **Cộng các chip lại không ra tổng số phiếu.**

✅ **ĐÃ SỬA 24/09/2026 — hàng chip từng tụt về 0 khi bấm chọn một chip.** Phần tóm tắt dùng chung
`where_sql` vốn đã có `TRANG_THAI = ?`, nên chọn một trạng thái là mọi chip khác về 0 — "Đã nhận
đủ · 0" nhìn như cả tháng không ai nhận hàng. **Dính cả ba tab** `dcnb_reconcile`, `btp_reconcile`
**và `po_list`**. Sửa: ba hàm dựng WHERE nhận thêm cờ **`bo_trang_thai=True`** (bỏ riêng mệnh đề
trạng thái, giữ mọi bộ lọc khác); ba hàm tóm tắt phơi thêm **`so_dong` tách theo từng trạng thái**
để endpoint lấy số dòng phân trang của nhóm đang chọn — **không tốn thêm câu SQL nào.**

⛔ **Thêm bộ lọc mới cho các tab này thì đặt vào `outer`/`where` như cũ — ĐỪNG kẹp thêm điều kiện
theo trạng thái ở bất cứ đâu khác**, không là bệnh quay lại mà không ai thấy (chip vẫn ra số, chỉ
là số sai).

📐 **Thứ tự chip cố ý:** `Tất cả` · **`Không thấy phiếu nhập`** · **`Không thấy phiếu xuất`** ·
`Phiếu nhập chưa ghi sổ` · `Phiếu xuất chưa ghi sổ` · `Lệch số lượng` · `Đã nhận đủ`. Hai chip
"Không thấy…" để **cạnh nhau** vì tên chỉ khác một chữ và là hai chiều ngược của cùng một việc —
tách xa nhau là bấm nhầm. Đừng sắp lại theo thứ tự bảng chữ cái.

⚡ **ĐÃ SỬA 24/09/2026 — bấm chip từng chậm gấp 4–7 lần.** Kẹp `TRANG_THAI = ?` thẳng vào CTE
làm kế hoạch thực thi xấu hẳn. Nay `get_dcnb_reconcile` **dựng `DC` ra bảng tạm `#dc` MỘT lần**
rồi đọc cả tóm tắt lẫn phân trang từ đó. Đo T08/2026, `page_size=50`:

| Thao tác | Trước | Sau |
|---|---|---|
| Không chọn chip | 9,7s | **6,6s** |
| Chip `Đã nhận đủ` | 42,9s | **7,9s** |
| Sang **trang 2** | 50,1s | **6,6s** |
| Đổi **cột sắp xếp** | 45,9s | **7,3s** |
| Ô tìm **mã hàng** | 7,8s | 9,5s ⚠️ |

⚠️ **Đánh đổi có thật:** ô tìm mã hàng **chậm thêm ~2s** vì điều kiện đó vốn đẩy sâu xuống được
bảng gốc, `SELECT INTO` chặn mất. Đổi 2s đó lấy 35–43s ở chip là đáng — nhưng phải biết.

⛔ **Đã thử và KHÔNG ăn thua, đừng thử lại:** `ORDER BY … OFFSET/FETCH` (31,9s) ·
`OPTION (RECOMPILE)` (28,8s). Chi phí của riêng bộ lọc chỉ **+1,9s** (COUNT 2,0s → 4,0s) — chỗ đắt
là lọc **cộng với** `ROW_NUMBER` + danh sách cột đầy đủ.

⚠️ **Chỉ `dcnb_reconcile` dùng `#dc`.** `btp_reconcile` không cần (bấm chip 7,5s, bằng lúc không
bấm) và `po_list` chỉ 0,2s. Đừng bê sang khi chưa đo.

✅ **ĐÃ ĐÓNG 24/09/2026 — phiếu `POSTED` mà 0 dòng `WAREHOUSE` bị tab giấu là ĐÚNG, không phải lỗi.**
Nhánh `X` đọc `WAREHOUSE` nên phiếu kiểu đó không hiện ở nhóm nào. Đo **cả năm 2026** trước khi kết luận:

| Loại phiếu | POSTED | 0 dòng kho | Trong đó **SL > 0** |
|---|---|---|---|
| `XDCNB` | 20.089 | 5 (0,02%) | **0** |
| `NDCNB` | 19.479 | 4 (0,02%) | **0** |
| `XKHOSXBTP` | 21.848 | 2 (0,01%) | **0** |
| `NSP` | 21.561 | 1 (0,00%) | **0** |

**Cả 12 phiếu đều là phiếu rỗng** — có dòng chứng từ nhưng số lượng bằng 0. Phiếu rỗng thì không có
gì để đối chiếu ⇒ giấu đi là đúng. **Đừng "sửa giúp" cho nó hiện ra.** (`XNB00001/T09` ngày 03/09
đơn vị `10` là một trong 12 ca đó — dòng chứng từ có, `QUANTITY_WH` = 0.)

**Kho nhập nay luôn có**, kể cả dòng chưa nhận: lấy theo 3 mức ưu tiên
đã ghi sổ → bản nháp → `SALE.WAREHOUSE_ID_RECEIVE` ghi sẵn trên đầu phiếu xuất. Mức 3 đo cả năm
2026: **19.225/19.226 cặp khớp kho nhận thật** (1 lệch), **0 phiếu đi tới nhiều kho**; suy đơn vị
nhận từ `DM_WAREHOUSE.ORGANIZATION_ID` khớp **1.511/1.511**.

⛔ **KHÔNG có cột "giờ xuất kho"** — đo 4 cột (`TRAN_DATE`, `DOCUMENT_DATE`, `RECEIVE_DATE`,
`USE_DATE`) trên cả `SALE`/`PURCHASE`/`WAREHOUSE`: **0 dòng nào có giờ khác `00:00`**. Giờ thật chỉ
có trong `dbo.LOGGING`, nhưng `LOGGING.PR_KEY` **không phải khoá phiếu** (đối chiếu với `SALE`:
0 dòng trùng), phải dò chuỗi tự do trong `DESCRIPTION`, quét 1 tháng mất **8,95 giây**, và LOGGING
**chỉ còn từ 17/05/2026**. Đại Ca chốt bỏ 21/09/2026. Đừng đo lại.

Phân bố 2026 (đo trước khi tách nhóm): khớp **133.348** · chưa nhận **4.603** · lệch **28**.

**Ba điểm khác BTP — đừng bê nguyên:**
1. **Xuất và nhập ở HAI ĐƠN VỊ KHÁC NHAU** (kho tổng `01` xuất → cửa hàng `35`/`71`/`32`… nhận).
   Bảng có **cả hai cột đơn vị**. Thanh lọc *(Đại Ca chốt 25/09/2026, nhánh `giaodien`)*: **Kho xuất**
   + **Kho nhận** đứng ngoài — hàng mình chuyển đi thì lọc Kho xuất, người ta chuyển cho mình thì lọc
   Kho nhận; *Đơn vị xuất* + *Hàng hoá* nằm trong Bộ lọc nâng cao.
   🔑 **Quyền đơn vị của tab này KHÁC mọi tab khác:** tài khoản bị giới hạn thấy dòng mà **MỘT TRONG
   HAI phía** thuộc quyền — `(DON_VI_XUAT IN quyền OR DON_VI_NHAP IN quyền)` ở WHERE ngoài của
   `_build_dcnb_where`. Trước đó quyền chỉ cắt phía xuất ⇒ cửa hàng **không bao giờ thấy hàng chuyển
   đến mình**. Tài khoản **không giới hạn** thì chạy y như cũ (`_org_filter_sql`, loại đơn vị ngoài cây).
   ⚠️ Đánh đổi: với tài khoản bị giới hạn, phía xuất không đẩy xuống CTE được nữa ⇒ tốc độ ngang tài
   khoản xem toàn công ty. ⛔ Quyền phải áp **cả ở phần tóm tắt** (`bo_trang_thai=True`) — thiếu là
   chip đếm lộ dòng ngoài quyền.
2. ⛔ **`NDCNB` có `IS_SALE = 0`** ⇒ **KHÔNG nằm trong `PURCHASE_VIEW`** (Bẫy 15). Phải đọc thẳng
   `dbo.PURCHASE`; đọc qua view là ra **0 dòng mà không báo lỗi**.
3. **So thẳng `QUANTITY` là ĐÚNG** — hai phía cùng ĐVT cơ bản. **Không** dùng mẹo "mốc gần hơn"
   của BTP (mẹo đó chỉ sinh ra vì `JOB_QTY` của BTP ghi bằng 1 trong 2 đơn vị tuỳ người gõ).
   Tên đơn vị nhận để trống khi một phiếu xuất đi tới nhiều đơn vị (`DON_VI_NHAP` là chuỗi `35 + 71`).

⚠️ Hiệu năng ~6–8,5s/tháng, tương đương BTP. Nhánh mồ côi cũng **phải join một lượt**.

#### `po_list` — danh sách PO (yêu cầu mua hàng `TX` / `TX1` / `TX2`) *(thêm 21/09/2026)*

Nguồn `dbo.PO` + `dbo.PO_DETAIL` (**không có view**). 2026: 4.217 phiếu / 3.384 dòng. ~0,2s, nhanh.
`TX` = Yêu cầu mua hàng (PO) · `TX1` = PO Kho tổng · `TX2` = Đặt mua NCC (Kho Xưởng).
(`KTX` "Yêu cầu **không** thường xuyên" đã `ACTIVE=0` ⇒ "thường xuyên" đúng là bộ TX.)
⚠️ **Đừng đụng `dbo.PURCHASE_ORDER`** — bảng đó **trống 0 dòng**, là di sản.

⛔ **CỐ Ý KHÔNG có cột "đã có phiếu mua hàng chưa"** — xem **Bẫy 20**.

### 1.2 Ma trận báo cáo — **BC001 → BC016**

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
| BC015 | Bán hàng theo nguồn đơn | `/api/sale_by_source` | SALE_VIEW (`STATUS='POSTED'`) ⋈ DM_EXTRA_2 (nguồn đơn = `EXTRA_ID_2`) ⋈ DM_ORGANIZATION; `mode=summary`/`detail` (thêm dòng theo ngày) |
| BC016 | Nhập xuất tồn nhà hàng | `/api/nxt` | WAREHOUSE_VIEW + DM_ITEM / DM_WAREHOUSE / DM_ITEM_CLASS / SYS_TRAN; nhập–xuất trong kỳ là **cột động theo `TRAN_ID`**; `group_by=class`/`warehouse` |

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
9. **Ghi nhật ký thì MỚI NHẤT Ở TRÊN** — chèn mục mới lên **đầu** phần nhật ký, ⛔ không nối xuống
   cuối file. Trên cùng mọi file nhật ký luôn là **việc tồn đọng + nguyên tắc**, rồi mới tới các
   mục theo ngày xếp **mới → cũ**. Áp cho **mọi** file nhật ký của project, không riêng
   `NHAT_KY_CONG_VIEC.md`.

---

## 4. 🐛 BẪY ĐÃ TRẢ GIÁ

### Bẫy 1 — `session['logged_in']` KHÔNG TỒN TẠI *(15/08/2026)*
`/api/login` chỉ gán `session['db_config']`. Endpoint nào kiểm `session.get("logged_in")` sẽ **luôn trả 401**,
frontend gặp 401 là `setIsLoggedIn(false)` → **user bị đá về màn hình đăng nhập ngay khi bấm Xem báo cáo**.
Đã giết BC001–BC004 + BC011. Triệu chứng người dùng: *"bấm là văng ra khỏi phần mềm"*.
➡️ Kiểm đúng: **`_db_cfg()`** (từ 21/09/2026 — trước đó là `session.get('db_config')`, xem Bẫy 17).
Nghe báo triệu chứng đó thì `grep -n "logged_in" server.py` đầu tiên.

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

⛔ **Chiều ngược lại — `import server` TẮT app đang mở ở cổng 5050** *(phát hiện 25/09/2026)*.
`server.py` gọi `kill_process_on_port(5050)` **ở cấp module**, nên nó chạy ngay lúc import, kể cả khi bỏ
qua khối `__main__` (kể cả `test_client`). Hàm này `taskkill /F` mọi tiến trình LISTENING có `:5050`.
Bật server thử lúc Đại Ca đang dùng EXE ⇒ app bị tắt ngang, *"Failed to fetch"*.
➡️ Trước khi `import server`: `netstat -ano | grep ":5050" | grep LISTENING` phải rỗng; có thì dừng, hỏi.
Và `index.html` được tìm theo **thư mục đang đứng** (`resource_path` dùng `os.path.abspath(".")`) — chạy từ
chỗ khác là trang chủ 404.

### Bẫy 7 — Lọc đa tài khoản
`ACCOUNT_ID LIKE '111,112%'` trả 0 dòng. Dùng `_acc_like_sql("111,112", "ACCOUNT_ID")`.

### Bẫy 8 — `<colgroup>` làm vỡ layout file `.xls` *(hết hiệu lực từ 25/09/2026)*
Chỉ đúng cho bản xuất `.xls` HTML cũ. Nay Báo cáo TC xuất **`.xlsx` thật** (xem dưới) — đọc lưới ô, không
chép HTML nên `<colgroup>` không còn ảnh hưởng. Giữ mục này để ai đọc code cũ trong git khỏi bối rối.

**Xuất Excel Báo cáo TC = `.xlsx` thật, giữ y biểu mẫu đang xem** *(Đại Ca chốt 25/09/2026, việc 35)*:
`exportReportXls()` đọc `.report-table` ĐANG HIỆN (chữ, gộp ô, đậm/nghiêng, màu chữ/nền kể cả nền tô cả dòng,
căn lề, cỡ chữ, độ rộng cột, chiều cao dòng) + khối tiêu đề / chữ ký ⇒ gửi **mô hình** cho
`/api/xuat_xlsx_bieu_mau` ⇒ `xlsxwriter` ghi file vào thư mục xuất ⇒ trình duyệt tải qua `/api/tai_file_xuat`.
Luật nhận dạng số giữ nguyên bản `.xls` đã đạt M4. **Cỡ chữ: 1px màn hình = 1pt Excel** (thân bảng 11pt — Đại Ca chốt
25/09/2026, cả BC016); ⛔ độ rộng cột + chiều cao dòng phải phóng **cùng tỉ lệ** (`PHONG`), không là số tràn ô `#####`.
⛔ Đừng quay lại ghi HTML đuôi `.xls` — Excel hỏi
*"định dạng và phần mở rộng không khớp"* mỗi lần mở. ⚠️ Máy chủ bật `constant_memory` ⇒ **cấm `merge_range()`
cho vùng gộp nhiều dòng** (đẩy mất dòng đang ghi dở) — xem chú thích `_ghi_xlsx_bieu_mau`.

### Bẫy 9 — Xuất Excel báo cáo phân trang bị thiếu dòng
DOM chỉ có trang hiện tại. Dùng helper `exportFullXls` (backend nhận `page_size=0` trả toàn bộ).
Backend phải chặn `ZeroDivisionError` khi `page_size=0`.
⚠️ Từ 25/09/2026 `exportReportXls` là hàm **async** mà `exportFullXls` dọn bảng tạm ngay khi nó trả về ⇒ phần
**đọc bảng phải chạy đồng bộ, trước lệnh `await` đầu tiên**. Thêm `await` lên trên phần đọc bảng là xuất ra bảng rỗng.

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

### Bẫy 13 — Tự cập nhật xong, bản mới chết vì kế thừa biến môi trường bootloader *(28/08/2026)*
Triệu chứng: bấm cập nhật → tải xong → EXE cũ đổi thành `.old` → **bản mới không lên**, hiện hộp thoại
`Security validation failure: parent process has different executable!` rồi thoát. Server không bind
cổng 5050 nữa, file `.old` nằm lại vì không ai dọn.

Nguyên nhân: `subprocess.Popen([exe_path])` kế thừa nguyên `os.environ` của tiến trình đang chạy, trong đó
bootloader PyInstaller onefile đã đặt `_PYI_APPLICATION_HOME_DIR`, `_PYI_ARCHIVE_FILE`,
`_PYI_PARENT_PROCESS_LEVEL` (PyInstaller ≤5 là `_MEIPASS2`). Bootloader của EXE **mới** thấy các biến này
thì hiểu mình là tiến trình con giai đoạn 2 của một lần khởi chạy đã giải nén xong, nên **đối chiếu
executable của tiến trình cha với chính mình** — cha là `...exe.old`, con là `...exe` ⇒ khác ⇒ chặn ngay
ở tầng bootloader, Python chưa kịp chạy dòng nào.

➡️ Spawn EXE mới thì phải truyền `env` đã gỡ 4 biến đó: `_child_env_without_pyi()` trong `server.py`.
Đây là luật cho **mọi** chỗ EXE onefile tự spawn lại chính nó, không riêng updater.

⚠️ Đo thế nào cho đúng: process bản mới bị chặn vẫn **nằm trong `tasklist`** nhưng chỉ ~10 MB RAM (bootloader
đang giữ hộp thoại lỗi) và **không LISTENING cổng 5050**. Nhìn mỗi `tasklist` sẽ tưởng nó đang chạy.

### Bẫy 14 — Dựng bộ lọc từ DỮ LIỆU PHÁT SINH thay vì DANH MỤC *(15/09/2026)*
Bộ lọc **"Loại CT"** từng dựng bằng `SELECT DISTINCT TRAN_ID FROM dbo.LEDGER` → chỉ ra 39 mã
(**14,9 giây**), trong khi danh mục gốc `dbo.SYS_TRAN` có 90 mã (**0,04 giây**).
Hậu quả: **35 mã `ACTIVE=1` chưa có bút toán không hề xuất hiện** — mà **mã chứng từ mới lập luôn rơi
đúng vào nhóm này**. Nhóm đơn đặt hàng (`SO`, `SOXU`, `TX`, `TX1`, `TX2`) bản chất không sinh bút toán
nên **thiếu vĩnh viễn**. Tệ hơn, nhánh dự phòng trong `/api/ledger` lại lấy `SYS_TRAN ACTIVE=1` (74 mã)
→ **cùng một `meta['tran_ids']` mà nội dung khác nhau tuỳ đường vào**.
➡️ Luật: **bộ lọc danh mục phải lấy từ bảng danh mục**, dữ liệu phát sinh chỉ dùng làm lưới an toàn
(hợp thêm mã lạ không khai trong danh mục). Xem `_build_tran_catalog()` / `_load_tran_usage()`.

Danh sách **chỉ lấy `ACTIVE = 1`** cho gọn (bỏ 16 mã đã ngưng dùng trên `IACC_CHULONG`), **trừ** mã
`ACTIVE = 0` mà còn chứng từ lịch sử thì vẫn giữ — xem Bẫy 16. Nhưng vẫn phải **đọc hết bảng** để lấy
TÊN: lọc `ACTIVE=1` ngay lúc lấy tên là mã ngưng dùng hiện trơ mã, không có tên chứng từ.

### Bẫy 15 — `SALE_VIEW` và `PURCHASE_VIEW` lọc `IS_SALE = 1` ngay trong view *(15/09/2026)*
Tab đọc **VIEW**, không phải bảng gốc — và định nghĩa view có sẵn mệnh đề lọc:

| View | Mệnh đề trong view | Hệ quả |
|---|---|---|
| `SALE_VIEW` | `WHERE SYS_TRAN.IS_SALE = 1` | bảng `SALE` có 18 mã, tab Bán hàng **chỉ xem được 8** |
| `PURCHASE_VIEW` | `WHERE SYS_TRAN.IS_SALE = 1` | bảng `PURCHASE` có 10 mã, tab Mua hàng **chỉ 5** — `NKHO`, `NSP`, `NSC`, `NDC`, `NDCNB` (`IS_SALE=0`) **không bao giờ hiện** |
| `WAREHOUSE_VIEW` | `WHERE DM_ITEM.IS_WAREHOUSE_BALANCE = 1` | lọc theo **hàng hoá**, không theo loại chứng từ |

Đo thật: `dbo.SALE` có 2.475 dòng `XKHOSXBTP` tháng 1/2026, `dbo.SALE_VIEW` có **0**. Ai đối chiếu số
liệu tab Bán hàng với bảng `SALE` sẽ tưởng mất dữ liệu.
➡️ Mọi phép đo phục vụ một tab phải chạy trên **đúng đối tượng tab đó đọc**.

### Bẫy 16 — Dropdown danh mục lọc `ACTIVE=1` → chứng từ cũ không lọc được *(ghi nhận 15/09/2026)*
Mọi dropdown `DM_*` đều lọc `WHERE ACTIVE=1`. Mã bị ngưng dùng mà **vẫn còn chứng từ lịch sử** sẽ biến
mất khỏi bộ lọc. Đã đo trên `IACC_CHULONG`: năm 2026 an toàn (0 ca), nhưng **`DM_JOB` có 139 dòng
`ACTIVE=0`**, trong đó công việc **`CH.162BT` có 48 dòng LEDGER ngày 02/12/2025** → xem kỳ 2025 là
không chọn được. **Đã bàn và quyết định để nguyên** (sửa sẽ làm dropdown Công việc phình 98 → 237 mục).
Chỉ ghi nhận — gặp triệu chứng "có chứng từ mà không lọc được" thì kiểm `ACTIVE` của danh mục trước.

### Bẫy 17 — Cookie phiên của Flask được **KÝ, KHÔNG MÃ HOÁ** *(21/09/2026)*

`session['db_config'] = data` đặt nguyên **server / database / user / password** của SQL vào cookie.
Cookie Flask chỉ được ký để chống sửa — **nội dung là base64 đọc được, không cần `secret_key`**:

```python
payload = cookie.split('.')[1]          # phần sau dấu chấm đầu = dữ liệu đã nén
print(zlib.decompress(base64.urlsafe_b64decode(payload + '==')).decode())
# -> {"db_config":{"server":"...","user":"sa","password":"...","database":"IACC_CHULONG"}, ...}
```

Mở **F12 → Application → Cookies** là đọc được mật khẩu SQL của người đang đăng nhập —
mượn máy đồng nghiệp một phút là lấy được. Đi kèm: `secret_key` ghi cứng
`'IACC_SECRET_SUPREME_2026'` trong mã nguồn của repo **CÔNG KHAI** ⇒ ai cũng **tự ký được
cookie giả** (tự cấp quyền `app_items`), và phiên cũ sống xuyên qua mọi lần build lại.

➡️ **Đã sửa:** cookie nay chỉ giữ một **mã phiên ngẫu nhiên `sid`**; db_config nằm trong kho
`_phien_db` phía máy chủ (RAM). Dùng `_db_cfg()` / `_dat_db_cfg()` / `_xoa_db_cfg()`.
`secret_key` đổi thành `os.urandom(32)` mỗi lần khởi động.

⛔ **Đừng quay lại đặt bất cứ thứ gì bí mật vào `session`** — cookie là chỗ ai cũng đọc được.
Những thứ đang nằm đó (`app_user`, `app_group`, `app_items`, `app_orgs`) đều là thông tin
không bí mật, và nay chữ ký ngẫu nhiên mới thật sự chống được sửa.

⚠️ **Hệ quả vận hành phải biết:** kho phiên nằm trong RAM nên **khởi động lại app là phải
đăng nhập lại** — kể cả sau khi tự cập nhật. Trước đây cookie mang sẵn thông tin kết nối nên
app dựng lại kết nối được mà người dùng không hề hay.

⚠️ `SESSION_COOKIE_SECURE` **cố ý KHÔNG bật**: app chạy trên `http://localhost:5050`, bật lên
là trình duyệt ngừng gửi cookie ⇒ đăng nhập xong vẫn bị coi là chưa đăng nhập.

### Bẫy 18 — `_GS_TOKEN_GHIM` trong `server.py` là CỐ Ý, đừng "sửa giúp" *(21/09/2026)*

`server.py` ghim cứng **URL + TOKEN của Apps Script** (`_GS_URL_GHIM` / `_GS_TOKEN_GHIM`) để
chỉ phải phát **một file EXE**, không kèm file cấu hình nào. Repo này **CÔNG KHAI** nên
hai chuỗi đó ai cũng đọc được — **đã cân nhắc và Đại Ca chốt chấp nhận.**

| | |
|---|---|
| TOKEN này là gì | chuỗi **Đại Ca tự đặt** ở `const TOKEN` trong Code.gs — **KHÔNG phải token Google** |
| Cầm được thì vào được Drive/Gmail/Sheet? | **Không.** Trong app không có một mẩu credential Google nào (đó là lý do bỏ hướng Service Account 19/09) |
| Cầm được thì đọc được danh sách tài khoản? | **Không.** 7/8 lệnh đòi thêm mật khẩu qua `_doiAdmin()` |
| Cầm được thì chạm được số liệu kế toán? | **Không.** Số liệu ở SQL Server sau VPN, không dính dáng |
| Vậy mất gì | người lạ **gõ cửa dò mật khẩu** và **spam cạn quota Apps Script**. Chống bằng rate limit trong `Code.gs` (KHOA_SO_LAN / KHOA_PHAT_S) |

⛔ **CHỈ ĐÚNG CHO TOKEN APPS SCRIPT.** Tuyệt đối **không ghim kiểu này bất cứ thông tin
SQL Server nào** — cái đó mở thật vào dữ liệu kế toán. Nhân viên vẫn tự gõ thông tin SQL
(Đại Ca chốt 21/09/2026).

⚠️ **Quét secret trước commit sẽ báo động ở hai dòng này** — đó là báo đúng, không phải
báo nhầm. Biết rồi thì cho qua, đừng hoảng và cũng đừng bỏ lệ quét.

Đổi token thì phải đổi **CẢ HAI đầu**: `const TOKEN` trong `phanquyen_gas/Code.gs` **và**
`_GS_TOKEN_GHIM` trong `server.py`, rồi triển khai Apps Script bằng **Phiên bản mới**
(⛔ đừng bấm *"Triển khai mới"* — sinh URL khác, mọi EXE đã phát sẽ mất kết nối).

`ketnoi.json` cạnh EXE **vẫn được đọc và ĐÈ LÊN bản ghim cứng** — giữ lại để đổi gấp mà
khỏi build lại EXE. Bình thường không cần file này.

### Bẫy 19 — Dán thẳng `Code.gs` lên Google là XOÁ MẤT TOKEN THẬT *(21/09/2026)*

Repo này **công khai**, nên `phanquyen_gas/Code.gs` **cố ý** để hai hằng bí mật ở dạng giữ chỗ:

```javascript
const TOKEN = 'DAN_TOKEN_NGAU_NHIEN_VAO_DAY';
const ADMIN_DK_BOOTSTRAP = 'DAN_CHUOI_BAM_ADMIN_VAO_DAY';
```

Dán thẳng file đó vào Apps Script ⇒ **ghi đè TOKEN thật bằng chuỗi giữ chỗ**. Editor hỏng ngay,
và lần **Triển khai** kế tiếp là **toàn bộ EXE đã phát mất kết nối** — token trong EXE không còn
khớp token trên Google. Người dùng thấy *"Không kết nối được tới Google"*, không ai đăng nhập được.

⚠️ **Đã vấp thật 21/09/2026.** Cứu được **chỉ vì** lúc đó chưa bấm Triển khai: bản đang chạy vẫn là
Version cũ mang token thật, nên app vẫn sống trong lúc sửa. Sớm vài phút là chết cả công ty.

➡️ **Luôn dùng `python phanquyen_gas/chuan_bi_deploy.py`** — nó lấy token thật từ `ketnoi.json`,
thay vào, rồi đưa vào clipboard. Không ghi ra file nào trong repo (file đó sẽ chứa token thật).

**Kiểm sau khi dán, TRƯỚC khi Triển khai:** Ctrl+F trong editor tìm `DAN_TOKEN_NGAU_NHIEN` →
phải ra **"No results"**.

**Kiểm sau khi Triển khai:** `ping` phải trả `"ban"` đúng bằng `BAN_CODE` trong file, và `ok: true`
(nghĩa là token vẫn khớp).

⚠️ `ADMIN_DK_BOOTSTRAP` **không khôi phục được** — nó chỉ dùng một lần lúc `khoiTao()` sinh admin
đầu tiên. Sheet đã có admin nên để nguyên chuỗi giữ chỗ là vô hại.

### Bẫy 20 — iPOS **KHÔNG** ghi liên kết PO → phiếu nhập mua hàng *(đo 21/09/2026)*

Ai được giao "đối chiếu PO với phiếu mua hàng" thì **đọc mục này trước, đừng đo lại** — đã đo
**7 khoá** trên `IACC_CHULONG`, không khoá nào dùng được:

| Khoá thử | Kết quả |
|---|---|
| `PURCHASE.SALE_PR_KEY` (khoá mà BTP và ĐCNB dùng) | **0 / 4.950** phiếu `NM` có |
| `PURCHASE.ORIG_TRAN_NO` | **0** — chỉ 147 phiếu ghi `EXCEL` (nhập từ file) |
| Cột nào đó trên `WAREHOUSE` | **không có cột nào** trỏ về PO |
| `PURCHASE_DETAIL.PO_TRAN_NO` + `ORGANIZATION_ID` | duy nhất, 0 nổ dòng, **nhưng mã hàng chỉ khớp 3,3%** |
| `PURCHASE_DETAIL.PO_TRAN_NO` không kèm đơn vị | mã hàng khớp 41,6% **nhưng 1 dòng nhập ghép với tới 50 phiếu PO** |
| `PO_DETAIL.FR_KEY` → `PURCHASE.PR_KEY` | 766 dòng có, **mã hàng khớp 2,2%**; 5 PO khác đơn vị cùng trỏ về MỘT phiếu nhập ⇒ giá trị rác |
| `PO_DETAIL.QUANTITY_RECEIVE` | **= 0 trên cả 3.383 dòng** — iPOS không ghi ngược SL đã nhận |

**Ca soi tận nơi:** PO `POCH2026/0001/T01` của đơn vị `44` đặt `LY-NH600` **22.000 CÁI**; 12 dòng
nhập ghi tham chiếu **đúng số PO đó** lại toàn mã `KEA-*` — không dính dáng gì.

Hai gốc rễ:
1. **Số phiếu PO trùng nặng** — `POCH2026/0001/T08` có **50 bản ở 50 đơn vị, cùng ngày**.
   4.217 phiếu PO 2026 thì **1.924 trùng** theo `(TRAN_ID + TRAN_NO)`. Nối theo số phiếu là nổ dòng.
2. **`PURCHASE_DETAIL` gần như trống**: phiếu `NM` có **11.434 dòng hàng ở `WAREHOUSE`** nhưng chỉ
   **340 dòng** ở `PURCHASE_DETAIL` (3%). Bảng này còn **tắt hẳn T02→T06/2026** (0 dòng), mới bật
   lại từ **T07/2026**. Mà `PO_TRAN_NO` **chỉ tồn tại trên `PURCHASE_DETAIL`**.

⇒ Chiều ngược: **99/4.217 PO (2,3%)** truy được sang phiếu nhập; `TX2` = **0%**.
➡️ **Đại Ca chốt 21/09/2026: BỎ hẳn cột "đã có phiếu mua hàng chưa".** Thêm vào là bịa liên kết
và **đổ oan cho nhân viên** trong khi lỗi là iPOS không ghi. Muốn làm thì phải hỏi Chú Long / iPOS
xem có nút "nhập hàng từ PO" không — đúng như luật BTP đã xác nhận trước đây.

### Bẫy 21 — Không dùng được bí danh cột trong `ROW_NUMBER() OVER (ORDER BY …)` *(21/09/2026)*

Phân trang của các tab dùng `ORDER BY` theo **tên cột đầu ra** (`DON_VI`, `NGAY`, `SO_PHIEU`…).
Viết thẳng kiểu này là lỗi ngay:

```sql
SELECT DON_VI = PO.ORGANIZATION_ID, …,
       RowNum = ROW_NUMBER() OVER (ORDER BY DON_VI)   -- ❌ Invalid column name 'DON_VI'
FROM dbo.PO PO …
```

SQL Server **không** cho tham chiếu bí danh của chính câu `SELECT` đó bên trong `OVER (ORDER BY …)`.
➡️ **Vật chất hoá qua CTE trước rồi mới `ORDER BY`** — đúng cách `btp_reconcile` / `dcnb_reconcile`
đang làm (`WITH DC AS (…) SELECT … FROM DC ORDER BY …`). Tab `po_list` vấp đúng lỗi này lúc đầu
vì viết phẳng không CTE; đã bọc `WITH POL AS (…)`.

⚠️ Lỗi này **chỉ lộ ở nhánh phân trang**, còn `/count` vẫn chạy ⇒ đừng tin mỗi `/count` xanh là xong.

### Bẫy 22 — Thêm tab mới ⇒ **Google nuốt mã quyền trong im lặng** *(21/09/2026)*

Triệu chứng người dùng: *"phân quyền thêm cho nhóm, bấm Lưu không ăn"*. App báo **lưu thành công**,
Sheet không đổi gì — **y hệt hình dạng con bug đổi mật khẩu** cùng ngày.

Nguyên nhân: `phanquyen_gas/Code.gs` **ghi cứng danh sách mã trong hằng `PERM`** (7 tab), còn
checklist trong app dựng từ `DOC_TABS` **ở máy**. Thêm tab mới vào app ⇒ checklist hiện ra tick
được, nhưng `_apiLuuChucVu` lặp `PERM.forEach` **không thấy mã đó nên bỏ qua**, và Sheet cũng
không có cột để ghi. Ba chỗ cùng bệnh: `_apiLuuChucVu`, `_quyenChucVu`, `_apiNap`.

**Đã sửa ba tầng — nhớ đủ cả ba, thiếu tầng nào là bệnh quay lại:**

1. **Google đọc mã từ SHEET, không đọc từ `PERM`** — `_maQuyenTrenSheet()` lấy mã từ chính hàng
   tiêu đề (hàng 3) của sheet *Chức vụ*.
2. **App gửi `tat_ca_muc` + `nhan_muc` lên; Google TỰ TẠO cột cho mã lạ.**
   ⇒ **Từ nay thêm tab mới KHÔNG phải sửa `Code.gs` rồi Triển khai lại.**
   (Mã lạ bị siết `^[A-Za-z0-9_]{2,40}$` — mã đó ghi thẳng vào hàng tiêu đề, không siết là bẩn
   vĩnh viễn cấu trúc Sheet.)
3. **Chức vụ `ADMIN` được tính đủ 100% mục ở phía app** (`_current_perms()`), không phụ thuộc Sheet.
   ⚠️ Chỉ nhận đúng chuỗi `'ADMIN'` **do Sheet cấp** — phiên hỏng / chưa đăng nhập vẫn trả tập
   RỖNG, **không** quay lại lỗi "phiên hỏng thì toàn quyền" của bản trước 21/09.

**Lưới an toàn ở app:** sau khi lưu chức vụ, frontend đọc lại từ Google và đối chiếu; mã nào bị
vứt thì **giữ hộp thoại lại kèm cảnh báo**, không đóng im lặng (`kiemMucBiVutBo`).

⚠️ **Đổi `Code.gs` thì phải Triển khai mới có tác dụng** — `_apiLuuChucVu` chạy **trên Google**,
không nằm trong EXE. Kiểm bằng `ping`: phải trả `"ban": "2026-09-21c"`. Và **luôn** dán qua
`python phanquyen_gas/chuan_bi_deploy.py` (Bẫy 19).

✅ **Đã Triển khai 21/09/2026 19:33 — Version 5.** Deployment ID giữ nguyên ⇒ URL không đổi.
`ping` trả `{"ok": true, "ban": "2026-09-21c", "co_ratelimit": true}`.

### Bẫy 23 — Clipboard qua PowerShell làm **nát tiếng Việt** *(21/09/2026)*

`chuan_bi_deploy.py` bơm UTF-8 vào **stdin của PowerShell**, nhưng `[Console]::In` giải mã theo
**bảng mã ANSI của console** (cp1252 trên máy này) ⇒ mọi chữ tiếng Việt thành rác kiểu
`Chá»n gá»­i`. Dán lên Apps Script là **toàn bộ chú thích VÀ các chuỗi thông báo lỗi hiện cho
người dùng đều hỏng**.

⚠️ **Đã vấp thật.** Bắt được **chỉ vì nhìn màn hình trước khi Ctrl+S** — lưu rồi Triển khai là cả
công ty nhận thông báo lỗi rác. Cùng họ với **Bẫy 12** (PowerShell + tiếng Việt + bảng mã).

➡️ **Đã sửa hai lớp trong `chuan_bi_deploy.py`:**
1. `[Console]::InputEncoding=[System.Text.Encoding]::UTF8;` **trước** khi đọc stdin.
2. **Đọc ngược clipboard ra và đối chiếu từng ký tự** với bản gốc; lệch là dừng, không cho dán.
   Cùng tinh thần `Sync-And-Backup.ps1`: **không tin lệnh copy, phải đối chiếu.**

Script nay in `[OK ] Da doc nguoc clipboard va doi chieu: KHOP tung ky tu`. **Không thấy dòng đó
thì đừng dán.**

### Bẫy 24 — Phiếu CHƯA GHI SỔ vô hình với mọi tab đọc `WAREHOUSE` *(21/09/2026)*

`STATUS` trên `SALE` / `PURCHASE` chỉ có **đúng 2 giá trị**: `POSTED` (đã ghi sổ) và `DRAFT`.
⚠️ `REVIEW_STATUS` **không phải** cái đó (chỉ 29/19.887 phiếu `CHECKED`) — đừng lấy nhầm.

**Phiếu `DRAFT` KHÔNG sinh một dòng nào trong `dbo.WAREHOUSE`.** Đo T09/2026: 13 phiếu `XDCNB`
nháp → **0 dòng**; 211 phiếu `NDCNB` nháp → **0 dòng**. Nghĩa là **mọi tab/báo cáo đọc
`WAREHOUSE` đều không nhìn thấy chúng**, và tệ hơn: tab đối chiếu quy hết thành *"bên nhận chưa
bấm nhập"* — **đổ oan cho cửa hàng trong khi lỗi nằm ở chỗ chưa ai bấm ghi sổ.**

➡️ Muốn thấy phiếu nháp thì phải đọc `SALE` + `SALE_DETAIL` (và `PURCHASE` + `PURCHASE_DETAIL`).
Ba luật khi làm việc đó:

1. ⛔ **Nối bằng `FR_KEY`, KHÔNG phải `PR_KEY`.** Trên mọi bảng `*_DETAIL` của iPOS, `PR_KEY` là
   khoá của **chính dòng đó**, `FR_KEY` mới trỏ về phiếu cha (giống `PO_DETAIL.FR_KEY` ở Bẫy 20).
   ⚠️ **Đã vấp thật:** nối nhầm `PR_KEY` ra **0 dòng cho CẢ phiếu đã ghi sổ**, suýt kết luận
   "iPOS không lưu dòng hàng của phiếu nháp" và bỏ luôn việc. Con số 0 cho nhóm *đã ghi sổ* là
   dấu hiệu nối sai khoá — **thấy 0 ở chỗ chắc chắn phải có dữ liệu thì nghi câu SQL trước.**
2. ⛔ **Số lượng lấy `QUANTITY_WH`.** Đo với `WAREHOUSE.QUANTITY` trên T09/2026:
   `QUANTITY_WH` khớp **12.706/12.706 (100%)** · `QUANTITY` chỉ **3.569 (28%)** ·
   `QUANTITY_EXTRA` **3.273 (26%)**. `QUANTITY` ghi theo **ĐVT nhập liệu**, kho theo **ĐVT cơ bản**:
   mã `KEPC-PMR` ghi `10 BỊCH` nhưng kho là `7.000 G` — lấy nhầm cột thì **sai gấp 700 lần**.
   Cùng họ với bẫy `JOB_QTY` của tab BTP.
3. **Lọc `QUANTITY_WH <> 0`.** 39 cặp lệch giữa `SALE_DETAIL` và `WAREHOUSE` **đều là dòng SL = 0**
   (dòng trống trên phiếu, iPOS không đẩy xuống kho). Lọc đi là hai nguồn trùng khít.

⚠️ **Bảng `*_BUFFER` đều TRỐNG** (11 bảng, 0 dòng) — di sản, đừng mất công tìm ở đó.

⚠️ **`PURCHASE_DETAIL` gần như trống là chuyện RIÊNG của phiếu `NM`** (Bẫy 20), không phải của cả
bảng: với `NDCNB` và `NSP` thì độ phủ là **100% mọi tháng 2026**, cả `POSTED` lẫn `DRAFT`.

💡 **Cách kiểm một nhánh chưa có dữ liệu thật:** chạy đúng công thức của nhánh đó lên phiếu **đã
ghi sổ** rồi bắt nó phải trùng với nhánh cũ. Nhờ mẹo này mà nhánh nháp của tab BTP được kiểm
thật (10.094/10.094 và 4.149/4.149) dù `XKHOSXBTP`/`NSP` **chưa từng có phiếu nháp nào**.

### Bẫy 25 — Bảng tạm `#temp` **chết ngay** khi câu lệnh có tham số kết thúc *(24/09/2026)*

pyodbc chạy câu lệnh **có tham số** qua `sp_executesql`. Bảng tạm tạo bên trong đó nằm trong
**scope con**, nên hết câu lệnh là biến mất. Tách làm hai lượt `cursor.execute` là lỗi ngay:

```python
cur.execute("WITH X AS (...) SELECT ... INTO #dc FROM DC WHERE ...", params)
cur.execute("SELECT * FROM #dc")     # ❌ Invalid object name '#dc'
```

⚠️ Câu **không có tham số** thì lại chạy được — nên thử nhanh bằng `SELECT 1 INTO #t` sẽ thấy
"bảng tạm sống bình thường" rồi kết luận sai. Đã vấp thật.

➡️ **Gộp tất cả vào MỘT `cursor.execute`**, các câu cách nhau bằng `;`, rồi duyệt result set bằng
`cursor.nextset()`. Xem `_doc_ket_qua_ke_tiep()` và `get_dcnb_reconcile()`.
Lợi thêm: hết batch là `#dc` **tự biến mất**, không phải dọn, lần gọi sau luôn có bảng sạch.

### Bẫy 26 — Sửa file 9.000 dòng bằng cách **dò số dòng** là xoá nhầm cả vùng *(24/09/2026)*

Tôi tìm dòng bắt đầu bằng `sql = f"{cte} SELECT` để thay một khối trong `get_dcnb_reconcile`.
Chuỗi đó **cũng có ở endpoint BTP nằm phía trên**, còn mốc kết thúc thì khớp ở dcnb ⇒ vùng thay
trải từ BTP sang tận dcnb, **xoá mất 574 dòng** mà vẫn ghi file ra bình thường.

Cứu được **chỉ vì** working tree đã commit sạch trước đó: `git checkout -- server.py` là xong,
rồi đối chiếu lại **162 hàm / 69 route** đúng như trước.

➡️ **Luật:** sửa `server.py` thì **khớp nguyên khối bằng chuỗi và `assert count == 1`**, tuyệt đối
không dùng chỉ số dòng. Và **commit trước khi làm việc lớn** — đó là thứ duy nhất cứu được.
Sau mỗi lần sửa lớn, đếm lại hàm + route (đoạn script ở mục 2.3) trước khi chạy tiếp.

### Bẫy 27 — Arial + độ đậm 800/900 ⇒ **Arial Black** ⇒ mất chữ tiếng Việt *(25/09/2026, nhánh `giaodien`)*

Arial chỉ có 400 và 700. Xin **800/900** thì Windows (DirectWrite) lấy **Arial Black** — font đó
**thiếu 10/13 chữ Việt có dấu chồng** (`Ả Ấ Ễ Ố Ổ Ộ Ợ Ứ Ừ Ự`, đo bằng `fontTools`). Trình duyệt vá
từng chữ thiếu bằng font khác ⇒ **một chữ trộn hai font, dấu lệch, trông như nhoè**. Không báo lỗi gì.

Đo bằng Chrome chạy ngầm trên máy thật, cùng một câu 20px: Arial 800 = **457px** = Arial Black ·
Arial Bold = **421px**.

➡️ **Đã chặn tận gốc** bằng họ font riêng **`AppSans`** (`@font-face` + `local()` trong `index.html`):
độ đậm **600–900 chỉ trỏ về Arial Bold**. Chặn được cả style inline, lớp Tailwind lẫn thẻ `<b>`.
⛔ **Mọi chỗ khai `font-family` phải để `AppSans` đứng đầu** — một chỗ quên là lọt lưới.

⚠️ **Đã vấp thật, hai lần báo "xong" sai:**
- `.report-table { font-family: 'Inter' }` **ghi cứng tên font** ⇒ bảng báo cáo không theo font chung,
  sửa `body` mấy lần cũng không ăn. Đổi font thì **quét MỌI `font-family`**, không chỉ `body`.
- Dò độ đậm chỉ tìm `fontWeight: 800` ⇒ **sót 20 chỗ `fontWeight: isBold ? 800 : 300`**. Phải dò cả
  dạng biểu thức: `(font-weight|fontWeight)[^;,}\n]{0,30}?\b[89]00\b`.

⚠️ Arial nhỏ hơn 10px ở chữ HOA thì dấu chồng chỉ còn 1–2 điểm ảnh. Đã nâng tối thiểu 9px → 10px;
**10px là cỡ lớn nhất không làm gãy dòng tiêu đề** — 10,5px là `MÃ CT` gãy trong cột `w-16`.

### Bẫy 28 — Thay **một mã màu hàng loạt** trong khi màu đó nằm trên **cả nền sáng lẫn nền tối** *(25/09/2026)*

Đổi tông chàm → navy bằng cách thay `#4f46e5` → `#1e3a8a` ở mọi chỗ. Trên nền trắng thì đẹp hơn,
nhưng `.tab-btn.active` nằm trên **header tối** ⇒ **navy trên nền tối = tàng hình**. Tab đang chọn
biến mất mà không có lỗi nào.

➡️ Thay màu xong phải **rà NỀN PHÍA SAU từng chỗ**. Đổi tông cả app thì **đừng thay mã màu hàng
loạt** — ghi đè thang màu trong `tailwind.config` (403 lớp `indigo-*` đổi theo mà không sửa lớp nào),
còn các mã ghi thẳng thì duyệt tay từng chỗ.

### Bẫy 29 — `useEffect(…, [ref.current])` gắn listener vào khung CŨ ⇒ bảng chỉ vẽ ~87 dòng rồi trắng *(25/09/2026)*

Triệu chứng Đại Ca báo (màn Chứng từ tiền): *Kết quả 149.522 dòng*, trang 10.000 dòng, nhưng cuộn xuống
tới **dòng 87 là hết, bên dưới trắng**. Nhìn như lọc sai kỳ — **không phải**: số đếm và dữ liệu đi chung một
lần gọi API, dữ liệu về đủ 10.000 dòng.

Gốc: `useVirtualScroll` gắn listener cuộn + ResizeObserver bằng deps `[containerRef.current]`. Giá trị đó đọc
lúc **render**, còn ref chỉ được gán lúc **commit** ⇒ sang tab khác, **có một lần vẽ lại ở tab đó**, rồi quay
về: khung bảng MỚI không được gắn gì. `scrollTop` kẹt ở 0, `containerHeight` kẹt ở `window.innerHeight` ⇒ chỉ
vẽ `innerHeight / 29 + 50` dòng (≈87 trên màn Đại Ca). Bấm Lọc lại thì hết (có lần vẽ lại). **Dính cả 9 màn,
có sẵn từ commit đầu tiên — bản đang phát hành cũng bị.**

➡️ Nay effect **không có deps**, chạy sau mọi commit và tự so khung đang gắn với khung hiện tại. ⛔ Đừng dùng
`ref.current` làm deps ở bất cứ đâu — lint đã cảnh báo đúng chỗ này, bản cũ tắt cảnh báo bằng `eslint-disable`.

⚠️ **Thử lại lỗi cuộn trong trình duyệt tích hợp khi khung đang ẩn:** trình duyệt **không bắn sự kiện `scroll`**
khi trang không được vẽ ⇒ gán `scrollTop` xong phải tự `dispatchEvent(new Event('scroll'))`, không thì phép thử
báo "trắng" giả. Đã vấp khi dựng lại lỗi này.

---

### Bẫy 30 — Thêm route `/api` mà quên khai báo quyền ⇒ **nhân viên thường bị 403, quản trị thì không** *(26/09/2026)*

`_perm_guard` chặn mọi route `/api` **chưa có** trong `PERM_PUBLIC` / `PERM_ROUTE_STATIC` — trừ tài khoản có `perm_admin`.
⇒ **Tự thử bằng tài khoản quản trị sẽ KHÔNG BAO GIỜ thấy lỗi.** Đã vấp thật: 2 route xuất Excel Báo cáo TC
(`/api/xuat_xlsx_bieu_mau`, `/api/tai_file_xuat`, việc 35) nằm trong **v2.0.0 và v2.0.1** mà chưa khai báo — Đại Ca (ADMIN) xuất
bình thường, nhân viên bấm xuất là *"Không xuất được file Excel: Route chưa khai báo quyền"*. Phát hiện tình cờ khi thêm route
`/api/ly_do_dang_xuat` và bị chính guard này chặn trong lúc thử bằng tài khoản thường.

➡️ **Thêm route `/api` là khai báo quyền NGAY** (public nếu không đọc thêm dữ liệu; theo mục nếu có). Và **luôn thử một lần
bằng tài khoản KHÔNG phải quản trị** (`app_group` khác `ADMIN`, `app_items` giới hạn — cách gieo phiên ở skill/memory).
Quét nhanh trước khi phát hành (phải ra `[]`):
```python
python -c "import ast,re;s=open('server.py',encoding='utf-8').read();t=ast.parse(s);ns={}
[exec(compile(ast.Module([n],[]),'s','exec'),ns) for n in t.body if isinstance(n,ast.Assign) and getattr(n.targets[0],'id','') in ('PERM_PUBLIC','PERM_ROUTE_STATIC')]
r={d.args[0].value for n in ast.walk(t) if isinstance(n,ast.FunctionDef) for d in n.decorator_list if isinstance(d,ast.Call) and getattr(d.func,'attr','')=='route' and d.args}
dong={'/api/report','/api/report_by_job','/api/cash_flow','/api/export_excel_backend','/api/report_export_csv'}
print(sorted(x for x in r if x.startswith('/api/') and '<' not in x and x not in ns['PERM_PUBLIC'] and x not in ns['PERM_ROUTE_STATIC'] and x not in dong))"
```

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

# B3.5 — Viết mục "## vX.Y.Z" vào CO_GI_MOI.md (app đọc file này TẠI TAG để hiện "Có gì mới" — push rồi là muộn)

# B4 — Build EXE (M3)
taskkill /F /IM iPOS_Accounting_Report.exe /T
python build_exe.py            # tự tăng version.txt, sinh version_info.txt
# python build_exe.py iPOS_Accounting_Report 2.0.0   # lên đời: ĐẶT HẲN số hiệu (phải lớn hơn bản hiện tại)
# ⚠️ CI build bằng version.txt + version_info.txt ĐÃ COMMIT ⇒ commit cả hai file sau khi build

# B5 — Đồng bộ + push (Actions tự tạo Release)
powershell -File Sync-And-Backup.ps1 -Commit -Message "fix: ..."
```

`build_exe.py` chọn tên EXE **theo thư mục đang đứng**: đường dẫn chứa `ledgerreport` →
`iPOS_Accounting_Report`, ngược lại → `iPOS_Ledger_Studio`. **Chạy sai thư mục là ra sai tên EXE.**

### 🔴 Sửa code mà BỎ QUA B4 thì phải TĂNG `version.txt` BẰNG TAY *(vấp thật 21/09/2026)*

`version.txt` **chỉ** được tăng khi chạy `build_exe.py` ở máy. Bỏ qua bước B4 (hay gặp: Đại Ca
đang dùng app nên không được build đè — Bẫy 10) rồi gộp thẳng `main` ⇒ **nội dung đổi mà số hiệu
đứng yên**, và Actions phát hành một EXE mang **đúng số hiệu cũ**.

Hậu quả đo thật: máy có sẵn EXE `1.11.9` build local (14.712.220 B, `21ef4e6f…`) so với bản phát
hành `1.11.9` do CI build (13.100.698 B, `b3ad2a60…`) — **hai file khác hẳn nhau, cùng số hiệu.**
`check_github_update()` chốt bằng `has_update = latest > current` (**lớn hơn hẳn**), nên
`1.11.9 > 1.11.9` là sai ⇒ **app im lặng, máy đó kẹt lại bản cũ vĩnh viễn.**

⚠️ Triệu chứng cực khó thấy: app chạy bình thường, không báo lỗi gì, **chỉ là thiếu tính năng**.
Người dùng sẽ báo *"sao máy tôi không có cái đó"* chứ không ai nghĩ tới chuyện phiên bản.

➡️ Trước khi gộp `main`: mở `version.txt`, **tăng số bằng tay**. Kiểm nhanh bản đang chạy có đúng
bản phát hành không bằng **SHA256** — đối chiếu với `digest` mà GitHub công bố cho asset, đừng tin
mỗi số hiệu:
```powershell
(Get-FileHash "dist\iPOS_Accounting_Report.exe" -Algorithm SHA256).Hash.ToLower()
& "C:\Program Files\GitHub CLI\gh.exe" release view v1.11.9 --json assets
```

⚠️ **Mở EXE để thử thì phải chạy TÁCH HẲN.** Gọi qua `Start-Process` trong một lệnh PowerShell thì
tiến trình con bị kết thúc theo lệnh cha: cổng 5050 lên rồi tắt trong vòng một phút, nhìn tưởng
app crash. Đã vấp 24/09/2026.

CI: [.github/workflows/release.yml](.github/workflows/release.yml) — push `main` là build EXE trên
`windows-latest` rồi tạo Release theo `version.txt`.

### ⏳ VIỆC CÒN TREO — nâng 3 action lên bản chạy Node 24 *(ghi 14/09/2026)*

GitHub đã báo **Node 20 hết vòng đời**; 3 action trong workflow đang bị **ép** chạy trên Node 24
(xem phần ANNOTATIONS của mọi lần build gần đây). Build vẫn thành công, nhưng khi GitHub gỡ hẳn
cơ chế ép đó thì workflow **gãy mà không báo trước** — và chỉ lộ ra đúng lúc đang cần phát hành.

Cần đổi đúng 3 dòng trong [.github/workflows/release.yml](.github/workflows/release.yml):

| Dòng | Hiện tại | Đổi thành |
|---|---|---|
| 20 | `actions/checkout@v4` | `actions/checkout@v7` |
| 25 | `actions/setup-python@v5` | `actions/setup-python@v7` |
| 69 | `softprops/action-gh-release@v2` | `softprops/action-gh-release@v3` |

**Đã đối chiếu breaking change ngày 14/09/2026 — không vướng cái nào:**
- `checkout@v7` chặn checkout fork PR cho `pull_request_target` / `workflow_run`. Workflow này chạy
  bằng trigger `push` nên không dính.
- `setup-python@v6` chuyển sang Node 24 (đòi runner ≥ v2.327.1 — runner GitHub-hosted luôn mới hơn);
  `@v7` **bỏ input `pip-install`**, workflow không dùng input đó.
- `action-gh-release@v3` chỉ chuyển runtime Node 20 → 24, giữ nguyên toàn bộ input.

⛔ **Vì sao chưa làm được:** token `gh` trên máy đang dùng (14/09/2026) chỉ có scope
`gist`, `read:org`, `repo` — **thiếu `workflow`**. GitHub từ chối MỌI commit đụng tới
`.github/workflows/`:

```
! [remote rejected] main -> main (refusing to allow an OAuth App to create or
  update workflow `.github/workflows/release.yml` without `workflow` scope)
```

➡️ **Ai có quyền thì làm:** `gh auth refresh -h github.com -s workflow` (phải bấm xác nhận trên
trình duyệt — đây là cấp quyền cho tài khoản GitHub, agent không được tự làm thay), rồi sửa 3 dòng
trên và push. Hoặc sửa thẳng trên giao diện web GitHub, khỏi cần đụng token.

**Đã đo ngày 14/09/2026 — đừng mất công thử lại hai đường này:**

| Kiểm tra | Kết quả |
|---|---|
| Quyền của `phuongquangtran18` trên repo | `push: true`, `admin: false` — **đủ quyền write để sửa workflow** |
| Scope token (đọc từ header `X-OAuth-Scopes`) | `gist, read:org, repo` — **thiếu `workflow`** |
| Đẩy bằng `git push` | ❌ `refusing to allow an OAuth App to update workflow without workflow scope` |
| Đẩy bằng REST API `PUT /contents/...` | ❌ `404 Not Found` (GitHub trả 404 thay vì 403 khi thiếu scope) |

⇒ GitHub chặn ở **tầng OAuth scope**, không phải tầng quyền repo. Có quyền write vẫn vô ích nếu token
không mang scope `workflow`. Không có đường vòng nào — hoặc cấp scope, hoặc sửa trên web GitHub,
hoặc nhờ chủ repo (`trungkhanhduong93`) làm.

### 💡 Tiện tay khi sửa workflow: thêm `paths-ignore`

Workflow hiện **không lọc theo đường dẫn**, nên push sửa mỗi `CLAUDE.md` cũng kích hoạt build EXE đầy
đủ (~1 phút runner) rồi cập nhật lại Release bằng bản y hệt. Ai vào sửa 3 dòng ở trên thì thêm luôn:

```yaml
on:
  push:
    branches:
      - main
    paths-ignore:
      - '**.md'
      - 'docs/**'
      - 'docs-cu/**'
    tags:
      - 'v*'
```

⚠️ Đẩy thay đổi này lên là Actions chạy lại với `version.txt` hiện tại. Tag đã tồn tại thì
`action-gh-release` **cập nhật lại Release cũ** chứ không tạo bản trùng — vô hại, và chính lần build
đó là phép thử cho 3 action mới. Build hỏng thì dừng trước bước publish, Release đang có vẫn nguyên.

---

## 6. 📎 GHI CHÚ HIỆU NĂNG

Nút thắt gốc **không nằm ở code**: DB 10,6 GB / buffer pool 1.410 MB (trần cứng của SQL Express) ≈ **7,7 : 1**
→ phần lớn truy vấn phải đọc đĩa. Index không nâng được trần RAM.

Đã đo và **đừng làm lại**: `IX_LEDGER_ACC_DATE` là có lợi (giảm 95% số trang đọc) — **không drop**;
thêm INCLUDE dài cho `SALE_DETAIL` là lỗ; nâng cấu hình IIS không cứu được nghẽn SQL.
Chi tiết đầy đủ ở skill `chulong-db-perf`.

⛔ **`AUTO_SHRINK` / `AUTO_CLOSE` KHÔNG phải việc còn treo — đã tắt sẵn, đừng đi tắt lại.**
Đo **16/08/2026 trên chính máy chủ đó**: cả 3 database **và** `model` đều đã OFF
([TOI_UU_DB_16082026.sql:16](TOI_UU_DB_16082026.sql)); [SU_CO_15082026.md:184](SU_CO_15082026.md)
chốt *"kiểm rồi, không phải thủ phạm"*. Tài liệu từng ghi đây là "việc rẻ nhất, hiệu quả nhất còn
treo" — **sai, đã sửa 24/09/2026.**

Giữ `TOI_UU_DB_16082026.sql` lại làm **dây bẫy**: chạy vào mà không đổi gì nghĩa là vẫn OK; đổi gì
đó nghĩa là có người bật lại. Hai cờ này **theo từng database** nên phục hồi từ `.bak` cũ hoặc tạo
DB mới từ `model` bị bật là chúng quay lại — kiểm định kỳ, đừng coi là xong vĩnh viễn.
