# HANDOFF — Thêm cột/trường vào "Danh sách chứng từ tiền" (VOUCHER)

> Tài liệu bàn giao để thêm field mới vào tab **Danh sách chứng từ tiền**. Đọc hết trước khi sửa.
> Mọi thay đổi PHẢI làm GIỐNG HỆT cho **CẢ HAI** folder (2 app song song).

---

## 0. Bối cảnh kiến trúc

- 2 app song song, mỗi app = **1 file backend + 1 file frontend**, đóng gói thành EXE bằng PyInstaller:
  - `D:\IACC HCM\iPOS ACC\ACC PMKT\LedgerReport\` — `server.py` (Flask) + `index.html` (React 18 + Babel standalone qua CDN, single-file)
  - `D:\IACC HCM\iPOS ACC\ACC PMKT\LedgerStudio\` — cùng cấu trúc, **code voucher giống hệt**
- DB: **SQL Server 2016**, kết nối bằng `pyodbc`. DB demo: `IACC_CHULONG` (server `171.244.129.176,9001`, user `ipchulong`).
- Frontend gọi backend qua `/api/voucher` (+ `/count`, `/stream_csv`). React render bảng bằng **virtual scroll** (chỉ render dòng trong viewport).

### Nguồn dữ liệu voucher (QUAN TRỌNG)
Danh sách tiền KHÔNG query `VOUCHER_VIEW` (chậm ~390s). Thay vào đó query **2 bảng gốc**:
```
FROM dbo.VOUCHER H  WITH (NOLOCK)
INNER JOIN dbo.VOUCHER_DETAIL D WITH (NOLOCK) ON H.PR_KEY = D.FR_KEY
```
- Cột "đầu" (đơn vị, số CT, ngày, người nộp, địa chỉ, trạng thái...) nằm ở **VOUCHER (alias H)**.
- Cột "chi tiết" (TK Nợ/Có, số tiền, mã đối tượng, mã chi phí, mã CV, tham chiếu, NV, tiền tệ...) nằm ở **VOUCHER_DETAIL (alias D)**.
- Tên đối tượng + ngân hàng (`PR_DETAIL_NAME_*`, `BANK_NAME_*`, `BANK_ACCOUNT_*`) KHÔNG join trong SQL mà **map ở Python** từ `dbo.DM_PR_DETAIL` (hàm `_voucher_prdetail_map`). Tên đơn vị/chứng từ map từ metadata cache.
- ⚠️ Muốn biết một cột nằm ở bảng nào, kiểm tra schema (skill `ipos-acc-schema`) hoặc chạy `SELECT TOP 1 * FROM dbo.VOUCHER` / `dbo.VOUCHER_DETAIL`. ĐỪNG đoán tên cột.

---

## 1. Bảng cột hiện tại (29 ô/dòng, theo đúng thứ tự hiển thị)

| # | Field (key) | Nhãn | Nguồn |
|---|-------------|------|-------|
| 1 | *(STT)* | # | số dòng, không phải field |
| 2 | ORGANIZATION_ID | Mã ĐV | H |
| 3 | ORGANIZATION_NAME | Tên đơn vị | enrich (meta) |
| 4 | TRAN_ID | Mã CT | H |
| 5 | TRAN_NAME | Tên chứng từ | enrich (meta) |
| 6 | TRAN_NO | Số CT | H |
| 7 | TRAN_DATE | Ngày CT | H |
| 8 | ACCOUNT_ID_DEBIT | TK Nợ | D |
| 9 | ACCOUNT_ID_CREDIT | TK Có | D |
| 10 | AMOUNT | Số tiền | D |
| 11 | DESCRIPTION | Diễn giải | D |
| 12 | PR_DETAIL_ID_DEBIT | Mã ĐT Nợ | D |
| 13 | PR_DETAIL_NAME_DEBIT | Đối tượng Nợ | enrich (DM_PR_DETAIL) |
| 14 | PR_DETAIL_ID_CREDIT | Mã ĐT Có | D |
| 15 | PR_DETAIL_NAME_CREDIT | Đối tượng Có | enrich (DM_PR_DETAIL) |
| 16 | EXPENSE_ID_DEBIT | MCP Nợ | D |
| 17 | EXPENSE_ID_CREDIT | MCP Có | D |
| 18 | JOB_ID_DEBIT | CV Nợ | D |
| 19 | JOB_ID_CREDIT | CV Có | D |
| 20 | BANK_NAME_DEBIT | NH Nợ | enrich |
| 21 | BANK_ACCOUNT_DEBIT | TKNH Nợ | enrich |
| 22 | BANK_NAME_CREDIT | NH Có | enrich |
| 23 | BANK_ACCOUNT_CREDIT | TKNH Có | enrich |
| 24 | CONTACT_PERSON | Người nộp/nhận | H |
| 25 | ADDRESS | Địa chỉ | H |
| 26 | REFERENCE_NO | Tham chiếu | D |
| 27 | EMPLOYEE_ID | Mã NV | D |
| 28 | CURRENCY_ID | Tiền | D |
| 29 | STATUS | Trạng thái | H |

➡️ **Mỗi dòng có đúng 29 ô.** Mọi nơi (header, ô tìm kiếm, dòng dữ liệu, dòng tổng) phải khớp con số này.

---

## 2. CÁC ĐIỂM PHẢI SỬA khi thêm 1 cột (làm cho CẢ 2 folder)

### A) BACKEND — `server.py` (khối voucher bắt đầu ~dòng 2200)

**A1. Cho cột lấy thẳng từ bảng** → thêm tên cột vào đúng danh sách:
```python
# dòng ~2200 — nếu cột thuộc bảng VOUCHER:
VOUCHER_H_COLS = [..., "CỘT_MỚI"]
# hoặc nếu thuộc VOUCHER_DETAIL:
VOUCHER_D_COLS = [..., "CỘT_MỚI"]
```
`VOUCHER_SELECT` tự ghép từ 2 list này → không cần sửa SQL tay.

**A2. Cho cột "suy ra" (tên/lookup, vd map từ DM_xxx hoặc meta)** → KHÔNG thêm vào H/D, mà set trong `_voucher_enrich` (dòng ~2271):
```python
for r in rows_dicts:
    ...
    r['CỘT_MỚI'] = <tra cứu từ map/meta>
