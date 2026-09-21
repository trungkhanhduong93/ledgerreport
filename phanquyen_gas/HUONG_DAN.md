# Dịch vụ tài khoản & phân quyền trên Google Sheet

> **Đã triển khai xong 20/09/2026** — phần này để bảo trì về sau, không phải việc phải làm lại.
> Sheet: bảng tính **TOOL_CHULONG** (link ở ghi chú nội bộ — repo này công khai nên không ghi vào đây).
> Apps Script: mở Sheet → **Extensions → Apps Script**

---

## Đang chạy cái gì

| | |
|---|---|
| Bản triển khai | **Version 4** (21/09/2026 14:39), mô tả `v3 - sua doi mat khau khi SUA user + chong do mat khau (ban 2026-09-21b)` |
| Mã bản đang chạy | `2026-09-21b` — kiểm bằng `ping`, xem mục *Kiểm nhanh* cuối file |
| Chạy dưới tư cách | tài khoản Google chủ Sheet |
| Ai gọi được | Bất kỳ ai có URL **và** TOKEN |
| URL + TOKEN | **ghim cứng trong `server.py`** (`_GS_URL_GHIM` / `_GS_TOKEN_GHIM`) từ 21/09/2026 — cố ý, để chỉ phát một file EXE. `ketnoi.json` cạnh EXE nếu có thì **đè lên** bản ghim |
| Chống dò mật khẩu | khoá tạm **15 phút** sau **8 lần sai** trong 15 phút, tính **theo từng tài khoản** (`KHOA_SO_LAN` / `KHOA_PHAT_S` đầu Code.gs) |
| 3 sheet | `User đăng nhập` · `Chức vụ` · `Nhật ký` |
| Tài khoản khởi tạo | `admin` / `admin@123` — **vẫn chưa đổi tính tới 21/09/2026**, phải đổi trước khi phát |

⛔ **TRƯỚC KHI DÁN `Code.gs` LÊN GOOGLE, ĐỌC CÁI NÀY.**
Repo công khai nên `Code.gs` trong repo cố ý để `TOKEN` là chuỗi giữ chỗ `DAN_TOKEN_NGAU_NHIEN_VAO_DAY`.
**Dán thẳng file đó lên Google là ghi đè token thật** ⇒ lần Triển khai kế tiếp là mọi EXE mất kết nối.
Đã vấp thật 21/09/2026, cứu được chỉ vì lúc đó chưa bấm Triển khai.

```bash
python phanquyen_gas/chuan_bi_deploy.py
```

Script đó lấy token thật từ `ketnoi.json`, thay vào, rồi đưa vào clipboard (không ghi ra file nào
trong repo). Dán xong, **trước khi Triển khai**: Ctrl+F trong editor tìm `DAN_TOKEN_NGAU_NHIEN`
→ phải ra **"No results"**.

---

## Mật khẩu được bảo vệ thế nào

Chia làm 2 tầng, vì Apps Script chạy chậm hơn Python khoảng **2.500 lần** (đo thật 19–20/09/2026):

```
Máy nhân viên                          Google Apps Script
─────────────                          ──────────────────
mật khẩu gốc
   │ PBKDF2 200.000 vòng (95 mili-giây)
   │ salt = "TOOL_CHULONG|<tài khoản>"
   ▼
chuỗi băm ──────── HTTPS ────────────►  PBKDF2 thêm 1.000 vòng
                                        salt ngẫu nhiên riêng từng người
                                                │
                                                ▼
                                        so với cột PW_HASH
```

**Hệ quả:**
- Google **không bao giờ** thấy mật khẩu gốc.
- Bảng hash **không bao giờ** rời khỏi Sheet — app chỉ nhận về danh sách quyền.
- Ai trộm được cả Sheet vẫn phải trả **201.000 vòng cho mỗi lần đoán**.
- Đăng nhập mất **khoảng 4–7 giây** (trong đó ~2 giây là độ trễ cố định của Apps Script).

⛔ **Vì vậy KHÔNG gõ mật khẩu thẳng vào Sheet.** Apps Script không quay nổi 200.000 vòng
(mất ~3 phút) nên không tạo được cùng giá trị — gõ tay sẽ sinh hash không khớp và người đó
mất đường đăng nhập. Cột *"KHÔNG gõ ở đây"* đã được lập trình để tự xoá và báo lại.
**Đặt mật khẩu trong tab Phân quyền của phần mềm.**

---

## Cấu trúc 2 sheet

Cả hai đều **3 hàng tiêu đề, dữ liệu từ hàng 4**:

