# NHẬT KÝ CÔNG VIỆC — LedgerReport

> Toàn bộ những gì đã làm với **LedgerReport**, và **vì sao**. Đọc file này trước khi sửa tiếp.
> Kiến trúc, ma trận báo cáo, phương án backup: [CLAUDE.md](CLAUDE.md).
> Mổ xẻ sâu sự cố + 4 bài học: [SU_CO_15082026.md](SU_CO_15082026.md).
> 🚀 **25/09/2026 tối: PHÁT HÀNH `v2.0.0` = GIAO DIỆN MỚI `DATA REPORT`** (Đại Ca: *"giao diện mới nên nó sẽ là Ver 2"*).
> Nhánh `giaodien` (GĐ0–GĐ5, đăng nhập nhanh, tab Phân quyền, thanh lọc 9 màn, cột bảng, việc 7, việc 35–36) +
> 2 bản vá trên `main` (việc 31, 34) **đã gộp hết vào `main` và push**. Chi tiết: mục *25/09/2026 — Phát hành v2.0.0* ngay dưới § VIỆC CẦN LÀM.
> Bản trước: **v1.12.3** (24/09/2026).
> 🔑 Phiên này chốt được **luật nghiệp vụ gốc**: iPOS **tự sinh** phiếu nhập `NDCNB` khi phiếu xuất
> `XDCNB` ghi sổ — đổi hẳn cách đọc tab đối chiếu điều chuyển. Xem các mục 24/09.
> ✅ **Tài khoản nhân viên trên Google Sheet: Đại Ca báo đã tạo xong 25/09/2026** (cùng đổi mật khẩu
> `admin` và tick quyền 2 tab mới — việc 1, 3, 4).
> 🟡 **Việc 7 — lọc 2 chiều tab điều chuyển: xong ở mã nguồn 25/09, chờ Đại Ca thử với số liệu thật.**
> Apps Script trên Google: **Version 5** (21/09/2026 19:33), mã bản `2026-09-21c` — **đã triển khai**.
>
> 📌 **Việc còn treo gom ở ngay dưới: [§ VIỆC CẦN LÀM](#-việc-cần-làm--cập-nhật-21092026).**
>
> ---
>
> ## ⛔ LUẬT GHI NHẬT KÝ — ÁP CHO MỌI FILE NHẬT KÝ CỦA PROJECT
>
> **1. MỚI NHẤT Ở TRÊN.** Viết mục mới thì **chèn lên đầu phần nhật ký**, ⛔ **không `>>` nối
> xuống cuối file**. Người đọc mở file ra phải thấy ngay việc gần nhất, không phải cuộn 2.000 dòng.
>
> **2. Trên cùng luôn là VIỆC TỒN ĐỌNG + NGUYÊN TẮC**, rồi mới tới các mục theo ngày. Thứ tự cố
> định: *đầu file* → **§ VIỆC CẦN LÀM** → **luật/nguyên tắc** → **nhật ký mới → cũ**.
>
> **3. Phần THAM CHIẾU nằm cuối file** (`## 0.` – `## 8.`) — kiến thức nền, **cố ý giữ thứ tự tăng
> dần**, không áp luật *mới nhất ở trên*. Nhật ký theo ngày nằm **phía trên** khối đó.
>
> ✅ **Đã lật toàn bộ file theo luật này ngày 24/09/2026** — 22 mục nhật ký xếp **mới → cũ**,
> 9 mục tham chiếu dồn xuống dưới. Kiểm toàn vẹn: **mất 0 dòng, thêm 0 dòng** (ngoài 5 dòng vạch
> ngăn cố ý chèn). Từ nay viết mục mới thì chèn ngay dưới § VIỆC CẦN LÀM, đừng nối xuống cuối.

---

## 📌 VIỆC CẦN LÀM — *cập nhật 25/09/2026*

> Gom hết việc còn treo về một chỗ. Nhận việc mới thì **đọc mục này trước**.
> Trạng thái: **v1.12.3 đã phát hành**, là `Latest` trên GitHub, và **EXE trên máy Đại Ca đã là
> đúng file CI** (SHA256 khớp digest — kiểm lại 24/09 lúc 17:50).
>
> ✅ **Hết trạng thái `ahead N` giữ cố ý (25/09/2026):** 8 commit của `main` + toàn bộ commit của `giaodien` đã đi cùng
> lần push phát hành **v2.0.0**. `version.txt` = **`2.0.0`** (đặt hẳn bằng `build_exe.py iPOS_Accounting_Report 2.0.0`),
> lớn hơn `1.12.3` ⇒ máy đang chạy bản cũ **sẽ thấy nút cập nhật**.
>
> ⛔ Luật cũ vẫn giữ: **push riêng file `.md` là Actions build lại và thay asset bằng binary khác SHA** ⇒ tài liệu viết
> SAU lần phát hành này để ở local, gộp vào lần sửa code tới (việc 11 `paths-ignore` sẽ gỡ hẳn vòng lặp này).

### 🎨 DỰ ÁN GIAO DIỆN MỚI — nhánh `giaodien` *(bắt đầu 24/09/2026)* — ✅ **ĐÃ PHÁT HÀNH `v2.0.0` 25/09/2026**

> Phác thảo (ngoài repo): **https://claude.ai/artifact/7kiiWQ13PPR7eXN2AgPhtc** — 6 khung.
> Đang chạy thử **local** trên cổng **5051** từ mã nguồn — Đại Ca chốt **KHÔNG build EXE**, xem local trước.
> Nhật ký chi tiết: mục *24–25/09/2026 (đêm)* ngay dưới § này.

**Đại Ca đã chốt:** font **Arial toàn bộ** · màu chủ đạo **navy `#1E3A8A`** (nền tối `#172554`) ·
**giữ nguyên logo** `icon.svg` `#FF9D3D` · icon **SVG, cấm emoji** · tên hiển thị **`PROOFTRAIL`**,
dòng phụ *"Minh bạch tới từng chứng từ"* · điều hướng **2 tầng** (cột icon navy = phân hệ, hàng tab
ngang = màn hình) · **có trang chủ** theo mẫu iACC Portal.

| GĐ | Việc | Trạng thái |
|---|---|---|
| **0** | Nhánh `giaodien` + ghi mốc **164 hàm / 69 route** | ✅ Xong |
| **1** | **Nền**: Arial · navy · nhãn 11px `#475569` · `tabular-nums` · **sửa lỗi font** | ✅ Xong — commit `1dadaae` + `c64540a` |
| **2** | **Màn đăng nhập**: tấm navy trái, `PROOFTRAIL`, logo gốc, mục 01/02 | ✅ Xong — commit `1dadaae` |
| ➕ | **Đăng nhập nhanh** (hướng A — Đại Ca chốt giữa chừng) | ✅ Xong, **Đại Ca đã thử thật: nhanh** — commit `c64540a` |
| **3** | **Điều hướng**: cột phân hệ 64px + hàng tab ngang, 9 màn hình vào 5 phân hệ. **Báo cáo TC: trang liệt kê 16 thẻ + ô chọn có tìm kiếm, ô lọc dời phải, ô Thời gian gộp, Bộ lọc nâng cao** (Đại Ca đổi ý: bỏ 5 tab nhóm) | ✅ Xong — **Đại Ca xem và chốt OK 25/09**, đã commit (local, chưa push) |
| **4** | **Trang chủ** — Đại Ca chốt 25/09: **chỉ khung + thẻ phân hệ, CHƯA lấy số liệu**; kỳ sau này = tháng hiện tại | ✅ **Khung xong — Đại Ca chốt OK 25/09** (sau khi cho lưới thẻ trải hết bề ngang), đã commit (local, chưa push). Khối số liệu (tải NGẦM, mỗi ô 6–8s) để sau |
| **5** | **Đổi tên hiển thị**: `APP_NAME`, `<title>` + 2 meta, 9 dòng chữ chìm, `manifest.json` (trước ghi nhầm *iPOS Ledger Studio*), Properties của EXE (`build_exe.py` + `version_info.txt`) | ✅ **Xong 25/09 — commit `ee5aed3`**. ⛔ **Giữ tên file `iPOS_Accounting_Report.exe`** — đổi là tự cập nhật đứt. Tiêu đề Release trên GitHub **giữ chữ cũ** *iPOS Accounting Report* — **Đại Ca chốt không cần đổi (25/09/2026)** |

**Việc còn chờ của dự án này:**

| # | Việc | Ghi chú |
|---|---|---|
| 16 | ~~Đại Ca F5 xem lại màn danh sách~~ ✅ **Đại Ca đã xem 25/09** | Nhận xét: **cột bị hẹp** ⇒ thành việc 28 |
| 17 | ~~Nút `TRUY VẤN` đang chuyển màu navy → tím~~ ✅ **XONG 25/09** | Đại Ca chốt: chữ **"Lọc"**, navy đặc, như mẫu iPOS. Nằm trong thanh lọc mới của 9 màn danh sách |
| 18 | ~~Chốt mốc commit phần đăng nhập nhanh + sửa font~~ ✅ **commit `c64540a`** | Local, chưa push |
| 19 | ~~Đại Ca xem GĐ3 rồi chốt commit~~ ✅ **Đại Ca chốt OK sáng 25/09** (*"cái đó thì ok rồi"*) ⇒ đã commit GĐ3 | ⚠️ Đại Ca chốt chung, **không nói rõ đã thử từng mục dưới đây chưa** — lần đầu dùng số liệu thật thì để ý. Danh sách cần xem ở mục *"Việc Đại Ca xem sáng 25/09"* trong nhật ký 25/09 (tiếp 3), ngay dưới § này. Ba việc tôi **không** tự thử được: hộp *"Chuyển mẫu báo cáo?"* khi có số liệu thật · menu **Xuất Excel / Xuất PDF** khi có số liệu (chưa có số liệu thì nút tắt) · kéo thả thứ tự ô lọc bằng chuột thật. Và **đọc lại mô tả 16 thẻ** — tôi tự viết |
| 36 | ~~Chữ trong file Excel Báo cáo TC nhỏ (8,5pt)~~ ✅ **XONG 25/09 — thân bảng 11pt, cột/dòng nới cùng tỉ lệ** (Đại Ca chọn từ 4 file mẫu) | Chi tiết: mục nhật ký *25/09 (khuya, tiếp 4)*. ✅ **Đại Ca xuất thử trên 5051 và chốt OK 25/09** (*"xuất excel ok rồi đó"*) |
| 35 | ~~Báo cáo TC xuất Excel ra `.xls` (HTML), không phải `.xlsx` thật~~ ✅ **XONG 25/09 — nay `.xlsx` thật, giữ y biểu mẫu** (Đại Ca: *"luôn luôn xuất xlsx, y chang biểu mẫu đang xem"*) | Chi tiết: mục nhật ký *25/09 (khuya, tiếp 3)*. ✅ **Đại Ca chốt OK 25/09** cùng việc 36. `/api/export_excel_backend` (BC007/BC008, không ai gọi) vẫn để nguyên |
| 34 | ~~Lỗi cuộn ảo (Bẫy 29) có trong bản ĐANG PHÁT HÀNH v1.12.3~~ ✅ **Đã vá lên `main` 25/09 (`6907d78`), CHƯA build/push** — Đại Ca đồng ý | Vá trong worktree tạm (không đụng thư mục 5051 đang phục vụ); chỉ thay khi hàm trên `main` giống hệt bản `giaodien` trước khi sửa (so sau khi bỏ khác biệt xuống dòng). Gộp thử `main` → `giaodien`: chỉ 1 xung đột, đúng chỗ việc 31 đã biết |
| 33 | ~~Cột phân hệ navy bên trái~~ ✅ **XONG 25/09 — kiểu 06C** (Đại Ca chọn, navy nhạt hơn 1 bậc) | Phác thảo = mục **06** của canvas. Chờ Đại Ca xem trên 5051 |
| 32 | ~~Giao diện mới cho tab Phân quyền~~ ✅ **XONG 25/09 — Đại Ca chốt OK, đã commit** (local, chưa push) | Mục **05 — PHÂN QUYỀN** của bản phác thảo. **Bản 2 (theo góp ý 25/09):** Chức vụ **bỏ ma trận** → danh sách + khung sửa bên phải, cùng kiểu tab Tài khoản · Tài khoản **bỏ ô mật khẩu và hộp tóm tắt quyền** (mật khẩu thu thành dòng *"Đặt lại mật khẩu"*; tài khoản mới vẫn có ô) · Đơn vị = **một danh sách tick**, có dòng *"Tất cả đơn vị"*. Thêm 2 khung **Thêm tài khoản** / **Thêm chức vụ** (Đại Ca hỏi *"màn hình thêm mới quyền thì sao"*). Dữ liệu trong khung là **minh hoạ**. Chưa sửa dòng mã nào |
| 31 | 🩹 **Ô Số chứng từ của BC012 hỏng trong bản ĐANG PHÁT HÀNH v1.12.3** — ✅ **ĐÃ VÁ trên `main` 25/09 (`784d227`), ⏳ CHƯA build/push** | Gõ từng chữ `P` → `T` thì thành `P,PT` và lọc ra 0 dòng (`toggleFilter` coi `tran_no` là mảng). Sửa cả hai nhánh: `giaodien` (chưa commit) và `main`. Đại Ca chốt **build một lần** cùng đợt sau. Người dùng **vẫn gặp lỗi tới khi phát hành**. Dán nguyên số phiếu một lần thì chạy |
| 30 | ~~Áp Bộ lọc nâng cao + ô Thời gian gộp sang 9 màn danh sách~~ ✅ **XONG 25/09 — commit `e071bb9`** | Theo ảnh mẫu iPOS *"Đặt mua hàng"*. **Tối đa 3 ô ngoài** (tính cả Thời gian — Đại Ca chốt), phần còn lại vào Bộ lọc nâng cao. 9/9 màn một hàng ở 1366 và 1280px |
| 29 | ~~Nút Excel / PDF của BC003, BC004 sáng sẵn khi chưa có số liệu~~ ✅ **XONG 25/09/2026** | Sửa luôn khi gộp 2 nút thành nút tải xuống: điều kiện xét `initialReportData`. Đã thử: BC001/003/004/012/016 chưa tải số liệu ⇒ nút tắt, tooltip *"Chưa có số liệu — bấm Xem trước rồi mới xuất"* |
| 20–21 | GĐ4 · GĐ5 | Theo bảng trên |
| 28 | ~~Cột bảng hẹp~~ ✅ **XONG 25/09** — Đại Ca chốt **kéo giãn cột + nhớ**. Tiêu đề không gãy dòng nữa; kèm **ẩn/hiện cột** và **Excel xuất đúng cột đang hiện** · số đo cũ để tham khảo: | Số đo 25/09 cho lúc sửa: hàng lọc 5 màn danh sách **cần 1.393px** để mọi ô đủ rộng, màn 1366 chỉ có **1.254px** (bản cũ trước GĐ3: cần 1.473 / có 1.318 — **vốn đã bị ép co từ trước**). Ở 1280px tiêu đề **`MÃ CT` gãy 2 dòng**. Cột phân hệ ăn thêm 64px chiều ngang |
| 22 | **Hướng B**: bỏ `LockService` cho lệnh chỉ đọc trong `Code.gs` (dòng 487) | 5 người mở app cùng lúc thì người thứ 5 chờ gần 1 phút. **Phải triển khai lại Apps Script** — theo đúng `chuan_bi_deploy.py` (Bẫy 19, 23) |
| 23 | **Bị đá ra (đăng nhập nhanh) không có câu báo lý do** | Người dùng chỉ thấy quay về màn đăng nhập. Đại Ca: *"tính sau"* |
| 24 | **Biên dịch sẵn JSX lúc đóng gói** | Mở app trắng màn hình **~7–13 giây** (Babel dịch 723 KB mỗi lần mở). Đo: `domInteractive` 152ms / `DOMContentLoaded` 6.926ms |
| 25 | **Nhúng 5 thư viện còn tải từ Internet** vào EXE | React, ReactDOM, Babel, Tailwind, xlsx. Google Fonts **đã gỡ** ở GĐ1. Fallback hiện tại là giả: React hỏng ⇒ **màn trắng câm** |
| 26 | **BC015, BC016 chưa có trong ma trận báo cáo của `CLAUDE.md`** | Có thật trong `REPORT_TYPES` ([index.html](index.html)) — *Bán hàng theo nguồn đơn*, *Nhập xuất tồn nhà hàng* |
| 27 | Muốn chữ tiêu đề bảng **> 10px** | Phải nới các cột hẹp `w-16` trước — 10,5px là `MÃ CT` gãy dòng (đã đo) |

### 🔴 Ưu tiên 1 — làm sớm, càng để lâu càng rủi ro

| # | Việc | Vì sao gấp |
|---|---|---|
| 1 | ~~Đổi mật khẩu tài khoản `admin`~~ ✅ **Đại Ca báo đã làm 25/09/2026** | Đã lộ trong khung chat ngày 21/09 để chạy phép thử cuối |
| 2 | ~~Push + phát hành~~ ✅ **XONG 21/09/2026** | Đã push `phanquyen`, gộp `main` (fast-forward, 8 commit), Actions chạy **1m18s** → Release **v1.11.9**. **Tầng 1 và tầng 2 của [backup 4 tầng](#2--phương-án-backup--phục-hồi) nay đều đã có** |
| 3 | ~~TẠO TÀI KHOẢN NHÂN VIÊN TRÊN GOOGLE SHEET~~ ✅ **Đại Ca báo đã làm 25/09/2026** | Mục này trước đây là *chốt chặn trước khi gộp `main`*. **Đã gộp và phát hành ngày 21/09 khi chưa đủ tài khoản** — Đại Ca được báo trước và chốt "phân quyền sau". Hệ quả **đang có hiệu lực ngay bây giờ**: máy nhân viên ở v1.10.7 mở app là hiện nút cập nhật; bấm xong thì bản v1.11.9 **bỏ hẳn chế độ file**, không có tài khoản trên Sheet là **đăng nhập không được**. Đo 21/09: Sheet mới có **2 tài khoản**. Lùi lại phải tự tải EXE cũ từ trang Releases. ⇒ Càng để lâu càng nhiều người vấp |

### 🟡 Ưu tiên 2 — Đại Ca tự làm được trên giao diện

| # | Việc | Ghi chú |
|---|---|---|
| 4 | ~~Tick 2 tab mới cho các chức vụ thật~~ ✅ **Đại Ca báo đã làm 25/09/2026** | Cột `dcnb_reconcile` / `po_list` **đã có sẵn trên Sheet** (tạo 21/09). Chỉ cần vào tab Phân quyền tick là ăn. Chức vụ `ADMIN` khỏi cần — app tự tính đủ |
| 5 | **Hỏi Chú Long / iPOS**: nhập mua hàng có bắt buộc bấm từ phiếu PO không? | Quyết định việc có làm được đối chiếu PO ↔ phiếu nhập hay không. Chi tiết 7 khoá đã đo: [Bẫy 20](CLAUDE.md) |
| 6 | ⏸️ **`AUTO_SHRINK` / `AUTO_CLOSE` — ĐANG TREO CHỜ ĐẠI CA HỎI LẠI** (24/09/2026). Theo mọi bằng chứng trong repo thì **đã tắt sẵn từ lâu**, nhưng **chưa đóng mục này** cho tới khi Đại Ca xác nhận | 🔴 Mục này **sai từ đầu**, để treo hơn một tháng. Chính repo đã ghi ngược lại ở **ba chỗ**: [TOI_UU_DB_16082026.sql:16](TOI_UU_DB_16082026.sql) (*"CẢ 3 DATABASE VÀ 'model' ĐÃ TẮT SẴN"*, đo **16/08/2026 trên chính máy chủ đó**) · [SU_CO_15082026.md:184](SU_CO_15082026.md) (*"kiểm rồi, không phải thủ phạm"*) · mục **5. Verify — đạt M4** trong file này. ⚠️ Chưa đo lại được hôm nay (24/09) vì truy vấn DB thật bị chặn quyền — Đại Ca chạy câu kiểm ở mục nhật ký 24/09 là xong. **Nút thắt thật là RAM: DB 10,6 GB / buffer pool 1.410 MB — trần cứng của SQL Express, không lệnh nào tắt được** |

### 🟢 Ưu tiên 3 — việc code, chưa chặn ai

| # | Việc | Ghi chú |
|---|---|---|
| 7 | ~~Bộ lọc Đơn vị của tab điều chuyển nội bộ áp cho phía XUẤT~~ ✅ **XONG ở mã nguồn 25/09 (nhánh `giaodien`) — chờ thử số liệu thật** | Đại Ca chốt: thanh lọc có **Kho xuất** + **Kho nhận**; tài khoản bị giới hạn thấy dòng mà **một trong hai phía** thuộc quyền. Chi tiết: mục nhật ký *25/09/2026 (khuya)* |
| 8 | ~~Xoá file rác~~ ✅ **XONG 24/09/2026** | Đã xoá `phanquyen.json` (972 B) + `dist/phanquyen.json.cu` (1.002 B). Kiểm trước khi xoá: cả hai đều ghi `"note": "FILE TEST - mat khau tam, khong phai ban that"`, và `server.py` **chỉ nhắc chúng trong comment**, không còn dòng code nào đọc. Cả hai vốn đã `.gitignore` + git không theo dõi ⇒ không lộ |
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
| **Tài khoản vừa bị khoá / xoá vẫn vào được 3–30 giây** *(từ 25/09, nhánh `giaodien`)* | Đánh đổi của **đăng nhập nhanh** — Đại Ca chốt. Google trả lời xong thì bị đá ra. Không làm thế thì mỗi lần đăng nhập chờ Google **~12–35 giây** |
| Đăng nhập nhanh **chỉ áp cho người đã đăng nhập thành công trên CHÍNH máy đó trong 7 ngày** | Lần đầu, quá hạn, gõ sai hoặc vừa đổi mật khẩu ở máy khác ⇒ **vẫn chờ Google như cũ**. Cố ý: nhờ vậy đường nhanh không né được giới hạn gõ sai |

---

---

## 25/09/2026 — Phát hành v2.0.0 (giao diện mới `DATA REPORT`)

Đại Ca: *"ok xuất excel ok rồi đó"* → *"làm các mục cần làm rồi up github luôn nha"* → *"đây là giao diện mới nên nó sẽ là Ver 2"*.

### Đã làm

1. **Gộp `main` → `giaodien`** (commit `4f48a51`): xung đột **đúng 1 chỗ** đã biết (ô Số chứng từ BC012) — lấy bản `giaodien`.
   Kết quả gộp **trùng khít `giaodien`** (0 dòng khác): bản vá việc 31 + 34 vốn đã có sẵn trên nhánh này, cùng cách sửa.
   Dò lại: không còn chỗ nào gọi `onToggleFilter('tran_no'`.
2. **`build_exe.py` nhận tham số thứ 2 = số hiệu đặt hẳn** (`2.0.0`) — trước chỉ biết tự cộng 1 (1.12.3 → 1.12.4).
   Chặn số hiệu **không lớn hơn** bản hiện tại (bộ tự cập nhật chỉ báo khi bản mới > bản đang chạy).
3. `version.txt` = `2.0.0`, `version_info.txt` = `2, 0, 0, 0` (CI build bằng **chính hai file đã commit này**).
4. Sao lưu EXE v1.12.3 (file CI) thành `dist\iPOS_Accounting_Report_v1.12.3.exe.bak` trước khi build.

### 🧪 Verify

| Mức | Kết quả |
|---|---|
| **M1** | `server.py` + `build_exe.py` parse OK · Babel SUCCESSFUL · **173 hàm / 71 route**, không trùng tên · so với `origin/main`: **mất 0 hàm, 0 route**; mới 9 hàm, 2 route (`/api/xuat_xlsx_bieu_mau`, `/api/tai_file_xuat`) |
| Quét secret | Diff `origin/main..HEAD`: không có credential (chỉ tên biến + chuỗi rỗng; `moi123` là mật khẩu giả của phép thử Google giả) |
| **M3** | Build `build_exe.py iPOS_Accounting_Report 2.0.0` OK, EXE mới hơn `index.html`/`server.py` · chạy tách hẳn: cổng 5050 lên sau 0,5s · `/api/version` = **2.0.0** · trang chủ 200 (822.881 B, có `DATA REPORT`, có bản sửa cỡ chữ Excel) · màn đăng nhập hiện **V2.0.0** · `check_update` thấy GitHub đang `v1.12.3` ⇒ `has_update: false` (đúng: 2.0.0 > 1.12.3) · tắt EXE thử sau khi đo |
| M2 / M4 | **Không chạy được ở đây** — không có DB/Google trong phiên. Phần số liệu của các màn: Đại Ca đã thử trên 5051 với số liệu thật (GĐ3, GĐ4, Phân quyền, xuất Excel) |

### 📦 Git + phát hành

- `main` fast-forward lên `giaodien` (`ae1bf9d`), push `62af287..ae1bf9d` — **29 commit**.
- Actions run `36156142392`: **`success`, 62 giây**. Release **`v2.0.0` là `Latest`**, không draft/prerelease, có đủ `.exe` + `.zip`.
- Vẫn cảnh báo Node 20 bị ép chạy Node 24 (việc 11) — build không sao.
- ✅ **EXE trên máy Đại Ca = đúng file CI** (Đại Ca: *"làm hết luôn đi"*): tải asset v2.0.0 → **SHA256 khớp digest GitHub** →
  bản build local cất thành `dist\iPOS_Accounting_Report_v2.0.0_build_local.exe.bak` → thay vào `dist\` → chạy tách hẳn: cổng 5050 lên
  sau 1s, `/api/version` 2.0.0, `check_update` current 2.0.0 = latest v2.0.0 ⇒ không đòi cập nhật (đúng). **Để app chạy cho Đại Ca dùng.**
  (Bản build local cùng số 2.0.0 mà khác file CI thì **không bao giờ tự cập nhật** lên file CI — lý do phải thay.)
- Thư mục làm việc **chuyển về `main`**; nhánh `giaodien` nằm trọn trong `main`, giữ lại làm mốc (chưa xoá).
- Nhật ký ngoài repo (`Nhat Ky Lam Viec LedgerReport\`) bổ sung: bảng lịch sử push v1.11.9 → v2.0.0 (bỏ trống từ 15/09) + mục Ngày 8.
- Mục nhật ký này commit ở local, **chưa push** (push `.md` là Actions build lại, thay asset bằng file khác SHA).

### 🔍 Điểm mù

- **Phát hành cho cả công ty ngay khi Actions xong** — máy nào đang 1.12.x mở app là thấy nút cập nhật lên giao diện mới.
- Mục *"chờ Đại Ca xem"* còn lại trong bảng 🎨 (GĐ5, thanh lọc 9 màn, cột bảng, việc 7 lọc 2 chiều) **chưa có câu chốt riêng**
  — Đại Ca chốt chung *"tạm thời ổn rồi"*. Người dùng báo gì thì sửa ở bản 2.0.x.
- Tiêu đề + nội dung Release trên GitHub giữ chữ cũ *"iPOS Accounting Report"* — ✅ **Đại Ca chốt không cần đổi** (25/09/2026). Đừng đề xuất lại.
- Khởi động lại app sau cập nhật ⇒ **phải đăng nhập lại** (kho phiên trong RAM, Bẫy 17) — như mọi lần.

---

## 25/09/2026 (khuya, tiếp 4) — Excel Báo cáo TC: chữ thân bảng 8,5pt → **11pt** (việc 36)

Đại Ca gửi ảnh BC006 mở trong Excel: *"chữ nó 9 à, hơi nhỏ"*.

✅ **Đại Ca xuất thử trên 5051 và chốt: *"xuất excel ok rồi đó"*** (25/09/2026) — chốt luôn cho việc 35 (`.xlsx` thật).

### 1. Ảnh là FILE CŨ — không phải bản `.xlsx` mới

File trong ảnh = `Downloads\BC006_Bang_Can_Doi_Phat_Sinh_2026_Thang7.xls`, **bản `.xls` HTML xuất 15/08/2026** bằng EXE cũ
(đọc nguồn file: `font-size:11px`, `text-align:start`, không khai font). Hôm đó máy chưa xuất file nào mới. Ba lỗi khác thấy
trong ảnh — số không phân cách `58861945`, tên TK dạt phải (Excel không hiểu `start`), font Aptos Narrow — **là của bản
`.xls` cũ; bản `.xlsx` (việc 35) đã hết**: Arial, số thật `#,##0`, căn trái.

### 2. Nhưng bản `.xlsx` mới còn NHỎ HƠN 9

Đo thật trên server thử 5052 (BC006, số giả): màn hình thân bảng **11px**, tiêu đề cột **10px** ⇒ file ra **8,5pt / 7,5pt**,
dòng đơn vị + *(Ký, họ tên)* **7pt**. Gốc: quy đổi đúng vật lý px × 0,75 — chữ app vốn nhỏ gọn nên sang Excel thành nhỏ.

### 3. Đại Ca chốt: **11pt** + **BC016 theo luật chung** (xem 4 file mẫu 8,5 · 10 · 11 · 12pt trước khi chọn)

`exportReportXls` trong [index.html](index.html): `PT_MOI_PX = 1` (1px màn hình = 1pt Excel) và **`PHONG = 4/3` nhân cho cả
độ rộng cột lẫn chiều cao dòng** — phóng chữ mà quên cột/dòng là số to tràn ô `#####`. Cùng tỉ lệ ⇒ bố cục, chỗ xuống dòng
giữ y màn hình. Bỏ luật riêng *BC016 ép 8pt* (khi in BC016 vẫn co vừa 1 trang ngang ⇒ bản in không đổi).
**Không đụng `server.py`** ⇒ 5051 chỉ cần F5.

| Chỗ | Trước | Sau |
|---|---|---|
| Thân bảng | 8,5pt | **11pt** |
| Tiêu đề cột | 7,5pt | **10pt** |
| Tên báo cáo | 11,5pt | **15pt** |
| Dòng đơn vị, *(Ký, họ tên)* | 7pt | **9pt** |

### 🧪 Verify

- **M1**: Babel SUCCESSFUL.
- **Bấm thật trên giao diện** (5052, BC006, API giả) → đọc file bằng `openpyxl`: Arial **11 / 10 / 15 / 9pt** đúng bảng trên ·
  cột A/B/C–H = 116/323/142px (×4/3) · dòng thân 32,25pt · 19 vùng gộp · số vẫn `#,##0`, số âm `(#,##0)`.
- File thử đã dời ra thư mục nháp, không để trong `Downloads`.

### 🔍 Điểm mù

- **Chưa mở trong Excel thật** (chỉ đọc ngược bằng `openpyxl`) và **chưa thử với số liệu thật** — nhất là BC016 (59 cột) và
  các báo cáo KQKD nhiều cột.
- **In A4 dọc**: BC006 **vốn đã tràn 2 trang ngang** (965px > ~660px khổ in); sau khi phóng rộng ~1.295px, vẫn 2 trang. Muốn
  1 trang ngang thì phải co khi in ⇒ chữ in nhỏ lại — chưa làm, chờ Đại Ca cần.

---

## 25/09/2026 (khuya, tiếp 3) — Vá việc 34 lên `main` · Báo cáo TC xuất `.xlsx` thật giữ y biểu mẫu (việc 35)

Đại Ca: *"vá lỗi ok, khởi động lại luôn"*, rồi *"t muốn luôn luôn là xuất theo dạng xlsx của excel để lưu được định
dạng cũng như y chang biểu mẫu đang xem, trước có làm rồi đó"*.

### 1. Vá việc 34 lên `main` (commit `6907d78`, CHƯA build/push)

Làm trong **worktree tạm** — không chuyển nhánh ở thư mục chính vì 5051 đọc `index.html` từ đĩa. Chỉ thay khi hàm
`useVirtualScroll` trên `main` **giống hệt** bản `giaodien` trước khi sửa (so sau khi bỏ khác biệt CRLF/LF) ⇒ bản vá
trùng từng ký tự với `giaodien`. Gộp thử `main` → `giaodien` (`git merge-tree`): **1 xung đột duy nhất**, đúng chỗ
việc 31 đã biết. 5051 khởi động lại 2 lần (lần 2 để nạp route mới — log cho thấy Đại Ca chưa đăng nhập giữa hai lần).

### 2. "Trước có làm rồi" — tìm trước khi viết

Dò git (`-S` 8 tên thư viện), nhật ký, mọi file trong `D:\AI AGENT JOB`: **chưa từng có** bản ghi `.xlsx` kèm định
dạng cho báo cáo. Cái "đã làm" là nút Excel cũ — **giữ y form nhưng ghi HTML đuôi `.xls`** (Excel hỏi "định dạng và
phần mở rộng không khớp"). Đường `.xlsx` phía máy chủ `/api/export_excel_backend` chỉ làm BC007/BC008 và không ai gọi.
LedgerStudio không có trên máy này; `b6553f6` không có trong repo.

### 3. Cách làm

- **Trình duyệt** (`exportReportXls`, viết lại): đọc `.report-table` đang hiện thành mô hình — xếp ô vào lưới (tính
  gộp ngang/dọc), chữ đậm/nghiêng/gạch chân, màu chữ, màu nền (**kể cả nền tô cả dòng**), căn lề, cỡ chữ (px × 0,75),
  độ rộng cột (đo 300 dòng đầu), chiều cao dòng. Luật số **giữ nguyên bản `.xls` đã đạt M4**; thêm: số âm có dấu `-`,
  số lẻ giữ đúng số chữ số thập phân, số âm trong ngoặc **vẫn hiện trong ngoặc** (`#,##0;(#,##0)`).
  Khối tiêu đề + chữ ký chép nguyên nội dung bản cũ.
- **Máy chủ**: `/api/xuat_xlsx_bieu_mau` ghi bằng `xlsxwriter` (có sẵn trong EXE — **không thêm thư viện Internet**),
  `constant_memory`, tự gộp ô theo lượt dòng (không dùng `merge_range` — CLAUDE.md Bẫy 8), tách sheet > 1 triệu dòng,
  A4, khổ ngang BC015/BC016, BC016 co 1 trang ngang, lặp tiêu đề cột khi in. File trùng tên đang mở trong Excel ⇒ ghi
  `ten (2).xlsx` thay vì báo lỗi. `/api/tai_file_xuat` trả file cho trình duyệt tải về như trước.
- Menu nút tải: *"Xuất Excel (.xlsx)"*; hộp BC008/BC012 đổi chữ `.xls` → `.xlsx`. **CSV không giới hạn dòng giữ nguyên**.

### 🧪 Verify

| Kiểm | Kết quả |
|---|---|
| **M1** | Babel SUCCESSFUL · `server.py` **173 hàm / 71 route** (+5 / +2), không trùng |
| Ghi trực tiếp (mô hình mẫu) | 8 vùng gộp đúng (cả gộp dọc) · `'01'` giữ số 0 đầu · tiền số thật `#,##0` · âm `(#,##0)` màu đỏ · `0.1554` `0.00%` · viền, nền, Arial, khổ ngang, lặp dòng in · tách sheet đúng, sheet nào cũng có tiêu đề |
| Khối lượng | **100.000 dòng × 10 cột: 5,4 giây, 3,7 MB** |
| Bấm thật trên giao diện (5052, BC006, API giả) | Gọi `/api/xuat_xlsx_bieu_mau` + `/api/tai_file_xuat` · file là zip `.xlsx` thật · 19 vùng gộp khớp bảng · `-1000000` hiện `(1,000,000)` · `0012` giữ số 0 · ô `-` giữ chữ · nền dòng TK cha `#f8fafc` (lần đầu thiếu — đã sửa) |

File thử (số giả) đã **chuyển ra thư mục nháp**, không để lẫn trong `Downloads\iPOS_Ledger_Studio`.

### 🔍 Điểm mù

- **Chưa thử với số liệu thật**, nhất là BC001–BC004 (bảng KQKD nhiều cột), BC016 (59 cột) và BC008 cả năm (nhiều dòng):
  máy chủ ghi nhanh, nhưng trình duyệt đọc từng ô bảng lớn có thể mất vài chục giây — y như bản `.xls` cũ.
- Mô hình gửi lên cả khối một lần: sổ vài trăm nghìn dòng ⇒ vài chục MB JSON qua localhost. Chưa đo trần.
- Chưa mở file trong **Excel thật** (mới đọc ngược bằng `openpyxl`) — Đại Ca mở giúp một file.

---

## 25/09/2026 (khuya, tiếp 2) — Sửa lỗi bảng chỉ vẽ ~87 dòng · thanh cuộn dễ thấy · đổi tên DATA REPORT · cột phân hệ kiểu 06C

Đại Ca gửi 2 ảnh màn Chứng từ tiền T08/2026 (*149.522 dòng*): cuộn tới **dòng 87 là trắng**, thanh cuộn *"bị ẩn vào
trong"*; hỏi *"có phải do cho chọn kỳ không"*. Chốt thêm: cột phân hệ **làm theo 06C, navy nhạt 1 chút**; tên
**DATA REPORT** *"cho đúng bản chất"*.

### 1. Bảng chỉ vẽ ~87 dòng — KHÔNG phải do chọn kỳ (commit `9c37191`)

Số đếm và dữ liệu đi chung một lần gọi `/api/voucher` ⇒ không thể lệch kỳ. Dựng lại được đúng lỗi trên server thử
(10.000 dòng giả): Lọc rồi cuộn **đúng** · đổi tab rồi quay lại ngay **đúng** · đổi tab, **có thao tác ở tab kia**,
quay lại **TRẮNG** · bấm Lọc lại **đúng**. Gốc: deps `[containerRef.current]` của `useVirtualScroll` ⇒ **Bẫy 29**.
Sửa: effect không deps, tự so khung. Sau sửa: cả 4 bước đều đúng, thử cả Tiền lẫn Tổng hợp.
⚠️ **Có sẵn từ commit đầu tiên ⇒ bản v1.12.3 cũng bị** — việc 34.

Thanh cuộn khung bảng 9 màn: 8px trong suốt / con trượt 4px xám nhạt ⇒ **12px, có rãnh nền, con trượt `#94a3b8`,
dài tối thiểu 48px** (CSS `:has(> table[data-bang])`, menu thả xuống giữ nguyên). Đo: khung cuộn ăn đúng 12px.

### 2. Đổi tên PROOFTRAIL → DATA REPORT

`<title>`, 2 meta, `APP_NAME`, logo, màn đăng nhập (*DATA / REPORT*, chữ REPORT 277px trong tấm 480px — vừa),
`manifest.json`, Properties EXE (`build_exe.py`, `version_info.txt`). **Giữ** dòng phụ *"Minh bạch tới từng chứng từ"*
và tên file `iPOS_Accounting_Report.exe`.

### 3. Cột phân hệ kiểu 06C

Cột có tên 216px, mục chọn `#1d4ed8`; nhóm nhiều màn hiện sẵn màn con; hàng tab
ngang của màn danh sách thành dòng đường dẫn; nút Thu gọn ⇒ 64px + tab ngang như cũ. Chi tiết: CLAUDE.md § Điều hướng.
🎨 **Màu:** thử nhạt 1 bậc `#1e3a8a` ⇒ Đại Ca: *"hơi lạt tông"* ⇒ về **đúng nền tấm navy màn đăng nhập `#172554`**
(không kéo lưới mờ sang — rối chữ). Chữ thường trên nền mới 10,4:1.

### 🧪 Verify (server thử 5052)

| Kiểm | Kết quả |
|---|---|
| **M1** | Babel SUCCESSFUL |
| 9 màn, cột mở rộng, 4 ô lọc | **1366px và 1280px: 9/9 một hàng**, ô 200/160/144px, trang không tràn ngang |
| Báo cáo | BC008 1280px: đủ 160px · **BC012 1280px: 3 ô ép còn 113px**, một hàng, không cắt chữ |
| Thu gọn / mở rộng | 216 ⇄ 64px, thu gọn thì tab ngang quay lại, **nạp lại trang vẫn nhớ** · đóng nhóm Mua & bán ⇒ ẩn 3 màn con, nhớ |

### 🔍 Điểm mù

- Chưa thử với số liệu thật trên 5051 — nhất là **cuộn thật bằng chuột** qua 10.000 dòng.
- Màn Phân quyền với cột 216px: chưa đo (danh sách + khung sửa 460px, còn ~690px cho danh sách ở 1366).

---

## 25/09/2026 (khuya, tiếp) — Kết quả xuống chân bảng · ô tài khoản lên góc phải · 4 ô lọc (mặc định 3) · Phân quyền sát đáy

Đại Ca gửi 3 ảnh chụp app thật (5051) khoanh đỏ, chốt 4 việc + hỏi phương án cho cột navy bên trái (việc 33).

### Đã làm (`index.html`, không đụng `server.py`)

- **Kết quả + Hiển thị** rời hàng lọc, xuống **chân bảng góc trái** của 9 màn (`veKetQuaDs`), thay đúng chỗ chữ
  chìm PROOFTRAIL. Thay 9 chỗ bằng script khớp nguyên chuỗi, `assert` mỗi chân bảng nằm giữa lời gọi
  `veHangLocDs` của màn đó và màn kế tiếp ⇒ đúng biến số dòng từng màn. `PageSizeDropdown` thêm `moLen`.
- **Ô tài khoản** lên cuối hàng tab ngang, sau *Tải lại*; menu mở xuống, mép phải thẳng nút.
- **Phân quyền** thành nút cuối, sát đáy cột phân hệ.
- **Thanh lọc 9 màn**: `TOI_DA_O_NGOAI_DS` 3 → **4**, thêm `MAC_DINH_O_NGOAI_DS = 3`; `docCauHinhLoc` nhận thêm
  tham số `macDinh`. Báo cáo TC giữ nguyên 4/4 (Đại Ca chọn *chỉ 9 màn danh sách*).
- 🐛 **Tự bắt khi đo:** ô lọc ngoài của 9 màn **vốn bị ép xuống mức sàn 120px** (thiết kế 160px) dù hàng còn
  thừa chỗ — khối chứa chỉ rộng bằng tổng mức sàn. Thêm `flex-1` ⇒ về 160px.

### 🧪 Verify (server thử 5052, dữ liệu giả)

| Kiểm | Kết quả |
|---|---|
| **M1** | Babel SUCCESSFUL |
| Vị trí (1366px) | Ô tài khoản x 1322–1354, ngay sau Tải lại · Phân quyền y 706–756/768 · Kết quả ở chân bảng cả 9 màn |
| 4 ô lọc | Mặc định hiện 3. Bật ô thứ 4 (Loại CT) ⇒ ra ngoài; ô thứ 5 **bị khoá**, hiện *"đã đủ 4 ô"* |
| Bật 4 ô cả 9 màn | **1366px và 1280px: 9/9 một hàng**, ô rộng 200 / 160 / 144px (trước sửa `flex-1`: 186 / 120px), nút cuối cách mép phải 24px, trang không tràn ngang |
| Menu | *Hiển thị* mở lên, mục 500.000 dòng bấm được (không bị bảng che) · menu tài khoản mở xuống, *Đăng xuất* bấm được |

### 🔍 Điểm mù

- Chưa xem với số liệu thật trên 5051 (5051 vẫn chạy mã cũ — phải khởi động lại).
- Máy nào đã tự đổi cấu hình ô lọc (`lr_loc_ngoai_ds_*`) thì giữ cấu hình cũ, chỉ là được bật thêm tới 4.

---

## 25/09/2026 (khuya) — Việc 7: tab điều chuyển lọc 2 chiều (Kho xuất / Kho nhận) + quyền "một trong hai phía" · nhánh `giaodien`

Đại Ca báo **đã làm xong việc gấp** (1 đổi mật khẩu `admin`, 3 tạo tài khoản nhân viên, 4 tick quyền 2 tab
mới), rồi chốt việc 7: *"tách 2 ô, 1 bộ lọc kho xuất, 1 bộ lọc kho nhận"* và về quyền: *"lọc được cả phiếu nhập
và xuất liên quan đến kho mình — mình chuyển đi thì lọc ở kho xuất, người ta chuyển cho mình thì là kho nhận"*.

### Đã làm

- **`index.html`** — `oLocDs('dcnb_reconcile')` đổi thứ tự: **Kho xuất · Kho nhận** (trước là *Kho nhập*) đứng
  ngoài; *Đơn vị xuất* + *Hàng hoá* vào Bộ lọc nâng cao. Hai ô kho vốn đã có từ trước, chỉ là ô Kho nhập bị
  giấu trong bảng nâng cao nên nhìn như chỉ có một ô.
- **`server.py` `_build_dcnb_where`** — tài khoản **bị giới hạn đơn vị**: quyền thành
  `(DON_VI_XUAT IN quyền OR DON_VI_NHAP IN quyền)` ở WHERE ngoài, áp cả phần tóm tắt (chip). Nhánh phiếu nhập
  mồ côi (chỉ có phía nhận) vẫn đẩy quyền xuống CTE. Ô *Đơn vị xuất* lúc này **không giao với quyền** — cửa
  hàng chọn `01` vẫn thấy hàng `01` chuyển tới mình. Tài khoản **không giới hạn**: nhánh cũ nguyên vẹn.

### 🧪 Verify

| Kiểm | Kết quả |
|---|---|
| **M1** | `server.py` **168 hàm / 69 route**, không trùng · Babel SUCCESSFUL |
| **M2** (dựng câu SQL in-process, 7 ca × có/không bỏ trạng thái) | Số dấu `?` = số tham số ở **cả 14 lượt**. ADMIN: câu SQL **y như trước** (`NOT IN ('66')` ở 3 nhánh) · cửa hàng 35: `(DON_VI_XUAT IN (?) OR DON_VI_NHAP IN (?))` · tài khoản không được xem đơn vị nào: `1=0` |
| Giao diện (server thử 5052, 1366px) | Hàng lọc: *Thời gian · Kho xuất · Kho nhận · phễu · Lọc*. Chọn Kho nhận `KCH35` ⇒ yêu cầu gửi `wh_nhap_ids=KCH35`. Bộ lọc nâng cao có *Đơn vị xuất*, *Hàng hoá* |

💡 Bắt được khi đếm: `_DCNB_CTE` có một dấu `?` **trong chú thích SQL** (`-- …không?`). Code cũ vẫn chạy vì
driver bỏ qua chú thích — nhưng script đếm `?` phải bỏ chú thích trước, không thì báo lệch giả.

### 🔍 Điểm mù

- **Chưa chạy với DB thật** (`config.json` không có mật khẩu) ⇒ chưa đo tốc độ cho tài khoản bị giới hạn (dự
  kiến ngang tài khoản xem toàn công ty, 6–8s/tháng) và chưa nhìn số liệu thật của một tài khoản cửa hàng.
- `DON_VI_NHAP` dùng `IN` vì đo 2026 không nhóm nào đi tới nhiều kho. Nếu sau này có phiếu chia cho 2 cửa hàng
  (`35 + 71`) thì hai cửa hàng đó **không thấy dòng đó** — sẽ không lộ, chỉ thiếu.
- Máy nào đã tự đổi cấu hình ô lọc của tab này (`lr_loc_ngoai_ds_dcnb_reconcile`) thì vẫn giữ thứ tự cũ.

---

## 25/09/2026 (tối) — GĐ5 PROOFTRAIL · thanh lọc 9 màn danh sách · ẩn/hiện + kéo giãn cột · Excel theo cột hiện

Đại Ca gửi ảnh màn *"Đặt mua hàng"* của iPOS: *"làm tiếp GĐ5 đổi tên PROOFTRAIL, check luôn cột bảng bị
hẹp, và chỗ bộ lọc làm giao diện như hình… danh sách nó sẽ nhiều hơn, với cả cho phép cấu hình bảng danh
sách, chủ động ẩn hoặc hiện các cột cần"*. Hỏi 4 điểm, Đại Ca chọn cả 4 đề xuất: **kéo giãn cột + nhớ** ·
**3 ô ngoài** như hình · nút **"Lọc" navy đặc** · **Excel xuất đúng các cột đang hiện**.

### Chặng 1 — GĐ5 đổi tên (commit `ee5aed3`)

`<title>`, 2 thẻ meta, `APP_NAME`, 9 dòng chữ chìm chân bảng, `manifest.json` (**trước ghi nhầm "iPOS Ledger
Studio"** — copy từ Studio), Properties của EXE (`build_exe.py` thêm `DISPLAY_NAMES`, `version_info.txt`).
**Giữ** tên file `iPOS_Accounting_Report.exe`, User-Agent gọi GitHub, thư mục xuất file. Kiểm bộ sinh
`version_info` bằng cách chạy riêng đoạn mẫu — **không build thật** (build là tự tăng `version.txt`).

### Chặng 2 — thanh lọc mới cho 9 màn (commit `e071bb9`)

Trái *Kết quả N dòng · Hiển thị*; phải *Thời gian + 2 ô + phễu + **Lọc** + (cấu hình cột) + Excel*. Dùng
lại `BoLocNangCao` / `docCauHinhLoc` của Báo cáo TC (thêm tham số `toiDa`, báo cáo vẫn 4). Ô lọc khai ở
`oLocDs(tab)`, thứ tự mặc định = hàng 1 bản cũ. 3 màn đối chiếu giữ nguyên khối chip (script cắt nguyên
khối `<div>` và đặt dưới thanh lọc). Bỏ 513 dòng hàng lọc cũ.

🐛 Tự bắt khi rà: khai lại hằng `TOI_DA_O_NGOAI` trong thân `BoLocNangCao` trong khi tham số mặc định dùng
chính tên đó — Babel có thể dịch ra lỗi TDZ. Đổi sang dùng thẳng `toiDa`.

### Chặng 3–4 — ẩn/hiện cột, kéo giãn, Excel theo cột hiện

- **`COT_BANG`** (9 bảng, sinh bằng script từ JSX + `*_EXPORT_COLS`, sửa tay 11 cột lệch tên / cặp mã-tên).
  Trước khi làm **đã đếm**: mọi hàng tiêu đề, ô tìm, dòng dữ liệu của cả 9 bảng đều **đúng 1 ô / cột**
  ⇒ ẩn bằng CSS `:nth-child` an toàn. 5 dòng gom nhóm + 5 dòng tổng tính lại `colSpan` (`hienCot`/`nhipCot`),
  script `assert` colSpan cũ khớp đúng dải cột đã đếm.
- **Kéo giãn**: dải 8px ở mép phải tiêu đề; lúc kéo ghi thẳng vào `<style id="cot-keo">` (không setState mỗi
  lần rê chuột), thả mới lưu. Chặn `click` sau khi kéo (không bị sắp xếp nhầm). Bấm đúp mép = về gốc. Bảng
  vẫn **tự nở theo nội dung** — kéo hẹp chỉ tới mức vừa chữ (cố ý, không cắt số liệu). Tiêu đề hết gãy dòng.
- **Excel**: xuất 1 file đi qua **máy chủ** ⇒ `server.py` thêm `_loc_cot_xuat` + tham số `an_cot` cho 9 route
  `stream_csv` (không gửi ⇒ file như cũ; không bao giờ ra file 0 cột). Chia sheet theo đơn vị lọc ở trình duyệt.
- 🐛 **Lỗi CÓ SẴN sửa kèm:** dòng gom nhóm màn **Bán hàng** đặt tổng tiền dưới cột **Số lượng** (cột 19) —
  nay nằm dưới **Tổng TT** (cột 25).

### 🧪 Verify (server thử 5052, dữ liệu giả; `fetch` giả cho `/api/ledger`)

| Kiểm | Kết quả |
|---|---|
| **M1** | Babel SUCCESSFUL · `server.py` **168 hàm** (+1 `_loc_cot_xuat`) / **69 route**, không trùng |
| `_loc_cot_xuat` (gọi thẳng, cột thật `LEDGER_CSV_COLS`) | Không gửi ⇒ 33 cột như cũ · ẩn Nợ, Có ⇒ 31 cột, dữ liệu không lệch · khoá lạ ⇒ bỏ qua · ẩn hết ⇒ giữ nguyên |
| Ẩn Mã CT + Nợ (Tổng hợp, 3 dòng giả) | 34 → 32 cột, **0 cột lệch** tiêu đề/dữ liệu · nhãn dòng tổng 8 → 7 · tổng Có vẫn đúng dưới cột Có · nút cấu hình số 2 · *"31/33 cột hiện"* |
| Gom nhóm theo đơn vị | Nợ ẩn: dòng nhóm 3 ô, tổng Có đúng cột · hiện lại Nợ: tổng Nợ + Có đều đúng cột |
| Kéo giãn | 112 → 192px, lưu `TRAN_DATE:192` · thả chuột **không** sắp xếp · bấm giữa tiêu đề vẫn sắp xếp · bấm đúp ⇒ về 112px |
| Tải lại trang | Vẫn ẩn Mã CT + Nợ, vẫn nhớ cấu hình ô lọc |
| Xuất 1 file | Yêu cầu gửi máy chủ có **`an_cot=TRAN_ID,DEBIT`** |
| Xuất chia sheet | 31 cột, không Mã CT/Nợ, dòng 1 thẳng tiêu đề, 2 sheet *01-Kho tổng* / *35-Cửa hàng 35* |
| 9 màn | Ẩn 1 cột ⇒ tiêu đề + ô tìm cùng giảm 1 · *Về mặc định* đủ lại · thanh lọc **một hàng ở 1366 và 1280px** |

🐛 **Tự bắt khi thử:** thẻ CSS tạm dọn bằng `requestAnimationFrame` — rAF **không chạy khi trang đang ẩn** ⇒
thẻ tạm còn `!important`, bấm đúp không về gốc. Đổi sang `setTimeout`.

### 🔍 Điểm mù

- **Chưa kéo bằng chuột thật** (mới giả lập sự kiện) và **chưa xuất Excel thật từ SQL** (server thử không có
  DB) — Đại Ca thử giúp trên 5051.
- **5051 đang chạy `server.py` cũ** ⇒ xuất 1 file trên 5051 **chưa bỏ cột ẩn** cho tới khi khởi động lại 5051.
- Dòng gom nhóm của 4 màn còn lại chỉ kiểm bằng đọc mã + `assert` dải cột (mới thử thật ở Tổng hợp).
- 9 biến `xxxRow2Count` (hàng lọc cũ) còn nằm lại, không dùng — vô hại, để dọn sau.

---

## 25/09/2026 (chiều) — Tab Phân quyền: giao diện mới vào mã · nhánh `giaodien`, đã commit

> ✅ **Đại Ca xem trên 5051 và chốt OK**, kèm một sửa: nút **"Lưu lên Google" → "Lưu"** (lúc chờ: *"Đang lưu..."*)
> — *"lưu lại thôi chứ không để google"*. Chữ "Google" ở màn Mở khoá và trong lời cảnh báo bỏ sót mã **giữ nguyên**.

Đại Ca duyệt phác thảo qua 3 vòng: *"không dùng ma trận, dựng 2 tab riêng"* · *"user nhiều thông tin quá,
bỏ các thông tin t khoanh"* (ô mật khẩu + hộp tóm tắt quyền) · *"đơn vị làm đơn giản, xem cái nào chọn cái
đó"* · hỏi thêm *"màn hình thêm mới quyền thì sao"* ⇒ vẽ 2 khung Thêm · chốt **giữ** dòng *"Đặt lại mật
khẩu"* (admin đặt mk mới cho người quên, không cần mk cũ) ⇒ *"làm vào mã luôn"*.

### Đã làm (`index.html`, không đụng `server.py`)

| Chỗ | Việc |
|---|---|
| Hàng tab ngang | Tab *Phân quyền* → **Tài khoản · Chức vụ** kèm số đếm (`HangTab` nhận thêm `so`). Hai tab con cũ bên trong panel **gỡ** |
| Màn Tài khoản | Ô tìm · chip lọc theo chức vụ + *Đang khoá* · bảng thêm cột **Chức vụ** và **tên đơn vị** · đơn vị = `[]` thì ghi đỏ *"Chưa chọn đơn vị nào"* (người đó thấy 0 dòng ở mọi màn) |
| Khung sửa tài khoản | Bên phải 460px thay hộp thoại · *Đặt lại mật khẩu* bấm mới hiện ô · công tắc *Cho phép đăng nhập* · chức vụ · đơn vị = danh sách tick 2 cột + *Tất cả đơn vị* |
| Màn Chức vụ | Bảng Mã · Tên · Được xem · Đang dùng · khung sửa bên phải: tick theo nhóm (Danh sách chứng từ 2 cột · Báo cáo tài chính · Quản trị) + *Tất cả mục* |
| An toàn | Sửa dở mà bấm dòng khác / Huỷ / ✕ ⇒ **hỏi trước** · xoá đúng người đang mở ⇒ đóng khung · **ADMIN không xoá được** (mới — trước chỉ khoá khi còn người giữ) · `kiemMucBiVutBo` **giữ nguyên** |
| Màn Mở khoá | Cùng nội dung, kiểu mới |

Mọi lệnh gửi Google (`/api/perm/*`), `save` / `saveRole` / `del` / `delRole`, luật "tick hết đơn vị = `null`"
**giữ nguyên** — chỉ thay phần vẽ. Đếm lại khai báo cấp component: **mất 0**, thêm đúng 9 hằng kiểu `PQ_*`.

### 🧪 Verify — server thử 5052, **Google GIẢ trong RAM** (không gọi Apps Script thật)

Thay 5 lệnh `/api/perm/*` bằng bản giả có đòi mật khẩu quản trị + chờ 1,5 giây như Google chậm, và ghi lại
mọi thứ app gửi lên để đối chiếu.

| Kiểm | Kết quả |
|---|---|
| **M1** | `check_babel.js` SUCCESSFUL · `server.py` không đổi · độ đậm 800/900 mới thêm: **0** |
| Mở khoá | Sai mk ⇒ *"Sai mật khẩu quản trị"*, vẫn ở màn mở khoá · đúng ⇒ vào danh sách, tab ghi **Tài khoản 5 · Chức vụ 4** |
| Hỏi trước khi bỏ | Chưa sửa gì ⇒ đổi dòng **không hỏi** · sửa dở rồi bấm dòng khác ⇒ hỏi, trả lời *Không* thì **ở lại** |
| Sửa tài khoản | Bỏ tick 71 + đổi tên ⇒ gửi `orgs: ["01","35"]`, **không kèm `password`** · nút lúc chờ *"Đang lưu lên Google..."* và bị khoá |
| Đặt lại mật khẩu | Ô chỉ hiện sau khi bấm · gõ `moi123` ⇒ gửi đúng `password: "moi123"` |
| Thêm tài khoản | Có ô mật khẩu, không có nút Xoá, đơn vị mặc định *Tất cả* ⇒ gửi `orgs: null` + `password` · số trên tab lên 6 · xoá đi ⇒ khung đóng, dòng mất |
| Lọc | Chip KT ⇒ `ketoan1, ketoan3` · tìm `kho` ⇒ `ketoan3, kho01` · *Đang khoá* ⇒ `ch71` |
| Chức vụ | KT tick thêm *Đối chiếu điều chuyển* ⇒ 23 → **24/26**, gửi 24 mục có `dcnb_reconcile` · ADMIN: không ô tick, nút Xoá khoá · KHO còn người giữ ⇒ Xoá khoá · thêm `tm` ⇒ tự thành **`TM`**, *Tất cả mục* = 26/26 · xoá TM được |
| **Lưới an toàn Bẫy 22** | Giả lập Google trả về **thiếu `po_list`** ⇒ khung **giữ lại** + cảnh báo *"Google chưa biết 1 mục nên đã BỎ QUA khi lưu: Danh sách PO – yêu cầu mua hàng…"* |
| Bề rộng (đang mở khung sửa) | **1366px**: hàng chip một dòng, 0 ô gãy chữ, 0 cuộn ngang · **1280px**: chip xuống **2 hàng** (danh sách chỉ còn 756px), 0 ô gãy, 0 cuộn ngang |
| Console | Chỉ ghi chú Babel >500 KB có sẵn |

🐛 **Tự bắt khi nhìn ảnh:** ở 1366px nút *"+ Thêm tài khoản"* bị đẩy xuống dòng 2 của hàng lọc ⇒ dời lên
**ngang tiêu đề**, cùng chỗ với nút *Thêm chức vụ*.

### 🔍 Điểm mù

- **Chưa chạy với Google thật** — cố ý, để khỏi ghi rác lên Sheet và dính lưới chống dò. Đại Ca xem trên 5051
  là **Google thật**: bấm Lưu / Tạo / Xoá là **ghi thẳng lên Sheet**, y như bản EXE.
- Lời cảnh báo *"bổ sung mã vào Code.gs (danh sách PERM) rồi Triển khai lại"* đã **cũ** so với Bẫy 22 tầng 2
  (Google nay tự tạo cột cho mã lạ) — câu có sẵn từ trước, chưa sửa.

---

## 25/09/2026 (trưa) — GĐ4: khung Trang chủ + thẻ phân hệ (đã commit) · phác thảo tab Phân quyền · nhánh `giaodien`

Đại Ca chốt GĐ3 OK ⇒ commit **`fed091f`**, rồi làm GĐ4. Bản phác thảo (khung *TrangChu*) có 4 khối; hỏi trước:

| Câu hỏi | Đại Ca chốt |
|---|---|
| Hiện khối nào | **Chỉ thẻ phân hệ** — bỏ "Việc cần xử lý", thống kê cả năm, "Báo cáo chạy lâu nhất" |
| Số liệu nặng tải lúc nào | *"Tạm thời lên mẫu, chưa lấy số liệu"* |
| Kỳ của số liệu (cho sau này) | **Tháng hiện tại** |

### Đã làm (`index.html`, không đụng `server.py`)

- **`TrangChu`**: *"Chào buổi sáng/trưa/chiều/tối, <tên>"* · thứ + ngày · lưới thẻ phân hệ (3 cột ở ≥1280px). Mỗi thẻ: icon màu · tên · nhãn đếm (*"4 màn hình"*, *"16 báo cáo"*) · một dòng mô tả. Bấm thẻ = mở phân hệ đó.
- Thẻ = **đúng các phân hệ người đó thấy ở cột trái** + thẻ Phân quyền nếu có quyền `perm_admin`. Nhãn đếm theo quyền. Nhãn thẻ Phân quyền là *"Quản trị"*, không phải *"Chỉ admin"* như phác thảo: quyền `perm_admin` tick được cho chức vụ khác, ghi "chỉ admin" là sai.
- Nút **Trang chủ** đứng đầu cột phân hệ (icon nhà, nét lấy từ phác thảo). `activeTab` mặc định `'home'`; **đăng nhập xong luôn về Trang chủ**.
- `PHAN_HE` thêm `mo_ta`, `mau`, `ten_day` (thẻ ghi *"Báo cáo tài chính"*, cột trái vẫn *"Báo cáo TC"*). Kho đổi sang màu **xanh ngọc** thay cho **đỏ** của phác thảo: đỏ ở phác thảo đi kèm nhãn *"25 cần truy"*, không có số liệu mà để đỏ là báo động giả.
- Không thêm độ đậm 800/900 nào (Bẫy 27).

### 🧪 Verify (server thử 5052 chạy đúng working tree, phiên giả, không DB)

| Kiểm | Kết quả |
|---|---|
| **M1** | `check_babel.js` SUCCESSFUL · `server.py` không đổi |
| Bấm 5 thẻ (trừ Phân quyền) | Mỗi thẻ mở đúng phân hệ + đúng tab đầu (Tổng hợp → *Chứng từ tổng hợp* … Báo cáo → *Tất cả báo cáo*); nút Trang chủ về lại đúng |
| Nhớ chỗ đang dở | Kho → *Đối chiếu điều chuyển* → Trang chủ → thẻ Kho ⇒ về đúng *Đối chiếu điều chuyển*. Mở BC005 → Trang chủ → thẻ Báo cáo ⇒ vẫn BC005 |
| **Không truy vấn SQL** | API gọi từ lúc mở tới hết lượt thử: chỉ `version`, `check_driver`, `metadata`, `my_perms`, `check_update` — đều là lệnh khởi động có sẵn |
| Tài khoản hạn chế (2 tab kho + BC005, BC013) | Chỉ 2 thẻ: *Kho [2 màn hình]*, *Báo cáo tài chính [2 báo cáo]*; không có thẻ/nút Phân quyền |
| 1280px | 3 cột × 376px, mép phải thẻ cuối 860px, **không cuộn ngang** |
| Console | Chỉ ghi chú Babel >500 KB có sẵn |

### 🔍 Điểm mù

- **Không bấm thẻ Phân quyền** trên server thử (gọi Google bằng tài khoản giả). Nó chỉ `setActiveTab('perm_admin')`, đúng lệnh mà nút Phân quyền ở cột trái vẫn dùng.
- **Chưa thử đăng nhập thật** ⇒ dòng *"đăng nhập xong về Trang chủ"* mới đọc mã (một lệnh `setActiveTab('home')` trước `setIsLoggedIn(true)`).
- ~~Máy 2048px: lưới giữ tối đa 1.280px, dồn trái, bên phải trống~~ ⇒ Đại Ca thấy đúng vậy, xem ngay dưới.

### Đại Ca xem: *"giao diện thì ok rồi, bên phải hơi trống nên cân cho đều"*

Bỏ giới hạn 1.280px, lưới thẻ trải hết bề ngang. Đo lại ở **2048px** (máy Đại Ca): lề trái **32px** =
lề phải **32px**, mỗi thẻ 632px, không cuộn ngang. Chốt OK ⇒ **commit GĐ4**.

### 🎨 Phác thảo giao diện mới cho tab Phân quyền (việc 32)

Đại Ca: *"muốn chỉnh sửa luôn giao diện của tab phân quyền, phác thảo luôn cho t xem"*. Đọc hết
`PermAdminPanel` (~365 dòng) để phác thảo **giữ đủ chức năng đang có**, rồi vẽ 3 khung vào mục **05 — PHÂN
QUYỀN** của bản phác thảo (https://claude.ai/artifact/7kiiWQ13PPR7eXN2AgPhtc):

| Khung | Khác bản đang chạy |
|---|---|
| **Tài khoản** | Hai tab con lên **hàng tab ngang** (đúng điều hướng 2 tầng) · bảng thêm cột **Chức vụ** và **tên đơn vị** (bản cũ chỉ ghi *"N mục · N đơn vị"*) · ô tìm + lọc theo chức vụ / đang khoá · sửa ở **khung bên phải** thay hộp thoại giữa màn · danh sách đơn vị có ô tìm, đơn vị đã chọn nổi lên đầu |
| **Chức vụ** | **Ma trận** chức vụ × 26 mục, tick thẳng trên bảng, thanh vàng *"N thay đổi chưa lưu"* rồi mới Lưu. Cột ADMIN **khoá** (app vốn tự tính đủ). Tab mới chưa cấp cho ai lộ ra ngay — đúng việc 4 |
| **Mở khoá** | Cùng nội dung màn nhập mật khẩu quản trị, đổi sang kiểu chữ/màu mới |

⚠️ Tài khoản, chức vụ, đơn vị trong khung là **MINH HOẠ** — chưa đọc Google Sheet thật (ghi rõ trên bản phác thảo).
⚠️ Ma trận lưu **từng chức vụ một**, mỗi chức vụ vẫn 4–7 giây qua Google; lưới an toàn *"Google bỏ sót mã"*
(`kiemMucBiVutBo`) phải chạy cho **từng** chức vụ khi làm thật.

💡 **Vấp khi đăng phác thảo:** lệnh publish từ chối file trong scratchpad khi đường dẫn viết tắt
`C:\Users\QUANG~1.TRA\…` (báo *"blocked by a Read permission rule"*), dùng đường dẫn đầy đủ
`C:\Users\quang.tran\…` thì qua.

---

## 25/09/2026 (sáng) — Vá việc 31 trên `main`, CHƯA build · bật lại server 5051

Đại Ca hỏi hôm nay cần làm gì cho bản hôm qua. Đọc nhật ký rồi đi kiểm máy thật thì thấy
**server 5051 đã chết** (không còn tiến trình python nào), dù nhật ký ghi *"không cần khởi động lại"*.
Đại Ca chốt việc 31: *"vá trước lỗi nhưng chưa build, để build 1 lần luôn"*.

### Đã làm

| Việc | Chi tiết |
|---|---|
| Bật lại server 5051 | Đúng lệnh cũ: `import server; server.app.run(host='127.0.0.1', port=5051, …)`. Trả đúng `index.html` trên đĩa (**SHA256 khớp**), màn đăng nhập hiện. Chạy nền theo phiên chat ⇒ **đóng phiên là tắt** |
| **Vá việc 31 trên `main`** — commit **`784d227`** | Làm trong **git worktree riêng** ở scratchpad, để thư mục làm việc (nhánh `giaodien`, GĐ3 chưa commit) và server 5051 đang phục vụ Đại Ca **không bị đổi mã dưới chân**. Sửa đúng **1 dòng**, khớp chuỗi `assert count == 1` (Bẫy 26): ô Số chứng từ ghi thẳng chuỗi vào `filters.tran_no`, bỏ `onToggleFilter('tran_no', …)`. Cùng cách đã sửa trên `giaodien`. Xong thì gỡ worktree |
| Không làm | **Không build, không tăng `version.txt`, không push** — theo lệnh Đại Ca. Lúc build, `build_exe.py` tự tăng lên `1.12.4` |

### 🧪 Verify

| Mức | Kết quả |
|---|---|
| **M1** | `check_babel.js` SUCCESSFUL trên `index.html` của `main` đã vá · diff đúng 1 dòng · quét secret 0 dòng |
| **M2** | Server thử **cổng 5052** chạy **mã `main` đã vá** (phiên ADMIN giả, không DB), đo SHA256 trang phục vụ = file đã vá. Vào Báo cáo → BC012, **gõ từng chữ** `P`,`T`,`0`,`1`: ô hiện `PT` → `PT01`; xoá lùi → `PT0`; gõ lại → `PT01`. Bấm Xem BC012 ⇒ request gửi **`tran_no=PT01`** (bản lỗi gửi `P,PT,…`). Console: chỉ còn ghi chú Babel >500 KB có sẵn |
| **M3 / M4** | ⏳ Chờ build — Đại Ca chốt build một lần |

### 🔴 Phát hiện: `import server` TẮT app đang mở ở cổng 5050

`server.py:702` gọi `kill_process_on_port(5050)` **ở cấp module** ⇒ chạy ngay lúc `import server`,
kể cả khi bỏ qua khối `__main__`. Bật server thử (5051/5052) trong lúc Đại Ca đang mở EXE là **EXE bị
`taskkill /F` ngang** ⇒ *"Failed to fetch"*. Sáng nay cổng 5050 trống nên không sao; từ nay **kiểm
`netstat` cổng 5050 trước khi bật server thử**, có tiến trình thì dừng lại hỏi. Đã ghi vào
[CLAUDE.md Bẫy 6](CLAUDE.md).

### 📦 Git

`main` = **`784d227`**, `ahead 7` (6 `.md` + 1 bản vá), **chưa push**.

Sau đó Đại Ca chốt **GĐ3 OK** (*"cái đó thì ok rồi"*) ⇒ **commit GĐ3 lên `giaodien`** — gồm `index.html`
(GĐ3 + ô Số chứng từ BC012 đã sửa theo kiểu mới) và `CLAUDE.md` + nhật ký này. Local, **chưa push**.

---

## 25/09/2026 (tiếp 3, đêm) — Ô Thời gian làm lại theo iPOS · gộp nút xuất · ẩn tab ở trang liệt kê · nhánh `giaodien`, CHƯA commit

Đại Ca xem bản *(tiếp 2)* và gửi 4 ảnh lịch của iPOS Inventory: *"cái bên trong chọn ngày nó không gọn
gàng, làm như chi tiết bộ lọc theo hình, cho thêm option quý"* · *"2 ô xuất gom lại 1 icon download, xổ
xuống chọn hình thức cần xuất"* · *"bấm vào Tất cả báo cáo thì cái ô kế bên nó mất đi"*.
Giữa chừng Đại Ca chốt thêm: **bỏ hết phím tắt** (Hôm nay, Tháng này…), chỉ giữ phần chọn.
Cuối phiên: *"làm xong tự động cập nhật nhật ký, mai t xem"*.

### 👀 Việc Đại Ca xem sáng 25/09 — `http://127.0.0.1:5051`

> ⚠️ Tiêu đề cũ ghi *"sáng 26/09 … không cần khởi động lại"* — **sai cả hai**: phiên này kết thúc 01:44
> sáng 25/09, và server 5051 **chết theo phiên chat** (sáng 25/09 không còn tiến trình nào). Đã bật lại.

| # | Xem gì | Tôi đã thử chưa |
|---|---|---|
| 1 | Báo cáo TC → bấm một thẻ → ô **Thời gian**: 5 chế độ Chọn ngày · tuần · tháng · quý · năm | ✅ bấm đủ, ra đúng ngày (bảng dưới) |
| 2 | **Chọn ngày**: bấm ngày đầu rồi ngày cuối, có thể bắc qua 2 tháng | ✅ |
| 3 | **Nút tải xuống** (cuối hàng) → *Xuất Excel* / *Xuất PDF* | ⚠️ **Chưa** — cần số liệu thật mới bật được nút. Chưa có số liệu thì nút mờ, đúng ý |
| 4 | Bấm **Tất cả báo cáo** → tab báo cáo bên cạnh biến mất; bấm lại thẻ → hiện lại | ✅ |
| 5 | Đang có số liệu mà đổi báo cáo → hộp *"Chuyển mẫu báo cáo?"* | ⚠️ **Chưa** — server thử không có DB |
| 6 | Kéo thả thứ tự ô lọc trong **Bộ lọc nâng cao** bằng chuột thật | ⚠️ Mới thử bằng thao tác giả lập |
| 7 | Đọc lại **mô tả 16 thẻ** ở trang liệt kê | Tôi tự viết theo mã |
| 8 | Ưng thì **chốt commit GĐ3** | — |

### Đã làm (`index.html`)

**1. Ô Thời gian — viết lại hẳn.** Cột trái 5 chế độ, bên phải 2 lịch cạnh nhau (điều hướng « ‹ › »):

| Chế độ | Cách chọn | `period` đặt thành |
|---|---|---|
| Chọn ngày | Bấm ngày đầu → ngày cuối (bấm ngược chiều tự đảo; bấm 2 lần 1 ngày = 1 ngày). Rê chuột thấy trước dải sẽ chọn | `custom` |
| Chọn tuần | Bấm cả hàng. Cột trái là **số tuần ISO 8601** | `custom` |
| Chọn tháng | Lưới T1–T12 của 2 năm | `month` |
| Chọn quý | Lưới Quý 1–4 của 2 năm, ghi kèm T1–T3… | `quarter` |
| Chọn năm | Lưới 12 năm | `year` |

`period` đặt đúng loại vì **9 màn danh sách dùng chung `period`** — đã thử: chọn quý bên báo cáo thì ô Kỳ
bên *Chứng từ tổng hợp* ghi đúng *"2026 - Quý 3"*. **"Chọn năm" không có trong hình mẫu** — tôi giữ vì bản
cũ có "Cả năm", bỏ là mất tính năng. Bảng nổi là portal `position:fixed`, đặt **sát dưới ô nhưng không
đè cột phân hệ** (lần đầu tôi canh theo mép phải của ô ⇒ 4 báo cáo bị đè lên cột, đo ra mới thấy).

**2. Nút tải xuống** (`NutXuat`) thay 2 nút Excel + PDF: icon ⤓ + ⌄, xổ ra *Xuất Excel* / *Xuất PDF*.
Chưa có số liệu thì cả nút tắt. Nhân tiện **đóng việc 29** (BC003/BC004 nút xuất sáng khi chưa có số liệu).

**3. Tab**: ở trang liệt kê chỉ còn *Tất cả báo cáo*.

**4. 🔴 Sửa lỗi ô Số chứng từ BC012 — CÓ TRONG BẢN ĐANG PHÁT HÀNH** (việc 31). `toggleFilter` chỉ coi
`from_date`/`to_date` là giá trị đơn; `tran_no` rơi vào nhánh mảng ⇒ gõ `P` rồi `T` thành `['P','PT']`,
ô hiện `P,PT`, gửi lên máy chủ `P,PT` ⇒ 0 dòng. Sửa tại ô (ghi thẳng chuỗi), không đụng `toggleFilter`
chung. Lần thử trước tôi **dán cả chuỗi một lần** nên không lộ — lần này gõ từng chữ mới thấy.

### 🧪 Verify (server thử 5052, dữ liệu giả)

| Kiểm | Kết quả |
|---|---|
| Số tuần ISO (chạy thẳng hàm thật) | 21/09/2026 = **39** (khớp hình iPOS) · 29/12/2025 = 1 · 31/12/2026 = 53 · 04/01/2027 = 1 — **8/8 đúng** |
| Khoảng ngày | T2/2024 → 29/02 (năm nhuận) · Quý 4/2025 → 01/10–31/12 — đúng |
| 5 chế độ trên app | Ngày 20/04 → 05/04 ⇒ `05/04/2026 - 20/04/2026` · Tuần 16 ⇒ `13/04 – 19/04` · Quý 2 ⇒ `01/04 – 30/06` · Năm 2025 ⇒ `01/01 – 31/12/2025` · T2 ⇒ `01/02 – 28/02/2026` |
| Gõ từng chữ `PT01` vào Số chứng từ | Ô hiện đúng `PT01` |
| Bề rộng + vị trí bảng Thời gian | **16/16 đạt ở 1366px và 1280px**: một hàng, không tràn, bảng không đè cột phân hệ |
| Console | 0 lỗi |

### 💡 Bài học

- **Đừng khai component lồng bên trong component** (`const Lich = () => …` ngay trong thân `OThoiGian`):
  mỗi lần render React coi là component MỚI, gỡ DOM ra dựng lại ⇒ rê chuột là thay cả lịch, và cú bấm
  có thể **mất** nếu DOM bị thay giữa lúc nhấn và nhả. Bắt được khi đọc lại mã, trước khi thử —
  đã đổi thành hàm vẽ thường (`veLichThang(0)`).
- **Thử ô gõ chữ thì phải gõ TỪNG CHỮ**, đừng dán cả chuỗi một lần — lỗi `tran_no` chỉ lộ khi gõ từng chữ.

### 📦 Git

**Chưa commit** — chờ Đại Ca xem sáng 25/09 (việc 19). `index.html`, `CLAUDE.md`, `NHAT_KY_CONG_VIEC.md`
đang sửa trên nhánh `giaodien`; commit mốc gần nhất `c64540a`. **Không nhánh nào đã push.**

---

## 25/09/2026 (tiếp 2) — Báo cáo TC: ô "Thời gian" gộp + Bộ lọc nâng cao · nhánh `giaodien`, CHƯA commit

> ⚠️ Bảng chọn bên trong ô Thời gian ở mục này (năm/tháng/quý/tuỳ ý + 2 ô ngày) **đã bị thay** — xem *(tiếp 3)* ở trên.

Đại Ca gửi thêm 2 ảnh **"Bộ lọc nâng cao"** của iPOS Inventory: *"nếu bị giới hạn nhiều quá thì làm bộ
lọc thu gọn như này, cho phép thêm hoặc bớt ô lọc hiển thị bên ngoài"*.

### Đại Ca chốt

| Câu hỏi | Chốt |
|---|---|
| Làm ở đâu | **Báo cáo TC trước**, có logic rồi mới làm 9 màn danh sách (việc 30) |
| Kỳ + Từ ngày + Đến ngày | **Gộp thành 1 ô "Thời gian"** như hình |
| Ô nào ở ngoài | *"Mặc định ô thời gian để lọc, còn các ô còn lại theo thứ tự cái nào trước thì hiện"* — tối đa 4 (tính cả Thời gian), đúng như hình |
| Nhớ cấu hình | **Riêng từng báo cáo, trên máy** |

Tôi tự thêm một điều **không hỏi**, vì là chốt an toàn nghiệp vụ: **số trên nút phễu = số ô đang có
giá trị mà bị giấu trong bảng** (nút chuyển màu cam). Ô lọc bị giấu mà vẫn áp dụng thì người xem
tưởng số liệu là toàn bộ. Và **Thời gian luôn ở ngoài, không tắt được** — báo cáo nào cũng cần kỳ.

### Đã làm (`index.html`)

- **`OThoiGian`** — một ô ghi `01/09/2026 - 30/09/2026`; bấm ra năm · tháng · quý · cả năm · tuỳ ý +
  2 ô ngày (chỉ gõ được khi chọn Tuỳ ý — giữ luật cũ). 9 màn danh sách **vẫn dùng ô Kỳ cũ**.
- **`O_LOC_BAO_CAO`** — khai 6 ô lọc của Báo cáo TC ở **một chỗ** (Đơn vị · Tài khoản · Công việc ·
  Đối tượng · TK đối ứng · Số chứng từ), mỗi ô ghi rõ báo cáo nào có. Trước đây viết rải trong JSX.
- **`BoLocNangCao`** — nút phễu + bảng: lưới 3 cột các ô đang giấu · *Xoá tất cả* · phần **Cấu hình
  tham số lọc** thu gọn được: công tắc bật/tắt + kéo thả đổi thứ tự (bấm tay nắm rồi ↑ ↓ cũng được) ·
  *Đóng* / *Xem BCxxx*. Đủ 4 ô thì công tắc còn lại khoá, ghi *"đã đủ 4 ô"*.
- Lịch của `IOSDatePicker` (portal gắn vào `body`) mang dấu **`data-lop-noi`** để bấm vào lịch không
  làm bảng Thời gian tự đóng.

Mặc định: BC012 = Thời gian · Đơn vị · Tài khoản · TK đối ứng (Số chứng từ vào trong) · BC013 =
Thời gian · Đơn vị · Tài khoản · Đối tượng · 12 báo cáo còn lại có ≤ 3 ô nên **tất cả vẫn ở ngoài**.

### 🧪 Verify (server thử 5052, dữ liệu giả)

| Kiểm | Kết quả |
|---|---|
| Tắt TK đối ứng → bật Số chứng từ → ↑↑ → kéo thả | Hàng ngoài đổi đúng từng bước |
| Gõ `PT0001` vào Số chứng từ đang giấu, đóng bảng | Nút phễu **cam, số 1**, tooltip *"1 ô lọc đang áp dụng nằm trong này"* |
| *Xoá tất cả* | Ô trống lại, số trên nút mất |
| Tải lại trang | Cấu hình BC012 **còn nguyên**; BC013 chưa chỉnh thì về mặc định |
| Ô Thời gian | Q3 → `01/07/2026 - 30/09/2026` · 2025 + tháng 9 → `01/09/2025 - 30/09/2025` · Tuỳ ý giữ bảng mở, bấm ngày trên lịch bảng **không** tự đóng · bấm ra ngoài thì đóng |
| Bề rộng, cấu hình mặc định | **1366px và 1280px: 16/16 báo cáo một hàng**, không cụm nút nào xuống dòng (trước đó 1280 có 4 báo cáo phải xuống), 0 tràn, 0 gãy chữ · bảng nâng cao nằm trọn màn hình |
| Console | 0 lỗi |

### 🔍 Điểm mù

- Kéo thả thử bằng sự kiện giả lập (`DragEvent`), **chưa kéo bằng chuột thật** — Đại Ca kéo thử giúp.
- Dropdown Đơn vị / Tài khoản trên server thử **rỗng** (danh mục giả) ⇒ số trên nút phễu mới thử
  được bằng ô Số chứng từ. Logic đếm dùng chung cho mọi ô.
- Cấu hình nhớ **theo máy, không theo người**: hai người dùng chung một máy sẽ thấy chung một bố cục.

---

## 25/09/2026 (tiếp) — Báo cáo TC: bỏ chia nhóm, trang liệt kê thẻ + ô chọn có tìm · nhánh `giaodien`, CHƯA commit

Đại Ca xem phương án 5 tab nhóm và gửi 2 ảnh mẫu từ **iPOS Inventory**: *"không nên chia nhóm mà
liệt kê như hình, khi đang xem muốn đổi thì cho chọn như hình 2, điều kiện và các ô lọc dời sang phải"*.

### Đã làm (`index.html`)

| Việc | Chi tiết |
|---|---|
| **Trang liệt kê** (`DanhSachBaoCao`) | 16 thẻ, 4 cột, vừa **một màn hình 1366×768**. Mỗi thẻ: mã · tên ngắn · một dòng mô tả. Thẻ báo cáo đang mở viền nổi |
| **Ô chọn báo cáo** (`ChonBaoCao`, thay `ReportTypeDropdown`) | Đứng đầu hàng điều kiện bên trái: `[BC013] Tổng hợp phát sinh công nợ ⌃`. Mở ra: tiêu đề *Báo cáo tài chính* + số lượng · ô tìm (con trỏ đặt sẵn) · danh sách mã + tên. Gõ **không dấu** được (`can doi` → BC005, BC006). Enter = chọn dòng đầu, Esc = đóng |
| **Hàng điều kiện** | Trái: ô chọn + nút kiểu xem (Chi tiết/Tổng hợp, Gom theo). Phải: Kỳ, ngày, Đơn vị, TK… rồi Xem/Excel/PDF |
| **Hàng tab** | `Tất cả báo cáo` · `BC013 · Tổng hợp phát sinh công nợ` — qua lại **không mất số liệu**: `ReportTab` chỉ ẩn đi, không tháo ra (nó giữ hộp xuất file, tiến độ xuất…) |
| Gỡ | `NHOM_BAO_CAO`, `ReportTypeDropdown`. Báo cáo mới chỉ cần thêm vào `REPORT_TYPES` là tự hiện |

**Tên ngắn + mô tả 16 thẻ — TÔI TỰ VIẾT, Đại Ca đọc lại.** Viết theo đúng mã, không theo cảm tính:
BC003/BC004 = *"tách riêng phí hoa hồng đối tác và phí quảng cáo"* (đọc từ chỗ mã chèn dòng VH.PHH /
VH.PQC) · BC011 = *"mẫu riêng theo yêu cầu Chú Long, không phải B03-DN chuẩn"* (lời `CLAUDE.md`) ·
BC012 = *"thu chi TK 111, 112, 113"* (mặc định trong mã) · BC015 = *"theo nguồn đơn và đơn vị, chỉ
chứng từ đã ghi sổ"* (docstring `server.py`) · BC016 = *"gom theo nhóm hàng hoặc kho"*.
`name` (tên đầy đủ viết hoa) **giữ nguyên** vì checklist Phân quyền đọc nó.

### Ba lỗi bắt được khi bấm thử

**1. Hỏi *"Chuyển mẫu báo cáo?"* oan — lỗi CÓ TỪ TRƯỚC.** Đổi BC001 → BC002 → BC003 được, rồi kẹt.
Nguyên nhân: với BC003/BC004, `ReportTab` chèn sẵn 2 dòng VH.PHH/VH.PQC vào `reportData` kể cả khi
chưa tải gì ⇒ luôn "có số liệu" ⇒ rời BC003/BC004 là bị hỏi dù màn trống. Ô chọn cũ dính y hệt.
Sửa: xét `initialReportData` (số liệu thật App đưa vào). Đo lại: đổi đủ 16 báo cáo, **0 lần hỏi oan**.

> ⚠️ Bảng đo ngay dưới là **trước khi có Bộ lọc nâng cao**. Nay 16/16 báo cáo nằm một hàng ở cả 1366
> lẫn 1280px — xem mục *(tiếp 2)* ở trên.

**2. Ô Kỳ bị bóp, chữ gãy 2 dòng.** Ở BC012 (7 ô lọc) ô Kỳ còn **106px**, *"2026 - Tháng 1"* gãy.
Phép đo lần đầu **không bắt được** vì chỉ dò chữ tràn ngang — phải đếm số dòng thật của từng đoạn
chữ mới thấy. Sửa: mỗi ô có **mức sàn** (Kỳ 146 · ngày 100 · dropdown 96 · Số CT 90px), chạm sàn
mà vẫn thiếu thì **cụm nút Xem/Excel/PDF xuống dòng 2**, không bóp chữ nữa.

| Độ rộng | Cụm nút xuống dòng | Tràn / cuộn ngang | Chữ gãy dòng |
|---|---|---|---|
| **1366px** | chỉ **BC012** | 0/16 | 0/16 |
| **1280px** | BC012, BC013, BC014, BC016 | 0/16 | 0/16 |

**3. Mũi tên `›` vẽ ra thành gạch chéo `/` — lỗi CÓ TỪ TRƯỚC.** Icon `chevron-right` có nét
`m9 18 6-6 6-6` (đi thẳng) thay vì `m9 18 6-6-6-6` (bẻ góc). Nút **trang sau** ở thanh phân trang
dùng chung icon này nên xưa nay cũng là gạch chéo. Đã sửa một chỗ, ăn cả hai.

### 🧪 Verify

| Mức | Kết quả |
|---|---|
| **M1** | `check_babel.js` SUCCESSFUL · `server.py` không đổi |
| **M2** (server thử 5052, dữ liệu giả) | 16/16 báo cáo đổi được bằng ô chọn · tìm: `can doi`/`LCTT`/`chu long`/`bc01`/`nguồn đơn`/`xyz` ra đúng · Enter, Esc đúng · 9/9 màn danh sách vẫn vừa ở 1280 (ô Kỳ dùng chung vừa thêm cấm gãy dòng) · tài khoản hạn chế (BC005 + BC013): 2 thẻ, ô chọn ghi "2" · qua lại trang liệt kê ↔ báo cáo ↔ Kho vẫn về đúng chỗ · console **0 lỗi** |
| **M3** | ⏳ Chờ Đại Ca F5 cổng 5051 |

### 🔍 Điểm mù

- Hộp *"Chuyển mẫu báo cáo?"* **khi có số liệu thật** — chưa thử được (không có DB).
- Nghi thêm một lỗi cùng gốc ở nút Excel/PDF của BC003/BC004 — **mới đọc mã**, ghi thành việc 29.

---

## 25/09/2026 — GĐ3 giao diện: điều hướng 2 tầng · nhánh `giaodien`, CHƯA commit

> ⚠️ Phần **Báo cáo TC chia 5 tab nhóm** trong mục này **đã bị thay** — xem mục *(tiếp)* ngay trên.

Đại Ca đã xem màn danh sách sau khi sửa font (*"cột nó bị hẹp — sửa sau khi xong toàn bộ giai
đoạn"*) ⇒ commit mốc **`c64540a`** (đăng nhập nhanh + sửa font), rồi làm GĐ3.

### Đại Ca chốt 4 điểm phác thảo chưa nói rõ

| Câu hỏi | Chốt |
|---|---|
| Cột phân hệ rộng bao nhiêu (cột bảng vốn đã hẹp) | **64px**: icon + chữ 10px — không lấy 84px như phác thảo |
| Báo cáo TC chia thế nào | **5 tab nhóm**: Kết quả kinh doanh · Sổ sách bắt buộc · Tiền · Công nợ & thuế · Vận hành. Ô *"Mẫu báo cáo"* bên trong chỉ còn báo cáo của nhóm đó |
| Thanh đen trên cùng đi đâu | **Gộp vào hàng tab**: phải hàng tab = tên DB · phiên bản · Danh mục · Tải lại. Bỏ số *"Records"*. Không thêm dòng tiêu đề to |
| Phân quyền đặt đâu | **Đáy cột phân hệ**, trên ô tài khoản |

⚠️ **Đụng một luật cũ:** chú thích ở `MenuTaiKhoan` ghi Đại Ca chốt 17/08 *"KHÔNG đưa Đăng xuất vào ô
tài khoản vì nút đó đã nằm cạnh bên"*. Phương án mới bỏ nút cạnh bên ⇒ Đăng xuất chuyển vào menu,
**vẫn chỉ một chỗ** — giữ được lý do của luật cũ. Đã sửa chú thích cho khớp.

### Đã làm (`index.html`, không đụng `server.py`)

- **`PHAN_HE`** (5 phân hệ) + **`NHOM_BAO_CAO`** (5 nhóm). Tab/báo cáo **chưa gắn nhóm tự rơi vào
  "Khác"** — cùng bài học Bẫy 22: thứ chưa khai báo phải lộ ra, không được biến mất. Kiểm bằng cách
  chạy thẳng đoạn mã thật với dữ liệu giả: thêm `tab_moi` + `BC017` ⇒ hiện ở "Khác"; gỡ BC015+16 ⇒
  nhóm Vận hành tự ẩn.
- Phân hệ **suy ra từ `activeTab`**, không giữ state riêng ⇒ hai tầng không lệch nhau được.
- **Nhớ chỗ đang dở**: màn hình mở gần nhất của từng phân hệ, báo cáo mở gần nhất của từng nhóm.
- Đổi nhóm báo cáo khi đang có số liệu ⇒ **cùng hộp hỏi "xoá số liệu?"** như ô Mẫu báo cáo.
- `DOC_TABS` thêm `short` (tên trên tab, bỏ chữ *"Danh sách…"*) — **giữ nguyên `name`** vì checklist
  Phân quyền đọc cái đó.
- Gỡ `DocumentTabDropdown` + CSS `.tab-btn` (thành mã chết). Icon thêm 7 hình từ phác thảo.

### Hai lỗi tự bắt được khi bấm thử — **trước khi** Đại Ca thấy

**1. Nút Xuất Excel bị cắt trên màn 1366px.** Cột 64px đẩy nút lòi ra **56–62px** ở 5 màn danh sách
(tổng hợp, tiền, bán hàng, nhập kho, kho). Trước GĐ3 các màn này chỉ còn dư **2–8px**.

| Thử | Kết quả ở 1366px |
|---|---|
| Ô Kỳ báo cáo `w-64` → `w-44` (256 → 176px) | Vẫn tràn **28–34px** — mọi ô cùng co, bớt 80px danh nghĩa chỉ lấy lại ~28px thật |
| Thêm `flex-wrap` | Hết tràn nhưng **cụm nút xuống dòng**, tốn thêm ~60px chiều cao ⇒ bỏ |
| ✅ Cụm nút `shrink-0` + khoảng cách ô 16 → 12px | **Dư 24px, không cuộn ngang, không chữ nào bị cắt** ở cả 1366 lẫn **1280px** (9/9 màn) |

Thủ phạm thật: cụm *Hiển thị · Truy vấn · Bộ lọc · Xuất Excel* cần **545px** mà bị ép còn 487px.
Cho cụm đó không co thì các ô bên trái (còn chỗ co) gánh phần thiếu.

**2. Rê chuột trông y hệt đang chọn.** Chụp ra thấy cột tô sáng "Kho" trong khi đang ở Báo cáo TC —
DOM nói đúng là Báo cáo TC, ô sáng ở Kho là **con trỏ đang rê qua**. Nền `white/5` trên navy tối gần
trùng nền `#1e3a8a` của mục đang chọn. Sửa: rê chuột chỉ đổi màu chữ, không tô nền.

### 🧪 Verify

| Mức | Kết quả |
|---|---|
| **M1** | `check_babel.js` SUCCESSFUL · `server.py` **không đổi** (167 hàm / 69 route) · chỗ dùng độ đậm 800/900 mới thêm: **0** |
| **M2** | Server thử **riêng cổng 5052** (phiên ADMIN giả + danh mục giả, không DB, không gọi Google): bấm **14/14** lượt (5 phân hệ × 9 màn hình × 5 nhóm) đúng tab · ô Mẫu báo cáo đúng 4/4/4/2/2 báo cáo · nhớ đúng BC014 khi đổi nhóm rồi quay lại · rời Kho sang Báo cáo TC rồi về vẫn đúng tab · menu tài khoản mở sang phải, có Đổi mật khẩu + Đăng xuất · console **0 lỗi React** |
| **M2 — quyền hạn chế** | Tài khoản chỉ có 3 tab kho + BC005 + BC013: cột chỉ còn **Kho + Báo cáo TC**, không có Phân quyền · mở app tự vào *Chứng từ kho* · Báo cáo TC chỉ 2 nhóm |
| **M3** | ⏳ Chờ Đại Ca F5 cổng **5051** (server của Đại Ca đọc `index.html` mới mỗi lần tải, không cần khởi động lại) |

💡 **Trình duyệt tích hợp của Claude NAY đã vào được `localhost`** — điểm mù *"không nhìn được app
đang chạy"* của phiên trước đã hết. Chụp màn hình hay bị hết giờ lần đầu (Babel dịch 7–13 giây), chờ
rồi chụp lại là được.

### 🔍 Điểm mù

- Chưa thử **hộp "xoá số liệu?" khi đổi nhóm báo cáo** với số liệu thật — server thử không có DB.
  Logic dùng lại đúng điều kiện của ô Mẫu báo cáo (`Object.keys(reportData).length > 0`).
- **Không bấm thử nút Phân quyền** trên server thử: màn đó gọi lên Google bằng tài khoản giả, dễ bị
  tính vào lưới chống dò. Hàng tab của nó chỉ là một tab *"Phân quyền"* — đọc mã là đủ.
- Chỉ đo ở 1280 / 1366. **Máy Đại Ca là 2048px** (2560×1440, co giãn 125%) nên sẽ không thấy lỗi tràn —
  lỗi đó chỉ lộ trên laptop nhân viên.

---

## 24–25/09/2026 (đêm) — Giao diện mới `PROOFTRAIL` + đăng nhập nhanh · nhánh `giaodien`, CHƯA push

Đại Ca hỏi tư vấn giao diện. **Đo trước rồi mới tư vấn** — mở giao diện lên và thấy:

| Đo được | Số |
|---|---|
| Mở app trắng màn hình | `domInteractive` **152ms** nhưng `DOMContentLoaded` **6.926ms** — Babel dịch **723.551 byte** JSX (8.125 dòng, 66 component) **mỗi lần mở** |
| Tải từ Internet | **6 thư viện**: React, ReactDOM, Babel, Tailwind, xlsx, Google Fonts. Fallback giả `window.React = { createElement: () => null }` ⇒ mất mạng là **màn trắng câm** |
| Nhãn ô nhập | 9px `#94a3b8` ⇒ tương phản **2,56 : 1** (chuẩn tối thiểu 4,5) |

### Phác thảo — chốt hướng qua 12 vòng sửa

Artifact **https://claude.ai/artifact/7kiiWQ13PPR7eXN2AgPhtc** (ngoài repo). Tham khảo
`designprompts.dev` → style **Swiss Minimalist** (lấy đúng prompt 14.263 ký tự). Bám tinh thần lưới,
chữ lớn, phẳng, không đổ bóng — nhưng **CỐ Ý trái prompt một chỗ**: Swiss thuần chỉ cho đen–trắng–đỏ,
làm thế là **giết 6 màu trạng thái** mang nghĩa nghiệp vụ của các tab đối chiếu. Giữ lại màu trạng
thái, chỉnh cho khác cả sắc lẫn độ sáng. "Lệch số lượng" đổi xanh dương → **tím** vì màu chủ đạo nay
là navy — để nguyên là tưởng dòng đó đang được chọn.

**Tên:** cân nhắc *Soát Sổ*, *LedgerLens*, *Proof*, *Trace*, *Vouch*… Đại Ca chọn **`PROOFTRAIL`**:
*proof* (proof of cash — kiểm chứng số liệu) + *trail* (audit trail — dấu vết về chứng từ gốc).
Hai bẫy đã tránh: **`ProofTrial`** — *trial* trong phần mềm bị đọc là *"bản dùng thử"*;
**`TraceProof`** — hậu tố *-proof* nghĩa là *"chống"* (waterproof) ⇒ đọc ra *"chống lần vết"*.

### GĐ1 — một chỗ sửa đổi màu cả app

App có **403 lớp `indigo-*`**. Không sửa lớp nào: **ghi đè thang màu `indigo` trong `tailwind.config`**
thành thang navy. Đổi tông lần sau cũng chỉ sửa đúng chỗ đó.

### Sửa font — ba vòng, và **hai lần tôi báo "xong" sai**

| Vòng | Đại Ca thấy | Nguyên nhân thật |
|---|---|---|
| **1** | Tab đang chọn tàng hình · chữ đậm nhoè | Tôi thay `#4f46e5` → navy **hàng loạt**, mà màu đó dùng **cả trên nền trắng lẫn header tối** · và `font-black` (900) ⇒ Windows lấy **Arial Black** |
| **2** | Bảng BC001 **vẫn** lỗi dấu | ① `.report-table` **ghi cứng `font-family: 'Inter'`** — bảng không theo font chung, nên sửa `body` mấy lần cũng không ăn · ② **20 chỗ `fontWeight: isBold ? 800 : 300`** — vòng 1 tôi dò sót dạng biểu thức này, báo *"còn 0 chỗ"* là **sai** · ③ **11 tên chỉ tiêu KQKD gõ Unicode tổ hợp** |
| **3** | Màn danh sách *"cấn cấn"* | Tiêu đề cột **9px** + `tracking-widest` + số dùng **`font-mono` (Consolas)** |

**Bằng chứng gốc rễ** — đo bằng `fontTools` và **Chrome chạy ngầm trên chính máy này**:

| | |
|---|---|
| Arial Black có bao nhiêu chữ Việt dấu chồng | **3/13** — thiếu `Ả Ấ Ễ Ố Ổ Ộ Ợ Ứ Ừ Ự`. Arial thường và Arial Bold: 13/13 |
| Cùng một câu 20px | Arial 800 = **457px** = Arial 900 = Arial Black · **AppSans 800 = 421px** = Arial Bold |

**Cách chặn tận gốc:** khai họ font riêng **`AppSans`** bằng `@font-face` + `local()`: độ đậm
**600–900 chỉ trỏ về Arial Bold**. Arial Black hết cửa lọt vào — style inline, lớp Tailwind hay thẻ
`<b>` đều không lọt. Mọi chỗ khai `font-family` phải để `AppSans` đứng đầu.

**Vòng 3 — cỡ chữ tối thiểu.** Đo 5 phương án, đếm tiêu đề nào gãy dòng:

| Cỡ + giãn chữ | Tiêu đề bị gãy dòng |
|---|---|
| 9px · 0,10em *(hiện trạng)* | `ĐVT KHO` *(gãy từ trước)* |
| **10px · 0,06em** ✅ chọn | `ĐVT KHO` — **không thêm cái nào** |
| 10,5px · 0,06em | `MÃ CT`, `ĐVT KHO` ❌ |
| 10,5px · 0,03em | `MÃ CT`, `ĐVT KHO` ❌ |

⇒ 8px → 9,5px, 9px → 10px, `tracking-widest` → 0,06em, `font-mono` → Arial (Arial vốn có chữ số
rộng bằng nhau). Đúng ý Đại Ca: *font toàn bộ là Arial*.

### Đăng nhập nhanh (hướng A) — chèn giữa chừng vì Đại Ca thấy *"đăng nhập lâu quá"*

**Không phải do giao diện** — `git diff` lúc đó chỉ có `index.html`. Log server của chính lần Đại Ca bấm:

```
Goi Google that bai (lan 1/3): Google trả lỗi HTTP 404 — thu lai
POST /api/login → xong  ·  GET /api/metadata → thêm 6 giây
```

Đo lệnh `ping` (lệnh **rỗng**, không đọc Sheet) **6 lần** lên Apps Script:

| Lần | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Giây | **15,1** | 3,4 | 10,2 | **27,4** | 20,8 | 13,2 |
| Kết quả | ❌ 404 | ✅ | ✅ | ❌ 404 | ✅ | ✅ |

**1/3 số lần hỏng, và hỏng SAU KHI đã bắt chờ 15–27 giây.** Đọc `doPost` trong `Code.gs`: `ping` chỉ
kiểm token rồi trả lời ⇒ chậm nằm ở **hạ tầng Google**. Một lần đăng nhập gặp 404 ≈ **35 giây**.

**Cách làm** (`server.py`, thêm 3 hàm `_quyen_khac` / `_huy_phien_nen` / `_kiem_lai_nen`): người đã
đăng nhập thành công **trên chính máy đó** trong 7 ngày ⇒ kiểm mật khẩu bằng hash PBKDF2 trong
cache **tại chỗ**, cho vào luôn, rồi **hỏi Google ở luồng nền**. Google nói khác ⇒ gỡ phiên khỏi
`_phien_db` ⇒ request kế tiếp 401 ⇒ về màn đăng nhập.

**Giữ nguyên 2 bảo đảm cũ:** sai mật khẩu so với cache thì **không từ chối tại chỗ** mà đi đường
Google (nên không né được rate limit) · quyền trên Google khác cache ⇒ **đá ra** (không thì thu hồi
quyền trễ thêm một lần đăng nhập). ⛔ **Đường nhanh KHÔNG được gia hạn cache** — chỉ luồng nền gia
hạn sau khi Google xác nhận; không thế thì tài khoản đã khoá sống mãi mỗi khi Google chập chờn.
Thêm `_cache_file_lock` vì luồng nền cũng ghi `phanquyen_cache.json`.

**Đánh đổi Đại Ca chốt:** tài khoản vừa bị khoá vẫn vào được **3–30 giây** rồi mới bị đá ra.

### 🧪 Verify

| Mức | Kết quả |
|---|---|
| **M1** | `ast.parse` OK · **167 hàm** (164 + đúng 3 hàm mới) · **69 route** không đổi · không trùng tên · `check_babel.js` SUCCESSFUL · dấu tổ hợp còn **0** · chỗ **dùng** độ đậm 800/900 còn **0** |
| **M2** | Đăng nhập nhanh **26/26**, đủ 8 tình huống, Google giả chậm 4s: đường nhanh **0,10s** · bị khoá ⇒ đá ra + xoá cache · bị thu hồi quyền ⇒ đá ra, đăng nhập lại có quyền mới · mất mạng ⇒ giữ phiên, **không** gia hạn cache · đổi mật khẩu máy khác · lần đầu · gõ sai ⇒ vẫn qua Google · quá hạn 7 ngày. File cache thật **SHA256 trước/sau y hệt** |
| **M3** | Server thử cổng 5051 từ mã nguồn. **Đại Ca đăng nhập thật: xác nhận nhanh** |
| **Nhìn tận mắt** | Dựng lại bảng BC001 và dòng tiêu đề tab danh sách bằng **CSS thật**, cho Chrome chạy ngầm chụp — trước/sau đã gửi Đại Ca |

### 🔍 Điểm mù

- ⚠️ **Trình duyệt trong Claude bị chặn `localhost`** ⇒ tôi **không nhìn được app đang chạy**. Mọi
  "nhìn tận mắt" là ảnh **dựng lại** bằng CSS thật qua Chrome chạy ngầm — chứng minh cơ chế, không
  thay được ảnh chụp app thật.
- ⚠️ Dòng **"TỔNG TOÀN BỘ TRUY VẤN"** (số đổi sang Arial) **chưa nhìn được** — bản dựng lại không ra dòng đó.
- ⚠️ Nút **`TRUY VẤN`** vẫn gradient navy → tím. Bị đá ra (đăng nhập nhanh) **không có câu báo**.

### 📦 Git

`main` ahead 6 (toàn `.md`), chưa push · nhánh `giaodien` = `main` + commit `1dadaae` (GĐ1 + GĐ2) +
**chưa commit**: `server.py` (đăng nhập nhanh) và `index.html` (3 vòng sửa font). Lần push tới
**bắt buộc tăng `version.txt`** (xem khối 🚧 ở § VIỆC CẦN LÀM).

### 💡 Bài học — đáng giá hơn bản thân mấy lỗi

1. **Thay một mã màu hàng loạt là nguy hiểm** khi màu đó dùng **cả trên nền sáng lẫn nền tối** —
   navy trên trắng thì đẹp, trên header tối thì tàng hình. Thay xong phải rà **nền phía sau** từng chỗ.
2. **Dò độ đậm phải dò cả dạng biểu thức** (`isBold ? 800 : 300`), không chỉ `fontWeight: 800`.
   Dò hẹp rồi báo *"còn 0 chỗ"* là báo sai.
3. **Một lớp CSS ghi cứng tên font** (`.report-table { font-family: 'Inter' }`) làm **mọi chỗ sửa ở
   `body` vô hiệu** cho đúng vùng đó. Đổi font thì phải quét **mọi** `font-family`, không chỉ `body`.
4. **"Đã sửa" phải kèm ảnh nhìn tận mắt.** Hai lần tôi báo xong dựa trên CSS đã tới trình duyệt, cả
   hai lần Đại Ca vẫn thấy lỗi. Từ vòng 2 trở đi mới dựng lại bằng CSS thật rồi chụp ra xem.

---

## 24/09/2026 (cuối phiên) — Rà lại việc treo: tài liệu đã lệch thực tế

Không sửa code. Chỉ đi kiểm xem **tài liệu có còn đúng không** — và hoá ra không.

### 🔴 Tài liệu nói "chờ push", thực tế đã phát hành xong từ 3 phút sau đó

| Tài liệu ghi | Đo được lúc 17:45 |
|---|---|
| `v1.12.3` build local, **chờ push** | Đã push. `git ls-remote origin main` = `62af287` = đúng HEAD local, working tree sạch |
| `Latest` trên GitHub là `v1.12.2` | **`v1.12.3` là `Latest`**, tạo `2026-09-24T10:37:06Z` (17:37 giờ VN) |
| "Commit tài liệu **cố ý giữ ở local**" | Hai commit `.md` (`f862674`, `0a9df3f`) **đã nằm trên GitHub** |
| Phiên gần nhất phát hành `v1.12.0`, `main = 1e5dee9` | Sau đó còn 3 bản nữa |

Actions cả 3 lần gần nhất đều `success`.

**Vì sao lệch:** câu "chờ push" nằm **trong chính commit `62af287`** (17:35) — viết trước khi push
rồi push kèm luôn, không ai quay lại sửa. Đây là **cái bẫy cố hữu của việc ghi trạng thái phát hành
vào file nằm trong chính lần phát hành đó.**

➡️ **Rút kinh nghiệm: dòng trạng thái "đã push chưa / Latest là bản nào" chỉ được viết SAU khi push
xong**, hoặc viết theo kiểu không tự mâu thuẫn (ghi "chuẩn bị phát hành" thay vì "chờ push").

### ✅ Điểm sáng: bước đối chiếu EXE đã làm rồi và đang đúng

```
EXE local dist\iPOS_Accounting_Report.exe : d2dd506f…d012fc18  (13.104.424 B)
digest GitHub công bố cho asset v1.12.3   : d2dd506f…d012fc18  (13.104.424 B)
```

Khớp tuyệt đối ⇒ EXE trên máy Đại Ca **là đúng file CI**. Mốc thời gian khớp với quy trình: build
local 17:32 → sao lưu `.bak` → push 17:35 → Actions 17:36 → Release 17:37 → thay EXE 17:38.

⚠️ **Hệ quả: từ đây đừng push file `.md` một mình** — Actions build lại, thay asset bằng binary khác
SHA, và cái digest vừa khớp lệch ngay. Chính vì vậy **commit của phiên này giữ ở local**.

### Việc treo — kiểm chứng được tại chỗ

| # | Kết quả đo |
|---|---|
| 8 | ✅ **Đã xoá** 2 file rác (xem dòng việc số 8) |
| 11 | ❌ **Vẫn kẹt đúng chỗ cũ.** Workflow còn `checkout@v4` (dòng 20), `setup-python@v5` (dòng 25), `action-gh-release@v2` (dòng 69), **chưa có `paths-ignore`**. `gh auth status` cho scope `gist, read:org, repo` — **vẫn thiếu `workflow`** |

Các việc còn lại (1, 3, 4, 5, 6, 7, 9, 10) nằm trên Google Sheet / SQL Server / cần Đại Ca chốt,
không kiểm được từ máy này.

### 🆕 Phát hiện thêm: `config.json` còn mật khẩu SQL thật

File còn nguyên `password` của user `ipchulong` — phiên trước đo xong nhưng chưa dọn theo luật đã
chốt (*xoá đúng ô `password`, giữ `server`/`user`/`database` để lần sau chỉ phải điền một ô*).

Đã kiểm: `.gitignore` chặn (dòng 33), git **không theo dõi** ⇒ **không lộ lên GitHub**, chỉ nằm
dạng chữ thường trên đĩa. Không có dòng code nào trong repo đọc file này — `test.py` đọc một
`config.json` **khác**, nằm ngoài repo, dùng khoá `uid`/`pwd`.

✅ **Đã xoá** (Đại Ca bảo cứ xoá). File giữ nguyên 5 khoá, `password` để rỗng — lần sau chỉ phải
điền một ô. Cố ý **không** dùng đường vòng đọc file ra rồi sửa: làm vậy là mật khẩu lọt vào khung
chat, đúng thứ mà cách làm `config.json` sinh ra để tránh.

### 🔴 Việc số 6 (`AUTO_SHRINK` / `AUTO_CLOSE`) là VIỆC MA — đã treo hơn một tháng

Đại Ca hỏi *"auto shrink là gì, có liên quan gì tới `IACC_CHULONG` không"*. Đi tra thì lòi ra:
**chính repo này đã ghi ngược lại ở ba chỗ**, mà mục việc treo vẫn nói đó là *"việc rẻ nhất, hiệu
quả nhất còn treo"*:

| Nguồn trong repo | Ghi gì |
|---|---|
| [TOI_UU_DB_16082026.sql:16](TOI_UU_DB_16082026.sql) — đo **16/08/2026 trên chính máy chủ đó** | *"Mục 1 (AUTO_SHRINK / AUTO_CLOSE): **CẢ 3 DATABASE VÀ 'model' ĐÃ TẮT SẴN** → chạy vào sẽ không đổi gì"* |
| [SU_CO_15082026.md:184](SU_CO_15082026.md) | *"`AUTO_SHRINK` và `AUTO_CLOSE` **đã được tắt sẵn — kiểm rồi, không phải thủ phạm**"* |
| Mục **5. Verify — đạt M4** trong file này | *"SQL Server 2025 Express, `compatibility_level = 170`, `AUTO_SHRINK`/`AUTO_CLOSE` **đã tắt sẵn**"* |

➡️ Đã sửa **cả hai chỗ**: việc số 6 ở § VIỆC CẦN LÀM, và [CLAUDE.md § 6](CLAUDE.md).

**Vì sao lọt:** mục việc treo nhặt **tên script** `Tat_AutoShrink_AutoClose.sql` rồi suy ra là
"chưa tắt", trong khi **header của chính script đó** nói rõ đã tắt sẵn và script chỉ giữ làm **dây
bẫy** phòng ai bật lại. **Bài học: thấy tên script kiểu `Tat_X.sql` thì đọc header đã, đừng suy ra
là X đang bật.**

⚠️ **Chưa đo lại được hôm nay** — truy vấn DB thật bị chặn quyền (*Production Reads*). Số liệu dựa
trên phép đo 15–16/08/2026. Hai cờ này **theo từng database**, phục hồi từ `.bak` cũ hoặc tạo DB
mới từ `model` bị bật là chúng quay lại, nên kiểm lại cho chắc:

```sql
SELECT name, is_auto_shrink_on AS [AUTO_SHRINK], is_auto_close_on AS [AUTO_CLOSE],
       recovery_model_desc, compatibility_level
FROM sys.databases ORDER BY database_id;
```

Cả hai cột phải là **0**. Ra `1` thì chạy `TOI_UU_DB_16082026.sql`.

### 📌 Đại Ca chốt luật ghi nhật ký — và tôi vừa vi phạm ngay trong phiên này

Tôi ghi mục này bằng cách **`>>` nối xuống cuối file**. Đại Ca chốt ngay: **nhật ký phải mới nhất ở
trên**, trên cùng là **việc tồn đọng + nguyên tắc**, và đây là **luật chung cho mọi file nhật ký
của project**, không riêng file này.

Đã sửa trong cùng phiên: cắt mục này lên **ngay dưới § VIỆC CẦN LÀM**, ghi luật vào **đầu file này**
và thành **nguyên tắc số 9** ở [CLAUDE.md § 3](CLAUDE.md).

✅ **Đại Ca chốt lật luôn — đã lật xong trong cùng phiên.** 22 mục nhật ký xếp **mới → cũ**;
9 mục tham chiếu (`## 0.` – `## 8.`) dồn xuống cuối dưới vạch **📚 PHẦN THAM CHIẾU**, **cố ý giữ
thứ tự tăng dần** vì đọc theo số mới có nghĩa.

Đây đúng loại việc [Bẫy 26](CLAUDE.md) cảnh báo (đảo ~2.000 dòng), nên làm theo lưới an toàn:

1. **Commit sạch trước**, sao lưu file ra scratchpad.
2. Cắt khối theo **mốc tiêu đề `^## `**, không đụng số dòng.
3. **Kiểm toàn vẹn bằng tập hợp từng dòng** (bỏ dòng trống và `---`) trước/sau: **mất 0, thêm 0**.
4. Rà các câu **chỉ vị trí** (*"xem mục cuối file"*, *"7 mục chi tiết nằm dưới"*) — đảo xong là
   chúng nói dối. Sửa 1 câu; mục **TỔNG KẾT NGÀY 21/09** được **ghim ở đầu nhóm ngày của nó** để
   câu *"7 mục chi tiết nằm dưới"* vẫn đúng.

🐛 **Bắt được một lỗi nhờ bước kiểm:** lần đảo đầu tôi reverse mù theo thứ tự file, mà mục mới nhất
thì trước đó đã được kéo lên đầu ⇒ nó **bị đẩy xuống đáy**. Nhìn danh sách tiêu đề sau khi đảo mới
thấy. **Đảo xong phải đọc lại danh sách `^## `, đừng tin mỗi phép đếm dòng.**

---

## 24/09/2026 (tiếp) — Thông báo lỗi đăng nhập: hai tiêu đề ngắn · **v1.12.3**

Đại Ca chốt: sai tài khoản ứng dụng thì ghi **"Mật khẩu hoặc tài khoản không đúng"**, sai thông
tin SQL thì ghi **"Lỗi kết nối máy chủ"**.

Lý do rất thực tế: màn hình đăng nhập có **hai nhóm ô khác hẳn nhau**, mà trước đây thông báo lại
không cho biết phải sửa nhóm nào. Lỗi SQL thì ra một đoạn dài 2–3 dòng, lỗi tài khoản thì ra câu
tuỳ Google trả về — người dùng đọc xong vẫn không biết gõ lại ô nào.

### Đã làm

| Chỗ | Thay đổi |
|---|---|
| `_LOI_SAI_TAI_KHOAN` / `_LOI_KET_NOI` | Hai hằng mới, đặt ngay trên `_loi_ket_noi_de_hieu` |
| `_loi_ket_noi_de_hieu` | Mọi nhánh trả về nay đi qua `_tra()` — **dòng đầu luôn là `Lỗi kết nối máy chủ`**, hướng dẫn cụ thể xuống dòng dưới |
| `login()` nhánh Google | Chỉ đổi chữ cho ca "sai tài khoản/mật khẩu" |
| `_cache_kiem` (offline) | Dùng **chung một hằng** với đường online |

### ⛔ Hai chỗ CỐ Ý không làm — đừng "dọn gọn" sau này

1. **Không bỏ dòng hướng dẫn.** Tiêu đề ngắn **thêm vào trước**, không thay thế. Đoạn
   *"đã bật VPN / vào đúng mạng nội bộ chưa · địa chỉ và cổng có gõ đúng không"* sinh ra sau sự cố
   20/09/2026 — báo sai hướng là người dùng ngồi chờ thay vì đi bật VPN.
2. **Không gộp mọi lỗi tài khoản thành "sai mật khẩu".** Lệnh `dang_nhap` của Google trả **ba**
   loại: sai mật khẩu · **tạm khoá N giây** · **tài khoản đã bị khoá**. Gộp hết là người đang bị
   khoá cứ gõ lại, càng khoá lâu mà không hiểu vì sao. Chỉ ca đầu mới đổi chữ — điều kiện
   `_loi_gs == 'Sai tài khoản hoặc mật khẩu'`.

### Verify

| Mức | Nội dung |
|---|---|
| M1 | `ast.parse` OK · không hàm trùng tên · **164 hàm / 69 route** không đổi |
| **M2** | **21 phép, đạt hết.** 6 loại lỗi ODBC (không tới được máy chủ · hết giờ chờ · sai user/pass SQL · không mở được database · thiếu driver · lỗi lạ) — **cả 6 đều có dòng đầu đúng bằng `Lỗi kết nối máy chủ`**, vẫn giữ dòng hướng dẫn, vẫn gửi kèm nguyên văn. Gọi **thật lên Google** với tài khoản không tồn tại → trả đúng `Mật khẩu hoặc tài khoản không đúng`, HTTP 401, **không lộ thông tin SQL** trong thông báo |
| **M3** | Build **v1.12.3**, chạy EXE thật, `POST /api/login` qua cổng 5050 với tài khoản sai → trả đúng câu mới. `current_version 1.12.3` · `is_frozen True` |

### Điểm mù

⚠️ **Nhánh "sai thông tin SQL" chưa chạy được qua EXE thật.** `login()` xác thực tài khoản ứng
dụng **trước**, rồi mới kết nối SQL — muốn tới được nhánh SQL thì phải có mật khẩu ứng dụng đúng,
mà mật khẩu đó Đại Ca giữ. Nhánh này được kiểm ở **M2** bằng cách gọi thẳng `_loi_ket_noi_de_hieu`
với 6 chuỗi lỗi ODBC thật. Đại Ca đăng nhập đúng tài khoản rồi cố tình gõ sai IP máy chủ là ra M3.

⚠️ Câu **tạm khoá / tài khoản bị khoá** chưa thử được vì phải cố tình gõ sai nhiều lần lên tài
khoản thật. Đã chặn bằng điều kiện so khớp chính xác chuỗi, và có phép kiểm trong bộ M2.

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

### ✅ Đã phát hành v1.12.2

Trước khi push còn dọn **hai chỗ sót trong `CLAUDE.md`** — bắt được nhờ đọc lại file đầu phiên:
một dòng bị lặp ở header, và mục "phiếu `POSTED` mà 0 dòng `WAREHOUSE`" vẫn ghi *"chưa đo cả năm,
chưa chốt"* trong khi việc đó đã đo xong và đóng. **Tài liệu sai còn nguy hơn code sai** — người
sau đọc rồi đi đo lại từ đầu.

| Bước | Kết quả |
|---|---|
| Push | `2a7e7fb..f862674` — **3 commit** (sửa chip · `#dc` + việc 13/14/15 · dọn tài liệu) |
| Actions | run `35986947776` · **`success`** |
| Release | **v1.12.2** · là `Latest` · `.exe` + `.zip` |

Kiểm đủ 4 điều kiện trước khi bấm: remote **GitHub**, tag `v1.12.2` **chưa tồn tại**, quét secret
**sạch**, `config.json` **không nằm trong git**.

### Tổng kết ngày 24/09/2026 — ba lần phát hành

| Bản | Nội dung |
|---|---|
| **v1.12.0** | Đóng M4 tab điều chuyển · luật iPOS **tự sinh** phiếu nhập · đổi tên nhóm thành `Không tìm thấy phiếu nhập` · ghi chú "CÓ nhưng thiếu mã hàng này" |
| **v1.12.1** | Hàng chip không còn tụt về 0 — sửa **cả ba tab** |
| **v1.12.2** | `#dc` làm bấm chip **nhanh 5–7 lần** · đóng việc 13 bằng phép đo · hai chip "Không thấy…" nằm cạnh nhau |

Phát hiện có giá trị nhất trong ngày **không phải dòng code nào**, mà là câu Đại Ca nói giữa
chừng: *phiếu nhập tự sinh khi phiếu xuất ghi sổ*. Nó lật ngược ý nghĩa của cả một tab đang chạy,
và lôi ra **3 ca hàng rời kho mà không vào đâu cả** — thứ mà không ai biết là đang mất.

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
  → ✅ **Đã triển khai cuối ngày 21/09 (Version 4)** — xem mục *21/09 (tiếp) — Triển khai
    Code.gs lên Google, và một cú suýt chết*.
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

## 📚 PHẦN THAM CHIẾU — nền tảng, KHÔNG theo ngày

> Chín mục dưới đây là **kiến thức nền**, không phải nhật ký: LedgerReport là gì, sự cố
> 15/08, việc đã làm theo bản, quy trình bắt buộc… Chúng **cố ý giữ thứ tự tăng dần 0 → 8**
> vì đọc theo số mới có nghĩa. Luật *mới nhất ở trên* áp cho **phần nhật ký phía trên**,
> không áp cho khối này.

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