```

**A3. (Tùy chọn) Cho phép sort server-side** → thêm vào `VOUCHER_SORT_WHITELIST` (dòng ~2207):
```python
"CỘT_MỚI": "D.CỘT_MỚI",   # hoặc "H.CỘT_MỚI"
```
(Cột suy ra ở Python KHÔNG sort server được — chỉ sort client trên trang đang xem.)

**A4. (Tùy chọn) Cho phép tìm kiếm server-side** → thêm vào `_build_voucher_where` (dòng ~2218). Tìm theo tiền tố dùng block `LIKE ?` + `f"{val}%"`; tìm chứa dùng block `f"%{val}%"`. Tên param đặt dạng `s_xxx`, phải KHỚP với param mà `buildVoucherQuery` gửi (mục B4).

**A5. Xuất Excel (qua nút Xuất từ stream_csv)** → thêm vào `VOUCHER_CSV_COLS` (dòng ~2358):
```python
("CỘT_MỚI", "Nhãn cột"),
```

### B) FRONTEND — `index.html`

**B1. Dòng dữ liệu** — component `VoucherRow` (~dòng 1997): thêm 1 `<td>` ĐÚNG VỊ TRÍ mong muốn.
⚠️ **Giữ dòng cao 1 hàng**: ô chữ dài để `whitespace-nowrap`; ô số `text-right font-mono`. KHÔNG để chữ xuống dòng (xem mục 3).
```jsx
<td className="border-r whitespace-nowrap px-3">{r.CỘT_MỚI}</td>
```

**B2. Tiêu đề** — trong `<thead>` của khối render voucher (~dòng 4166): thêm 1 `<SortableHeader field="CỘT_MỚI" ...>Nhãn</SortableHeader>` ĐÚNG vị trí tương ứng B1.

**B3. Hàng ô tìm kiếm** — mảng key ngay dưới header (~dòng 4197): thêm `'CỘT_MỚI'` vào ĐÚNG vị trí (phải cùng thứ tự với B1/B2). Để ô trống không cho tìm thì thêm `''`.

**B4. (Nếu làm A4) param tìm kiếm** — `buildVoucherQuery` (~dòng 3465): thêm
```js
s_xxx: take('s_xxx', cs.CỘT_MỚI),
```
(param `s_xxx` phải trùng tên ở A4. Nếu là "tìm chứa" thì thêm `'s_xxx'` vào Set `LONG`.)

**B5. Xuất Excel (frontend)** — `VOUCHER_EXPORT_COLS` (~dòng 2819): thêm `['CỘT_MỚI','Nhãn cột'],`.

**B6. ⚠️ Dòng TỔNG (tfoot)** — (~dòng 4220):
```jsx
<td colSpan="9" ...>Tổng toàn bộ truy vấn (... dòng):</td>   {/* phủ ô 1..9 (trước Số tiền) */}
<td ...>{tổng số tiền}</td>                                  {/* ô Số tiền (ô 10) */}
<td colSpan="19"></td>                                        {/* phủ ô 11..29 sau Số tiền */}
```
`9 + 1 + 19 = 29`. **Thêm cột TRƯỚC Số tiền → tăng `colSpan="9"`. Thêm SAU Số tiền → tăng `colSpan="19"`.** Tổng phải luôn = số ô mỗi dòng.

---

## 3. CẠM BẪY BẮT BUỘC TRÁNH

1. **Đếm ô phải khớp tuyệt đối** giữa: số `<SortableHeader>` (header) = số phần tử mảng key (ô tìm kiếm) = số `<td>` trong `VoucherRow` = tổng colSpan tfoot. Lệch 1 ô → bảng vỡ/lệch cột.
2. **Chiều cao dòng phải đều (1 hàng)**. Bảng dùng virtual-scroll: nếu vài dòng cao gấp đôi (do chữ xuống dòng) sẽ gây lỗi "cuộn xuống bị trắng". → ô chữ luôn `whitespace-nowrap`; ô số không có khoảng trắng nên an toàn.
3. **Sửa GIỐNG HỆT cả 2 folder** (LedgerReport và LedgerStudio).
4. **Cột suy ra (tên/bank)**: không nằm trong VOUCHER/VOUCHER_DETAIL → phải set ở `_voucher_enrich`, không thêm vào VOUCHER_H_COLS/D_COLS (sẽ lỗi "Invalid column name").
5. Kiểm tra tên cột thật trong DB trước khi thêm (đừng đoán). Có thể `SELECT TOP 1 * FROM dbo.VOUCHER` / `dbo.VOUCHER_DETAIL`.

---

## 4. VÍ DỤ HOÀN CHỈNH — thêm cột "Số tiền ngoại tệ" (`AMOUNT_OC`) từ VOUCHER_DETAIL, đặt ngay sau "Số tiền"

1. `server.py` A1: `VOUCHER_D_COLS = [..., "AMOUNT_OC"]`
2. `server.py` A3 (sort): `"AMOUNT_OC": "D.AMOUNT_OC",`
3. `server.py` A5 (CSV): thêm `("AMOUNT_OC", "Số tiền NT"),` ngay sau dòng AMOUNT.
4. `index.html` B1 (VoucherRow): thêm sau ô AMOUNT
   `<td className="border-r text-right font-mono px-2">{fmtInt(r.AMOUNT_OC)}</td>`
5. `index.html` B2 (header): thêm sau SortableHeader AMOUNT
   `<SortableHeader field="AMOUNT_OC" sort={voucherSort} onSort={f => setVoucherSort(s => cycleSort(s, f))} className="border-r w-32 px-2" align="right">Số tiền NT</SortableHeader>`
6. `index.html` B3 (mảng key tìm kiếm): chèn `'AMOUNT_OC'` ngay sau `'AMOUNT'`.
7. `index.html` B5 (export): thêm `['AMOUNT_OC','Số tiền NT'],` sau AMOUNT.
8. `index.html` B6 (tfoot): cột thêm SAU "Số tiền" → đổi `colSpan="19"` thành `colSpan="20"` (giờ mỗi dòng 30 ô; 9+1+20=30).
9. Làm lại các bước trên cho folder LedgerStudio.

---

## 5. Build lại EXE sau khi sửa

Đóng app đang chạy trước (EXE bị khóa thì không ghi đè được). Trong mỗi folder:

**LedgerReport:**
```powershell
cd "D:\IACC HCM\iPOS ACC\ACC PMKT\LedgerReport"
python -m PyInstaller --noconsole --onefile --clean --noconfirm --name "iPOS_Accounting_Report" --icon icon.ico --add-data "index.html;." --add-data "install_driver.ps1;." --add-data "manifest.json;." --add-data "icon.svg;." --collect-submodules flask --collect-submodules flask_cors --collect-submodules pyodbc --hidden-import pyodbc --hidden-import flask --hidden-import flask_cors server.py
```
**LedgerStudio:** y hệt nhưng `cd ...\LedgerStudio` và `--name "iPOS_Ledger_Studio"`.

EXE xuất ra ở `dist\`. Trước khi build nên kiểm cú pháp: `python -c "import ast; ast.parse(open('server.py',encoding='utf-8').read())"`.

---

## 6. Tham chiếu nhanh — vị trí code (LedgerReport; LedgerStudio gần giống)

| Việc | File | Dòng (xấp xỉ) |
|------|------|---------------|
| VOUCHER_H_COLS / D_COLS | server.py | ~2200 |
| VOUCHER_SORT_WHITELIST | server.py | ~2207 |
| _build_voucher_where (filter) | server.py | ~2218 |
| _voucher_enrich (map tên/bank) | server.py | ~2271 |
| VOUCHER_CSV_COLS (export backend) | server.py | ~2358 |
| VoucherRow (dòng dữ liệu) | index.html | ~1997 |
| VOUCHER_EXPORT_COLS (export frontend) | index.html | ~2819 |
| buildVoucherQuery (param) | index.html | ~3465 |
| thead header + mảng ô tìm kiếm | index.html | ~4166 / ~4197 |
| tfoot (dòng tổng, colSpan) | index.html | ~4220 |

*(Số dòng có thể xê dịch sau khi sửa — tìm theo tên biến để chắc.)*