| Hàng | Nội dung |
|---|---|
| 1 | Nhóm cột — chỉ để nhìn |
| 2 | Tên tiếng Việt — chỉ để nhìn |
| 3 | **MÃ — script đọc đúng hàng này** |

⇒ Chèn cột, đổi chỗ cột, đổi màu, sửa tên tiếng Việt: thoải mái. **Chỉ đừng sửa hàng 3.**

**`User đăng nhập`** — `USER_ID` · `HO_TEN` · `CHUC_VU` · `ACTIVE` · `DON_VI` · `MAT_KHAU_MOI` ·
`PW_HASH` · `SALT` · `DOI_MK_LUC` · `DANG_NHAP_LUC` · `GHI_CHU`

- `ACTIVE`: đánh `x` = còn dùng. **Bỏ `x` là khoá ngay**, không cần xoá dòng.
- `DON_VI`: mã đơn vị cách nhau dấu phẩy. **Để trống = xem TẤT CẢ đơn vị** (không phải "không xem gì").
- `PW_HASH` / `SALT`: script ghi, **không sửa tay**.

**`Chức vụ`** — `MA_CHUC_VU` · `TEN_CHUC_VU` · **24 cột quyền** (đánh `x`).
Đây là **nguồn duy nhất** quyết định quyền. Sửa một dòng là mọi người mang chức vụ đó đổi theo —
nhưng **chỉ có hiệu lực khi từng người đăng nhập lại** (quyền được chốt một lần lúc đăng nhập để
mỗi cú bấm không phải chờ Google).

**`Nhật ký`** — tự ghi ai đăng nhập, ai đổi quyền, ai đổi mật khẩu, lúc nào, từ máy nào.

---

## Bảo trì

### Sửa code Apps Script

**Deploy → Manage deployments → bút chì ✏️ → Version: New version → Deploy.**

⛔ **ĐỪNG bấm "New deployment"** — nó sinh URL khác và mọi EXE đã phát cho nhân viên sẽ mất kết nối.

### Thêm báo cáo mới (BC017…)

Thêm 1 dòng vào mảng `PERM` trong [Code.gs](Code.gs), chạy lại `khoiTao()` — nó **chỉ chèn thêm cột**,
không đụng dữ liệu đang có. Nhớ thêm mã đó vào `PERM_REPORTS` trong `server.py` cho khớp.

### Đổi TOKEN

Sinh chuỗi mới, sửa `const TOKEN` trong Code.gs, triển khai lại (New version), rồi sửa `ketnoi.json`
**trên mọi máy**. Quên máy nào là máy đó không đăng nhập được.

```bash
python -c "import secrets; print(secrets.token_urlsafe(36))"
```

### Dựng lại từ đầu trên Sheet khác

1. Dán [Code.gs](Code.gs), điền `TOKEN` và `ADMIN_DK_BOOTSTRAP`.
   `ADMIN_DK_BOOTSTRAP` là chuỗi băm sẵn của mật khẩu khởi tạo — Apps Script không tự tính được:
   ```bash
   python -c "import hashlib,base64; print(base64.b64encode(hashlib.pbkdf2_hmac('sha256', b'admin@123', b'TOOL_CHULONG|admin', 200000)).decode())"
   ```
2. Chạy `khoiTao()` **khi đang mở bảng tính** (hàm có hiện hộp thoại báo xong).
3. **Deploy → New deployment → Web app** · *Execute as*: **Me** · *Who has access*: **Anyone**.
4. Chép URL vào `ketnoi.json` cạnh EXE.

### Kiểm tra dịch vụ còn sống

```bash
python -c "import json,urllib.request; c=json.load(open('ketnoi.json',encoding='utf-8')); d=json.dumps({'token':c['token'],'hanh_dong':'ping'}).encode(); r=urllib.request.urlopen(urllib.request.Request(c['url'],d,{'Content-Type':'application/json'}),timeout=30); print(r.read().decode())"
```

Trả `{"ok":true,"iter":1000,...}` là bình thường.

---

## Hai lỗi đã trả giá khi dựng

| Lỗi | Nguyên nhân |
|---|---|
| `The parameters (number[],String) don't match the method signature` | `Utilities.computeHmacSha256Signature` chỉ nhận **(String,String)** hoặc **(Byte[],Byte[])** — cấm trộn. Đã thêm `_byteCuaChuoi()`. |
| `Cannot call SpreadsheetApp.getUi() from this context` | Chạy `khoiTao()` lúc không mở bảng tính. 3 sheet **đã dựng xong** rồi mới chết ở dòng cuối — dễ tưởng hỏng. Đã bọc `try/catch`. |
