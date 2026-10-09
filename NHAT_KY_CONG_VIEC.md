# NHẬT KÝ CÔNG VIỆC — LedgerReport

> Toàn bộ những gì đã làm với **LedgerReport**, và **vì sao**. Đọc file này trước khi sửa tiếp.
> Kiến trúc, ma trận báo cáo, phương án backup: [CLAUDE.md](CLAUDE.md).
> Mổ xẻ sâu sự cố + 4 bài học: [SU_CO_15082026.md](SU_CO_15082026.md).
> 🚀 **Bản mới nhất: `v2.1.5` (09/10/2026)** — màn Điểm sử dụng: **bộ lọc hạn bảo trì** (Hết hạn · Dưới 30 · Hơn 30 · Chưa điền hạn)
>   + ô "Còn" 0 ngày chữ đỏ + cột "Còn" không còn cắt chữ (việc 52).
>   `v2.1.4` (08/10) = code y `v2.1.3`, chỉ viết lại "Có gì mới" (*Thêm danh sách điểm sử dụng* · *Cập nhật hệ thống*).
>   `v2.1.3` (08/10) = **màn "Điểm sử dụng"** (việc 51, chỉ quản trị) + thanh bên: Báo cáo TC xuống cuối.
>   `v2.1.2` (06/10) = cột ghim phải hụt 4px khi cuộn chạm cuối.
>   `v2.1.1` (05/10) = **BC017 Báo cáo bán hàng** + cấu hình cột 5 báo cáo + ghim cột / vừa khít 9 màn danh sách (việc 49, 50).
>   `v2.1.0` (29/09) = Đại Ca chốt lên **2.1** cho đợt tính năng mở app nhanh; code y `v2.0.9`.
>   `v2.0.9` (29/09) = **mở app ~0,2s** (việc 24 dịch sẵn giao diện + việc 25 thư viện trong app) · Tải lại
>   hỏi Google quyền · popup Hủy xuất Có/Không + tạm dừng · icon từng màn · GitHub Actions Node 24 + `paths-ignore` (việc 11).
>   `v2.0.8` (29/09) = **Hủy xuất không còn thoáng hiện file dở trong thư mục xuất** (việc 44).
>   `v2.0.7` (29/09) = **nút Hủy xuất Excel Nhật ký chung** (việc 43).
>   `v2.0.6` (29/09) = **đồng hồ đếm ngược xuất Excel Nhật ký chung** (việc 41)
>   + **đăng nhập nhanh không đá người ra khi Google bận** (việc 42).
>   `v2.0.5` (28/09) = **màn đăng nhập mới 08A+**. `v2.0.4` (28/09) = code y `v2.0.3`, chỉ viết lại mục "Có gì mới".
>   `v2.0.3` (28/09) = file xuất *Nhật ký chung chi tiết* (BC007) thêm **Mã/Tên mục chi phí** + ô trống không còn chứa dấu cách. Các bản trước:
>   `v2.0.0` (25/09 tối) = **giao diện mới `DATA REPORT`** — Đại Ca chốt lên *Ver 2* ·
>   `v2.0.1` (26/09) = **thông báo có bản mới kiểu mới** (hộp thoại + nút cam + thẻ nhắc, "Có gì mới" đọc `CO_GI_MOI.md`) ·
>   `v2.0.2` (26/09) = **vá lỗi nhân viên thường không xuất được Excel Báo cáo TC** (có từ v2.0.0, Bẫy 30) + việc 9, 10, 23.
> ✅ **EXE trên máy Đại Ca = đúng file CI v2.1.5** (SHA256 khớp digest `1414d115…`) — lên bằng **đường cập nhật thật** CI 2.1.4 → 2.1.5
>   (Đại Ca bấm Cập nhật trên hộp thoại, 09/10/2026). Thư mục làm việc đang ở `main`.
> 🔑 Luật nghiệp vụ gốc chốt 24/09: iPOS **tự sinh** phiếu nhập `NDCNB` khi phiếu xuất `XDCNB` ghi sổ — đổi hẳn cách
>   đọc tab đối chiếu điều chuyển. Xem các mục 24/09.
> ✅ Tài khoản nhân viên trên Google Sheet + đổi mật khẩu `admin` + tick quyền 2 tab mới: **Đại Ca báo xong 25/09** (việc 1, 3, 4).
> 🟡 **Việc 7 — lọc 2 chiều tab điều chuyển: đã phát hành trong v2.0.0, CHƯA có xác nhận thử với số liệu thật.**
> Apps Script trên Google: **Version 6** (08/10/2026 22:25), mã bản `2026-10-08a` (việc 51) — **đã triển khai**, `ping` OK, token khớp.
>
> 📌 **Việc còn treo gom ở ngay dưới: [§ VIỆC CẦN LÀM](#-việc-cần-làm).**
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

## 📌 VIỆC CẦN LÀM

> *Cập nhật 09/10/2026.* Gom hết việc còn treo về một chỗ. Nhận việc mới thì **đọc mục này trước**.
> ⚠️ Tiêu đề mục này **cố ý không ghi ngày** — mọi đường dẫn `#-việc-cần-làm` trỏ vào nó; ghi ngày là gãy link.
> Trạng thái: **v2.1.5 đã phát hành** (09/10/2026), là `Latest`, **EXE trên máy Đại Ca = đúng file CI** (SHA256 khớp digest) —
> bộ lọc hạn bảo trì màn Điểm sử dụng (việc 52). Mục *09/10/2026 — Việc 52*.
> Việc 51 (màn Điểm sử dụng) **đã phát hành v2.1.3/v2.1.4**; Apps Script **Version 6** `2026-10-08a`. Còn: thử tài khoản không phải ADMIN.
>
> ✅ **Từ v2.0.9 (việc 11) workflow có `paths-ignore`** — push CHỈ tài liệu (`**.md`, `docs/**`, `docs-cu/**`) **không build lại EXE**,
> asset không đổi SHA ⇒ push nhật ký thoải mái. ⚠️ Commit đụng `.github/workflows/` thì `git push` thường bị từ chối (Git Credential
> Manager cấp token cũ thiếu scope `workflow`) ⇒ push bằng token `gh`: xem `CLAUDE.md` § 5 *ĐÃ XONG 29/09/2026 — nâng 3 action*.
>
> ✅ **Đại Ca đã dùng v2.0.6 xuất Excel Nhật ký chung** (gửi ảnh 29/09) ⇒ đăng nhập trên v2.0.6 chạy được. Góp ý ⇒ **việc 43**.
>
> ✅ **Việc 43 (29/09/2026): nút Hủy xuất + hộp xuất theo mẫu DataStudio — PHÁT HÀNH v2.0.7** (`Latest`), EXE trên máy Đại Ca
> = đúng file CI v2.0.7 (SHA khớp). Mục *29/09/2026 — Phát hành v2.0.7*.
>
> 🔴 **Lần phát hành tới BẮT BUỘC:** viết mục `## vX.Y.Z` vào **`CO_GI_MOI.md`** (chỉ tính năng; hệ thống ⇒ *Cập nhật hệ thống*)
> **trước khi push** · build bằng `build_exe.py` để số hiệu tự tăng · quét route `/api` chưa khai báo quyền phải ra `[]` (Bẫy 30)
> · thử ít nhất một lần bằng tài khoản **không phải quản trị**.

### 🎨 DỰ ÁN GIAO DIỆN MỚI — *(24/09/2026)* — ✅ **ĐÃ PHÁT HÀNH `v2.0.0` 25/09/2026** (nhánh `giaodien` đã gộp vào `main`)

> Phác thảo (ngoài repo): **https://claude.ai/artifact/7kiiWQ13PPR7eXN2AgPhtc** — 8 mục (01–08; 07 = thông báo có bản mới;
> 08 = màn đăng nhập mới, bản **08A+** đã làm vào app ở v2.0.5).
> Nhật ký chi tiết: các mục 24–26/09/2026 ngay dưới § này.

**Đại Ca đã chốt:** font **Arial toàn bộ** · màu chủ đạo **navy `#1E3A8A`** (nền tối `#172554`) ·
**giữ nguyên logo** `icon.svg` `#FF9D3D` · icon **SVG, cấm emoji** · tên hiển thị **`DATA REPORT`** (đổi từ
`PROOFTRAIL` 25/09), ~~dòng phụ *"Minh bạch tới từng chứng từ"*~~ (**Đại Ca bỏ 28/09, v2.0.5**) · điều hướng **2 tầng** (cột phân hệ navy **có tên**,
kiểu 06C, thu gọn được) · **có trang chủ** theo mẫu iACC Portal.

| GĐ | Việc | Trạng thái |
|---|---|---|
| **0** | Nhánh `giaodien` + ghi mốc **164 hàm / 69 route** | ✅ Xong |
| **1** | **Nền**: Arial · navy · nhãn 11px `#475569` · `tabular-nums` · **sửa lỗi font** | ✅ Xong — commit `1dadaae` + `c64540a` |
| **2** | **Màn đăng nhập**: tấm navy trái, `PROOFTRAIL`, logo gốc, mục 01/02 | ✅ Xong — commit `1dadaae` |
| ➕ | **Đăng nhập nhanh** (hướng A — Đại Ca chốt giữa chừng) | ✅ Xong, **Đại Ca đã thử thật: nhanh** — commit `c64540a` |
| **3** | **Điều hướng**: cột phân hệ 64px + hàng tab ngang, 9 màn hình vào 5 phân hệ. **Báo cáo TC: trang liệt kê 16 thẻ + ô chọn có tìm kiếm, ô lọc dời phải, ô Thời gian gộp, Bộ lọc nâng cao** (Đại Ca đổi ý: bỏ 5 tab nhóm) | ✅ Xong — **Đại Ca xem và chốt OK 25/09** — phát hành v2.0.0 |
| **4** | **Trang chủ** — Đại Ca chốt 25/09: **chỉ khung + thẻ phân hệ, CHƯA lấy số liệu**; kỳ sau này = tháng hiện tại | ✅ **Khung xong — Đại Ca chốt OK 25/09** (sau khi cho lưới thẻ trải hết bề ngang), phát hành v2.0.0. ⏳ **Khối số liệu (tải NGẦM, mỗi ô 6–8s) CHƯA làm** |
| **5** | **Đổi tên hiển thị**: `APP_NAME`, `<title>` + 2 meta, 9 dòng chữ chìm, `manifest.json` (trước ghi nhầm *iPOS Ledger Studio*), Properties của EXE (`build_exe.py` + `version_info.txt`) | ✅ **Xong 25/09 — commit `ee5aed3`**. ⛔ **Giữ tên file `iPOS_Accounting_Report.exe`** — đổi là tự cập nhật đứt. Tiêu đề Release trên GitHub **giữ chữ cũ** *iPOS Accounting Report* — **Đại Ca chốt không cần đổi (25/09/2026)** |

**Việc còn chờ của dự án này:**

| # | Việc | Ghi chú |
|---|---|---|
| 16 | ~~Đại Ca F5 xem lại màn danh sách~~ ✅ **Đại Ca đã xem 25/09** | Nhận xét: **cột bị hẹp** ⇒ thành việc 28 |
| 17 | ~~Nút `TRUY VẤN` đang chuyển màu navy → tím~~ ✅ **XONG 25/09** | Đại Ca chốt: chữ **"Lọc"**, navy đặc, như mẫu iPOS. Nằm trong thanh lọc mới của 9 màn danh sách |
| 18 | ~~Chốt mốc commit phần đăng nhập nhanh + sửa font~~ ✅ **commit `c64540a`** | Phát hành v2.0.0 |
| 19 | ~~Đại Ca xem GĐ3 rồi chốt commit~~ ✅ **Đại Ca chốt OK sáng 25/09** (*"cái đó thì ok rồi"*) ⇒ đã commit GĐ3 | ⚠️ Đại Ca chốt chung, **không nói rõ đã thử từng mục dưới đây chưa** — lần đầu dùng số liệu thật thì để ý. Danh sách cần xem ở mục *"Việc Đại Ca xem sáng 25/09"* trong nhật ký 25/09 (tiếp 3), ngay dưới § này. Ba việc tôi **không** tự thử được: hộp *"Chuyển mẫu báo cáo?"* khi có số liệu thật · menu **Xuất Excel / Xuất PDF** khi có số liệu (chưa có số liệu thì nút tắt) · kéo thả thứ tự ô lọc bằng chuột thật. Và **đọc lại mô tả 16 thẻ** — tôi tự viết |
| 51 | ✅ **Màn "Điểm sử dụng"** — danh sách điểm dùng phần mềm kế toán + thời hạn bảo trì (Đại Ca yêu cầu 08/10/2026). **Phát hành v2.1.3 (+ v2.1.4 sửa "Có gì mới") 08/10/2026**, Apps Script Version 6, Google thật đã đồng bộ 86 dòng + điền kỳ 79 dòng | ✅ Code.gs `2026-10-08a` **đã triển khai Version 6** (08/10 22:25). ✅ Google thật (ADMIN): đồng bộ 86 dòng + gia hạn 72 dòng + lưu 7 dòng, đọc lại 86/86 đúng (08/10 23:00). Còn: thử tài khoản **không phải ADMIN** · CO_GI_MOI + build + phát hành (hỏi trước khi push) · gia hạn kỳ BTKT mới cho 72 dòng (hết hạn 09/10/2026). Mục nhật ký *08/10/2026 — Việc 51* |
| 50 | ⏳ **Cấu hình cột 5 báo cáo + ghim cột / vừa khít cột 9 màn danh sách** (Đại Ca yêu cầu 05/10/2026). **Đợt 1 — cấu hình cột BC007 · BC008 · BC012 · BC015 · BC016: XONG** (Đại Ca bảo làm tiếp đợt 2). **Đợt 2 — ghim cột bất kỳ sát lề trái/phải + bấm đúp mép = vừa khít + nút "Vừa khít tất cả cột": XONG**, kiểm DB thật 9/9 màn. Đại Ca thử 05/10: OK, đổi icon ghim (mẫu ô bảng) + bỏ chú thích cuối hộp. ✅ **Phát hành `v2.1.1` 05/10/2026** (cập nhật thật 2.1.0 → 2.1.1 khớp SHA CI) | ✅ Lệch 4px cột ghim phải: **đã sửa** (tay kéo cột cuối thò ra ngoài bảng) — ✅ **phát hành `v2.1.2` 06/10/2026**. "Đứng hình": thử lại 88 lượt bằng dữ liệu giả **không tái hiện được**, giả thuyết làm mờ nền **bị bác** ⇒ chỉ còn theo dõi nếu nhân viên báo. Mục *05/10/2026 (khuya, tiếp)*. Server thử code mới: **cổng 5053** (`server_thu_5053.py` trong scratchpad phiên 05/10, chết theo phiên chat). Mục nhật ký *05/10/2026 (tối) — Việc 50 đợt 2* + *05/10/2026 — Việc 50 (đợt 1)* |
| 49 | ⏳ **BC017 Báo cáo bán hàng** (mẫu iPOS 3.1, đối chiếu doanh thu) — 3 kiểu xem × chi tiết/tổng hợp + cấu hình cột + mặc định BHVAT/BHK, **kiểm trên DB thật đạt**, ✅ **phát hành `v2.1.1` 05/10/2026** | Còn: soi vài phiếu với mẫu 3.1 trên iPOS Chú Long · **tick quyền BC017 cho chức vụ nhân viên ở tab Phân quyền** (ADMIN tự có) — hai việc này Đại Ca làm. ✅ Ô `password` trong `config.json` **đã xoá 05/10** (Đại Ca bảo) ⇒ thử DB thật lần sau phải điền lại. Điểm mở: chi tiết cả tháng **8–10s/trang** (chưa tăng tốc) · 1366px thêm cột là kéo ngang · mỗi lần tick một cột thêm chưa có là tải lại 1 lần. Server thử 5052 (script trong scratchpad) **tự tắt sau ~2 giờ** — giới hạn chạy nền của công cụ, không phải lỗi app; tắt thì bật lại. Mục nhật ký *04/10/2026* + *03/10/2026 — BC017* |
| 48 | ⏳ **Chưa thử với Google THẬT: Tải lại khi quyền vừa bị đổi** (v2.1.0) | Đã thử bằng Google giả lập (9 ca) + giao diện server thử. Ca thật: quản trị đổi quyền tài khoản đang đăng nhập ở máy khác → máy đó bấm Tải lại ⇒ phải về màn đăng nhập kèm *"Quyền của tài khoản vừa được thay đổi…"*. Đại Ca chốt *"tạm thời ok"* 29/09 nhưng chưa nói đã thử ca này |
| 47 | `Sync-And-Backup.ps1` đang là **UTF-8 KHÔNG BOM** dù có tiếng Việt | Bẫy 12: PowerShell 5.1 đọc sai. Script vốn không chạy trên máy này nên chưa ai thấy. Phát hiện 29/09 khi thêm file vào `$Files`. Sửa = lưu lại có BOM, thử chạy `-WhatIf`/không `-Commit` trên máy có thư mục cha |
| 46 | **Nút Hủy cho hộp xuất của 9 màn danh sách** (CSV/Excel qua `startServerExport`) | Chỉ Nhật ký chung có Hủy + tạm dừng. Server đã sẵn (`_cho_neu_tam_dung` có ở vòng ghi CSV); còn thiếu giao diện. ⚠️ Xuất **CSV** vẫn ghi thẳng vào thư mục xuất (file lớn dần lúc đang ghi) — việc 44 chỉ sửa `.xlsx` |
| 45 | 🔴 **Route tĩnh `serve_static` phục vụ MỌI file dưới thư mục đang đứng** + server nghe `0.0.0.0` | Chạy `server.py` **từ mã nguồn** thì máy khác trong LAN đọc được `config.json` (mật khẩu SQL), `ketnoi.json`. **EXE không bị** (`_MEIPASS` chỉ có file đóng gói). Đã tạo thẻ việc riêng *"Chặn route tĩnh lộ file bí mật khi chạy từ mã nguồn"* 29/09 — chờ Đại Ca bấm |
| 43 | ✅ **Nút Hủy xuất + hộp xuất Excel Nhật ký chung theo mẫu DataStudio** — **phát hành v2.0.7**. ✅ **Đại Ca bấm Hủy xuất trên EXE v2.0.7 với số liệu thật: OK (29/09)** — lần thử đầu Đại Ca **thấy file trong thư mục xuất** (xem việc 44) | Đại Ca 29/09: *"nên cho thêm nút hủy tiến trình nếu t test t muốn ngưng"* + *"cơ chế tính giây sao nó cứ tăng giảm 1 chổ vậy … hoặc làm theo hình thì sao"* (ảnh hộp xuất DataStudio). Hộp mới: 4 bước · Đã ghi / Tốc độ / Thời gian *đã chạy · còn ~* · Hủy xuất. Mục nhật ký *29/09/2026 — Việc 43* |
| 44 | ✅ **Hủy xuất không còn thoáng hiện file `.xlsx` dở trong thư mục xuất** — **v2.0.8** | Đại Ca bắt gặp 29/09. Gốc: huỷ giữa chừng thì `workbook.close()` đóng gói phần đã ghi **ngay trong thư mục xuất** rồi mới xoá. Nay ghi + đóng gói ở `%TEMP%`, xong hẳn mới chuyển sang; huỷ lúc ghi thì **bỏ đóng gói**, chỉ xoá file tạm từng sheet (`_bo_workbook_do`). Mục nhật ký *29/09/2026 — Việc 44* |
| 42 | ✅ **Đăng nhập nhanh đá người ra VÔ CỚ khi Google bận** — **phát hành v2.0.6** (commit `b887717`) | Luồng hỏi lại Google (`_kiem_lai_nen`) coi **mọi** `ok: false` là từ chối ⇒ chờ ổ khoá quá 20 giây (*"Máy khác đang ghi…"*), lỗi dịch vụ Sheets, sai token… đều **huỷ phiên + xoá bản lưu**. Nay chỉ 3 câu từ chối thật mới đá ra (`_GS_TU_CHOI_TK`). Đối chứng với bản cũ bằng cùng phép thử: bản cũ đá ra ở cả 3 ca "chưa trả lời được" |
| 41 | ✅ **Đồng hồ đếm ngược xuất Excel Nhật ký chung** — **phát hành v2.0.6**, đã đo + thử giao diện trên DB thật (mục *28/09/2026 (khuya, tiếp)*). ✅ Đại Ca đã dùng thật 29/09 — góp ý thành **việc 43** | Đại Ca hỏi *"ước tính thời gian xuất được không"* → chốt *"đếm ngược từ đầu, 1 đồng hồ thôi"*. % cũ là **giả** (30.000 dòng = 1%, chặn 95%). Việc còn lại + cách thử: mục nhật ký *28/09/2026 — Hộp xuất Excel Nhật ký chung* |
| 40 | ✅ ~~Nút **Tải lại** gặp phiên đã hết (401) thì **im lặng**~~ — **XONG 29/09 (v2.0.9)**: về màn đăng nhập kèm *"Phiên đăng nhập đã hết…"*; máy chủ có lý do cụ thể hơn (việc 23) thì câu đó thay vào | Mục nhật ký *29/09/2026 — Việc 11, 40, 24, 25* |
| 39 | Ô lọc **Kho** vẫn liệt kê kho của **mọi đơn vị** | Cùng bệnh việc 10: tài khoản bị giới hạn chọn kho đơn vị khác ⇒ 0 dòng. Tab điều chuyển (Kho xuất / Kho nhận) phải **giữ đủ** như ô Đơn vị xuất. Cần xem `meta.warehouses` có mang mã đơn vị không |
| 38 | ~~🔴 Nhân viên thường **không xuất được Excel** Báo cáo TC (403 *"Route chưa khai báo quyền"*)~~ ✅ **Phát hành v2.0.2** | Có từ **v2.0.0**: `/api/xuat_xlsx_bieu_mau` + `/api/tai_file_xuat` (việc 35) quên khai báo quyền; ADMIN qua được nên không ai thấy. Nay trong `PERM_PUBLIC`. **Bẫy 30** + lệnh quét trong CLAUDE.md |
| 37 | ~~Làm lại thông báo "có bản mới" cho dễ thấy~~ ✅ **Phát hành v2.0.1 — phương án B + C** (Đại Ca chọn), "Có gì mới" đọc từ `CO_GI_MOI.md`, kiểm lại mỗi 2 giờ | ✅ **Chạy thật trọn vòng** ở lần cập nhật 2.0.1 → 2.0.2 (hộp thoại hiện đúng 4 dòng lấy từ GitHub). Máy đang ở 1.12.x vẫn lên bằng dải cũ (code bản cũ) |
| 36 | ~~Chữ trong file Excel Báo cáo TC nhỏ (8,5pt)~~ ✅ **XONG 25/09 — thân bảng 11pt, cột/dòng nới cùng tỉ lệ** (Đại Ca chọn từ 4 file mẫu) | Chi tiết: mục nhật ký *25/09 (khuya, tiếp 4)*. ✅ **Đại Ca xuất thử trên 5051 và chốt OK 25/09** (*"xuất excel ok rồi đó"*) |
| 35 | ~~Báo cáo TC xuất Excel ra `.xls` (HTML), không phải `.xlsx` thật~~ ✅ **XONG 25/09 — nay `.xlsx` thật, giữ y biểu mẫu** (Đại Ca: *"luôn luôn xuất xlsx, y chang biểu mẫu đang xem"*) | Chi tiết: mục nhật ký *25/09 (khuya, tiếp 3)*. ✅ **Đại Ca chốt OK 25/09** cùng việc 36. `/api/export_excel_backend` (BC007/BC008, không ai gọi) vẫn để nguyên |
| 34 | ~~Lỗi cuộn ảo (Bẫy 29) có trong bản v1.12.3~~ ✅ **Phát hành v2.0.0** | Vá trên `main` (`6907d78`) rồi gộp vào `giaodien` — trùng khít, 0 dòng khác |
| 33 | ~~Cột phân hệ navy bên trái~~ ✅ **Kiểu 06C — phát hành v2.0.0** | Phác thảo = mục **06**. Màu nền = tấm navy màn đăng nhập `#172554` |
| 32 | ~~Giao diện mới cho tab Phân quyền~~ ✅ **Đại Ca chốt OK 25/09 — phát hành v2.0.0** | Mục **05 — PHÂN QUYỀN** của bản phác thảo. **Bản 2 (theo góp ý 25/09):** Chức vụ **bỏ ma trận** → danh sách + khung sửa bên phải, cùng kiểu tab Tài khoản · Tài khoản **bỏ ô mật khẩu và hộp tóm tắt quyền** (mật khẩu thu thành dòng *"Đặt lại mật khẩu"*; tài khoản mới vẫn có ô) · Đơn vị = **một danh sách tick**, có dòng *"Tất cả đơn vị"*. Thêm 2 khung **Thêm tài khoản** / **Thêm chức vụ** (Đại Ca hỏi *"màn hình thêm mới quyền thì sao"*). Dữ liệu trong khung là **minh hoạ**. Chưa sửa dòng mã nào |
| 31 | ~~Ô Số chứng từ của BC012 hỏng trong bản v1.12.3~~ ✅ **Phát hành v2.0.0** | Gõ từng chữ `P` → `T` từng thành `P,PT`, lọc ra 0 dòng (`toggleFilter` coi `tran_no` là mảng). Vá `784d227` |
| 30 | ~~Áp Bộ lọc nâng cao + ô Thời gian gộp sang 9 màn danh sách~~ ✅ **XONG 25/09 — commit `e071bb9`** | Theo ảnh mẫu iPOS *"Đặt mua hàng"*. **Tối đa 3 ô ngoài** (tính cả Thời gian — Đại Ca chốt), phần còn lại vào Bộ lọc nâng cao. 9/9 màn một hàng ở 1366 và 1280px |
| 29 | ~~Nút Excel / PDF của BC003, BC004 sáng sẵn khi chưa có số liệu~~ ✅ **XONG 25/09/2026** | Sửa luôn khi gộp 2 nút thành nút tải xuống: điều kiện xét `initialReportData`. Đã thử: BC001/003/004/012/016 chưa tải số liệu ⇒ nút tắt, tooltip *"Chưa có số liệu — bấm Xem trước rồi mới xuất"* |
| 20–21 | ~~GĐ4 · GĐ5~~ ✅ **Phát hành v2.0.0** | Theo bảng trên. Khối số liệu Trang chủ vẫn chưa làm |
| 28 | ~~Cột bảng hẹp~~ ✅ **XONG 25/09** — Đại Ca chốt **kéo giãn cột + nhớ**. Tiêu đề không gãy dòng nữa; kèm **ẩn/hiện cột** và **Excel xuất đúng cột đang hiện** · số đo cũ để tham khảo: | Số đo 25/09 cho lúc sửa: hàng lọc 5 màn danh sách **cần 1.393px** để mọi ô đủ rộng, màn 1366 chỉ có **1.254px** (bản cũ trước GĐ3: cần 1.473 / có 1.318 — **vốn đã bị ép co từ trước**). Ở 1280px tiêu đề **`MÃ CT` gãy 2 dòng**. Cột phân hệ ăn thêm 64px chiều ngang |
| 22 | ⏸️ **Ổ khoá chung `LockService` trong `Code.gs` (dòng 487)** — **CHƯA LÀM, chờ số liệu** (Đại Ca chốt 28/09) | 5 người mở app cùng lúc thì người thứ 5 chờ gần 1 phút (ước tính cũ, chưa đo). ⚠️ **Đính chính 28/09:** cách ghi cũ *"bỏ khoá cho lệnh chỉ đọc"* **không giải quyết được gì** — `dang_nhap` **không** chỉ đọc (ghi ô `DANG_NHAP_LUC`, 1 dòng Nhật ký, bộ đếm gõ sai), mà xếp hàng buổi sáng chính là `dang_nhap`. Cách đúng: đăng nhập **đúng** mật khẩu thì không khoá; **chỉ khoá khi gõ sai** (bỏ hẳn thì kẻ dò gửi song song lách được giới hạn 8 lần) và khi **quản trị ghi** (2 lần lưu tài khoản mới cùng lúc cùng lấy `getLastRow()+1` ⇒ ghi đè nhau). Đo 28/09 lúc vắng: có khoá (`ping`) trung vị **2,11s** · không khoá (`doGet`) **2,47s** ⇒ khoá chỉ tốn khi đông người. **Trước khi làm: Đại Ca xem Apps Script → Executions khung 7h30–8h30** có `doPost` chồng giờ, chạy lâu không. **Phải triển khai lại Apps Script** — theo đúng `chuan_bi_deploy.py` (Bẫy 19, 23). Nút **Lưu tab Phân quyền** (~6–9s, ước từ code) ép được còn ~3–4s (gộp lưu + tải lại 1 lần gọi · đọc mỗi sheet 1 lần · ghi dòng tài khoản 1 lần) — **Đại Ca chốt KHÔNG làm** vì ít sửa phân quyền |
| 23 | ~~Bị đá ra (đăng nhập nhanh) không có câu báo lý do~~ ✅ **XONG 26/09** | Màn đăng nhập hiện lý do: đổi mật khẩu / bị khoá / đổi quyền (`/api/ly_do_dang_xuat`). Mục nhật ký *26/09 — việc 9, 10, 23, 26* |
| 24 | ✅ ~~**Biên dịch sẵn JSX lúc đóng gói**~~ — **XONG 29/09 (v2.0.9)**: `dich_giao_dien.js` dịch lúc build, EXE nhúng `web_dich_san/index.html`. Đo cùng máy: **7,8s → 0,26s** lần đầu, **6,8s → 0,11s** mở lại; code dịch sẵn **trùng từng byte** code trình duyệt tự dịch | Mục nhật ký *29/09/2026 — Việc 11, 40, 24, 25* |
| 25 | ✅ ~~**Nhúng 5 thư viện còn tải từ Internet** vào EXE~~ — **XONG 29/09 (v2.0.9)**: `thu-vien/` (Babel chỉ để build, không vào EXE); cảnh báo "không tải được giao diện" nay hiện thật (xét `.version`) | Mục nhật ký *29/09/2026 — Việc 11, 40, 24, 25* |
| 26 | ~~BC015, BC016 chưa có trong ma trận báo cáo của `CLAUDE.md`~~ ✅ **XONG 26/09** | Đã thêm, kèm endpoint + nguồn đọc từ code |
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
| 7 | ~~Bộ lọc Đơn vị của tab điều chuyển nội bộ áp cho phía XUẤT~~ ✅ **Phát hành v2.0.0** — ⏳ **chưa có xác nhận thử với số liệu thật** | Thanh lọc có **Kho xuất** + **Kho nhận**; tài khoản bị giới hạn thấy dòng mà **một trong hai phía** thuộc quyền. Chi tiết: mục nhật ký *25/09/2026 (khuya)* |
| 8 | ~~Xoá file rác~~ ✅ **XONG 24/09/2026** | Đã xoá `phanquyen.json` (972 B) + `dist/phanquyen.json.cu` (1.002 B). Kiểm trước khi xoá: cả hai đều ghi `"note": "FILE TEST - mat khau tam, khong phai ban that"`, và `server.py` **chỉ nhắc chúng trong comment**, không còn dòng code nào đọc. Cả hai vốn đã `.gitignore` + git không theo dõi ⇒ không lộ |
| 9 | ~~Màn đăng nhập chưa bắt buộc điền Tài khoản ứng dụng~~ ✅ **XONG 26/09** | Chặn ở cả trình duyệt lẫn máy chủ: báo ngay, không gọi Google |
| 10 | ~~Dropdown lọc Đơn vị vẫn hiện tên đơn vị ngoài quyền~~ ✅ **XONG 26/09** | 9 màn danh sách + Báo cáo TC chỉ liệt kê đơn vị trong quyền; tab điều chuyển ("Đơn vị xuất") **cố ý giữ đủ**. ⚠️ Ô **Kho** vẫn liệt kê kho mọi đơn vị (chưa làm) |
| 12 | ~~Hàng chip tụt về 0 khi bấm chọn một chip~~ ✅ **XONG 24/09/2026** | Sửa cả **ba** tab (`dcnb_reconcile`, `btp_reconcile`, **`po_list`** — tab này cũng dính, phát hiện lúc sửa). Cờ `bo_trang_thai` + `so_dong` tách theo trạng thái. Đối chứng trước/sau: **không chậm đi** |
| 15 | ~~Bấm chip chậm gấp ~4 lần~~ ✅ **XONG 24/09/2026** | Dựng `DC` ra bảng tạm `#dc` một lần. Chip `Đã nhận đủ` **42,9s → 7,9s**, trang 2 **50,1s → 6,6s**, đổi cột sắp xếp **45,9s → 7,3s**. Đánh đổi: ô tìm mã hàng chậm thêm ~2s |
| 13 | ~~Phiếu `POSTED` mà 0 dòng `WAREHOUSE` bị tab giấu~~ ✅ **ĐÓNG 24/09/2026 — KHÔNG phải lỗi** | Đo cả năm 2026: chỉ **5/20.089** `XDCNB` · **4/19.479** `NDCNB` · **2/21.848** `XKHOSXBTP` · **1/21.561** `NSP` (≤0,02%), và **cả 12 phiếu đều có số lượng = 0** — phiếu rỗng. Phiếu rỗng thì không có gì để đối chiếu ⇒ giấu đi là **đúng**. Không sửa dòng code nào |
| 14 | ~~Hai chip tên gần giống nhau nằm cách xa~~ ✅ **XONG 24/09/2026** | Đã đưa `Không thấy phiếu xuất` lên ngay sau `Không thấy phiếu nhập` — hai chiều ngược của cùng một việc thì để cạnh nhau |
| 11 | ✅ ~~**Nâng 3 GitHub Action lên bản chạy Node 24**~~ — **XONG 29/09**: token `gh` đã có scope `workflow` (cấp 29/09, 14:40); `checkout@v7` · `setup-python@v7` · `action-gh-release@v3` + `paths-ignore` (`**.md`, `docs/**`, `docs-cu/**`) | Từ nay push chỉ tài liệu **không** build lại EXE ⇒ hết vòng lặp "push .md là lệch SHA". Mục nhật ký *29/09/2026 — Việc 11, 40, 24, 25* |

### ⚠️ Giới hạn thiết kế — KHÔNG phải lỗi, đừng "sửa giúp"

| Giới hạn | Vì sao cố ý |
|---|---|
| **Thu hồi quyền chỉ có hiệu lực khi người đó đăng nhập lại — hoặc bấm Tải lại** (từ v2.0.9) | Quyền chốt MỘT LẦN lúc đăng nhập. Gọi Google ở mọi request thì mỗi cú bấm chờ 1–3 giây. Nút **Tải lại** hỏi Google một lần: quyền đổi ⇒ đăng xuất. **Không tự đá ra** khi quản trị vừa sửa — người đó phải bấm Tải lại hoặc đăng nhập lại |
| **Mất mạng vẫn vào được 7 ngày bằng mật khẩu cũ** trên máy khác | Bản cache offline — cùng mô hình credential-cached như Windows domain. Nút "Tải lại" chỉ kiểm phiên của **chính mình** |
| **Khởi động lại app là phải đăng nhập lại** | Kho phiên nằm trong RAM. Đổi lại là quay về [Bẫy 17](CLAUDE.md) — mật khẩu SQL nằm đọc được trong cookie |
| Tab điều chuyển nội bộ **6–8,5 giây/tháng** | Dựng lại toàn bộ CTE mỗi lần gọi, ngang `btp_reconcile`. Nút thắt gốc là RAM của SQL Express, không phải code |
| `PO.EMPLOYEE_ID` **trống** ⇒ cột Người lập luôn rỗng | iPOS không ghi. Giữ cột phòng sau này có |
| **Tài khoản vừa bị khoá / xoá vẫn vào được 3–30 giây** *(từ 25/09, nhánh `giaodien`)* | Đánh đổi của **đăng nhập nhanh** — Đại Ca chốt. Google trả lời xong thì bị đá ra. Không làm thế thì mỗi lần đăng nhập chờ Google **~12–35 giây**. ⚠️ Từ việc 42 (28/09): lúc đó mà Google **chưa trả lời được** (bận, lỗi dịch vụ) thì người đó **dùng hết phiên đó**, lần đăng nhập nhanh sau mới bị đá — cùng mô hình với lúc mất mạng |
| Đăng nhập nhanh **chỉ áp cho người đã đăng nhập thành công trên CHÍNH máy đó trong 7 ngày** | Lần đầu, quá hạn, gõ sai hoặc vừa đổi mật khẩu ở máy khác ⇒ **vẫn chờ Google như cũ**. Cố ý: nhờ vậy đường nhanh không né được giới hạn gõ sai |

---

---

## 09/10/2026 — Việc 52: màn Điểm sử dụng thêm bộ lọc hạn bảo trì · phát hành v2.1.5

Đại Ca: *"Cái tab điểm sử dụng cho thêm điều kiện lọc đi m, đang không lọc được"* (trước đó màn này chỉ có ô tìm chữ) ⇒ chọn
mốc *"0 ngày, dưới 30 ngày, hơn 30 ngày"*; rồi *"ok ra bản v2.1.5 luôn, sửa màu đỏ luôn, làm các bước còn lại luôn và cập nhật nhật ký"*.
- `index.html` (chỉ giao diện, máy chủ không đổi):
  - **Hàng chip ngay dưới thanh trên** (`DSD_LOC_HAN`), cùng kiểu hàng chip trạng thái 3 màn đối chiếu (chọn MỘT, "Tất cả" đầu):
    Tất cả · **Hết hạn** (còn ≤ 0 ngày, gồm quá hạn) · **Dưới 30 ngày** (1–30) · **Hơn 30 ngày** (> 30) · **Chưa điền hạn** (thêm —
    thiếu nó thì dòng chưa có ngày hết hạn không thuộc mốc nào, không lọc ra được). Số trên chip = số dòng của nhóm trên **toàn danh
    sách** (không trừ ô tìm). Kết hợp được với ô tìm; chân bảng ghi `N dòng / tổng` khi đang lọc.
  - Nhóm tính bằng `dsdNhomHan` — **khớp màu ô "Còn"** (`OConNgay`) và chú thích chân bảng; đổi mốc thì đổi cả 3 chỗ.
  - Ô "Còn" = 0 ngày ⇒ chữ đỏ **"Hết hạn hôm nay"** (trước: "0 ngày" màu cam, lệch với chip "Hết hạn"). Chú thích chân bảng:
    *Còn 1 – 30 ngày* · *Hết hạn / quá hạn*.
  - **Cột "Còn" 104 → 124px**: "Quá hạn 280 ngày" cần 114px — từ v2.1.3 bị cắt thành *"Quá hạn 12 n…"*. Ghi chú còn ~152px ở 1366.
  - Bản đầu đặt chip chung hàng với ô tìm ⇒ đo 1366px: 4 chip chiếm 455px, 2 nút **Gia hạn** + **Đồng bộ** rớt xuống dòng ⇒ chuyển chip
    xuống hàng riêng.
- 🧪 M1 Babel OK · server thử 5052 (nạp `server.py` **bỏ dòng `kill_process_on_port(5050)`** — EXE Đại Ca lúc đó đang mở; dữ liệu
  giả 10 dòng; **không gọi Google**): từng chip, chip + ô tìm, không khớp, về Tất cả — đều đúng dòng, đúng số. 1366 + 1280px: hàng trên
  1 dòng, chip 1 dòng; cột Còn hết cắt ở 1366. ⚠️ 1280px bảng cuộn ngang 22px — **có từ trước** (`minWidth: 1060` > khung 1038px).
- Build `python build_exe.py iPOS_Accounting_Report` ⇒ **2.1.5** (12:53 — app Đại Ca đã tự tắt trước đó, không build đè app đang chạy).
  **M3:** chạy EXE tách hẳn ⇒ `/api/version` 2.1.5 · trang dịch sẵn, không còn `babel-standalone` · có `dsdNhomHan`, chữ "Hết hạn hôm
  nay", cột Còn 124.
- `CO_GI_MOI.md` `## v2.1.5` 2 dòng — mô phỏng `_tach_co_gi_moi`: máy 2.1.4 thấy đúng 2 dòng, máy 2.1.2 thấy 4.
- Kiểm trước push: `ast` OK · không trùng tên hàm · route chưa khai quyền `[]` · quét secret sạch.
- ⚠️ Chưa xem với Google Sheet thật (86 dòng) — lọc chạy hoàn toàn ở trình duyệt nên nguồn dữ liệu không ảnh hưởng. Chuyển màn
  rồi quay lại ⇒ bộ lọc về "Tất cả" (giống ô tìm).
- **Phát hành:** push `be2c6fe..b43bafa` ⇒ Actions run `37891117690` **`success`** ⇒ Release **`v2.1.5` = `Latest`**, tag → `b43bafa`,
  digest EXE `1414d115…` (13.726.444 B), `CO_GI_MOI.md` tại tag đúng 2 dòng.
- **Cập nhật thật 2.1.4 → 2.1.5:** đặt lại file CI v2.1.4 (SHA `deaf52d7…`, cất ở scratchpad trước khi build) vào `dist\` (bản build
  local 2.1.5 cất ở scratchpad) → mở → `check_update` ⇒ `has_update`, "Có gì mới" đúng 2 dòng, sha256 = digest → **Đại Ca tự bấm Cập nhật
  trên hộp thoại** (agent gọi `apply_update` cùng lúc ⇒ nhận `busy`, vô hại) ⇒ tải ~8s ⇒ `dist\` **SHA = digest CI** · gọn 3 file (bản mới
  đã tự dọn `.old` ⇒ đã khởi động được; cửa sổ sau đó bị đóng nên app tắt) ⇒ mở lại: `/api/version` 2.1.5 · hết báo cập nhật · trang
  dịch sẵn có bộ lọc. App để đang chạy.

---

## 08/10/2026 (khuya) — Phát hành v2.1.3 + v2.1.4 (màn Điểm sử dụng · sửa "Có gì mới")

Đại Ca: *"làm các phần còn lại đi nha, phát hành luôn để done"*.
- **v2.1.3:** push `bc17c21..819a739` (3 commit `c8cb929` · `a328214` · `819a739`) ⇒ Actions run `37810460023` **`success`** (~1,5 phút)
  ⇒ Release **`v2.1.3`**, tag → `819a739`, digest EXE `5253c621…` (13.725.350 B). **Cập nhật thật**: tải file CI v2.1.2 (SHA = digest
  `907a7481…`) vào `dist\` (bản build local 2.1.3 cất ở scratchpad) → chạy → `check_update` báo v2.1.3 → `apply_update` **~14s** ⇒
  2.1.3, `dist\` SHA = digest CI, gọn 3 file, hết báo cập nhật, trang dịch sẵn.
- ⚠️ **Đại Ca thấy hộp thoại cập nhật ghi *"Thanh bên trái: Báo cáo tài chính chuyển xuống cuối danh sách"*** ⇒ chốt: *"phải là thêm danh
  sách điểm sử dụng và cập nhật hệ thống mới đúng"*. App đọc `CO_GI_MOI.md` **tại tag** ⇒ v2.1.3 không sửa được ⇒ ra **v2.1.4 code y
  v2.1.3** (như v2.0.4). Mục `## v2.1.4` + `## v2.1.3` đều = *Thêm danh sách điểm sử dụng* · *Cập nhật hệ thống* (hàm `_tach_co_gi_moi`
  xếp bản mới trước ⇒ nếu v2.1.4 chỉ có "Cập nhật hệ thống" thì dòng đó đứng TRƯỚC — mô phỏng thấy, nên ghi đủ 2 dòng đúng thứ tự).
  **Số hiệu tăng TAY** (`version.txt` + `version_info.txt`): app 2.1.3 đang chạy ở `dist\` ⇒ không build đè (Bẫy 10); code không đổi.
- **v2.1.4:** push `819a739..6068716` ⇒ run `37811273435` **`success`** ⇒ Release **`v2.1.4` = `Latest`**, tag → `6068716`, digest EXE
  `deaf52d7…` (13.724.672 B), `CO_GI_MOI.md` tại tag đúng 2 dòng. **Cập nhật thật 2.1.3 → 2.1.4**: hộp thoại (đọc từ GitHub) đúng 2 dòng ·
  **~7s** · `dist\` **SHA = digest CI** · gọn 3 file · hết báo cập nhật · trang dịch sẵn. App để đang chạy.
- Đã tắt server xem 5051 + đóng tab Chrome của agent. Bảng *Lịch sử push* (`GITHUB_LEDGERREPORT.md`, ngoài repo) đã thêm 3 dòng.
- ⏭️ Còn: thử **tài khoản không phải ADMIN** (chưa tick ⇒ không thấy màn; tick `diem_su_dung` ⇒ vào được) — cần Đại Ca đăng nhập.
  7 điểm để trống ngày (03, 71, 73, 76, 77, 78, 79) Đại Ca tự điền. 72 dòng trong danh sách hết hạn 09/10/2026 ⇒ gia hạn khi HĐ BTKT chốt.

---

## 08/10/2026 (khuya) — Thanh bên: Điểm sử dụng lên trên, Báo cáo TC xuống cuối · build v2.1.3

Đại Ca: *"chổ thanh tác vụ thì điểm sử dụng đưa lên trên, báo cáo tài chính nằm dưới cuối cùng, làm các phần việc còn lại luôn đi"*.
- `index.html` — `PHAN_HE`: đổi chỗ `diemsudung` ↔ `baocao` ⇒ cột phân hệ + thẻ Trang chủ: … Kho · Điểm sử dụng · **Báo cáo tài chính**
  (cuối); Phân quyền vẫn **sát đáy cột** (khối riêng). Nhánh "Khác" (`ds.length - 1`) lại chèn **ngay trước Báo cáo TC** như trước việc 51.
  Người không có quyền `diem_su_dung` chỉ thấy Báo cáo TC chuyển xuống cuối.
- Kiểm: Babel OK · `ast` OK · 206 hàm / 80 route, không trùng · route chưa khai quyền `[]` · quét secret sạch (chỉ chữ "token" trong
  nhật ký) · xem trên server 5051 (ảnh: cột trái đúng thứ tự). `CO_GI_MOI.md` `## v2.1.3`: *"Thanh bên trái: Báo cáo tài chính chuyển
  xuống cuối danh sách"* + *"Cập nhật hệ thống"* (màn Điểm sử dụng chỉ quản trị thấy) — mô phỏng `_tach_co_gi_moi`: máy 2.1.2 thấy 2 dòng.
- Build `python build_exe.py iPOS_Accounting_Report` ⇒ **2.1.3** (23:31). **M3:** chạy EXE tách hẳn ⇒ `/api/version` 2.1.3 · trang dịch sẵn,
  0 thẻ `text/babel` · bản dịch có `diemsudung` đứng trước `baocao` ⇒ tắt EXE thử.
- ⚠️ Chưa thử tài khoản **không phải ADMIN** trên Google thật (cần Đại Ca đăng nhập tài khoản nhân viên — agent không gõ mật khẩu);
  phía máy chủ đã thử 403 ở M2 (việc 51).

---

## 08/10/2026 — Việc 51: màn "Điểm sử dụng" (điểm đang dùng phần mềm kế toán + thời hạn bảo trì) · ✅ commit local (CHƯA push) · ✅ Apps Script Version 6

> **Triển khai Apps Script 08/10/2026 22:25 — Version 6, cùng Deployment ID** (`AKfycbx8Zr…`, khớp `server.py` + `ketnoi.json`),
> `ping` ⇒ `{"ok": true, "ban": "2026-10-08a"}`. Cách làm (Đại Ca bảo tự xử, mở sẵn Chrome): đối chiếu bản trong trình soạn với git
> `HEAD~1` bằng SHA-256 **ngay trong trang** (chuẩn hoá dòng token về chuỗi giữ chỗ — khớp, tức Google = Version 5 không ai sửa tay) ·
> dán Code.gs repo vào ô tạm + so SHA-256 (khớp) · ghi vào Monaco **dòng 1–35 và 37–hết, KHÔNG đụng dòng 36 (`const TOKEN`)** ⇒ token
> thật không đi qua clipboard / khung chat · so SHA-256 lần nữa (khớp repo trừ dòng token) · Lưu · Quản lý bản triển khai → ✏️ → Phiên
> bản mới. Nút **Deploy cuối do Đại Ca bấm** (chế độ tự động chặn agent triển khai bản đang chạy thật).
>
> **Đại Ca hỏi: "Ngày bắt đầu" lấy được từ log ngày thêm đơn vị không? ⇒ KHÔNG.** Đo DB thật 08/10:
> - `DM_ORGANIZATION` / `ORGANIZATION_MAPPING` **không có cột ngày** nào.
> - `LOGGING` ghi thêm/sửa `DM_ITEM`, `DM_JOB`, `DM_WAREHOUSE`, `DM_PR_DETAIL`, `organization_mapping` (gắn máy POS ↔ đơn vị ↔ người
>   dùng)… nhưng **không có một dòng nào về thêm `DM_ORGANIZATION`** — cả `IACC_CHULONG` (log từ 17/05/2026) lẫn `IACC_CHULONG_2025`
>   (log từ 05/09/2025). Dò `LIKE` trên 3 triệu dòng LOGGING mất ~143s, nhóm theo tên bảng ~14s.
> - Log gắn máy POS **muộn hơn** ngày bán đầu (đơn vị 80: bán 28/08, log 03/09; 82: bán 05/10, log 08/10) ⇒ không dùng làm ngày bắt đầu.
> - Gần nhất là **ngày bán đầu tiên của máy POS** (`SALE.WORKSTATION_ID`, gộp 2 DB: `IACC_CHULONG_2025` SALE từ 09/01/2025 +
>   `IACC_CHULONG`): **~66/86 dòng rơi vào 25/08–01/09/2025** = đợt nối POS vào kế toán đồng loạt ⇒ chỉ biết "dùng từ trước"; ~16 điểm mở
>   sau đó có ngày tin được (vd 19 → 01/11/2025 · 74 → 17/01/2026 · 03 → 23/03/2026 · 82 → 05/10/2026).
> - ⚠️ **7 mã đơn vị bị đổi tên / dùng lại giữa 2 DB** (01, 03, 43, 60, 71, 72, 73 — vd `72` năm 2025 là xưởng *XU-BTA-8C*, nay là
>   *HKD Nông Sản Việt*) ⇒ ngày theo **mã đơn vị** của năm cũ có thể là của đơn vị khác; phải theo **máy POS**.
> - **Soi lại kỹ (Đại Ca hỏi lần 2):** lập *từ điển mọi dạng dòng* LOGGING của cả 2 DB (~20.000 dạng, bỏ chứng từ theo `SYS_TRAN`) ⇒ **không
>   có dạng nào là thêm/sửa đơn vị**. Nhưng **suy gián tiếp được** = lần đầu mã đơn vị xuất hiện trong log (tạo kho `Org:xx`, tài khoản
>   `Đơn vị:xx`, gắn máy POS, chứng từ đầu tiên) — chỉ có nghĩa với mã tạo **sau khi log bắt đầu**: `74` ≤ 18/12/2025 15:18 · `75` ≤
>   26/12/2025 14:12 · `80`, `81` sáng 21/07/2026 (kho tạo 09:22/09:23, `DM_JOB` 09:00) · `82` 18/09/2026 trong khoảng 10:04–15:47 (kho
>   `CH.00081` tạo lúc 10:04 còn `Org:00`, 15:47 chuyển `Org:00->82`) · xưởng `69`–`73` 13–17/09/2025 (⚠️ `71`–`73` sau này đổi thành cửa
>   hàng ⇒ ngày tạo mã ≠ ngày mở). Mã `01`–`68`, `76`–`79` có từ trước khi log bắt đầu ⇒ không biết. Ngày tạo mã **sớm hơn** ngày bán đầu
>   vài tuần (`80`: tạo 21/07, bán 28/08) ⇒ hai mốc khác nghĩa. Script: `do_lan_dau_log.py` (scratchpad phiên c02ece56).
> - ✅ **Đại Ca chốt + đã điền 08/10/2026 23:00 trên Google THẬT** (server xem 5051, Đại Ca tự đăng nhập + tự bấm **Đồng bộ** lần
>   đầu 22:31 ⇒ **86 dòng**): **72 dòng có trong `Danh sách điểm bảo trì_TỔNG_MÃ POS.xlsx`** (67 máy POS khớp mã POS + 5 dòng không POS:
>   VPCTY↔01, CHSVAM↔66, XUHUDTD↔69, XUHN111TD↔70, XUBTA8C↔72 — kể cả 4 dòng 0 đồng) ⇒ **10/10/2025 – 09/10/2026** (1 lần gọi
>   `gia_han`). **7 điểm ngoài danh sách có ngày tạo kho trong log** ⇒ từ ngày tạo kho, hết hạn +12 tháng − 1 ngày (7 lần `luu`):
>   19 22/10/2025 · 06 21/11/2025 · 12 24/11/2025 · 74 18/12/2025 · 75 25/12/2025 · 80 21/07/2026 · 82 18/09/2026. **7 điểm kho tạo
>   trước khi log bắt đầu ⇒ để trống** (Đại Ca chốt): 03, 71, 73, 76, 77, 78, 79. Đọc lại từ Sheet: **86/86 đúng**, lần BT = 1, không lịch
>   sử. ⚠️ 72 dòng danh sách hết hạn **09/10/2026** ⇒ màn hiện *"Còn 1 ngày"* — gia hạn kỳ BTKT mới khi hợp đồng chốt.
>   Ghi qua đúng API của app (`/api/diem_su_dung/gia_han`, `/luu`) từ tab đã đăng nhập; lệnh JS quá 45s của công cụ nhưng cả 8 request
>   xong (log server 200) — **không chạy lại**, đọc Sheet đối chiếu.
> - **7 điểm để trống — soi thêm (Đại Ca hỏi):** kho + mã CV của cả 7 **chỉ có ở DB 2026** (DB 2025 không có) ⇒ tạo trong khoảng
>   01/01–17/05/2026, đúng quãng LOGGING DB 2026 **không còn** (log bắt đầu 17/05/2026 15:01). Quét LOGGING mọi dòng nhắc mã kho / mã CV /
>   POS (bỏ kiểm kê, ~175s/DB): sớm nhất là người dùng cửa hàng sửa tài khoản 17–18/05 ⇒ đã có từ trước. `SEC_LOG` chỉ là log đăng nhập
>   phần mềm cũ 2013–2016. Mốc gần nhất = **chứng từ kho đầu tiên** (`dbo.WAREHOUSE`): 03 16/03 · 73 25/03 · 71 28/03 · 76, 77 21/04 ·
>   79 16/05 (bán 13/05) · 78 18/06/2026. Đo trên 7 điểm biết ngày tạo: kho tạo **trước** chứng từ kho đầu tiên **2–36 ngày** (19: +2,
>   75: +2, 12: +5, 82: +15, 06: +16, 74: +21, 80: +36) ⇒ chỉ là mốc muộn, không phải ngày tạo.
>   ⇒ **Đại Ca chốt: 7 điểm này để trống, Đại Ca tự điền** (08/10/2026). Không ghi gì thêm lên Sheet.

> **Commit local 08/10/2026** (Đại Ca duyệt, chưa push). Kiểm trước commit: `ast` OK · Babel OK · Code.gs dịch được · quét route chưa
> khai quyền `[]` · quét secret sạch (chỉ 2 chú thích nhắc tên cột `PASSWORD`/`TOKEN`) · Code.gs vẫn giữ chuỗi giữ chỗ `TOKEN` /
> `ADMIN_DK_BOOTSTRAP` (Bẫy 19) · `config.json`, `ketnoi.json` vẫn bị `.gitignore`.

**Bối cảnh.** Sáng 08/10 Đại Ca nhờ ráp **mã POS IC** vào danh sách điểm bảo trì của Chú Long (file Excel **ngoài repo**,
`Desktop\CHU LONG\`: `…_TỔNG_MÃ POS.xlsx` 72 dòng + `…_ĐIỂM MỚI.xlsx` 13 điểm). Mã POS IC = `ORGANIZATION_MAPPING.WORKSTATION_ID`; mã công
việc ↔ đơn vị **không có trong danh mục** (`DM_JOB` không có cột đơn vị, `DM_ORGANIZATION_MAPPING.JOB_ID` trống) ⇒ suy từ phiếu bán.
Đọc 2 hợp đồng .docx cùng thư mục: điểm mới mua bản quyền 3.000.000 ⇒ bảo hành 12 tháng ⇒ hợp đồng bảo trì **600.000/điểm/năm**
(BTKT 40.800.000, tự gia hạn). ⚠️ **HĐ BTKT ghi thời hạn *"từ 10/10/2026 đến 09/10/2026"* — sai năm, đã báo Đại Ca.**
⚠️ Máy `92042` (vốn của 421 Cộng Hoà) nay chạy cho **526 Quốc Lộ 50** (đơn vị 81, `CH00080`) từ 27/08/2026 **mà vẫn ghi đối tượng
`TN.421CH`** — cấu hình bên iPOS, đã báo, app không sửa. Rồi Đại Ca muốn theo dõi thời hạn **trên LedgerReport**.

**Đại Ca chốt** (qua nhiều vòng phác thảo — **mục 09** của https://claude.ai/artifact/7kiiWQ13PPR7eXN2AgPhtc, 6 khung 09A–09F):
- Bảng danh sách điểm + nút **Đồng bộ**: dò `DM_ORGANIZATION` (bỏ 10 dòng nhóm `ORGANIZATION_TYPE='01'`) ⇒ **82 đơn vị**; tự thêm mã điểm · tên ·
  POS ID · mã kho · mã công việc vào Google Sheet **"Danh sách điểm sử dụng"** (cùng file với tài khoản). Đơn vị 2 máy POS ⇒ **2 dòng** ⇒ **86 dòng**.
- **Chỉ đọc DB khi bấm Đồng bộ** (*"đơn giản, giảm tải tài nguyên"*); vào màn chỉ đọc Sheet. **Đồng bộ chỉ THÊM điểm mới** — dòng đã có không
  đụng ô nào (kể cả ô trống), không xoá dòng nào.
- Ngày **điền TRÊN APP**, app ghi lên Sheet (lúc đầu Đại Ca hiểu nhầm là điền thẳng trên Sheet). **Bảng chỉ xem** — bấm nút bút chì mới mở
  hộp sửa (*"tránh nhầm"*); **mọi ô sửa tay được**.
- Ngày bắt đầu + ngày hết hạn + **số lần bảo trì + lịch sử** (một ô chữ). **Gia hạn = Từ ngày · Đến ngày · Lưu** (*"làm đơn giản thôi"* — bỏ
  hộp so sánh trước/sau, bỏ chip "Bảo hành"); gia hạn nhiều dòng một lần (HĐ gia hạn cả loạt ngày 10/10).
- **Chỉ ADMIN thấy** (mã quyền `diem_su_dung`, chức vụ khác tick ở tab Phân quyền).

**Cách làm**
- **`phanquyen_gas/Code.gs`** (`BAN_CODE` **`2026-10-08a`**, thêm `diem_su_dung` vào `PERM`): khối *DANH SÁCH ĐIỂM SỬ DỤNG* cuối file — sheet
  (3 hàng tiêu đề như 3 sheet cũ, ô dữ liệu định dạng **chữ** để giữ `01` và `dd/mm/yyyy`) + 4 lệnh `doc_diem` · `dong_bo_diem` · `luu_diem` ·
  `gia_han_diem`. Xác thực bằng **tài khoản đang dùng app** (uid + mã đã băm), ADMIN hoặc có mã `diem_su_dung`. Cột ẩn **`KHOA`** (mã điểm|POS ID
  chụp lúc thêm, không ai sửa) ⇒ sửa tay mã điểm / POS ID không sinh dòng trùng; cột ẩn **`GOC_*`** giữ giá trị DB lúc thêm. Mọi lệnh **chịu được
  gọi lại** (`_gs_goi` tự gọi lại): thêm theo KHOA · `luu_diem` ghi đè cùng giá trị, **chặn ghi đè mù** khi ô vừa bị sửa nơi khác · `gia_han_diem`
  so kỳ cũ app đang thấy (đã là kỳ mới ⇒ "đã có", không cộng lần hai). Mỗi lần ghi 1 dòng vào sheet Nhật ký.
- **`server.py`** (+7 hàm, +4 route): mã quyền + nhãn + `PERM_ROUTE_STATIC`; `_gs_tk_phien` (mã băm trong kho phiên RAM — Bẫy 17), `_gs_diem`,
  `_diem_doc_db`, route `/api/diem_su_dung` (GET) · `/dong_bo` · `/luu` · `/gia_han`. ⛔ Lỗi phía Google **không trả 401** (Bẫy 1): thiếu mã băm
  400 · mất mạng 503 · Apps Script cũ ⇒ *"cần bản 2026-10-08a"*. Đồng bộ giữ khoá DB **chỉ trong lúc chạy SQL**, xong mới gọi Google.
  ⛔ `ORGANIZATION_MAPPING` có cột `PASSWORD` / `TOKEN` — câu SQL chỉ chọn đúng 3 cột.
- **`index.html`**: `MAN_RIENG` + `timManHinh` (⛔ **không nhét vào `DOC_TABS`** — checklist Phân quyền xếp DOC_TABS vào nhóm "Danh sách chứng từ"),
  phân hệ `diemsudung` trong `PHAN_HE`, icon `map-pin` / `pencil`, mã quyền ở nhóm *Quản trị*, component `DiemSuDung` + `HopSuaDiem` +
  `HopGiaHanDiem` + `HopKetQuaDongBo`.

**Số đo DB thật**: 5 câu đọc, câu phiếu bán 60 ngày (suy mã CV) **6,5s**, cả lượt **6,7–8,6s**. **86 dòng** · 6 dòng không máy POS (Kho tổng HCM,
Kho tổng HN `78`, Seven AM, 3 xưởng) · 1 dòng thiếu mã CV (`66` Seven AM — không bán từ 01/08) · **80/80 máy POS khớp mã CV + mã kho** với 2 file đã đối chiếu.

**🧪 Verify**
- **M1:** `ast` OK · **206 hàm / 80 route**, so `HEAD` mất **0** hàm, **0** route · không trùng tên · quét route chưa khai quyền **`[]`** · Babel OK ·
  Code.gs dịch được (`new Function`).
- **Code.gs trên Google giả lập** (node, Sheet trong bộ nhớ, `Utilities`/HMAC thật): **35/35**.
- **M2:** `server.py` thật (nạp **bỏ dòng tắt cổng 5050**) + Code.gs trên node + **DB thật**: **29/29** — gồm **403** ở cả 4 route cho chức vụ không có
  mã, chức vụ được tick thì vào được, mất mạng 503, phiên thiếu mã băm 400.
- **Giao diện:** server thử **5052** (DB thật + Google giả lập) + Chrome ngầm **1366×768**: đồng bộ 86 dòng · hộp kết quả · sửa `K.TONG → VPCTY`
  (hiện *"Từ DB lúc thêm dòng"*) · hỏi trước khi bỏ thay đổi · gia hạn 1 dòng + 3 dòng · lịch sử *"Lần 1"* · tìm không dấu · sắp theo cột Còn.
  **Sửa trong lúc thử:** cột Ghi chú bị ép còn **41px**, tiêu đề đè cột Sửa ⇒ cộng lại độ rộng còn **157px** · hộp kết quả hiện trước khi bảng nạp
  xong ⇒ đổi thứ tự · nhãn ô ngày IN HOA ⇒ chữ thường · dấu "—" lơ lửng dưới ô hết hạn trống ⇒ bỏ.
- ❌ **Chưa:** M3 (EXE) · **Google THẬT** (Code.gs đã triển khai 08/10 22:25, chờ thử) · tài khoản không phải ADMIN trên Google thật.

**⏭️ Còn**
1. **Đại Ca triển khai Code.gs**: `python phanquyen_gas/chuan_bi_deploy.py` → dán → *Triển khai → Quản lý bản triển khai → ✏️ → Phiên bản mới*
   (⛔ không "Triển khai mới") → `ping` phải ra **`2026-10-08a`**.
2. Thử lại trên Google thật (đồng bộ lần đầu ~86 dòng, sửa, gia hạn).
3. `CO_GI_MOI.md` (màn này chỉ ADMIN thấy ⇒ hỏi Đại Ca ghi gì) · build · phát hành — **hỏi trước khi commit / push**.
⚠️ Phát hành EXE mà **chưa** triển khai Code.gs ⇒ màn mới báo *"Bản Apps Script trên Google chưa có chức năng này"*; các màn khác không ảnh hưởng.
Script thử nằm ở scratchpad phiên `ec0e7817` (`thu_code_gs.js`, `gs_gia_lap.js`, `thu_m2.py`, `server_thu_5052.py`, `cdp.py`) — đã tắt server thử + Chrome ngầm.

---

## 06/10/2026 (rạng sáng) — Phát hành v2.1.2 (sửa lệch 4px cột ghim phải)

Đại Ca: *"phát hành v2.1.2 luôn đi"*.
- `CO_GI_MOI.md`: `## v2.1.2` 1 dòng. Build tự tăng ⇒ **2.1.2**; M3: `/api/version` 2.1.2, trang dịch sẵn, 0 thẻ Babel, có CSS sửa.
- Commit `4c9e567` (sửa) + `8d478d7` (số hiệu / CO_GI_MOI). Push `ea0d756..8d478d7` ⇒ Actions run `37344901415` **`success`** ⇒ Release
  **`v2.1.2` = `Latest`**, tag → `8d478d7`, digest EXE `907a7481…` (13.706.759 B).
- ✅ **Cập nhật thật 2.1.1 → 2.1.2** từ file CI v2.1.1 (`f26268b8…`): "Có gì mới" 1 dòng · **~11 giây** · `dist\` **SHA256 = digest CI** · gọn
  3 file · hết báo cập nhật · trang dịch sẵn. App để đang chạy. Bản build local 2.1.2 cất ở scratchpad.

---

## 05/10/2026 (khuya, tiếp) — Xoá mật khẩu config.json · sửa lệch 4px cột ghim phải · thử lại "đứng hình"

Đại Ca: *"xoá password trong config.json đi, và hoàn thành các mục còn lại luôn nha"*.
- **`config.json`**: xoá đúng ô `password` (giữ server / database / user / driver). Rà các thư mục nháp cũ + repo tìm bản chép: chỉ thấy
  mật khẩu giả của phép thử (`x`, tài khoản thử) và chữ minh hoạ `MatKhau…` trong nhật ký — không thấy bản chép mật khẩu SQL thật.
- **Lệch 4px** (Tồn kho thực tế, ghim phải, cuộn chạm cuối) — tái hiện bằng server dữ liệu giả 5052: khung cuộn 1.560px, bảng 1.556,5px.
  Lần lượt loại: CSS ghim (bỏ hết vẫn 1.560), bóng mép, lớp nền tràn 1px, dòng đệm `colSpan=100`, viền gộp. **Gốc: tay kéo đổi độ rộng
  (`th::after`, `right:-4px; width:8px`) của CỘT CUỐI thò ra ngoài bảng 4px** ⇒ khung cuộn rộng thêm, `position: sticky` không vượt được mép
  bảng nên cột ghim phải hụt đúng phần đó. Có ở **cả 9 bảng** (cùng CSS), chỉ thấy rõ khi ghim phải. Sửa: tay kéo cột cuối `right:0` (vạch
  xanh khi rê chuột dời vào trong). Sau sửa: khung 1.557 = bảng (làm tròn), cột ghim cách mép < 1px; kéo cột cuối vẫn ăn (96 → 156px, lưu đúng).
- **"Đứng hình sau khi Lọc"** — Chrome chạy ngầm (giống lần treo), 12.000 dòng giả, máy chủ trả chậm 3s:
  - 6 lượt nạp × 4 Lọc **có** làm mờ nền + 6 × 4 **không** làm mờ + lặp lại 3 × 4 mỗi bản + ca nặng (ghim 4 cột, Vừa khít tất cả, bấm Lọc
    3 lần dồn lúc đang tải) 4 × 4 = **88 lượt, 0 lần treo, 0 lỗi JS**. Lọc 3,2–3,4s (= độ trễ giả), Vừa khít tất cả 0,6–0,8s.
  - Làm mờ nền **không** đổi tốc độ: lượt sau chạy bản nào cũng ~66ms/khung cuộn (lượt đầu 33ms) — chậm dần theo thời gian Chrome chạy,
    không theo làm mờ ⇒ **bác giả thuyết `backdrop-blur`**, không sửa gì. 3 lần treo trước đều trùng lúc DB thật rất chậm (màn Tổng hợp 13 phút);
    chưa có nhân viên nào báo. Giữ theo dõi.
- Babel OK. Server thử 5052 + Chrome ngầm đã tắt. Sửa `index.html` (CSS 2 dòng) ⇒ Đại Ca bảo phát hành ngay: **v2.1.2** (mục trên).

---

## 05/10/2026 (khuya) — Phát hành v2.1.1 (BC017 + việc 50)

Đại Ca thử đợt 2 trên server xem 5051: chức năng OK → đổi icon ghim (mẫu A) → bỏ chú thích cuối hộp → *"commit luôn"* → *"phát hành luôn đi"*.
- Trước push: Babel OK · 199 hàm, không trùng tên · quét route chưa khai quyền `[]` (76 route) · quét secret sạch · `config.json` vẫn bị
  `.gitignore`. ⚠️ Skill `pre-push-qa` **không có** trong phiên này ⇒ chưa chạy; thử tài khoản không quản trị đã làm ở đợt 1 (403 đúng) — lượt
  này không thử lại.
- `CO_GI_MOI.md`: thêm `## v2.1.1` 5 dòng. Build `python build_exe.py iPOS_Accounting_Report` (tự tăng) ⇒ **2.1.1**. M3: `/api/version` 2.1.1,
  trang dịch sẵn, 0 thẻ Babel, có icon ghim mới + BC017.
- Commit `a9ba070` (code + tài liệu) + `1a8fe20` (số hiệu / CO_GI_MOI). Push `2dd96bb..1a8fe20` (git push thường) ⇒ Actions run
  `37340710783` **`success`** ⇒ Release **`v2.1.1` = `Latest`**, tag → `1a8fe20`, digest EXE `f26268b8…` (13.708.235 B). `CO_GI_MOI.md` tại tag
  có mục mới.
- ✅ **Cập nhật thật 2.1.0 → 2.1.1** từ file CI v2.1.0 (`740b6eaa…`): `check_update` báo đúng 5 dòng · `apply_update` ⇒ **~10 giây** chạy 2.1.1
  · `dist\` **SHA256 = digest CI** · `dist\` gọn 3 file · hết báo cập nhật · trang dịch sẵn. App để đang chạy. Bản build local 2.1.1 cất ở scratchpad.
- ⚠️ **BC017 là mục quyền mới** ⇒ ADMIN thấy ngay; chức vụ khác phải được tick BC017 ở tab Phân quyền (Google tự tạo cột — Bẫy 22).

---

## 05/10/2026 (tối) — Việc 50 đợt 2: ghim cột bất kỳ sát lề trái / phải + vừa khít cột · 9 màn danh sách

Đại Ca 05/10: *"ok rồi, làm tiếp đợt 2 đi"*. Theo đúng 2 điểm đã chốt: **ghim cột bất kỳ, cột ghim dời hẳn về lề** (không phải kiểu Excel
"cố định tới cột này" — em đã báo là phải sửa cách vẽ cả 9 bảng) · **bấm đúp mép phải tiêu đề = vừa khít, thêm nút "Vừa khít tất cả cột"**,
đo theo mọi dòng đang tải.

### Cách làm (chỉ `index.html`, máy chủ không đổi)
- **`HangCot`** bọc 27 hàng (9 × tiêu đề + ô tìm, 5 hàng dữ liệu component, 4 hàng viết thẳng) — sắp lại ô theo thứ tự hiện
  `# + ghim trái · không ghim · ghim phải` lấy từ `CotBangCtx` (`ctxCotBang`). Đã đếm: mọi hàng đúng số cột `COT_BANG` (34/44/29/31/28/15/21/19/17),
  không ô điều kiện.
- **`veDongCot`** dựng 5 dòng nhóm (`DongNhom` dùng chung) + 5 dòng tổng — thay các `colSpan` ghi cứng theo vị trí.
- **Độ lệch sticky đo từ độ rộng thật** sau mỗi lần vẽ (`apDungGhim`, kèm ResizeObserver) — bảng tự nở theo nội dung nên không ghi cứng được.
- Ẩn cột / độ rộng (`cssCot`) + kéo giãn (`tim` trong effect kéo) đổi sang **vị trí đang hiện**.
- **Vừa khít** (`vuaKhitCot`): max của tiêu đề, ô đang vẽ (Range) và **mọi dòng đã tải** (canvas measureText theo phông của ô); trần 900px;
  cột vừa khít bỏ trần `max-width` của ô (Diễn giải cắt ở 250px). Kéo tay ⇒ bỏ dấu vừa khít. **Về mặc định** xoá cả ẩn / rộng / ghim / vừa khít.
- Cấu hình cột của 9 màn: mỗi dòng thêm 2 nút ⇤ ⇥ (bấm lại = bỏ ghim), chân bảng cấu hình thêm "Vừa khít tất cả cột". Lưu `lr_cot_<tab>`
  thêm `ghim: { trai, phai }` + `vua`.

### Sửa trong lúc thử
- **Vệt chữ lọt khe 1px giữa 2 cột ghim liền nhau** (thấy ở Nợ | Có, phóng ảnh ra mới thấy): độ rộng cột lẻ phần thập phân + đường viền gộp.
  Lớp nền giả `::before`/`::after` của ô ghim tràn 1px sang trái + tự vẽ lại đường kẻ 1px (lớp nền che mất đường kẻ của bảng).
- Ghim trái ⇒ nhãn chân bảng "TỔNG TOÀN BỘ TRUY VẤN (2,287,832 DÒNG):" dồn vào vùng ghim hẹp (# + Số CT), **gãy 3 dòng** ⇒ chân bảng đặt nhãn
  ở vùng cuộn. Dòng nhóm giữ nhãn trong vùng ghim (cuộn ngang vẫn biết đang ở nhóm nào) nhưng cắt theo bề rộng vùng ghim, không phình cột.
- Không ghim mà ô đệm cuối dòng tổng vẫn mang `class="border-r"` (bản cũ không có) ⇒ bỏ, chân bảng nay giống hệt bản cũ.
- **Đại Ca thử 05/10: chức năng OK, icon ⇤ ⇥ "xấu quá"** ⇒ vẽ 3 mẫu, Đại Ca chọn **A · ô bảng nhỏ, cột tô ở lề trái / phải** (kiểu cố định
  cột của Excel): chưa ghim tô mờ, đang ghim tô đặc trên nền navy (`ghim-trai[-dang]`, `ghim-phai[-dang]`), icon 16px. Bỏ luôn viền đen
  trình duyệt vẽ quanh nút sau khi bấm (`outline-none` + vòng `focus-visible` xanh nhạt khi đi bằng phím Tab).
- Đại Ca bảo **bỏ dòng chú thích cuối hộp Cấu hình cột** của 9 màn (`ghiChu={false}`; nút ghim vẫn có `title` khi rê chuột). 5 báo cáo +
  BC017 giữ chú thích riêng của chúng (có thông tin "Ngày CT luôn hiện"…). Rồi bảo **commit** ⇒ commit local cùng BC017 (việc 49), chưa push.

### 🧪 Verify (Chrome chạy ngầm 1366×768, server thử 5053, DB thật T01/2026)
- **M1:** Babel OK; `server.py` không đổi trong đợt 2.
- **9/9 màn** (Tổng hợp, Bán hàng, Tiền, Nhập kho, Kho, Tồn kho, Đối chiếu BTP, Đối chiếu điều chuyển, PO): ghim 1 cột trái + 1 cột phải ⇒
  thứ tự đúng (# → cột ghim trái … cột ghim phải), mọi hàng đủ ô, **cuộn ngang 900px cột ghim đứng yên** (đo toạ độ trước/sau bằng nhau),
  dòng tổng đúng ô dưới cột ghim; "Vừa khít tất cả" 0,9–3,6s, **không còn ô nào bị cắt chữ**; "Về mặc định" trả đúng thứ tự gốc; 0 lỗi JS.
- Ledger: bấm đúp mép Diễn giải 256px → 204px (chữ dài nhất trong 10.000 dòng đã tải); vừa khít tất cả 33 cột ~1s. Gom nhóm theo Mã CT khi
  đang ghim: nhãn nhóm trong vùng ghim, tổng nhóm đúng dưới Nợ / Có ghim phải.
- **Hồi quy — KHÔNG ghim (so với bản đợt 1 ở cổng 5054): 9/9 màn giống hệt cả tiêu đề, thân bảng, chân bảng**, bề rộng bảng bằng nhau.
- ⚠️ Chưa so được dòng NHÓM khi không ghim giữa hai bản: SQL Server tối 05/10 rất chậm (màn Tổng hợp **13 phút** mới trả, bình thường ~20s;
  `sys.dm_exec_requests` chỉ thấy câu của phần mềm iPOS từ các máy khác, không có câu dở dang của server thử) ⇒ dừng phép thử nặng để khỏi
  đè thêm lên DB đang có người dùng. Theo code: khác duy nhất ô đệm cuối dòng nhóm `colSpan` = đúng số cột còn lại thay vì 100 — nhìn y nhau.
- ⚠️ Chrome chạy ngầm **treo 3 lần** (trang đứng, tiến trình vẽ + đồ hoạ bận liên tục, trình gỡ lỗi không ngắt được vào JS nào) — đều sau
  nhiều lượt nạp trang liên tiếp hoặc ngay khi dữ liệu về sau lúc DB chậm, **có cả trên giao diện đợt 1** (code danh sách = bản đang phát hành).
  Chạy từng bước thì không treo. Nghi do Chrome không card đồ hoạ vẽ hiệu ứng làm mờ nền (`backdrop-blur`) của tiêu đề bảng — chưa chứng minh.
  Để ý nếu máy nhân viên báo "đứng hình" sau khi Lọc.
- ⚠️ *Tồn kho thực tế*: cuộn chạm tận cùng thì cột ghim phải lệch 4px (bảng 1.556,5px, khung cuộn tính 1.560px — viền ngoài bảng gộp viền).
- ⏳ Chưa: Đại Ca bấm thử · M3 (EXE) · kéo thả tay bằng chuột thật (thử bằng sự kiện giả).

---

## 05/10/2026 — Việc 50 (đợt 1): Cấu hình cột BC007 · BC008 · BC012 · BC015 · BC016

Đại Ca 05/10: *"phần chỉnh cấu hình thêm cột ở BC017 đã ok rồi, xem thử chỉnh luôn ở các báo cáo này"* (ảnh khoanh BC007, BC008, BC012,
BC015, BC016) + *"các phần chứng từ cho phép chủ động freeze cột … sát lề trái hoặc phải, và cho phép auto fix bề rộng của cột"*.
Đã hỏi chốt 4 điểm: **ghim cột bất kỳ** (cột dời hẳn về lề — Đại Ca chọn, dù phải sửa cách vẽ 9 bảng) · **bấm đúp mép = vừa khít + nút
"Vừa khít tất cả"** · **làm cả 5 báo cáo** · **báo cáo trước, danh sách sau** (mỗi đợt Đại Ca thử xong mới làm đợt sau).

### Đo trước khi làm (DB thật)
- `LEDGER_VIEW` ngày 15/09/2026 (92.448 dòng): đối tượng 21% · MCP 37% · công việc 37% · mã hàng 90% · số lượng 68% · nguồn đơn 45% ·
  ghi chú 93% ⇒ bộ cột thêm của sổ BC007/BC008.
- `VOUCHER_VIEW` T09/2026, dòng chạm TK 111/112/113 (150.855 dòng): đối tượng 82–86% · người nộp/nhận 12% · tham chiếu 14% · ghi chú 92% ·
  người lập 100%. ⚠️ Mỗi dòng có HAI phía: thu Nợ 1131 / Có 131 (129.136 dòng) thì khách nằm bên Có; chi 331 ← 112 thì NCC bên Nợ (473/473)
  ⇒ **đối tượng lấy phía đối ứng, ngân hàng lấy phía TK tiền** (BANK_ID của mình — `SCB-526` Sacombank công ty).
- Khoá `SYS_TRAN` (90/90), `DM_ORGANIZATION` (92/92), `DM_BANK` (9/9) đều duy nhất ⇒ JOIN tên không nhân dòng.

### Đã làm
- `server.py` (+5 hàm, không thêm route ⇒ 199 hàm / 76 route): `/api/journal` + `/api/account_details` nhận `cot_them` (`_SO_COT_SQL`,
  `_so_cot_them`, `_so_ban_do_ten`, `_so_gan_cot`) · `/api/cash_book` nhận `cot_them` (`_CB_COT_SQL`, khoá cache kèm cột) · file "Bảng tổng
  hợp" BC007 (xlsx + csv) nhận `cot` (`_SO_COT_XUAT`, `_so_xuat_theo_cot` — cột nào cũng có tên, Bẫy 31). Không gửi gì ⇒ y đường cũ.
- `index.html`: khai báo `COT_SO` / `GOC_SO` / `COT_BC012` / `COT_BC015` / `nhomBC016` / `AN_MAC_DINH_BC`; state `anCotBC` ở App; nút Cấu
  hình cột cho 5 báo cáo (dùng chung `CauHinhCot`, thêm dòng tiêu đề nhóm + `khoaCot` — 9 màn danh sách y cũ); vẽ lại bảng BC007/BC008
  (một bộ vẽ chung) + BC012 (tiêu đề 2 tầng, colgroup theo trọng số) + BC015 + BC016 theo cột đang hiện; giấy nới theo cột khi bật cột thêm.
- Kèm: **thanh phân trang BC012 phải bấm 2 lần mới sang trang** (truy vấn dùng `filters.page` cũ trong closure) ⇒ dùng `_page`.
- Tick cột thêm ⇒ chờ 0,7s sau lần tick cuối mới tải (đo: tick 5 cột = **1** câu SQL; bản đầu là 5 câu xếp hàng).

### 🧪 Verify
- **M1:** `ast` OK — 199 hàm / 76 route, không mất hàm/route so với HEAD, không trùng tên · Babel OK · quét route chưa khai quyền = `[]`.
- **M2 + M4 (DB thật, `test_client`, đối chứng bản trước khi sửa):** BC007 15/09 trang 1 + 50, BC008 TK 111 / 642, BC012 15/09 ⇒ **không xin
  cột thêm: JSON trùng khít bản cũ**; xin hết cột ⇒ cột gốc giữ nguyên, tổng / phân trang / số dư không đổi. BC008 TK 131: tập dòng trùng
  23.217/23.217, chỉ đổi thứ tự trong cùng ngày + số CT (xem CLAUDE.md). Quyền: có quyền 200 · không quyền **403** cả 3 · giới hạn đơn vị
  01 chỉ thấy 01.
- File BC007 "Bảng tổng hợp" theo 24 cột, 15/09: **92.448 dòng = số đếm, tổng Nợ = tổng Có = 4.564.642.999,5** khớp màn; số lượng lẻ giữ
  (0,2 · 17,2); mã giữ chữ (`01`); CSV mã bọc `="…"`. Không gửi `cot` ⇒ file y bản cũ (tiêu đề `Ngày HT`, `TK Nợ`…).
- **Giao diện (Chrome chạy ngầm 1366×768, server 5053, DB thật T01/2026):** 5 báo cáo tick / bỏ tick ⇒ đúng cột, số liệu cột thêm đúng; số
  trên nút = số cột gốc bị ẩn; xuất Excel giữ form BC008 (13 cột), BC012 (tiêu đề 2 tầng + cột thêm), BC016 (25 cột chỉ SL) đúng cột màn;
  bấm xuất BC007 tổng hợp gửi đúng 15 cột rồi **Hủy xuất** — không để lại file dở.
- **Hồi quy:** dựng thêm server 5054 phục vụ `index.html` bản cũ, so nguyên HTML bảng ở mặc định: **BC007 chi tiết (951.944 ký tự), BC007
  tổng hợp, BC008, BC012, BC015, BC016 — giống hệt**, khổ giấy bằng nhau.
- ⏳ Chưa: Đại Ca bấm thử · M3 (EXE) · in PDF khi bật nhiều cột (giấy nới rộng, chưa xem bản in).

---

## 04/10/2026 — BC017: 3 kiểu xem · Chi tiết/Tổng hợp · mặc định BHVAT+BHK · cấu hình cột — việc 49 (tiếp)

Đại Ca thử bản 03/10 rồi đổi hướng qua 4 lượt (mỗi lượt đã hỏi chốt trước khi làm):

1. **3 kiểu xem, Đơn vị luôn ở trên cùng** — Theo đơn vị · Đơn vị → Ngày · Đơn vị → Nguồn đơn (`EXTRA_ID_2`); **bỏ tầng phiếu**,
   dòng dưới cùng vẫn là từng dòng hàng + thêm cột **Số CT, Mã/Tên nguồn đơn**. Kiểu Ngày → Đơn vị → Phiếu của bản 03/10 Đại Ca bỏ.
2. **Chi tiết / Tổng hợp** — tổng hợp chỉ dòng nhóm, tầng cuối không in đậm. Gộp với kiểu xem + "Ẩn dòng 0 đồng" vào một nút
   `ChonKieuBC017` (để riêng thì hàng điều kiện ở 1366px hết chỗ cho ô lọc).
3. **Loại CT mặc định `TRAN_ID IN ('BHVAT','BHK')`** — Đại Ca: *"để đối chiếu doanh thu"*. Tổng mặc định vì vậy KHÔNG còn bằng BC015.
4. **Cấu hình cột** — Đại Ca hỏi *"cho phép thêm hoặc bớt các cột thì sẽ như nào"* ⇒ em đo trước (cột nào có dữ liệu, tốc độ, độ rộng)
   rồi Đại Ca chốt: dùng nút Cấu hình cột như 9 màn danh sách, **13 cột thêm mặc định ẩn**, lọc theo **ngày chứng từ** (không theo
   ngày hoá đơn). Hai chỗ Đại Ca không trả lời, em làm theo đề xuất: bỏ Người lập + Mã máy POS, 8 cột tiền ẩn được.

### Số đo dẫn tới quyết định (T09/2026, BHVAT+BHK, 257.570 dòng)
- Cột trên `SALE_VIEW` **trống 100%**: giá vốn `COG_AMOUNT`, HTTT, nhân viên, số/ký hiệu hoá đơn VAT, tên/ĐT/MST/địa chỉ khách, mã vạch,
  bảng giá, `EXTRA_ID_1` ⇒ không cho chọn. Có dữ liệu 97–100%: kho (75), đối tượng (82), công việc (75), nhóm/loại hàng, nhóm CV (21 tỉnh),
  thuế suất (8% · 0% 739 dòng), ghi chú ("CÀ PHÊ - GRABFOOD"), người lập (98,5% "ADMIN"), mã máy POS (79).
- ⚠️ **Ngày hoá đơn khác ngày chứng từ trên 180.027/257.570 dòng (70%)** — ví dụ BH0612/T09: CT 15/09, HĐ 16/09.

### Sửa trong lúc làm
- 🔴 **Tổng hợp trả 500** — `SELECT INTO #g` gán `NULL` trần thành INT; tổng hợp không còn nhánh dòng hàng định kiểu ⇒ `JOIN DM_EXTRA_2`
  đổi `'CANHAC35K'` sang số ⇒ lỗi 245. Sửa: mọi cột để NULL đều `CAST` kiểu (ghi ngay tại chỗ trong code + CLAUDE.md).
- Bảng chi tiết 17 cột lố 50px ở 1366px ⇒ đệm ô 3px + Mã nguồn đơn được xuống dòng (giữ chữ 10px — Bẫy 27).
- `CauHinhCot` thêm `ghiChu` / `demAn` / `laMacDinh` (không truyền ⇒ 9 màn danh sách y cũ): BC017 ở mặc định từng hiện *"đang ẩn 13 cột"*.

### 🧪 Verify (DB thật; server thử 5052 + `test_client`)
- **M1:** `ast` OK — 196 hàm / 76 route, không trùng, không mất hàm/route so với HEAD · Babel OK · quét route chưa khai quyền = `[]`.
- **3 kiểu chi tiết, 15/09:** tổng các tầng khớp nhau; khớp BC015 8/8; đơn vị 75/75; đơn vị × ngày 75/75; **đơn vị × nguồn đơn 0 ô lệch**
  (349 nhóm vs 346 của BC015 — 3 nhóm toàn 0 đồng BC015 giấu). *(Chạy lúc còn lấy mọi mã trừ XDCNB, trước khi đổi sang BHVAT+BHK.)*
- **Tổng hợp cả tháng 9:** 3 kiểu khớp BC015, **đơn vị × ngày 2.242/2.242**, đơn vị × nguồn 0 lệch; 4,5 / 10,9 / 5,6s.
- **BHVAT+BHK:** 15/09 và cả tháng 9 **khớp SQL viết tay từng đơn vị** (74/74, 75/75; tháng 9: 257.570 dòng, tiền hàng 39.858.419.421) ·
  chọn đủ 5 mã ⇒ = BC015 8/8.
- **Cấu hình cột:** mặc định không lấy cột thêm nào (cả tháng 9,3s); hiện hết 12 cột 12,2s; tổng tiền không đổi; giá trị cột thêm đúng.
  Xuất Excel: hiện hết 30 cột · ẩn bớt cột tiền · tổng hợp ẩn SL + tiền ⇒ số dòng = số đếm, Tổng cộng = màn hình.
- **Giao diện 1366px:** hàng điều kiện 1 dòng; tick cột thêm ⇒ tải lại; bỏ tick ⇒ không gọi máy chủ; Tổng hợp theo cột đang ẩn; Về mặc định.
- ⏳ Chưa: tuần 01–07/09 cho bản 3 kiểu (dừng giữa chừng để Đại Ca thử) · M3 (EXE) · bấm lại xuất BC007 sau khi `exportJournalXlsx` thêm `tuyChon`.

---

## 03/10/2026 — BC017 Báo cáo bán hàng (mẫu iPOS "3.1 - Báo cáo bán hàng") — việc 49

Đại Ca 02/10: *"làm thêm 1 báo cáo cho số liệu bán hàng … cho thêm các điều kiện lọc để xem, số liệu thể hiện chi tiết phát sinh theo
điều kiện đó"*, gửi ảnh mẫu iPOS 3.1 (của Drip Drip Coffee) + hộp lọc (Kho · Nhóm hàng hoá · Danh mục hàng hoá · Nhóm đối tượng ·
Đối tượng · Nhóm công việc · Công việc). ⚠️ Danh sách "Danh mục" trong hộp lọc iPOS còn thanh cuộn — **chưa thấy phần dưới** (đã xin ảnh).

### Đo trước khi làm (T09/2026, `SALE_VIEW` POSTED)
262.798 dòng / 46.271 phiếu / ~80 đơn vị mỗi tháng; ~35% là dòng 0 đồng (ghi chú món "Đá bình thường"). Lấy chi tiết: 1 ngày 1,4s ·
1 tuần 6s · 1 tháng 22s. **38.410/46.271 phiếu trùng số với đơn vị khác cùng ngày** (+1 ca trùng cả đơn vị). `VAT_INCOME_AMOUNT`
của mẫu = **0 trên toàn bộ `BHVAT`** (39,9 tỷ tiền hàng). Loại CT trong view: BHVAT 254.686 dòng · **XDCNB 17.981 dòng toàn 0 đồng** ·
HDDC · BHK · **BNB bán nội bộ 2,25 tỷ** · BH.

### Đại Ca chốt (02/10)
Gom **Ngày → Đơn vị → Phiếu** (phiếu theo `PR_KEY`) · chỉ đã ghi sổ · **8 cột tiền của BC015**, nhãn tiếng Việt (Tiền hàng · Giảm giá ·
Chiết khấu · Voucher · Hoa hồng · Doanh thu · Thuế VAT · Tổng tiền) · mặc định **tất cả trừ XDCNB** (có ô Loại CT) · dòng 0 đồng
**hiện như iPOS, có ô tick ẩn**.

### Đã làm
- `server.py` (+6 hàm/lớp, +2 route ⇒ 191 / 76): `_bc017_where` · `/api/sale_detail` (phân trang trong SQL, dòng tổng là tổng đủ
  nhóm, trang bắt đầu giữa nhóm kèm dòng tổng cha `tiep`) · `/api/sale_detail/export` (job, `count_sql` đếm **số dòng file**) ·
  `_bc017_dong_xuat` + `_DongXuat` (dòng tổng in đậm, cột Số lượng giữ số lẻ). `_start_export_job` thêm `lap_dong`;
  `_write_xlsx_to_disk` đọc `kieu`/`cot_le` bằng `getattr` ⇒ **list thường của mọi bản xuất cũ đi đúng nhánh cũ**.
  `/api/metadata` trả thêm 3 danh mục nhóm (câu riêng, hỏng thì rỗng). Quyền: `PERM_REPORTS` tới BC017 + 2 route vào `PERM_ROUTE_STATIC`.
- `index.html`: thẻ BC017 · 6 ô lọc mới trong `O_LOC_BAO_CAO` (+ Công việc, Đối tượng dùng chung) · `THU_TU_O_LOC` (thứ tự hộp iPOS) ·
  `thamSoBC017` dùng chung cho xem + xuất · ô tick "Ẩn dòng 0 đồng" · đầu báo cáo in Kho / Đối tượng / Nhóm hàng hoá như mẫu ·
  `exportJournalXlsx(mode, tuyChon)` — BC017 dùng chung hộp đồng hồ + Hủy (không truyền `tuyChon` ⇒ y đường BC007 cũ);
  nhãn mã báo cáo trên hộp xuất hết ghi cứng "BC007".
- Thử giao diện thì sửa thêm: giấy BC017 cố định 340mm **khuất 2 cột Thuế VAT / Tổng tiền ở 1366px** ⇒ cho giấy co theo màn
  (tối đa 340mm), chữ 10px · thanh cuộn ngang thừa 2px · Số lượng in kiểu vi-VN lẫn với tiền kiểu en-US ⇒ đổi en-US.

### 🧪 Verify
- **M1:** `ast` OK, 191 hàm / 76 route, **không mất hàm/route nào so với HEAD**, không trùng tên · Babel OK · quét route chưa khai quyền = `[]`.
- **M2 + M4 (DB thật, `test_client`, nạp `server.py` bỏ dòng tắt cổng 5050):**
  - 15/09: 9.988 dòng hiển thị = 1 + 75 + 1.419 + 8.493; tổng 4 tầng khớp nhau 9/9 cột; **8/8 cột tiền = BC015 đến từng đồng**; 75/75 đơn vị khớp.
  - **Cả tháng 9: 8/8 cột = BC015** (tiền hàng 42.199.612.285 · tổng tiền 33.701.652.613); tuần 01–07/09 **đơn vị × ngày 523/523, 0 ô lệch**.
  - 7 ô lọc + Loại CT + kết hợp 2 ô: **khớp SQL viết tay** (đơn vị ngoài cây tính độc lập bằng CTE = `66`). Ẩn dòng 0 đồng: 8.493 → 5.974 dòng, 8 cột tiền không đổi.
  - Quyền: NV có BC017 → 200 · NV không có → **403 cả xem lẫn xuất** · NV giới hạn đơn vị 35 → chỉ thấy 35, chọn 36 → 0 dòng.
  - Xuất cả tháng: **308.874 dòng = số đếm**; cộng dòng hàng trong file = BC015; dòng tổng đậm, dòng hàng thường; SL lẻ (`LADUA` 0,2) giữ 2 số.
    Thời gian **4:23 lần đầu (SQL Server đọc đĩa), 0:47 lần sau** — tách khúc: bộ dựng dòng 0,6s/tuần, ghi xlsx ~5.500–10.000 dòng/s ⇒ nút thắt là đọc đĩa của SQL (CLAUDE.md § 6).
- **Giao diện thật trên DB thật** (server thử 5052, 1366×768 + 1280×720): xem 15/09 2,2s · trang 2 2,0s (3 dòng "(tiếp)") · tick ẩn 0 đồng ·
  xuất Excel từ giao diện 3,6s, file 7.400 dòng = số đếm. Hàng điều kiện một dòng ở 1366px; **1280px xuống 2 dòng** (cụm nút).
- ⏳ Chưa: **M3** (EXE) · Đại Ca bấm thử · đối chiếu vài phiếu với mẫu 3.1 trên iPOS · BC007 xuất Excel sau khi sửa `exportJournalXlsx` mới chỉ đọc lại code (chỉ thêm nhánh `tuyChon`), chưa bấm thử lại.

---

## 29/09/2026 — Lên v2.1.0 (Đại Ca chốt — cùng code v2.0.9)

Đại Ca: *"các tính năng update chỉnh sửa nãy giờ nó có thay đổi thế thì theo đúng quy trình luôn đi lên V2.1.0"*.
- **Không đổi dòng code nào** so với `v2.0.9` — chỉ số hiệu. `v2.0.9` **giữ nguyên** trên GitHub (không xoá tag / Release): máy đã lên
  2.0.9 hay còn ở 2.0.8 đều được báo lên thẳng 2.1.0 (`has_update` so LỚN HƠN hẳn).
- `CO_GI_MOI.md`: thêm `## v2.1.0` = đúng 6 dòng của đợt này, **giữ** `## v2.0.9` cho đúng lịch sử — app bỏ dòng trùng. Thử
  `_tach_co_gi_moi`: máy 2.0.9 → 6 dòng · 2.0.8 → 6 dòng · 2.0.7 → 8 dòng (thêm 2 dòng v2.0.8), không lặp.
- Build `python build_exe.py iPOS_Accounting_Report 2.1.0` ⇒ `version.txt` / `version_info.txt` 2.1.0, nguồn giao diện `537503ef…` (y
  v2.0.9). M3: `/api/version` 2.1.0, không báo cập nhật nhầm (GitHub còn 2.0.9), trang dịch sẵn. Bản CI v2.0.9 (`7d54e2a5…`) cất ở
  scratchpad để cập nhật thật 2.0.9 → 2.1.0.
- Push `e5144ce..0c94c49` (git push thường) ⇒ Actions run `36552085370` **`success`**, 0 cảnh báo ⇒ **Release `v2.1.0` = `Latest`**, tag →
  `0c94c49`, digest EXE `740b6eaa…`. `v2.0.9` vẫn còn (tag → `ed75979`).
- ✅ **Cập nhật thật 2.0.9 → 2.1.0** từ file CI v2.0.9: hộp báo 6 dòng · `apply_update` ⇒ **~22 giây** chạy 2.1.0 · `dist\` **SHA256 = digest
  CI v2.1.0** · `dist\` gọn 3 file · hết báo cập nhật · trang dịch sẵn, 0 thẻ Babel. App để đang chạy.
- Push tài liệu trước đó (`e5144ce`) **không sinh lần build nào** — `paths-ignore` (việc 11) có tác dụng, asset v2.0.9 giữ nguyên SHA.

---

## 29/09/2026 — Phát hành v2.0.9 (việc 11, 24, 25, 40 + Tải lại hỏi Google + popup Hủy xuất + icon)

Đại Ca: *"tạm thời ok rồi, làm hết các việc cần làm luôn đi"*.
- Trước push: working tree sạch · quét secret 8 commit sạch · quét route chưa khai quyền `[]` · **thử tài khoản KHÔNG quản trị** (KE_TOAN,
  chỉ `BC007`): `/api/export/pause` 200, `/api/tai_lai_kiem_quyen` 200 (`giu`), `/api/export/cancel` 200, `/api/sale` **403** (đúng).
- ⚠️ `git push` **bị từ chối**: *"refusing to allow an OAuth App to create or update workflow … without `workflow` scope"* dù `gh auth status`
  có `workflow`. Gốc: `credential.helper=manager` (cấu hình HỆ THỐNG của Git) đứng trước helper `gh` khai ở `.git/config` ⇒ Git dùng token
  cũ của Git Credential Manager. Push bằng token `gh` **chỉ cho lệnh đó**: `git -c credential.helper= -c 'credential.helper=!"C:/Program
  Files/GitHub CLI/gh.exe" auth git-credential' push origin main` — không sửa cấu hình máy. Push `4593870..ed75979` (8 commit).
- Actions run `36550666732` **`success` 12/12 bước**: bước mới *Dich san giao dien (viec 24)* chạy Node **22.23.2**, nguồn sha256
  `537503ef…` **trùng bản build trên máy** (chuẩn hoá xuống dòng có tác dụng — runner checkout CRLF) · 0 cảnh báo PyInstaller · **hết cảnh
  báo Node 20** (việc 11 xong thật). Release **`v2.0.9` = `Latest`**, tag → `ed75979`, digest EXE `7d54e2a5…` (13.662.884 B — v2.0.8
  13.166.800 B). `CO_GI_MOI.md` tại tag: 6 dòng.
- ✅ **Cập nhật thật 2.0.8 → 2.0.9** từ file CI v2.0.8 (`a20f1d4a…`, tải lại từ Releases — bản build local 2.0.9 cất ở scratchpad): hộp báo đủ
  6 dòng · `apply_update` ⇒ **~9 giây** chạy 2.0.9 · `dist\` **SHA256 = digest CI** · `dist\` gọn 3 file · hết báo cập nhật.
- ✅ **EXE do CI build đúng là bản dịch sẵn**: `<meta giao-dien-dich-san>` = `537503ef…`, 0 thẻ Babel / `text/babel` / `src="http` · 4 thư viện
  200 đúng byte, Babel 404 · mở trang **0,18s** lần đầu, **0,10s** mở lại. App để đang chạy.
- Dòng *Lịch sử push* đã thêm vào `GITHUB_LEDGERREPORT.md`.

---

## 29/09/2026 — Việc 11, 40, 24, 25: mở app nhanh (dịch sẵn giao diện + nhúng thư viện) · nâng GitHub Actions · Tải lại khi hết phiên

Đại Ca: *"làm việc 40, 24, 25 luôn nha"* → hỏi chỉnh quyền `workflow` ở đâu → cấp quyền → *"làm hết 4 mục luôn đi"* (kèm cho tải 5 thư viện).

**Cấp scope `workflow` cho token `gh`** (mở khoá việc 11 + cho sửa `release.yml`): `gh auth refresh -h github.com -s workflow` sinh mã
thiết bị; Đại Ca tự đăng nhập GitHub trong trình duyệt tích hợp, em nhập mã, trang xác nhận ghi đúng *GitHub CLI* xin thêm đúng
**Workflow** (yêu cầu lúc 14:40 từ máy này). Bước bấm Authorize: hệ thống an toàn của app chặn em thao tác tiếp ⇒ để Đại Ca; sau đó
`gh` báo *Authentication complete*, scope nay `gist, read:org, repo, workflow`.

**Vì sao phải có quyền này mới làm gọn được 24/25:** CI gọi thẳng PyInstaller với danh sách `--add-data` cố định trong `release.yml`
(chỉ `index.html`, không chạy `build_exe.py`) ⇒ thư viện hay bản dịch sẵn không có đường vào EXE nếu không sửa được file đó.

### Việc 25 — nhúng thư viện
5 file tải về `thu-vien/`, **đúng bản app đang chạy hôm đó** (`cdn.tailwindcss.com` không ghi số ⇒ chuyển hướng tới `/3.4.17`;
`react@18` ⇒ `18.3.1`):

| File | Nguồn | Byte | SHA256 |
|---|---|---|---|
| `tailwind-3.4.17.js` | cdn.tailwindcss.com/3.4.17 | 407.279 | `176e8946…c50d15` |
| `react-18.3.1.production.min.js` | unpkg.com | 10.751 | `d949f1c3…d4c4dd` |
| `react-dom-18.3.1.production.min.js` | unpkg.com | 131.835 | `35f4f974…98f66f0d` |
| `babel-standalone-7.29.7.min.js` | unpkg.com | 3.140.250 | `7f55bd5c…4739798e` — **chỉ để build, KHÔNG vào EXE** |
| `xlsx-0.18.5.full.min.js` | cdn.jsdelivr.net | 881.727 | `c9506197…d8623c99` |

- `index.html` trỏ `/thu-vien/…`; route tĩnh có sẵn (`serve_static`) phục vụ luôn ⇒ **không thêm route** (Bẫy 30 không dính). File
  trong `thu-vien/` gắn `Cache-Control: immutable` (tên có số phiên bản) ⇒ mở lại lấy từ bộ nhớ đệm, 0 byte tải.
- `.gitattributes`: `thu-vien/*.js -text` — giữ nguyên byte (runner Windows bật `core.autocrlf`).
- Cảnh báo *"Không tải được giao diện"* (thay *"Không thể kết nối CDN"*) nay **hiện thật**: xét `React.version`; bản cũ xét `typeof`
  mà khối "Fallback" ở `<head>` gán React giả ⇒ không bao giờ hiện, chỉ còn màn trắng câm.
- Rà cả trang: **0 địa chỉ `http(s)://`** còn lại.

### Việc 24 — dịch sẵn giao diện
- **`dich_giao_dien.js`** (node, không cần `npm install`): lấy khối `<script type="text/babel">` của `index.html`, dịch bằng **đúng file
  Babel 7.29.7 + đúng tuỳ chọn** mà `@babel/standalone` tự dùng cho thẻ đó (presets `react` + `env`, 3 plugin class-properties /
  object-rest-spread / flow-strip-types — đọc từ chính file thư viện), bỏ sourcemap, ghi `web_dich_san/index.html` (gỡ thẻ Babel,
  thêm `<meta name="giao-dien-dich-san">` = sha256 nguồn). `web_dich_san/` trong `.gitignore` — **sinh lúc build, không commit**.
- `build_exe.py` chạy script đó **trước khi tăng `version.txt`** (dịch hỏng ⇒ dừng, không để lại số hiệu đã tăng) và nhúng bản dịch sẵn +
  4 thư viện. `release.yml` thêm bước *Dich san giao dien (viec 24)* + đổi `--add-data` tương ứng. ⛔ Hai danh sách phải khớp nhau.
- Chạy `server.py` từ mã nguồn **vẫn** dùng `index.html` gốc (Babel dịch trong trình duyệt) ⇒ sửa giao diện vẫn chỉ sửa `index.html`.

**🧪 Verify (M2, trình duyệt tích hợp, 3 server thử 5052/5053/5054 dựng đúng như gói trong EXE):**
- **Code dịch sẵn TRÙNG TỪNG BYTE code trình duyệt tự dịch**: lấy script Babel chèn vào `<head>` trên trang mã nguồn, bỏ dòng sourcemap
  ⇒ SHA256 `cfeb6f3a…d77914`, 721.024 ký tự — đúng bằng bản `dich_giao_dien.js` sinh ra.
- Thời gian (mốc `DOMContentLoaded` kết thúc — bao cả lúc dịch lẫn lúc chạy code giao diện; trình duyệt tích hợp không ghi FCP/LCP):

| Bản | Lần đầu | Mở lại |
|---|---|---|
| Cũ v2.0.8 (CDN + Babel trong trình duyệt) | **7,79s** | **6,83s** |
| Mã nguồn mới (thư viện trong app, Babel trong trình duyệt) | — | 6,89s |
| **Dịch sẵn (= EXE mới)** | **0,26s** | **0,11s** |

- Màn đăng nhập bản dịch sẵn và bản cũ: form cùng vị trí/cỡ (155, 252, 406×489) ở cùng khung 731×706, cùng 235 quy tắc CSS
  (Tailwind), ảnh chụp trùng nhau. Console chỉ có 401 (chưa đăng nhập — bình thường). `typeof Babel` = `undefined`, React 18.3.1.

### Việc 40 — Tải lại khi phiên đã hết
`loadPerms` trả `'het_phien'` khi `/api/my_perms` 401; `taiLaiTrang` gặp vậy ⇒ đặt câu *"Phiên đăng nhập đã hết\nĐăng nhập lại để tiếp
tục — thường do ứng dụng vừa được mở lại hoặc vừa cập nhật."* rồi `setIsLoggedIn(false)`; `useEffect` việc 23 hỏi
`/api/ly_do_dang_xuat` và thay bằng lý do cụ thể nếu máy chủ có. **Thử trên giao diện** (server 5055, phiên giả): vào Trang chủ → xoá
phiên ở máy chủ → bấm Tải lại ⇒ về màn đăng nhập, dòng đỏ đúng câu trên.

### Thêm lúc Đại Ca thử EXE v2.0.9 — nút Tải lại làm lại + icon riêng cho từng màn danh sách
Đại Ca: *"bản chất t chưa lọc, nhưng bấm tải lại nó tự lọc … giống thao tác F5"* → *"mục đích chính là load lại quyền, giao diện
và tính năng … nếu có phân lại quyền thì tự động đăng xuất thì sao"* + *"các icon của các danh sách chứng từ, đề xuất thêm luôn"*.
Em báo rõ: Tải lại cũ chỉ đọc quyền trong PHIÊN (chốt lúc đăng nhập) ⇒ không bao giờ thấy quyền mới; muốn hỏi Google phải giữ mã
đã băm trong RAM. Đại Ca chọn phương án **"Hỏi Google + nạp lại trang"** (AskUserQuestion, kèm đánh đổi).
- **Tải lại mới:** `POST /api/tai_lai_kiem_quyen` (PERM_PUBLIC) ⇒ Google `dang_nhap` bằng mã đã băm giữ trong
  `_phien_db[sid]['kiem_quyen']` (ghi lúc `login()`), so `_quyen_khac` với bản lúc vào: đổi quyền / Google từ chối ⇒ huỷ phiên + lý do
  (`_cau_google_tu_choi`, `_CAU_QUYEN_DA_DOI` — tách ra dùng chung với `_kiem_lai_nen`) + xoá bản lưu offline (không có mật khẩu gốc
  để ghi bản mới); chưa trả lời được / mất mạng ⇒ giữ phiên. Giao diện: không đổi ⇒ `location.reload()` (bản dịch sẵn ~0,2s), nhớ màn
  đang đứng qua `sessionStorage 'lr_tai_lai_man'` (activeTab, báo cáo đang mở, tab Phân quyền) — **không chạy truy vấn nào**. Bỏ phần
  "chỉ nạp lại màn đã lọc" (`daLocRef`) làm lúc đầu — không còn cần.
  ⚠️ Mỗi lần bấm, Google Sheet ghi 1 dòng "đăng nhập" + ô `DANG_NHAP_LUC` (lệnh `dang_nhap` không chỉ đọc) · chờ ~2–3s.
- **Icon:** `DOC_TABS.icon` mỗi màn một cái — `book` · `receipt` · `banknote` · `truck` · `package` · `warehouse` · `factory` · `swap` ·
  `clipboard-list` (trước: 5 màn chung `table`, 2 màn chung `swap`, Tồn kho trùng icon nhóm Kho). Thêm 6 icon Lucide. `DongManHinh`
  vẽ icon 14px thụt 20px (chữ từ 36 → 42px). Hàng tab ngang (khi thu gọn cột) dùng chung icon này.
- **Thử máy chủ** (Google giả lập, SQL giả): kho phiên giữ `dk` = mã băm, **không có mật khẩu gốc, không vào cookie** · như cũ ⇒ `giu` ·
  đổi mục / đơn vị / chức vụ ⇒ `dang_xuat` + đúng câu + xoá cache · đổi mật khẩu, bị khoá ⇒ `dang_xuat` đúng câu · Google bận, mất
  mạng ⇒ `khong_kiem_duoc`, giữ phiên · chưa đăng nhập ⇒ 401.
- **Thử giao diện** (server 5056, 1366×768): ở Chứng từ bán hàng, chưa Lọc, bấm Tải lại ⇒ trang nạp lại thật, **về đúng màn**, vẫn đăng
  nhập, **0** truy vấn `/api/sale`, dấu nhớ đã xoá · bật "quyền đổi" ⇒ Tải lại ⇒ màn đăng nhập + *"Quyền của tài khoản vừa được thay
  đổi…"* · 7 màn con có icon, **không màn nào cắt chữ** (dài nhất "PO – yêu cầu mua hàng" 135px).
- **Build lại v2.0.9 (M3)** — commit `2919b5d`: EXE chạy, trang có `/api/tai_lai_kiem_quyen` + nhớ màn + icon mới + popup Hủy xuất, 0
  `daLocRef`, 0 thẻ Babel · `POST /api/tai_lai_kiem_quyen` chưa đăng nhập ⇒ **401** (không phải 403 ⇒ đã khai quyền). Chờ Đại Ca thử.

### Thêm lúc Đại Ca thử EXE v2.0.9 — Hủy xuất: popup giữa màn Có / Không + TẠM DỪNG trong lúc hỏi
Đại Ca (ảnh hộp *"localhost:5050 says — Hủy xuất file Excel?"* của `window.confirm`): *"thông báo bạn có chắc chắn hủy … popup ở
giữa và cho chọn là có hoặc không, có thì ngưng, không thì xuất tiếp. lúc bật thông báo thì tiến độ phải tạm ngưng không xuất nữa."*
- **Máy chủ:** job có cờ `tam_dung`; route mới **`/api/export/pause`** `{job_id, tam_dung}` (khai `PERM_PUBLIC` cạnh `/api/export/cancel`
  — Bẫy 30, quét `[]`). `_cho_neu_tam_dung(job_id)` đứng chờ ở: mỗi 2.000 dòng (xlsx + csv) · trước câu SQL lấy dữ liệu · sau câu SQL,
  trước khi ghi · sau đóng gói, trước khi chuyển file sang thư mục xuất (file nằm chờ ở `%TEMP%`). Chọn Có ⇒ cờ huỷ ⇒ ném lỗi như cũ.
  Bỏ mặc quá **10 phút** (`_TAM_DUNG_TOI_DA_S`) ⇒ tự huỷ, job `error` kèm câu giải thích (khỏi giữ kết nối SQL + file tạm mãi).
  ⚠️ Câu SQL / bước đóng gói **đang chạy** thì không dừng ngang — dừng ở điểm kế. Câu xuất Nhật ký chung đều `WITH (NOLOCK)` ⇒ đứng giữa
  lúc đọc dở không giữ khoá.
- **Giao diện:** `huyXuat` mở popup (không `window.confirm` nữa) + báo máy chủ tạm dừng; `chonHuyXuat(co)`: Có ⇒ huỷ + đóng hộp · Không ⇒
  bỏ tạm dừng. Đang hỏi thì vòng theo dõi ngừng hỏi tiến độ; chọn Không ⇒ dời `batDau` / `hanChot` / mốc giai đoạn đúng bằng khoảng
  đã dừng (tốc độ + "còn ~" không bị lệch). `DongHoXuat` nhận `tamDungTu`: đồng hồ đứng + chữ *tạm dừng*; thanh tiến độ sang màu hổ phách.
  Popup `role="alertdialog"`, nút **Không, xuất tiếp** được chọn sẵn, không bấm ra ngoài để đóng. ⛔ Popup nằm **NGOÀI** thẻ hộp xuất:
  `.animate-modal` (`forwards`) giữ `transform` ⇒ con `position:fixed` bên trong bị giam trong khung thẻ.
  Thêm icon `alert-triangle` (hộp lỗi xuất file vốn gọi mà chưa khai ⇒ trước nay ô trống) + `pause`.
- **Thử máy chủ** (hàm thật, dữ liệu giả): tạm dừng ⇒ đứng yên **42.000** dòng suốt 3s · Không ⇒ xong 200.000 · tạm dừng rồi Có ⇒
  `cancelled` sau 0,15s · bỏ mặc (rút hạn 2s) ⇒ tự huỷ, đúng câu · tạm dừng lúc đóng gói ⇒ file chờ ở TEMP, thư mục xuất trống; Không ⇒
  file sang · 0 rác TEMP.
- **Thử giao diện** (server 5056: code xuất THẬT, kết nối SQL giả 250.000 dòng, 1366×768): popup tâm (683, 394) ≈ giữa màn · máy chủ
  đứng yên 40.000 dòng suốt 3s · nút Không được chọn sẵn · Không ⇒ chạy tiếp (52.000) · đồng hồ đứng **00:31 · tạm dừng** suốt 5s, chọn
  Không 1,5s sau ⇒ 00:33 (không cộng 5s dừng), "còn ~" 0:42 → 0:41 · Có ⇒ hộp đóng, `cancelled` 114.000 · 0 file sót.

- **Build lại v2.0.9** (Đại Ca tắt app; `version.txt` trả về 2.0.8 cho `build_exe.py` tự tăng lại 2.0.9 — tham số ép số hiệu chỉ nhận số
  LỚN HƠN bản hiện tại): EXE 15.271.682 B · M3: `/api/version` 2.0.9 · trang có popup hỏi huỷ, gọi `/api/export/pause`, **0**
  `window.confirm('Hủy xuất`, nhãn xanh, `notranslate`, 0 thẻ Babel · `POST /api/export/pause` (job lạ) ⇒ 200. Đang chờ Đại Ca thử.

### Thêm lúc Đại Ca thử EXE v2.0.9 — chữ phiên bản + khung Google Dịch
- Đại Ca (kèm ảnh màn đăng nhập): *"sẵn chữ phiên bản cho thành màu khác luôn cho nó bật lên"*. Chữ *PHIÊN BẢN V2.0.9* xám `#64748b`
  chìm vào nền navy ⇒ thành **viên nhãn xanh** cùng tông chữ *REPORT*: chữ `#93c5fd`, nền `rgba(96,165,250,.14)`, viền
  `rgba(96,165,250,.45)`, cao 22px = nhãn cam *Có bản vX*. ⛔ **Không dùng cam** — cam là màu nhãn *Có bản vX* ngay cạnh.
- Cùng ảnh đó có khung **Google Translate "Vietnamese / English"** đè góc trái, dù launcher đã truyền `--disable-features=Translate`
  ⇒ thêm `<html translate="no">` + `<meta name="google" content="notranslate">`. Em tự thêm (báo Đại Ca), không ai yêu cầu.
- Kiểm (server thử 5054, bản dịch sẵn, 1366×768): nhãn đúng màu/cỡ, `translate="no"`, meta có.

### Việc 11 — GitHub Actions
`checkout@v4 → v7` (7.0.1) · `setup-python@v5 → v7` (7.0.0) · `action-gh-release@v2 → v3` (3.0.3) — đã kiểm các tag tồn tại; breaking
change đã đối chiếu 14/09 (không vướng). `paths-ignore: '**.md', 'docs/**', 'docs-cu/**'` ⇒ push chỉ tài liệu không build lại EXE.
YAML kiểm bằng `yaml.safe_load`: 8 bước đúng thứ tự.

**Kiểm chung:** M1 (ast `server.py` + `build_exe.py`, Babel parse) · 180 hàm / 72 route, không trùng · route chưa khai quyền `[]` ·
secret sạch.

**📦 Commit `f24d7b5` + build v2.0.9 (M3):** `build_exe.py` chạy bước dịch sẵn (9,0s) rồi PyInstaller ⇒ EXE **15,27 MB** (v2.0.8:
14,78 MB — thêm ~0,5 MB thư viện). Chạy EXE thật: `/api/version` 2.0.9 · trang chủ có `<meta name="giao-dien-dich-san">`, **0** thẻ
Babel, **0** thẻ `text/babel`, **0** `src="http` · 4 thư viện trả 200 đúng byte, Babel **404** (không nhúng — đúng thiết kế) ·
đo trên EXE: **0,39s** lần đầu, **0,19s** mở lại · màn đăng nhập hiện đủ. ⚠️ `dist\` lúc build đang là file CI v2.0.8 — bị ghi đè (bản
đó còn trên Releases, `a20f1d4a…`). `Sync-And-Backup.ps1`: thêm 7 file mới vào `$Files`. ⚠️ Phát hiện: file này đang là UTF-8 **không BOM** dù có tiếng Việt
(Bẫy 12) — **chưa sửa**, script vốn không chạy trên máy này.

---

## 29/09/2026 — Việc 44: Hủy xuất không còn thoáng hiện file dở · v2.0.8

Đại Ca thử Hủy xuất trên v2.0.7: lần đầu **thấy file trong thư mục xuất** (xoá tay bằng Shift+Delete), lần hai thì không. Đo: thư mục
`Downloads\iPOS_Ledger_Studio` sửa lúc 14:07 và 14:11:06, sau đó **0 file** ⇒ file không nằm lại, chỉ **hiện ra một lúc**.
Đại Ca: *"làm việc 44 luôn đi, làm những việc còn lại luôn nha"*.

**Gốc:** `_write_xlsx_to_disk` ghi thẳng vào thư mục xuất. Huỷ lúc đang ghi ⇒ `workbook.close()` **đóng gói phần đã ghi thành file
.xlsx hoàn chỉnh** (~5s/346 nghìn dòng, ~36s cả tháng) rồi mới xoá; huỷ lúc đóng gói ⇒ file nằm đó tới khi đóng gói xong. Phép thử
việc 43 chỉ đếm file **sau khi job dừng** nên không bắt được.

**Đã sửa (`server.py`, commit `4dc9887`, +1 hàm ⇒ 180 hàm / 72 route):**
- Ghi + đóng gói vào `%TEMP%\lr_xuat_<job_id>.xlsx`; xong hẳn mới `os.replace` sang thư mục xuất (khác ổ ⇒ `shutil.move`).
- Huỷ lúc đang ghi ⇒ **không `close()`**; `_bo_workbook_do` đóng + xoá file tạm của từng sheet. ⚠️ xlsxwriter 3.2.9 ở chế độ
  `constant_memory` **chỉ xoá file tạm lúc `close()`** — bỏ ngang mà không dọn là rác nằm lại `%TEMP%`.
- Lỗi / huỷ **không còn xoá nhầm** file cùng tên của lần xuất trước (bản cũ `os.remove(out_path)` trong nhánh lỗi).
- File cùng tên đang mở trong Excel ⇒ báo *"File … đang mở (thường là trong Excel) — đóng file đó rồi xuất lại."*
- Chỉ đổi đường `.xlsx` qua job (BC007 + xlsx của 9 màn danh sách). **CSV giữ nguyên** — vẫn ghi thẳng, file lớn dần trong thư mục
  xuất lúc đang ghi (9 màn danh sách chưa có nút huỷ).

**🧪 Verify — M1 + thử hàm thật với dữ liệu giả 17 cột, soi thư mục xuất mỗi 0,05s** (script `thu_viec44.py`, scratchpad phiên):

| Ca | Bản mới | Bản cũ v2.0.7 (cùng phép thử) |
|---|---|---|
| Xuất trọn 300 nghìn dòng | `done`, zip hợp lệ, file chỉ xuất hiện **khi đã xong** | — |
| Huỷ lúc ghi (100 nghìn) | `cancelled`, **0 file lộ ra**, dừng 0,52s | **file lộ ra**, dừng 2,60s |
| Huỷ lúc ghi, đã sang sheet 3 (sheet 50 nghìn dòng) | `cancelled`, 0 file lộ ra, 0 rác `%TEMP%` | — |
| Huỷ lúc đóng gói (400 nghìn) | `cancelled`, **0 file lộ ra**, dừng 8,2s | **file lộ ra** |
| Lỗi giữa chừng (mất kết nối giả) | `error`, 0 file, 0 rác | — |
| Trùng tên file cũ (không mở) | ghi đè | — |
| Trùng tên file cũ **đang mở** | `error` câu tiếng Việt, **file cũ còn nguyên** | — |

Mọi ca: **0 file `tmp*` / `lr_xuat_*` còn lại trong `%TEMP%`**. Không đụng SQL ⇒ không cần DB thật (Bẫy 31 chỉ áp cho câu SQL).
`_tach_co_gi_moi`: máy 2.0.7 thấy 2 dòng v2.0.8, máy 2.0.6 thấy 4 dòng. Quét route chưa khai quyền `[]`, secret sạch.
**M3:** build **v2.0.8**, EXE chạy, `/api/version` 2.0.8, sống sau 45s. Bản CI v2.0.7 (`2d6d9c76…`) cất ở scratchpad để cập nhật thật.

**📦 Phát hành:** push `25772c3..4593870` (kèm 2 commit nhật ký) ⇒ Actions run `36537053085` **`success`**, 0 cảnh báo PyInstaller ⇒
**Release `v2.0.8` = `Latest`**, tag → `4593870`, digest EXE `sha256:a20f1d4a…`. `CO_GI_MOI.md` tại tag đúng 2 dòng.
✅ **Cập nhật thật 2.0.7 → 2.0.8** từ file CI v2.0.7: hộp báo đúng 2 dòng · `apply_update` ⇒ **~6 giây** chạy 2.0.8 · EXE `dist\`
**SHA256 = digest CI v2.0.8** · `dist\` chỉ còn EXE + `ketnoi.json` + `phanquyen_cache.json` (không sót `.old`/`.new`, không cất `.bak`
trong `dist\` nữa — bản cũ lấy từ Releases) · hết báo cập nhật. App để đang chạy.
⏳ Chưa thử: Đại Ca bấm Hủy xuất trên v2.0.8 với số liệu thật (đường máy chủ đã thử bằng hàm thật + dữ liệu giả).

---

## 29/09/2026 — Phát hành v2.0.7 (việc 43 nút Hủy xuất)

Đại Ca: *"chơi lun"*.
- Push `201f9b7..b958722` (3 commit, kèm commit nhật ký v2.0.6) ⇒ Actions run `36527174555` **`success`** ⇒ **Release `v2.0.7` =
  `Latest`**, tag `v2.0.7` → `b958722`, phát hành 05:40 UTC 29/09/2026. Digest EXE `sha256:9ee9ce26…`. Cảnh báo Node 20 vẫn còn (việc 11).
- ⚠️ Lần này **build local đè lên file CI v2.0.6 trong `dist\` mà chưa cất `.bak`** — đã tải lại asset v2.0.6 từ GitHub (SHA khớp
  digest `afdf8d3e…`) rồi cất `…_v2.0.6.exe.bak`. Bản build local cất `…_v2.0.7_build_local.exe.bak`.
- ✅ **Cập nhật thật 2.0.6 → 2.0.7** từ file CI v2.0.6: `check_update` báo có v2.0.7 + đúng 2 dòng "Có gì mới" · `apply_update` ⇒
  **~7 giây** sau chạy 2.0.7 · EXE `dist\` **SHA256 = digest CI v2.0.7** · không sót `.old`/`.new` · hết báo cập nhật · trang chủ có
  nút Hủy xuất. App để đang chạy.
- Không thêm route mới ⇒ không cần thử lại tài khoản không quản trị (quét route chưa khai quyền = `[]`).
- Dòng *Lịch sử push* đã thêm vào `GITHUB_LEDGERREPORT.md`. Mục này commit ở local, **chưa push**.
- **Dọn `dist\`** (Đại Ca bảo, sau khi kiểm lại lần push: 11/11 bước `success`, 0 cảnh báo PyInstaller, zip đúng EXE, `CO_GI_MOI.md`
  tại tag đúng): **22 file `.bak` (~297 MB) chuyển vào Thùng rác** — bản CI nào cũng còn trên GitHub Releases. `dist\` nay chỉ còn
  EXE v2.0.7 + `ketnoi.json` + `phanquyen_cache.json`. Từ nay cần EXE cũ thì tải từ Releases.

---

## 29/09/2026 — Việc 43: nút Hủy xuất + hộp xuất Excel Nhật ký chung theo mẫu DataStudio · ✅ phát hành v2.0.7

### 🧪 Thử trên DB THẬT (T01/2026, Nhật ký chung chi tiết, `test_client` in-process — không mở cổng, không đụng app)
Script `thu_huy_db_that.py` trong scratchpad phiên; `server._export_dir` trỏ về scratchpad; nạp `server.py` bỏ dòng tắt cổng 5050.

| Ca | Kết quả |
|---|---|
| **C** — xuất trọn 1 ngày (02/01), không huỷ | `done` · **67.444 dòng = tổng đếm** · 35,8s · có file |
| **A** — huỷ lúc đang đếm | `cancelled` · job dừng **1,2s** sau khi bấm (sau câu đếm, **không chạy câu lấy dữ liệu**) · tổng đếm 2.287.832 · 0 file mới |
| **B** — huỷ lúc đang ghi (100.000/2.287.832) | `cancelled` · dừng ở 102.000 dòng, **1,5s** sau khi bấm · 0 file mới |
| **D** — huỷ lúc đang đóng gói (01–05/01, 345.786 dòng) | `cancelled` · dừng **4,6s** sau khi bấm · file dở đã xoá · 0 file mới |

`error` của cả 3 ca huỷ = *Cancelled by user* nhưng `status = cancelled` ⇒ trình duyệt đóng hộp, không báo lỗi.
Xong: xoá ô `password` trong `config.json` (giữ các ô khác).

### 📦 Commit + build
- `b85ba14` feat (server.py + index.html + `CO_GI_MOI.md` mục `## v2.0.7`, 2 dòng tính năng).
- Trước commit: M1 (ast + Babel) · **179 hàm / 72 route**, không trùng · quét route chưa khai quyền = `[]` · quét secret sạch.
- `build_exe.py` ⇒ **v2.0.7**. **M3:** chạy EXE tách hẳn ⇒ LISTENING 5050, `/api/version` = `2.0.7`, trang chủ có chữ *Hủy xuất*,
  vẫn sống sau 1 phút. ✅ **Đại Ca đã bấm Hủy xuất trên EXE v2.0.7 (file CI) với số liệu thật 29/09: OK** — trước đó đường máy chủ đã thử ở trên,
  giao diện đã thử ở server giả.

Đại Ca dùng v2.0.6 xuất *Sổ nhật ký chung* (tổng hợp) T01/2026, gửi 3 ảnh:
1. Hộp đang *"Đang lấy 2.287.832 dòng từ máy chủ… · Còn 3:12"*, khoanh chỗ trống dưới đồng hồ: *"nên cho thêm nút hủy tiến trình
   nếu trong trường hợp t test t muốn ngưng"*.
2. Cùng lần xuất, đã ghi 21% mà vẫn *"Còn 3:03"*.
3. Hộp xuất của **DataStudio** (LedgerStudio v1.10.5, T08): 4 bước *Chuẩn bị · Truy vấn dữ liệu · Ghi Excel · Hoàn tất* · 3 ô
   *Đã ghi 1.436.000 / 2.856.815 · Tốc độ 7.393 dòng/giây · Thời gian 04:14 · còn ~03:12* · *"Đang ghi sheet 2/3"* · nút **Hủy xuất**.
   Hỏi: *"cơ chế tính giây của m sao nó cứ tăng giảm 1 chổ vậy, không ước lượng được bao nhiêu lâu à, hoặc làm theo hình thì sao"*.

⚠️ Mã nguồn DataStudio **không có trên máy này** (dò `D:\AI AGENT JOB` và `D:\`) ⇒ làm theo ảnh.

### Vì sao đồng hồ đứng một chỗ
- **Tốc độ lần trước nhanh hơn thật** ⇒ mỗi giây trôi qua thì số "còn" bị đẩy lên gần bằng ⇒ nhìn như đứng. Mặc định tổng hợp là
  13.600 dòng/giây (đo qua `test_client`); lần Đại Ca xuất thì chậm hơn.
- **Luật lúc đang truy vấn:** hạn chót không được sớm hơn phần ghi + đóng gói còn nguyên ⇒ đứng suốt lúc chờ câu SQL (ảnh 1).
- Mô phỏng trên timeline thật T08 (chi tiết, thật 7.167 dòng/giây) khi tốc độ lần trước **nhanh gấp ~2**:

| Pha tốc độ lần trước như đã ghi thêm | 4 lần xem đầu (cách ~15s) | Lệch TB so với lúc xong thật |
|---|---|---|
| **30 giây** (v2.0.6) | 4:24 → 4:56 → 4:55 → 4:50 — **đứng ~1 phút** | 40s |
| **10 giây** (chọn) | 4:55 → 5:51 → 5:39 → 5:27 | 27s |
| 5 giây | 5:18 → 6:23 → 6:00 → 5:42 | 21s (nhưng nhảy lên đầu lần xuất nhiều hơn) |

  Tốc độ đúng thì cả 3 mức lệch 12–15s. **Không cách tính nào làm số "còn" giảm đều mãi** — tốc độ thật dao động ±40%.
  ⇒ Làm theo ảnh: hiện **thời gian ĐÃ CHẠY** (luôn nhảy — người xem thấy việc đang tiến) + *còn ~* + tốc độ + số dòng.
  Script mô phỏng: `mo_phong_uoc_tinh.py` trong scratchpad của phiên (mất khi đóng phiên).

### Đã làm (working tree — CHƯA commit)
- **`server.py`** (+2 hàm ⇒ **179 hàm / 72 route**): `_kiem_huy_xuat(job_id)` ném lỗi nếu người dùng đã bấm huỷ;
  `_dat_loi_xuat(job_id, e)` đặt `status = 'cancelled'` nếu do huỷ, còn lại `'error'` — trước đó huỷ cũng thành `'error'` ⇒ hộp sẽ
  báo *"Lỗi xuất file: Cancelled by user"*. Kiểm cờ huỷ **sau câu đếm, sau câu lấy dữ liệu, sau đóng gói** (đóng gói không ngắt được
  ⇒ xong thì xoá file). Cả 3 chỗ bắt lỗi của job xuất (`_runner`, `_write_csv_to_disk`, `_write_xlsx_to_disk`) dùng `_dat_loi_xuat`.
  Route `/api/export/cancel` **có sẵn từ trước nhưng chưa nút nào gọi** — không thêm route (Bẫy 30 không dính).
- **`index.html`**: hộp mới **chỉ cho job có giai đoạn** (BC007 `.xlsx`); các hộp xuất khác giữ nguyên:
  - tiêu đề *Nhật ký chung chi tiết* / *Sổ nhật ký chung (S03a-DN)* + chip `BC007` · kỳ · số dòng;
  - câu giai đoạn + % to; 4 bước **Chuẩn bị · Truy vấn dữ liệu · Ghi Excel · Đóng gói** (mẫu ghi *Hoàn tất* — ở mình giai đoạn cuối
    là đóng gói, xong thì sang màn hoàn tất riêng);
  - 3 ô **Đã ghi** · **Tốc độ** (đo từ lúc bắt đầu ghi, chưa đủ 2 giây thì `—`) · **Thời gian** `04:14 · còn ~03:12`
    (`DongHoXuat` nay nhận `batDau` + `hanChot`, định dạng 2 chữ số phút);
  - dòng sheet khi tổng > 1 triệu (*"Đang ghi sheet 2/3 — mỗi sheet tối đa 1.000.000 dòng"*, icon mới `layers`);
  - *"Đừng tắt ứng dụng cho tới khi xong."* — ⛔ **bỏ** câu *"không cần giữ nguyên cửa sổ này"* của mẫu: hộp của mình không thu
    nhỏ được, ghi vậy là sai;
  - nút **Hủy xuất** (viền đỏ): hỏi *"Hủy xuất file Excel? Phần đã ghi sẽ bị bỏ, không để lại file dở."* ⇒ **đóng hộp ngay**, gửi
    `/api/export/cancel`; bấm trước khi máy chủ kịp trả `job_id` thì gửi huỷ ngay khi có (`huyXuatRef`, `huyXuat`, `guiHuyXuat`);
  - pha tốc độ lần trước **30 → 10 giây**.

### 🧪 Verify — M1 + server thử 5052 **DB GIẢ** (câu đếm 1,5s, lấy dữ liệu 4s; phần ghi Excel là code THẬT), 1366×768
- **M1:** `ast` OK, 179 hàm / 72 route, không trùng tên · Babel OK.
- Trước khi bật: `netstat` 5052 **rỗng** (bài học mục 28/09 khuya, tiếp).

| Thử | Kết quả |
|---|---|
| **Huỷ lúc đang ghi** (tổng giả 2,5 triệu) | Hỏi đúng câu, hộp đóng ngay · job dừng ở **122.000 dòng**, `status = cancelled` · **0 file** còn lại |
| **Huỷ lúc đang lấy dữ liệu** | Dừng khi câu SQL trả về · **0 dòng ghi**, `cancelled` · **0 file** |
| **Xuất trọn 120.000 dòng** | 25,7s · *còn ~* giảm đều 00:21 → 00:01 → *sắp xong* · tốc độ 6.7–6.9 nghìn dòng/giây · ra màn *Xuất Excel hoàn tất!* |
| Bố cục | Chữ bước cuối *Đóng gói* không bị cắt — mép chữ = mép hàng, cách mép hộp 25px (đo bằng JS; ảnh thu nhỏ nhìn như sát) |

Đã tắt server thử, xoá file xuất, trả khung trình duyệt về cỡ cũ.

### ⏭️ Còn lại
1. **Thử huỷ trên DB thật** — Đại Ca điền `password` vào `config.json` (xong xoá lại đúng ô đó). Code SQL không đổi, nhưng đường huỷ
   chạy song song câu SQL thật ⇒ phải thấy một lần (Bẫy 31: DB giả không bắt được lỗi phía SQL).
2. `CO_GI_MOI.md` mục `## v2.0.7` — gợi ý: *"Nhật ký chung: hộp xuất Excel hiện số dòng đã ghi, tốc độ, thời gian đã chạy và có nút
   Hủy xuất"*.
3. Commit · build · M3 · **hỏi Đại Ca rồi mới push** · cập nhật thật 2.0.6 → 2.0.7 · đối chiếu SHA · nhật ký + `GITHUB_LEDGERREPORT.md`.

### 🔍 Điểm mù
- **Huỷ lúc đang lấy dữ liệu:** câu SQL vẫn chạy nốt trên máy chủ (~15s với chi tiết cả tháng) rồi job mới dừng — hộp thì đóng ngay.
  Chưa dùng `cursor.cancel()` để ngắt ngang vì chưa thử được trên DB thật.
- **Huỷ đúng lúc đang đóng gói:** phải chờ đóng gói xong (~36s chi tiết cả tháng) rồi mới xoá file.
- 9 màn danh sách (xuất CSV/Excel qua `startServerExport`) **vẫn chưa có nút huỷ** — hộp khác, chưa làm.
- Khung trình duyệt của em bị ẩn lúc thử ⇒ nhịp hẹn giờ bị bóp; số trên hộp vẫn đúng vì tính theo mốc thời gian.

---

## 29/09/2026 — Phát hành v2.0.6 (việc 41 đồng hồ đếm ngược + việc 42 không đá người ra)

Đại Ca: *"ok làm tất cả các bước còn lại rồi up github"*.

- Commit: `b887717` (việc 42) · `6e8163c` (việc 41 + tài liệu + `CO_GI_MOI.md` mục v2.0.6) · `201f9b7` (số hiệu 2.0.6).
  Trước commit: quét secret chỉ trúng chữ "password/token" trong câu chữ tài liệu · route chưa khai báo quyền `[]` · so `origin/main`
  mất 0 hàm / 0 route, thêm `_gs_tu_choi_tai_khoan` (177 hàm / 72 route) · tiêu đề commit không BOM.
- **Thử tài khoản KHÔNG quản trị** (Bẫy 30, `test_client`, không cần DB vì guard chạy trước khi nối SQL): có quyền `BC007` ⇒ xuất
  200 + `job_id`, `/api/export/status` 200 · không có quyền ⇒ **403** *"Bạn không có quyền xem mục này"*.
- Trước build: EXE `dist\` = file CI v2.0.5 (SHA `601030e9…` khớp digest) ⇒ cất `…_v2.0.5.exe.bak`. Build ⇒ **2.0.6**, EXE mới hơn
  `server.py`/`index.html`. **M3** chạy EXE thật (mở tách hẳn bằng `Win32_Process.Create`): 5050 lên sau 2s · `/api/version` 2.0.6 ·
  trang chủ có code việc 41 + màn đăng nhập 08A+ · `check_update` không báo nhầm (GitHub còn v2.0.5) · xuất khi chưa đăng nhập ⇒ 401 ·
  `_tach_co_gi_moi` tách mục v2.0.6 đúng 2 dòng (máy ở 2.0.4 thấy 5 dòng).
- Push `0a935e5..201f9b7` (4 commit, kèm commit nhật ký v2.0.5 để dành) ⇒ Actions run `36456128716` **`success` 72s** ⇒ **Release
  `v2.0.6` = `Latest`**, **tag `v2.0.6` → `201f9b7`**, phát hành 00:10 ngày 29/09/2026. Digest EXE `sha256:afdf8d3e…`.
  `CO_GI_MOI.md` đọc được tại tag (2 dòng). Cảnh báo Node 20 vẫn còn (việc 11).
- ✅ **Cập nhật thật 2.0.5 → 2.0.6** từ file CI v2.0.5: `check_update` báo có v2.0.6 + đúng 2 dòng "Có gì mới" · `apply_update` ⇒
  **11 giây** sau chạy 2.0.6 · EXE `dist\` **SHA256 = digest CI v2.0.6** · không sót `.old`/`.new` · hết báo cập nhật · trang chủ có
  code mới. ⇒ **EXE trên máy Đại Ca = đúng file CI v2.0.6.** App để đang chạy.
- Bản cất `dist\`: `…_v2.0.5.exe.bak` (CI) · `…_v2.0.6_build_local.exe.bak`. Dòng *Lịch sử push* đã thêm vào `GITHUB_LEDGERREPORT.md`.
- Mục này commit ở local, **chưa push** (lý do ở § Việc cần làm).
- ⏳ **Chưa thử được:** đăng nhập trên v2.0.6 (cần tài khoản Google của Đại Ca) · việc 42 ở ca thật (cần nhiều người đăng nhập cùng lúc).

---

## 28/09/2026 (khuya, tiếp) — Việc 41 đo DB THẬT: bắt lỗi làm hỏng hẳn xuất Excel chi tiết · số mặc định thật · đồng hồ hết nhảy ngược

Đại Ca điền mật khẩu vào `config.json` (*"làm từng cái đi"*). Việc 42 commit trước: **`b887717`** (chỉ local, 11/11 ca thử lại
trên đúng bản sắp commit). Đo xong đã **xoá lại ô `password`** (giữ `server`/`user`/`database`).

### 1. 🔴 Lỗi thật chỉ DB thật mới lộ — câu đếm làm HỎNG HẲN xuất Excel Nhật ký chung chi tiết
Chạy thử 1 ngày: `SELECT COUNT(*) FROM (<câu xuất>) t` lỗi **8155** — cột đầu câu chi tiết là chữ `'NKC'` **không tên**. Câu đếm
chạy trước ⇒ **cả lần xuất báo lỗi**. DB giả của phiên trước không bắt được (cursor giả không dịch SQL). Phát hành nguyên như cũ là
v2.0.6 làm hỏng hẳn tính năng đang chạy tốt. **Bẫy 31** trong CLAUDE.md. Sửa 2 lớp: `'NKC' AS BANG` + đếm hỏng thì **xuất tiếp
không có tổng** (`_start_export_job`) + trình duyệt lấy tạm tổng trên màn (`sj.total || tongTam`).

### 2. Số đo thật — T08/2026, 2.856.814 dòng (qua `test_client`, file ghi vào thư mục tạm rồi xoá)
| Kiểu | Đếm | Lấy dữ liệu | Ghi | Đóng gói | **Cả quá trình** | File |
|---|---|---|---|---|---|---|
| **Chi tiết** (17 cột) | 2,7s | 15,6s | 398,6s — **7.167 dòng/s** (từng 30s: 4.171–9.026) | 36,1s | **453s = 7:33** | 196 MB |
| **Tổng hợp** (10 cột) | 2,1s | 13,0s | 210,0s — **13.601 dòng/s** | 20,6s | **246s = 4:06** | 121 MB |
| Chi tiết 1 ngày (01/08) | ⎯ 1,6s ⎯ | | 16,1s — 5.922 dòng/s | 1,0s | 18,7s | 6,5 MB |
Tổng đếm **khớp đúng** số dòng ghi ra ở cả 4 lần. ⚠️ Ghi chú cũ *"2,85 triệu dòng mất 4–5 phút"* chỉ đúng cho **tổng hợp**; câu đó nằm
cả trên hộp chọn kiểu xuất ⇒ đã sửa: *"tổng hợp khoảng 4 phút, chi tiết khoảng 7–8 phút"*.

### 3. Sửa giao diện theo số thật (`exportJournalXlsx`)
- **`MAC_DINH` = số đo thật**, **hồ sơ tốc độ RIÊNG từng kiểu** (`lr_toc_do_xuat_nkc_detail` / `_summary`): hai kiểu nhanh chậm
  gần gấp đôi nhau, dùng chung thì xuất kiểu này xong kiểu kia đoán lệch ~40%. Số mặc định ước lại tháng 08: **7:29 / 4:04** (thật 7:33 / 4:06).
- **Đồng hồ nhảy ngược** — thấy khi thử giao diện thật tháng 01: giây 30 *"Còn 4:40"*, giây 45 *"Còn 7:07"*. Tốc độ lấy theo ~15 giây
  gần nhất mà tốc độ thật dao động 2 lần ⇒ nhảy. Đổi sang **trung bình cộng dồn từ lúc bắt đầu ghi + pha tốc độ lần trước như đã ghi
  thêm 30 giây**. Mô phỏng trên timeline thật T08: lệch trung bình **45s → 12s**, cú nhảy lớn nhất giữa 2 lần xem cách 15 giây **174s → 33s**.

### 4. ⚠️ Suýt đo nhầm — server thử CŨ còn sống
Phiên trước để lại server thử **DB giả** ở cổng 5052 (PID 11516, bật 17:58, lẽ ra chết theo phiên). Server mới cũng bind 5052 được
(Windows cho **hai tiến trình cùng LISTENING một cổng**) ⇒ trình duyệt vào nhầm server giả: *"Đang lấy 200.000 dòng"*, màn tháng 01 hiện
dòng *"CH A · Chi tien dien · 03/08"*. Đã tắt (đối chiếu dòng lệnh là script trong scratchpad phiên cũ) + xoá hồ sơ tốc độ giả trong
`localStorage`. ➡️ **Trước khi bật server thử: `netstat` cổng đó phải RỖNG** — có tiến trình cũ là tắt trước, đừng tin "bind được là cổng trống".

### 5. 🧪 Thử GIAO DIỆN THẬT trên DB thật — BC007 tháng 01/2026 (2.287.832 dòng), xuất chi tiết, 1366×768
Server thử 5052 (DB thật, phiên gieo sẵn), bấm đúng đường người dùng: Báo cáo TC → BC007 → Xem → Xuất → Excel → *Nhật ký chung chi
tiết*; ghi chữ trên hộp mỗi 5 giây. ⚠️ Khung trình duyệt của em bị ẩn ⇒ nhịp hẹn giờ bị bóp; đồng hồ vẫn đúng vì tính theo mốc thời gian.
| Lần | Code | Đồng hồ lúc bấm / lúc bắt đầu ghi | Thật | Trên đường đi |
|---|---|---|---|---|
| 1 | cách tính CŨ (~15s gần nhất), số mặc định T08 | lúc ghi: *Còn 5:47* (≈ 6:02) | **~388s (6:28)** | **nhảy ngược**: 4:40 @30s → 7:07 @45s → 6:20 @60s |
| 2 | cách tính MỚI (cộng dồn), hồ sơ học từ lần 1 | lúc bấm: *Còn 6:25* | **~318s (5:18)** | **đếm lùi đều, không lần nào tăng**: 6:17 · 5:38 · 5:04 · 4:39 · 4:23 · … · 0:39 · đóng gói 0:23 · 0:08 · 0:03 · xong. Từ giây 205, thời điểm xong dự kiến lệch thật ≤ 2s |
Hai lần cùng một tháng mà tốc độ máy chủ khác nhau **~25%** (6.584 vs 8.254 dòng/s) ⇒ con số lúc bấm **chỉ là ước lượng**, đồng hồ
tự chỉnh trong lúc ghi. Hộp *"Xuất Excel hoàn tất · 100% · Mở file ngay"* hiện đúng; hồ sơ tốc độ lưu đúng khoá `…_detail`; câu nhắc
mới trên hộp chọn kiểu xuất hiện đúng. Đã tắt server thử, xoá 2 file xuất (157 MB + 149 MB), trả khung về cỡ cũ.
**Mức verify:** M1 (ast 177/72, Babel) · M2 (`test_client` DB thật: 4 lần xuất chi tiết/tổng hợp, 1 ngày/1 tháng) · **thử giao diện thật
trên DB thật** (chưa phải EXE — M3 làm khi build v2.0.6).

---

## 28/09/2026 (khuya) — Bàn Supabase (giữ Google) · đo Apps Script · việc 42: đăng nhập nhanh không đá người ra vô cớ · ✅ phát hành v2.0.6

### 1. Đại Ca hỏi thay Google Sheet bằng Supabase ⇒ **giữ Google** (Đại Ca nghiêng về giữ, 28/09)
- **Bảo mật không phải lý do để đổi.** Làm đúng thì ngang hiện nay; làm sai một chỗ thì tệ hơn hẳn: nhúng khoá `service_role`
  vào EXE (repo công khai ⇒ ai cũng tải được mã băm, tự làm ADMIN) hoặc quên bật RLS (khoá `anon` công khai theo thiết kế ⇒ đọc
  được cả bảng). Muốn làm thì phải chép `Code.gs` sang **Edge Function**, bảng khoá kín, app chỉ gọi hàm — giữ mô hình hiện tại.
- Gói miễn phí **dừng dự án sau 1 tuần không hoạt động** (nghỉ Tết là dính; bản lưu offline cũng chỉ 7 ngày) và **không tự sao
  lưu**; Pro 25 USD/tháng (supabase.com/pricing, đọc 28/09).
- Mã băm chép sang được nguyên: `_pbkdf2` trong `Code.gs` là PBKDF2-HMAC-SHA256 chuẩn (1 khối) ⇒ không ai phải đặt lại mật khẩu.
- Xem lại khi: nhân viên phàn nàn chờ đăng nhập · nhiều người dùng cùng lúc hơn hẳn · Google siết hạn mức Apps Script.
- ⚠️ **Câu hỏi còn mở, lớn hơn chuyện Google/Supabase:** phân quyền trong app chỉ quyết định app **cho xem gì**. Nhân viên tự gõ
  thông tin SQL; nếu dùng chung tài khoản SQL (máy này là `ipchulong`) thì ai biết thông tin đó mở Excel → *Get Data → SQL
  Server* là đọc được cả `IACC_CHULONG`, không qua app. **Chưa biết** nhân viên dùng tài khoản SQL chung hay riêng, quyền đến đâu.

### 2. Đo Apps Script (lệnh không đọc Sheet)
| Lần đo | Kết quả |
|---|---|
| `ping` 4 lần (qua ổ khoá) | 2,18 · 14,19 · 11,80 · 19,14 s |
| Xen kẽ 6 lần: `doGet` (KHÔNG qua khoá) / `ping` (CÓ khoá) | trung vị **2,47s / 2,11s**, dải 1,6–3,7s cả hai |
⇒ Sàn ~2s là **của bản thân Apps Script**, sửa `Code.gs` không bớt được. Khoá chỉ tốn khi đông người. Lần đo đầu 11–19s không lặp
lại — chưa tách được do có người đang đăng nhập hay Google chậm thất thường. Việc 22 đính chính + để chờ số liệu (bảng § Việc cần làm).

### 3. Việc 42 — đăng nhập nhanh đá người ra vô cớ (Đại Ca: *"làm cái đăng nhập trước đi, phương án A"*)
**Lỗi (đọc code ra, chưa ai báo):** Google chờ ổ khoá quá 20 giây thì trả `ok: false` *"Máy khác đang ghi, thử lại sau vài giây"*
(`doPost`, `Code.gs`). `_kiem_lai_nen` (luồng hỏi lại Google của đăng nhập nhanh) coi **mọi** `ok: false` là từ chối ⇒ **huỷ phiên**
(màn đăng nhập hiện *"Máy khác đang ghi… Phiên đang dùng đã bị đăng xuất"*) + **xoá bản lưu trên máy** (lần sau chờ Google 12–35s).
Cùng bệnh: lỗi dịch vụ Sheets, sai token.

**Đã sửa (`server.py`, +1 hàm ⇒ 177 hàm / 72 route):** hằng `_GS_TU_CHOI_TK` + hàm `_gs_tu_choi_tai_khoan()` — chỉ **3 câu từ
chối thật** của `_apiDangNhap` (sai mật khẩu · đã bị khoá · tạm khoá do gõ sai) + câu rỗng (giữ nghĩa cũ) mới đá ra. Câu khác ⇒ xử
như mất mạng: **giữ phiên, không xoá bản lưu, không gia hạn bản lưu**, ghi log. So chữ sau khi chuẩn hoá NFC. ⚠️ Đổi chữ 3 câu đó
trong `Code.gs` thì phải đổi hằng này. **Không đụng Google, không phải triển khai lại Apps Script.**

**Đánh đổi đã biết:** tài khoản vừa bị khoá / đổi mật khẩu mà đúng lúc đó Google bận ⇒ người đó dùng hết phiên đó, lần đăng nhập
nhanh sau mới bị đá (ghi vào bảng *Giới hạn thiết kế*). **Cố ý giữ** đường đăng nhập thường: Google bận thì vẫn báo nguyên câu
*"Máy khác đang ghi…"*, không tự thử lại.

### 🧪 Verify
- **M1:** `ast` OK · 177 hàm / 72 route · không trùng tên. Không đổi `index.html`.
- **M2** (nạp `server.py` bỏ dòng tắt cổng 5050, giả `_gs_goi`, không gọi Google): **11/11 ca đạt** — giữ phiên: bận · sai token ·
  lỗi dịch vụ Sheets · mất mạng · ok quyền không đổi (có gia hạn bản lưu) · đá ra: sai mật khẩu · câu rỗng · đã bị khoá · tạm khoá ·
  đã bị khoá viết dạng NFD · ok nhưng quyền đã đổi. Câu báo trên màn đăng nhập của 6 ca đá ra **giữ y bản cũ**.
- **Đối chứng:** cùng phép thử trên `git show HEAD:server.py` ⇒ bản cũ **đá ra ở 3 ca bận / sai token / lỗi Sheets**, 8 ca kia giống hệt.
- Chưa M3 (chưa build EXE) — đi cùng v2.0.6. **Chưa dựng được ca thật** (cần nhiều người đăng nhập cùng lúc để Google chờ khoá > 20s).

### ⏭️ Phát hành v2.0.6 — gợi ý dòng `CO_GI_MOI.md`
*"Sửa lỗi thỉnh thoảng bị đăng xuất khi nhiều người mở app cùng lúc"* (cùng dòng đồng hồ đếm ngược của việc 41).

---

## 28/09/2026 (tối) — Hộp xuất Excel Nhật ký chung: % thật + ĐỒNG HỒ ĐẾM NGƯỢC · ⚠️ CHƯA COMMIT (việc 41)

Đại Ca gửi ảnh hộp *"Đang xuất file Excel … 43%"* (BC007 chi tiết): *"với cái này ước tính thời gian xuất được không"* →
xem thử bản 2 đồng hồ → *"cho nó đếm ngược đi"* → *"làm đếm ngược từ đầu luôn đi và 1 đồng hồ thôi"*.
Kèm: Đại Ca **đăng nhập thật trên màn đăng nhập mới v2.0.5 — OK** (*"t đăng nhập thử rồi, ok nha"*) ⇒ điểm mù cuối của v2.0.5 đã đóng.

### Phát hiện: % cũ là GIẢ
`exportJournalXlsx` bò theo số dòng đã ghi: **30.000 dòng = 1%, chặn 95%** (máy chủ không biết tổng). 43% trong ảnh ≈ 1,23 triệu
dòng đã ghi, **không phải 43% việc**. Xuất 1 ngày (~94 nghìn dòng) thì đứng 5% rồi nhảy 100%.

### Đã làm (working tree — CHƯA commit)
- **`server.py`** — `_start_export_job(..., count_sql=, count_params=)`: đếm TỔNG trước ⇒ `job['total']` thật; `job['phase']` =
  `dem` → `truy_van` → `ghi` → `dong_goi` (`_write_xlsx_to_disk` đặt `dong_goi` trước `workbook.close()`). Nhánh BC007 xlsx đếm bằng
  `SELECT COUNT(*) FROM (<đúng câu xuất, bỏ ORDER BY>) t` ⇒ tổng luôn khớp số dòng sẽ ghi. Không đổi route nào (vẫn 176 hàm / 72 route).
- **`index.html`** — `exportJournalXlsx`: % thật (đếm/truy vấn ⇒ 0%); **một** đồng hồ `DongHoXuat` (component cấp ngoài cùng, tự
  nhảy 4 lần/giây — không kéo cả App vẽ lại) hiện `Còn m:ss` / `Đang ước tính…` / `Sắp xong…`; bên trái là việc đang làm
  (*Đang đếm số dòng… · Đang lấy N dòng từ máy chủ… · Đang ghi x / N dòng · Đang đóng gói file Excel…*).
  **Đếm ngược từ lúc bấm**: lấy tạm `reportData.pagination.total_rows` của màn BC007, ước cả quá trình (lấy dữ liệu + ghi + đóng gói)
  theo **lần xuất trước trên chính máy đó** (`localStorage` khoá `lr_toc_do_xuat_nkc`: `tong`, `giayTruyVan`, `dongMoiGiay`,
  `giayDongGoi` — chỉ lưu khi ≥ 20.000 dòng). Khi ghi: tốc độ theo ~15 giây gần nhất, hạn chót **làm mượt 30%/lần hỏi**; đang truy
  vấn mà lâu hơn dự kiến thì hạn chót không được sớm hơn phần ghi + đóng gói còn nguyên (đồng hồ đứng chờ, không tụt về 0).
  Hộp này dùng chung với vài chỗ xuất khác ⇒ chỉ bật khi có `giaiDoan`, chỗ khác giữ chữ cũ.

### 🧪 Verify (server thử 5052, **DB GIẢ** chạy chậm như thật: đếm 1s, truy vấn 3s, ghi 200.000 dòng)
| Thử | Kết quả |
|---|---|
| Bản 2 đồng hồ (trung gian) | lỗi 1: lúc đếm thanh nhảy 2% rồi tụt 0% ⇒ sửa · lỗi 2: "Còn khoảng 10 giây" đứng ~14s ⇒ bỏ làm tròn, thành đếm ngược |
| Đếm ngược, lần 1 (máy chưa có số cũ, dùng mặc định tạm) | bấm là hiện **Còn 0:31**; về 0:01 ở giây 40, **xong giây 42** |
| Lần 2 (dùng tốc độ lần 1 đã lưu) | bấm là hiện **Còn 0:39**; ghi chậm hơn lần 1 ~20% ⇒ đồng hồ đứng chờ ~5s rồi đếm tiếp; về 0:01 giây 50, **xong giây 53** |
| M1 | `ast` OK 176/72 · Babel OK · không còn tham chiếu `uocTinhConLai` / `batDau` |
⚠️ Khung trình duyệt của em bị ẩn thì trang chạy chậm (timer bị bóp) — đồng hồ đứng 0:00 vài giây ở lần thử đầu là do đó, không phải lỗi app.

### ⏭️ Phiên sau làm tiếp — đúng 4 bước
1. Đại Ca điền `password` vào `config.json` (xong nhớ **xoá lại đúng ô đó**).
2. **Đo 1 tháng thật** (vd 08/2026, ~2,86 triệu dòng): gọi xuất xlsx qua `test_client` (gieo phiên như memory) rồi đọc `/api/export/status`
   theo thời gian ⇒ ghi lại: giây đếm, giây truy vấn (`truy_van`→`ghi`), dòng/giây lúc ghi, giây đóng gói (`dong_goi`→`done`).
   ⚠️ `import server` tắt app ở 5050 — kiểm cổng trước, hoặc nạp source bỏ dòng `kill_process_on_port(5050)`.
3. Thay `MAC_DINH` trong `exportJournalXlsx` (đang là số **TẠM**: `tong 2856882, giayTruyVan 20, dongMoiGiay 10000, giayDongGoi 30`
   ≈ 4:45 cả tháng — suy từ ghi chú cũ "2,85 triệu dòng mất 4–5 phút", **chưa đo**). Nếu đóng gói lâu bất thường thì ghi chú lại.
4. Commit · `CO_GI_MOI.md` mục `## v2.0.6` (gợi ý: *"Nhật ký chung: xuất Excel có đồng hồ đếm ngược thời gian còn lại, thanh tiến
   trình chạy đúng %"*) · build · M3 · push · cập nhật thật 2.0.5 → 2.0.6 · đối chiếu SHA · nhật ký + `GITHUB_LEDGERREPORT.md`.

### 🔍 Điểm mù
- Chưa đo DB thật ⇒ lần xuất **đầu tiên** trên mỗi máy dùng số tạm (từ lần 2 dùng số của chính máy đó).
- Chỉ áp cho xuất **.xlsx** Nhật ký chung. Xuất CSV (tải thẳng) và các chỗ xuất khác không đổi.
- Server thử 5052 + script DB giả nằm trong scratchpad của phiên này — **mất khi phiên đóng**; cách dựng lại: nạp `server.py` bỏ dòng
  tắt cổng 5050, thay `_make_conn` bằng cursor giả (`execute` ngủ, `fetchmany` trả lô 1.000 dòng 17 cột), `_export_dir` về thư mục tạm,
  `get_journal` trả `pagination.total_rows`.

---

## 28/09/2026 — Phát hành v2.0.5 (màn đăng nhập mới 08A+)

Đại Ca: *"ok làm các bước còn lại luôn, đẩy github đóng tag hôm nay luôn"*.

- Commit `3ced087` (màn đăng nhập + 2 câu lỗi `server.py` + tài liệu). Kiểm trước commit: 176 hàm / 72 route, so `origin/main`
  mất 0/0 · route chưa khai báo quyền `[]` · Babel OK · quét secret: 4 dòng dính chữ "password" đều là tên ô/kiểu ô, không lộ gì.
- Trước build: EXE `dist\` = file CI v2.0.4 (SHA khớp) ⇒ cất `…_v2.0.4.exe.bak`. Build ⇒ **2.0.5**. M3 chạy EXE thật: 5050 lên ·
  `/api/version` 2.0.5 · trang chủ là giao diện mới (có `HinhDangNhapPhai`, hết "Server Address") · `check_update` không báo nhầm ·
  xuất khi chưa đăng nhập ⇒ 401. ⚠️ Phép thử `/api/login` thiếu tài khoản ứng dụng **lỗi do script PowerShell của em** (đọc
  response rỗng), không chạy được — nhánh đó trong `server.py` không đổi, đã kiểm 26/09.
- Commit `0a935e5` (số hiệu, tiêu đề không BOM) · push `5ce8beb..0a935e5` (3 commit, kèm commit nhật ký v2.0.4) ⇒ Actions run
  `36410142846` **`success` 64s** ⇒ **Release `v2.0.5` = `Latest`**, **tag `v2.0.5` → `0a935e5`**, phát hành 17:31 ngày 28/09/2026.
  `CO_GI_MOI.md` đọc được tại tag (3 dòng màn đăng nhập).
- ✅ **Cập nhật thật 2.0.4 → 2.0.5** từ file CI v2.0.4: hộp thoại có đúng 3 dòng "Có gì mới" · `apply_update` ⇒ ~24s sau chạy 2.0.5 ·
  EXE `dist\` **SHA256 = digest CI v2.0.5** · không sót `.old`/`.new` · hết báo cập nhật · trang chủ là giao diện mới.
  ⇒ **EXE trên máy Đại Ca = đúng file CI v2.0.5.** App để đang chạy. Server xem 5052 đã tắt.
- Bản cất `dist\`: `…_v2.0.4.exe.bak` (CI) · `…_v2.0.5_build_local.exe.bak`. Dòng *Lịch sử push* đã thêm vào `GITHUB_LEDGERREPORT.md`.
- Mục này commit ở local, **chưa push** (lý do ở § Việc cần làm).
- ✅ **Sau phát hành: Đại Ca đăng nhập thật (SQL + Google) trên màn mới — OK** (*"t đăng nhập thử rồi, ok nha"*).

---

## 28/09/2026 — Màn đăng nhập mới 08A+ (ảnh nền minh hoạ + form tiếng Việt 2 khối)

Đại Ca: *"chỉnh chút xíu về màn hình đăng nhập, có thể làm cho nó đẹp hơn và thêm hình ảnh"* → *"mô phỏng thôi, kiểu ảnh nền
cho nó đỡ trống"* · *"làm lại tiếng việt hết, và bỏ mấy cái ví dụ ẩn ẩn đi nhìn tưởng đã nhập rồi"*.

### Phác thảo trước (mục 08 của canvas phác thảo) — 6 vòng góp ý
Hiện tại · **A** (giữ tấm navy, nền sáng bên phải) · **B** (nền navy phủ cả màn) → Đại Ca: bỏ khẩu hiệu, 2 ô tài khoản đang
**trùng icon người** ⇒ tách **2 khối** + icon riêng từng ô → chọn A, *"làm nó xịn hơn"* ⇒ **A+** → *"thực tế đâu có biểu đồ"* ⇒
thay mọi biểu đồ bằng **thứ app có thật** → *"cách điệu hơn chút"* ⇒ thẻ nghiêng, lớp giấy lót, thùng hàng 3D, quỹ đạo chấm → chốt.

### Đã làm (`index.html` + 2 câu `server.py`)
- Tấm trái: bỏ khẩu hiệu; 3 dòng giới thiệu có tiêu đề + mô tả; xấp tờ biểu mẫu (`HinhDangNhapTrai`, 2 SVG neo góc).
- Vùng phải: `HinhDangNhapPhai` = lớp màu (`slice`) + lớp đồ vật `.dn-vat` (cỡ gốc, căn giữa, `--k` theo chiều cao,
  `--gian` theo bề rộng) · thẻ form `.dn-the`: 2 khối 01/02, nhãn Việt, không placeholder, icon mới `server` `globe`
  `id-card` `users` `eye` `eye-off`, nút con mắt, nút *Đăng nhập →*, dòng *"Chưa có tài khoản? Liên hệ quản trị để được cấp."*
  Giữ nguyên `handleLogin`, khối báo lỗi (nút *Chi tiết kỹ thuật*), hộp cập nhật, nhãn cam *Có bản*, hộp cài driver.
- `server.py`: 2 câu hướng dẫn lỗi SQL đổi theo nhãn mới (*"Sai Tên đăng nhập hoặc Mật khẩu ở mục 01 — Máy chủ SQL…"*,
  *"Kiểm tra ô Tên cơ sở dữ liệu…"*). Dòng tiêu đề `_LOI_KET_NOI` giữ nguyên.
- `CO_GI_MOI.md` mục `## v2.0.5` (3 dòng, mô phỏng đúng hàm của app: máy 2.0.4 thấy 3 dòng). Luật màn đăng nhập ghi vào CLAUDE.md.

### 🧪 Verify (server xem 5052 — nạp `server.py` **bỏ dòng tắt cổng 5050**)
| Đo | Kết quả |
|---|---|
| 1366×690 (laptop thật) | form 599px vừa màn; **có thông báo lỗi**: lần đầu 725px ⇒ tràn 35px ⇒ thu gọn thêm ⇒ **655px, vừa** |
| 1280×650 có lỗi | tràn 29px, cuộn được, đầu form không bị cắt |
| 900px (tấm trái ẩn) | tiêu đề DATA REPORT trên form, không tràn ngang |
| Tờ biểu mẫu vs chữ REPORT | không chạm ở mọi chiều cao |
| Bấm Đăng nhập thiếu tài khoản ứng dụng | đúng câu việc 9, chữ đã gõ còn nguyên · con mắt: password ↔ text |
| 🔴 **Màn 2K (ảnh Đại Ca)** | cả khối hình `slice` phóng ~1,8 lần ⇒ thẻ to quá khổ, **bị cắt mép** — em chỉ đo SỐ ở 1920, không nhìn ảnh ⇒ sót. Tách 2 lớp ⇒ hết cắt; rồi Đại Ca chọn **giãn thẻ ở màn rộng**: 2K dạt 150 mỗi bên, **form che 0px**; laptop giữ nguyên |

### 🔍 Điểm mù
- Chưa đăng nhập thật (SQL + Google) trên giao diện mới — phần gửi đi không đổi (`handleLogin` cũ).
- `--gian` dùng container query (`cqw`) — Chrome ≥105; máy dùng Chrome quá cũ thì thẻ không giãn (vẫn hiện đúng như laptop).

---

## 28/09/2026 — Phát hành v2.0.4 (chỉ viết lại "Có gì mới", code y v2.0.3)

Đại Ca: *"Chổ có gì mới viết sao cho người dùng đọc vào hiểu á, đừng ghi mấy từ thật giả vào đây, với lại t nhớ update
canh giữa canh lề nữa mà"*.

- **Canh lề**: đã báo thật — lần này **không sửa code canh lề**; Excel Báo cáo TC canh đúng từ **v2.0.0** (BC001–BC004 đã
  đo ở mục v2.0.3 bên dưới). Đại Ca vẫn muốn nhân viên **đọc được** ý đó ⇒ đưa vào mục **v2.0.4**, câu nói sự thật
  (*"giữ đúng mẫu đang xem"*), không xưng là sửa lỗi.
- ⚠️ **Em từng giải thích sai rồi tự đính chính** trước khi làm: nói dòng ghi ở `## v2.0.0` thì "người ở 1.x nhảy lên sẽ thấy"
  — **sai**: máy 1.x / 2.0.0 báo cập nhật bằng code cũ, **không có** mục "Có gì mới" (có từ v2.0.1); máy ≥ 2.0.1 thì đã qua
  v2.0.0. ⇒ Dòng ghi ở `## v2.0.0` **hộp thoại không bao giờ hiện**. Chạy đúng `_tach_co_gi_moi` lên file (không `import
  server`) để thấy điều này — **mô phỏng trước khi viết `CO_GI_MOI.md`**.
- **Vì sao phải ra bản mới**: app đọc `raw.githubusercontent.com/…/<tag>/CO_GI_MOI.md` — tag `v2.0.3` đã khoá ở `36d0dd5`,
  sửa trên `main` vô tác dụng. Dời tag (force push) thì Actions build lại + thay asset ⇒ không làm.
- `CO_GI_MOI.md`: v2.0.4 = 1 dòng canh lề · v2.0.3 viết lại 2 dòng (*"Nhật ký chung: …"*, bỏ chữ "thật") · dòng v2.0.0 bỏ
  *".xlsx thật"* · thêm luật viết ở đầu file (mở đầu bằng tên màn hình, cấm chữ kiểu thật/giả, sửa câu sau phát hành ⇒ ra bản kế).
- Build 2.0.4 (M3: EXE lên, `/api/version` 2.0.4, `check_update` không báo nhầm, xuất chưa đăng nhập ⇒ 401) · commit `5ce8beb`
  · push `36d0dd5..5ce8beb` (kèm commit nhật ký v2.0.3) ⇒ Actions run `36401422055` **`success` 61s** ⇒ **`v2.0.4` = `Latest`**.
- ✅ **Cập nhật thật 2.0.3 → 2.0.4** từ file CI v2.0.3: hộp thoại hiện **đúng 1 dòng** canh lề · `apply_update` ⇒ ~31s sau chạy
  2.0.4 · EXE `dist\` **SHA256 = digest CI v2.0.4** · không sót `.old`/`.new` · hết báo cập nhật. App để đang chạy.
- Người ở **2.0.2** lên thẳng 2.0.4 sẽ thấy 3 dòng: canh lề + 2 dòng Nhật ký chung. Ai đã lên 2.0.3 trong ~1 tiếng giữa hai bản
  thì đã đọc câu cũ (có chữ "thật") — không sửa được nữa.
- Bản cất `dist\`: `…_v2.0.3.exe.bak` (CI) · `…_v2.0.4_build_local.exe.bak`. Dòng *Lịch sử push* đã thêm vào `GITHUB_LEDGERREPORT.md`.
- Mục này commit ở local, **chưa push**.

---

## 28/09/2026 — Phát hành v2.0.3 (BC007 chi tiết thêm Mã/Tên mục chi phí)

Đại Ca: *"làm luôn các việc còn lại để up github lun nha"*.

- Trước build: EXE trong `dist\` = file CI v2.0.2 (SHA256 khớp digest) ⇒ cất thành `…_v2.0.2.exe.bak` để thử cập nhật thật.
- Build ⇒ **2.0.3** (EXE mới hơn `server.py` / `index.html`). M3 chạy EXE thật: 5050 lên ngay · `/api/version` 2.0.3 · trang
  chủ có dòng mô tả mới · `check_update` không báo nhầm · xuất khi chưa đăng nhập ⇒ 401. Tắt EXE thử.
- Commit `36d0dd5` (số hiệu). ⚠️ Lần đầu tiêu đề commit dính **BOM** (PowerShell chèn khi pipe chuỗi vào `git commit -F -`) —
  đã `--amend` bằng file UTF-8 không BOM **trước khi push**. Commit qua PowerShell thì dùng `-F <file>`, đừng pipe.
- 📦 Push `410e5ef..36d0dd5` (4 commit, gồm 2 commit tài liệu v2.0.2 giữ lại từ trước) ⇒ Actions run `36399947370`
  **`success`, 82 giây** ⇒ Release **`v2.0.3` là `Latest`**, tag trỏ `36d0dd5`. `CO_GI_MOI.md` đọc được tại tag (2 dòng).
- ✅ **Cập nhật thật 2.0.2 → 2.0.3**: chạy file CI v2.0.2 ⇒ `check_update` thấy v2.0.3 + đúng 2 dòng "Có gì mới" ⇒ gọi
  `/api/apply_update` (lệnh nút *Cập nhật ngay*) ⇒ tải 12,5 MB ~7s, bản mới tự mở lại ở giây ~9. EXE trong `dist\`
  **SHA256 = digest CI v2.0.3**, không sót `.old`/`.new`, tiến trình 51 MB nghe 5050, `check_update` hết báo.
  ⇒ **EXE trên máy Đại Ca = đúng file CI v2.0.3.** App để đang chạy.
- Bản cất trong `dist\`: `…_v2.0.2.exe.bak` (CI) · `…_v2.0.3_build_local.exe.bak`.
- Thêm dòng vào bảng *Lịch sử push* (mục 8) của `GITHUB_LEDGERREPORT.md` ngoài repo.
- Mục này commit ở local, **chưa push** (lý do ở § Việc cần làm).

---

## 28/09/2026 — BC007: file xuất "Nhật ký chung chi tiết" thêm Mã/Tên mục chi phí · bỏ ô "trống" chứa dấu cách

Đại Ca: *"cho t thêm 2 cột là mã mục chi phí (EXPENSE_ID) và Tên Mục chi phí (EXPENSE_NAME)"* — chỉ file xuất **chi tiết**
(mode `detail` của `/api/report_export_csv`), không đụng màn hình BC007 hay bản xuất "như đang xem".

### Đã làm
- **2 cột mới** đặt **ngay sau Tên đối tượng** (Đại Ca chọn, thay vì cuối file) ⇒ file từ **15 → 17 cột**; Số tiền nợ /
  Số tiền có / Ghi chú dịch phải 2 cột. Áp cả `.xlsx` lẫn `.csv`; mã MCP ở CSV bọc `="…"` như mã đối tượng (giữ số 0 đầu).
- **Không JOIN `DM_EXPENSE`**: đo `OBJECT_DEFINITION` thì **`LEDGER_VIEW` đã tự JOIN danh mục**, có sẵn `EXPENSE_NAME`
  (bản đầu em JOIN thêm — đã bỏ). Ghi vào Bẫy 3 của CLAUDE.md.
- **Bỏ ô "trống" chứa dấu cách** ở Công việc / Tên đối tượng / Tên MCP: view bọc `ISNULL(…, N' ')`. Ngày 03/09/2026 có
  **60.476/94.086** ô Công việc và **74.292/94.086** ô Tên đối tượng là một dấu cách — lọc *(Blanks)* của Excel bỏ sót,
  `COUNTA` vẫn đếm. Lỗi có sẵn từ trước (bản đang phát hành cũng bị), nay `.strip()`.
- Hộp thoại xuất (`index.html`): dòng mô tả "Nhật ký chung chi tiết" ghi thêm *Mã/Tên mục chi phí*.
- `CO_GI_MOI.md`: mục **`## v2.0.3`** (2 dòng).

### 🧪 Verify

| Mức | Kết quả |
|---|---|
| M1 | parse OK, **176 hàm / 72 route** (bằng trước), không trùng tên · Babel OK |
| M2 dữ liệu giả | CSV + xlsx: 17 cột, dòng nào cũng 17 ô, Nợ/Có đúng cột, mã `007` giữ số 0, ô `' '` ra rỗng |
| M2 **DB thật** (`test_client`, phiên gieo tay) | Xuất ngày 03/09/2026 bằng **bản HEAD và bản mới**: cùng **94.086 dòng**, bỏ 2 cột mới ⇒ **0 dòng khác** · xlsx thật 94.086 dòng, 2 cột MCP trùng CSV |
| Đối chiếu nguồn | Tổng số dòng + Nợ/Có **theo từng MCP** của file khớp `dbo.LEDGER` (ngày 03/09, loại đơn vị `66`) — **0 nhóm lệch**; tháng 08/2026: `LEDGER_VIEW` khớp `LEDGER` 111/111 nhóm (MCP × Nợ/Có) |
| Nở dòng? | `DM_EXPENSE` 101 dòng / 101 mã, không trùng · tháng 08/2026 vẫn **2.856.882 dòng**, tổng Nợ/Có y nguyên |
| Tốc độ | SQL cũ/mới chạy **xen kẽ 4 lượt** (1 ngày, 94k dòng): cũ 12,8–20,8s · mới 14,6–22,6s ⇒ chênh ~1,5s (dữ liệu nặng hơn ~10%). Lần đầu đo 16,1s vs 42,7s là **nhiễu máy chủ**, đừng trích con số đó |
| M3 | ❌ **chưa build EXE** |

⚠️ Bản cuối (thêm `.strip()` cho Công việc / Tên đối tượng) chỉ chạy lại M1 + M2 dữ liệu giả — mật khẩu SQL đã xoá khỏi
`config.json` sau lần đo DB thật.

### 🔎 Canh lề Excel các báo cáo KQKD — KHÔNG phải lỗi của bản hiện tại
Đại Ca gửi ảnh file P&L (sheet `P&L CH_T7`) có tiêu đề cột không canh giữa, cột Chỉ tiêu canh phải, nhờ sửa cho các báo
cáo KQKD. Dựng lại **BC001, BC002, BC003, BC004** trên server thử 5052 (số liệu giả), bấm Xuất Excel thật rồi đọc từng ô
bằng `openpyxl`: **tiêu đề canh giữa 100%** (kể cả ô gộp 2 dòng), **Chỉ tiêu canh trái 27/27 dòng** ⇒ **không sửa gì**.
File trong ảnh gần như chắc ra từ **bản cũ trước v2.0.0** (xuất `.xls` HTML): tiêu đề chữ thường "Mã số" trong khi bản mới
luôn ra "MÃ SỐ" (`innerText` áp `text-transform: uppercase`), số 0 hiện `0` thay vì `-`. Đã báo Đại Ca: xuất lại bằng
v2.0.2; máy nhân viên còn ở 1.x thì cập nhật.

### 🔍 Điểm mù
- Chưa build, chưa phát hành ⇒ chưa ai dùng được 2 cột mới.
- Cả tháng (~2,86 triệu dòng) chưa xuất thử hết vòng với bản mới; ước chừng chậm thêm ~10% theo lượng dữ liệu.
- Người đã dựng file mẫu / công thức Excel trỏ theo **vị trí cột** của file chi tiết cũ (15 cột) phải sửa lại vì Nợ/Có/Ghi
  chú dịch phải 2 cột.

---

## 26/09/2026 — Phát hành v2.0.2 (vá lỗi xuất Excel của nhân viên + việc 9, 10, 23)

Đại Ca: *"chơi lun"*.

- M1: **176 hàm / 72 route**, so `origin/main` mất 0 / 0 · **route chưa khai báo quyền: `[]`** · Babel OK · quét secret sạch ·
  `CO_GI_MOI.md` có mục `## v2.0.2` (4 dòng, đều là thứ nhân viên thấy).
- Build ⇒ **2.0.2**. M3 chạy EXE thật: 5050 lên sau 0,5s · `/api/version` 2.0.2 · `/api/ly_do_dang_xuat` trả lời · trang có
  `orgsTrongQuyen` + lời gọi lý do đăng xuất · tắt EXE thử.
- Cất file CI v2.0.1 thành `dist\iPOS_Accounting_Report_v2.0.1.exe.bak` để thử **hộp thoại MỚI** cập nhật thật 2.0.1 → 2.0.2.
- 📦 Push `e9ff73f..410e5ef` ⇒ Actions run `36170397384` **`success`, 65 giây** ⇒ Release **`v2.0.2` là `Latest`**. `CO_GI_MOI.md` đọc được tại tag.
- ✅ **Lần đầu hộp thoại MỚI chạy thật hết vòng** (đúng file CI 2.0.1 → 2.0.2): mở app ⇒ hộp thoại *DATA REPORT v2.0.2*, `v2.0.1 → v2.0.2`,
  **4 dòng "Có gì mới" đọc từ GitHub**, *Tải 12,5 MB* ⇒ bấm **Cập nhật ngay** ⇒ vài giây sau app tự mở lại: EXE trong `dist\`
  **SHA256 = digest CI v2.0.2 lúc đó**, `.old` tự dọn, tiến trình mới 48 MB nghe cổng 5050, màn đăng nhập **V2.0.2**, không còn
  hộp thoại / nhãn cam. ⇒ **EXE trên máy Đại Ca = đúng file CI v2.0.2.**
- Bản cất trong `dist\`: `…_v2.0.1.exe.bak` (CI) · `…_v2.0.2_build_local.exe.bak`.
- Mục này commit ở local, **chưa push**.

---

## 26/09/2026 — Việc 9, 10, 23, 26 + 🔴 phát hiện lỗi xuất Excel của nhân viên trong bản đang phát hành

Đại Ca: *"làm đi m"* → chọn *"Việc code còn treo"*.

### Đã làm

- **Việc 9** — bỏ trống Tài khoản/Mật khẩu ứng dụng ⇒ báo ngay (trình duyệt chặn trước khi gửi; máy chủ chốt thêm ở `login()`).
  Dòng đầu giữ tiêu đề nhóm `Mật khẩu hoặc tài khoản không đúng`, dòng hai *"Chưa nhập đủ … ở mục 02"*.
- **Việc 23** — `_huy_phien_nen` ghi lý do theo sid (`_phien_bi_huy`); màn đăng nhập gọi `/api/ly_do_dang_xuat` một lần.
  Ba câu: đổi mật khẩu (dòng đầu `_LOI_SAI_TAI_KHOAN`) · bị khoá (giữ nguyên câu Google) · đổi quyền.
- **Việc 10** — `orgsTrongQuyen` (lọc `meta.orgs` theo `allowed_orgs`) cho ô Đơn vị của 9 màn danh sách + Báo cáo TC.
  `meta.orgs` giữ đủ (tiêu đề báo cáo / file xuất cần đơn vị `00`); tab điều chuyển "Đơn vị xuất" giữ đủ (quyền hai phía).
- **Việc 26** — BC015 (`/api/sale_by_source`) + BC016 (`/api/nxt`) vào ma trận CLAUDE.md § 1.2.
- 🔴 **LỖI ĐANG CÓ TRONG v2.0.0–v2.0.1:** `/api/xuat_xlsx_bieu_mau` + `/api/tai_file_xuat` (việc 35) **chưa khai báo quyền** ⇒
  nhân viên thường xuất Excel Báo cáo TC bị **403**; Đại Ca là ADMIN nên không thấy. Đã thêm vào `PERM_PUBLIC` (không đọc thêm
  dữ liệu). Ghi **Bẫy 30** + lệnh quét route chưa khai báo. `CO_GI_MOI.md` có sẵn mục **v2.0.2**.

### 🧪 Verify

| Mức | Kết quả |
|---|---|
| M1 | parse OK, **176 hàm / 72 route**, không trùng · Babel OK (lần đầu **lỗi**: em chèn `//` giữa dòng object — đã sửa) · quét route chưa khai báo: `[]` |
| M2 (nạp `server.py` **bỏ dòng tắt cổng 5050**, không đụng app thật) | **Bản đang phát hành: nhân viên xuất Excel ⇒ 403** (xác nhận lỗi) · bản sửa ⇒ 200 + tải file về 200 · việc 9: 2 ca bỏ trống ⇒ 401 trong ≤5ms, **0 lần gọi Google** · việc 23: 3 ca bị đá ⇒ 401 + đúng câu, hỏi lần hai ra rỗng; Google xác nhận / mất mạng ⇒ giữ phiên |
| Giao diện (5052, nhân viên chỉ xem đơn vị 35 + 71) | Ô Đơn vị Chứng từ tổng hợp + BC006: **chỉ 35, 71** · tab điều chuyển "Đơn vị xuất": **đủ 5** · bị huỷ phiên rồi bấm Xem BC006 ⇒ về màn đăng nhập, hiện *"Quyền của tài khoản vừa được thay đổi…"* · bỏ trống tài khoản ứng dụng ⇒ báo ngay, **0 request `/api/login`** |

### 🔍 Điểm mù

- "Tải lại" gặp 401 thì im lặng (không đá ra) — hành vi sẵn có; người bị huỷ phiên chỉ về màn đăng nhập ở lần tải số liệu kế tiếp.
- Ô **Kho** vẫn liệt kê kho của mọi đơn vị — cùng bệnh với việc 10, chưa làm.
- **Chưa build / chưa phát hành.** Lỗi xuất Excel của nhân viên còn nguyên trên mọi máy tới khi phát hành v2.0.2.

---

## 26/09/2026 — Phát hành v2.0.1 (thông báo có bản mới kiểu mới)

Đại Ca: *"chơi luôn đi"*.

- M1: parse OK, **175 hàm / 71 route**, so `origin/main` mất 0 hàm / 0 route (mới: `_doc_co_gi_moi`, `_tach_co_gi_moi`) · Babel OK ·
  quét secret sạch · `CO_GI_MOI.md` có mục `## v2.0.1` (`- Cập nhật hệ thống`).
- Build `build_exe.py iPOS_Accounting_Report` ⇒ tự lên **2.0.1** (EXE mới hơn mọi file nguồn).
- M3 chạy EXE thật: cổng 5050 lên sau 1s · `/api/version` 2.0.1 · trang có `HopThoaiCapNhat` + chu kỳ 2 giờ · `check_update` thấy GitHub
  đang v2.0.0 ⇒ không báo (đúng) · tắt EXE thử.
- Cất file CI v2.0.0 thành `dist\iPOS_Accounting_Report_v2.0.0.exe.bak` để **thử cập nhật THẬT 2.0.0 → 2.0.1** sau khi Actions xong.
- 📦 Push `ae1bf9d..e9ff73f` (7 commit) ⇒ Actions run `36167161529` **`success`, 63 giây** ⇒ Release **`v2.0.1` là `Latest`** (`.exe` + `.zip`).
  `CO_GI_MOI.md` đọc được ngay tại tag v2.0.1 (raw.githubusercontent.com).
- ✅ **"Có gì mới" chạy thật với GitHub** (code 2.0.1, giả số bản đang chạy): máy **2.0.0** ⇒ `['Cập nhật hệ thống']` · máy **1.12.3** ⇒
  6 dòng ("Cập nhật hệ thống" + 5 dòng v2.0.0, không lặp) · máy **2.0.1** ⇒ không báo. Mỗi lần hỏi 0,6–0,8 giây.
- ✅ **Thử CẬP NHẬT THẬT 2.0.0 → 2.0.1 lần đầu** (điểm mù của mọi lần trước): chạy lại đúng file CI 2.0.0, dải cũ hiện *"Đã có phiên bản
  v2.0.1 (12.5 MB)"*, bấm **Cập nhật ngay** ⇒ vài giây sau app tự mở lại bản 2.0.1: EXE trong `dist\` **SHA256 = digest CI v2.0.1**
  lúc đó, file `.old` đã tự dọn, tiến trình mới 48 MB và nghe cổng 5050 (không dính Bẫy 13), màn đăng nhập hiện **V2.0.1**,
  không còn dải/hộp thoại. ⇒ **EXE trên máy Đại Ca = đúng file CI v2.0.1**, đang chạy.
- Bản cất trong `dist\`: `…_v2.0.0.exe.bak` (CI) · `…_v2.0.1_build_local.exe.bak`.
- ⚠️ Máy nhân viên đang ở **1.12.x** lên thẳng 2.0.1 bằng **dải cũ** (code bản cũ) — hộp thoại mới chỉ thấy từ lần cập nhật sau 2.0.1.
- Mục này commit ở local, **chưa push** (push `.md` là build lại, thay asset khác SHA).

---

## 26/09/2026 — Thông báo có bản mới: hộp thoại + nút cam + thẻ nhắc (việc 37, phương án B + C)

Đại Ca: *"t muốn làm lại cái màn hình thông báo cho dễ thấy hơn"* → xem 3 phương án ở mục **07** bản phác thảo → chọn **B + C**.
Chốt thêm: *"Có gì mới"* lấy từ **file ghi chú trong repo**; đang mở app thì **kiểm lại mỗi 2 giờ**.

### Đã làm

- **`index.html`**: `useAutoUpdate` kiểm 1 giây sau khi mở + `setInterval` 2 giờ. Lúc mở app có bản mới ⇒ `HopThoaiCapNhat` (B).
  Giữa ngày ⇒ **không** bật hộp thoại, chỉ `NutCoBanMoi` trên thanh trên + `TheNhacCapNhat` góc phải (C). "Để lần sau" /
  "Nhắc lại sau 2 giờ" / ✕ ⇒ thẻ quay lại đúng 2 giờ sau (`setTimeout`, lần kiểm định kỳ không bật sớm hơn nhờ `nhacLuc`).
  Màn đăng nhập: nhãn cam *Có bản vX* cạnh số phiên bản. Gỡ hẳn `AutoUpdateBanner` (dải 36px cũ). Thêm icon `arrow-right`, `refresh`.
- **`server.py`**: `_doc_co_gi_moi` đọc `CO_GI_MOI.md` **tại tag bản mới** (raw.githubusercontent.com, 3 giây), `_tach_co_gi_moi`
  lấy mọi mục `## vX.Y.Z` nằm giữa bản đang chạy và bản mới, tối đa 8 dòng. Chỉ gọi khi có bản mới; lỗi ⇒ rỗng. Tag lạ bị chặn.
- **`CO_GI_MOI.md`** (file mới, có luật viết ở đầu file): mục v2.0.1 + v2.0.0. Đã thêm vào `$Files` của `Sync-And-Backup.ps1`.
- ✏️ Đại Ca chốt thêm: *"có gì mới nên ghi các tính năng update thôi, còn các hệ thống hay code thông báo thì chỉ cần ghi là update
  hệ thống"* ⇒ v2.0.1 (toàn thay đổi cách thông báo) chỉ còn **`- Cập nhật hệ thống`**; luật ghi ở đầu `CO_GI_MOI.md`;
  `_tach_co_gi_moi` **bỏ dòng trùng** (nhảy cóc nhiều bản thì "Cập nhật hệ thống" chỉ hiện một lần) — thử 4/4 ca đúng.

### 🧪 Verify

| Mức | Kết quả |
|---|---|
| **M1** | `server.py` parse OK, **175 hàm / 71 route** (+2 hàm), không trùng · Babel SUCCESSFUL |
| Hàm tách ghi chú | 7/7 ca đúng: nhảy 1 bản (3 dòng) · nhảy cóc 1.12.3 → 2.0.1 (8 dòng) · đã mới nhất (rỗng) · quá 8 dòng (cắt, báo *và 3 khác*) · bỏ `**` / `` ` `` · bỏ khối ghi chú `>` |
| Mạng thật (GitHub) | Giả máy 1.12.3: `has_update` true, tag v2.0.0 chưa có file ⇒ `co_gi_moi` rỗng (hộp thoại ẩn mục), **1,72 giây** · máy 2.0.0: false · tag rác bị chặn |
| Giao diện (server thử 5052, 2 giờ rút còn 15 giây CHỈ trong bản phục vụ thử) | Mở app ⇒ hộp thoại có 3 dòng *Có gì mới* · "Để lần sau" ⇒ đóng, nút cam còn · giây 9 chưa nhắc, giây 17 thẻ nhắc hiện · "Nhắc lại sau 2 giờ" ⇒ ẩn, giây 7 chưa hiện lại · bấm nút cam ⇒ mở lại hộp thoại · đăng xuất ⇒ nhãn cam ở màn đăng nhập, bấm ⇒ hộp thoại |
| Bề ngang | 1280px, cột thu gọn, Kho 4 tab: nút cam cách tab cuối 86px, không tràn, không gãy chữ |

### 🔍 Điểm mù

- **Chưa bấm "Cập nhật ngay" thật** — phần tải + thay EXE giữ nguyên code cũ, chỉ thêm đóng hộp thoại/thẻ trước khi chạy.
- **Chưa thấy "Có gì mới" đọc từ GitHub thật** — tag nào cũng chưa có `CO_GI_MOI.md`; lần phát hành v2.0.1 là lần đầu có.
- F5 giữa phiên cũng tính là "mở app" ⇒ hộp thoại hiện đè lên màn đang xem (do người dùng tự bấm F5 nên chấp nhận được).
- Mỗi máy gọi GitHub thêm 12 lần/ngày (mỗi 2 giờ). GitHub cho **60 lượt/giờ cho mỗi IP** không đăng nhập — cả văn phòng chung một IP
  thì mỗi máy mở cả ngày tốn ~0,5 lượt/giờ (+1 lượt mỗi lần mở app) ⇒ khoảng 100 máy mới chạm trần; chạm trần thì app chỉ im lặng không báo (không lỗi). File `CO_GI_MOI.md` đọc qua raw.githubusercontent.com, không tính vào 60 lượt đó.

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
> + [§ VIỆC CẦN LÀM](#-việc-cần-làm).*

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
> 🕘 *Ảnh chụp lúc đó — nhiều mục dưới đây nay đã xong. Danh sách còn treo THẬT ở [§ VIỆC CẦN LÀM](#-việc-cần-làm).*


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
> 🕘 *Ảnh chụp lúc đó — nhiều mục dưới đây nay đã xong. Danh sách còn treo THẬT ở [§ VIỆC CẦN LÀM](#-việc-cần-làm).*


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
> 🕘 *Ảnh chụp lúc đó — nhiều mục dưới đây nay đã xong. Danh sách còn treo THẬT ở [§ VIỆC CẦN LÀM](#-việc-cần-làm).*


1. **Triển khai lại Apps Script**: mở Sheet → Extensions → Apps Script → dán `Code.gs` mới →
   Triển khai → **Quản lý bản triển khai** → bút chì → Phiên bản: **Mới** → Triển khai.
   ⛔ **ĐỪNG bấm "Triển khai mới"** — nó sinh URL khác và mọi EXE đã phát sẽ chết.
2. Quyết định có **đổi token mới** hay không. Token hiện tại sẽ công khai ngay khi push.
   Đổi hay không thì kết quả cuối cũng như nhau (token mới cũng công khai) — nêu ra để Đại Ca biết.

### Còn treo
> 🕘 *Ảnh chụp lúc đó — nhiều mục dưới đây nay đã xong. Danh sách còn treo THẬT ở [§ VIỆC CẦN LÀM](#-việc-cần-làm).*

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
> 🕘 *Ảnh chụp lúc đó — nhiều mục dưới đây nay đã xong. Danh sách còn treo THẬT ở [§ VIỆC CẦN LÀM](#-việc-cần-làm).*


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
> 🕘 *Ảnh chụp lúc đó — nhiều mục dưới đây nay đã xong. Danh sách còn treo THẬT ở [§ VIỆC CẦN LÀM](#-việc-cần-làm).*

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
