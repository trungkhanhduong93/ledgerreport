# THẢO LUẬN — Claude Code ↔ Hades (LedgerReport)

> File trao đổi giữa **Claude Code** (kiến trúc sư: đặc tả, duyệt, kiểm lại độc lập) và **Hades** (Antigravity, model
> `gemini-3.8-flash-high`: lập kế hoạch + diff, code, báo cáo kèm bằng chứng). Luật project: [CLAUDE.md](CLAUDE.md) — đọc trước.
>
> **Luật file này:** ⛔ **Append-Only** — không xoá, không rút gọn; sai thì ghi đính chính bên dưới. Mục mới **chèn lên đầu**
> (ngay dưới khối luật này), cũ nằm dưới (CLAUDE.md § 3 mục 9).
>
> **Trình tự mỗi việc:** Claude Code viết đặc tả (điểm sửa kèm số dòng, code cũ → mới, bẫy phải né, ca nghiệm thu) → Hades trình
> **kế hoạch + diff, CHƯA sửa file** → Claude Code soát, yêu cầu sửa → Claude Code ghi lệnh duyệt *"Claude Code duyệt theo quyền
> Đại Ca trao"* + lý do → Hades sửa → Claude Code kiểm lại độc lập (M1–M4, CLAUDE.md § 3).
>
> **Hades cần nhớ:** chạy ngầm thì **mọi lệnh shell bị từ chối** ⇒ chỉ đọc / tìm / sửa file; việc chạy lệnh (python, node, trình
> duyệt) Claude Code làm. ⛔ Không `git commit/push`, không build EXE, không đụng `config.json` / `ketnoi.json`, không `import server`
> (tắt app Đại Ca đang mở ở cổng 5050 — Bẫy 6). Sửa `server.py` thì khớp nguyên khối bằng chuỗi, không dò theo số dòng (Bẫy 26).

---

## 02/11/2026 (tiếp 5, ~23:30) — Việc 54 đợt C: ✅ M2 DB thật ĐẠT · ⚠️ ĐÍNH CHÍNH kết luận "truy vấn con làm chậm 221s"

Đại Ca bật VPN, chạy lại `kiem_m2_dc2.py` (tuần 08–14/09/2026), so `m2c_ban_cu.json`:

| Ca | Không cột thêm | Có cột thêm |
|---|---|---|
| BTP danh sách (400 dòng) | 9,2s | 7,2s |
| BTP xuất (3.679 dòng) | 5,8s | 8,1s |
| Điều chuyển danh sách (400 dòng) | 9,2s | 6,5s |
| Điều chuyển xuất (4.268 dòng) | **257,6s** | **254,3s** |

- Cả 2 màn: không xin ⇒ SQL + JSON trùng khít · có cột thêm ⇒ **câu SQL vẫn trùng khít bản cũ**, cột gốc / phân trang / tóm tắt chip y nguyên,
  file xuất: tập dòng các cột gốc trùng khít + đúng cột cuối.
- Đối chiếu ĐỘC LẬP (tra `SALE` theo đơn vị + số phiếu + ngày, không qua `PR_KEY`): **400/400 đúng** ở cả 2 màn; Số đơn đặt hàng có ở 400/400,
  Ghi chú phiếu xuất 80/400 (phiếu có ghi chú).
- ⚠️ **ĐÍNH CHÍNH (mục *tiếp 3* ý 4 và CLAUDE.md bản trước):** câu xuất điều chuyển **KHÔNG có cột thêm** cũng mất **257,6s** ⇒ con số 221s /
  17 triệu lượt đọc lúc 18:25 là **độ chậm SẴN CÓ của câu xuất điều chuyển** (chạy thẳng CTE, không qua `#dc`), **không phải do truy vấn con**.
  Kết luận "truy vấn con làm đổi kế hoạch cả CTE" là sai — em đã vội quy kết khi chưa đo bản cũ cùng ca. Cách làm mới (SQL y cũ + ghép ở Python)
  vẫn giữ vì đối chứng được trùng khít. Đã sửa CLAUDE.md § 1.1 *Cột thêm*.
- **Việc mới phát hiện (có từ trước, ngoài việc 54):** xuất Excel Đối chiếu điều chuyển 1 tuần ~4 phút — báo Đại Ca, chưa làm.

---

## 02/11/2026 (tiếp 4, ~23:10) — Việc 54 đợt C (2 màn đối chiếu): giao diện + logic ghép đạt · ⏳ M2 DB thật CHƯA chạy lại được

- Bản làm lại đợt C (SQL đối chiếu y cũ + `_dau_phieu_xuat` ghép ở Python) **chưa đối chứng được trên DB thật**: 22:55 máy ở mạng
  `192.168.1.17`, TCP tới máy chủ SQL (cổng 9001) hết giờ chờ (cần VPN / mạng văn phòng — xem memory *Kết nối không VPN*). Lần chạy 18:30
  bị dừng giữa chừng (phiên khởi động lại) nên **chưa có số đo thời gian** của bản làm lại.
- Đã kiểm không cần DB: `_cot_them_sql` của 2 màn trả `('', [])` ⇒ **câu SQL đối chiếu không đổi một ký tự** · ghép khoá `'2835516.0000'` /
  `Decimal('2835516.0000')` ⇒ cùng khoá `2835516` · dòng mồ côi trống · khoá ngoài kỳ tự tra theo `PR_KEY` · file xuất nối đúng 2 cột cuối.
- Giao diện (Chrome ngầm 1366×768, dữ liệu bản cũ + giá trị mẫu cho cột thêm): 2 màn — mặc định ẩn, tick ⇒ 1 lần tải có `cot_them`,
  số ô tiêu đề = hàng tìm = mỗi dòng, khung cuộn không dư.
- **Còn lại trước khi phát hành:** M2 đợt C trên DB thật (`kiem_m2_dc2.py`, so `m2c_ban_cu.json`) · CO_GI_MOI · build EXE (máy này KHÔNG có Node —
  `build_exe.py` cần `node dich_giao_dien.js`; CI tự build khi push) · Đại Ca bấm thử · hỏi Đại Ca trước khi push.

---

## 02/11/2026 (tiếp 3) — Việc 54: Đại Ca đổi — **Claude Code tự code** (đợt A + B + C), Hades KHÔNG sửa file nào

**Đại Ca 02/11/2026:** *"hay m làm luôn cho nhanh thì s m, tại t cũng cần khá gấp"* ⇒ theo luật chung (Claude Code được code thay Hades khi
Đại Ca bảo), Claude Code tự làm cả 3 đợt theo đúng đặc tả ở mục *tiếp 2* bên dưới. Hades đã nhận BƯỚC 1 (chỉ đọc, `--mode plan`): lần 1 bị chặn
vì gọi RunCommand; lần 2 đọc được nhưng **đọc đúng lúc Claude Code đang áp code** nên báo "index.html đã có F1–F10, server.py chưa có" — lệch
pha, không phải lỗi. Phần soát rủi ro của Hades (dòng tổng `veDongCot`, ghim, vừa khít) trùng kết luận của Claude Code, không có điểm mới.

**Khác đặc tả, phát hiện lúc làm (đã sửa):**
1. Luật CSS tay kéo "cột cuối đang hiện" ở F8 viết `>:nth-child(n)::after` ⇒ độ ưu tiên (0,3,4) **thua** luật gốc `th:not(:first-child)::after`
   (0,3,5) ⇒ vẫn lệch ~3,3px. Sửa: `>th:nth-child(n):not(:first-child)::after`. Đo lại < 1px ở mọi ca.
2. `loadPurchaseData` / `loadWarehouseData` **tự dựng tham số, không qua `buildXxxQuery`** ⇒ tick cột thêm có tải lại nhưng không xin
   `cot_them` (cột hiện ra trống). Thử giao diện bắt được; thêm `datCotThem(query, …)` ngay trước `fetch` của 2 hàm đó.
3. Màn PO / 2 màn đối chiếu: ô cuối "Ghi chú" cùng một chuỗi ở 3 bảng ⇒ thay khoanh trong khối từng bảng.

4. **Đợt C bản đầu dùng truy vấn con trong SELECT** `(SELECT TOP 1 SX.… FROM dbo.SALE SX WHERE SX.PR_KEY = DC.PR_KEY_XUAT)` ⇒ đối chứng
   bắt được: câu xuất điều chuyển 1 tuần chạy **221s CPU, 17.077.141 lượt đọc, dop 1** (đọc `sys.dm_exec_requests`) dù `SALE` có khoá chính
   cụm `PK_SALE(PR_KEY)` ⇒ kế hoạch cả CTE đổi hẳn. Claude Code **dừng bài kiểm ngay** (đè DB thật đang chạy iPOS) và làm lại: SQL đối chiếu
   y cũ, đầu phiếu xuất đọc 1 câu riêng (`_dau_phieu_xuat`, `SALE` theo `TRAN_ID` + kỳ) rồi ghép ở Python (`_khoa_pk`, `_dau_phieu_theo_khoa`).
   ⇒ Câu "Đợt C … truy vấn con" ở đoạn dưới đã **HẾT HIỆU LỰC** (giữ nguyên chữ theo luật Append-Only).

**Đợt B / C (khác đợt A ở chỗ nào):** Chứng từ tiền dùng biến cục bộ `VSEL = VOUCHER_SELECT + cột thêm` (3 câu SQL trong `get_voucher`); PO chèn cột
thêm vào CTE `POL` ngay sau `GHI_CHU` (`_po_cte_them`); Bán hàng / Mua hàng / Kho / PO / Đối chiếu gắn `cot_them` trong `buildXxxQuery` (dùng chung
xem + đếm + 2 đường xuất); 2 màn đối chiếu lấy cột từ đầu phiếu xuất bằng truy vấn con `SALE.PR_KEY = DC.PR_KEY_XUAT` (màn điều chuyển tính
1 lần lúc đổ vào `#dc`). Tên danh mục mới: `_dm_ten_cot_them` (Bộ phận = `DM_EXTRA_1`, Nhà cung cấp = `DM_PR_DETAIL`).

**Kiểm (Claude Code, DB thật `IACC_CHULONG`, `test_client`, đối chứng bản `e24d138`):**
- M1: `ast` OK · 206 → 214 hàm (+8 hàm cột thêm), route 80 → 80 · không trùng tên · Babel dịch `index.html` OK (Chrome ngầm — máy không có Node).
- Đợt A Tổng hợp 15/09/2026: **không xin cột thêm ⇒ SQL + JSON trùng khít** ở danh sách, xuất chia sheet, xuất file · xin 4 cột ⇒ cột gốc / tổng
  / phân trang y nguyên, file thêm đúng 4 cột cuối, 33 cột đầu trùng · tên nguồn đơn đúng `DM_EXTRA_2` **500/500** dòng (BHVAT+BHK).
- Đợt B (5 màn): không xin ⇒ SQL + JSON trùng khít (trừ 2 chỗ chỉ khác THỨ TỰ / bộ nhớ đệm, đã chứng minh: Bán hàng — bản cũ chạy thêm 3 câu
  nạp danh mục vì bộ đệm chưa có; Chứng từ kho — **bản cũ gọi 2 lần liên tiếp đã tự ra thứ tự khác**: `ORDER BY ngày, số phiếu` không duy nhất).
  Xin đủ cột ⇒ cột gốc / phân trang / tổng y nguyên ở cả 5 màn · tên NCC đúng `DM_PR_DETAIL` 300/300 · Chứng từ tiền xuất cả ngày 4.807 dòng:
  TẬP dòng 28 cột gốc trùng khít (chỉ khác thứ tự) · Kho cả ngày 20.552 dòng: tập dòng gốc trùng khít · `JOB_QTY` có ở 15.138/15.138 dòng `XKHO`.
- Giao diện (Chrome ngầm 1366×768, server thử 5052 DB giả, dữ liệu từ JSON thật): 6 màn — mặc định cột thêm ẩn, nút không hiện số, "Về mặc
  định" mờ · tick ⇒ **1** lần tải sau 0,7s có `cot_them` · tick 2 cột liền ⇒ 1 lần · bỏ tick ⇒ 0 lần · cấu hình cũ `{an:[…]}` ⇒ cột thêm vẫn ẩn ·
  ghim phải cột thêm OK · số ô tiêu đề = hàng tìm = mỗi dòng dữ liệu · khung cuộn không dư > 1px.

---

## 02/11/2026 (tiếp 2) — Việc 54 · ĐẶC TẢ ĐỢT A cho Hades: khung "cột thêm" + màn Tổng hợp (`ledger`)

### Đại Ca đã chốt bộ cột (02/11/2026, đọc lại từ trang tick — collection `chon_cot`, khớp bản Đại Ca dán)
| Màn | Cột thêm (nguồn) |
|---|---|
| Tổng hợp `ledger` | Ghi chú `L.COMMENTS` · Số lượng `L.QUANTITY` · Nguồn đơn `L.EXTRA_ID_2` (mã + tên) |
| Chứng từ tiền `voucher` | Ghi chú · Tài khoản lập phiếu `USER_ID` · Nguồn nhập phiếu `ORIG_TRAN_ID` · Số chứng từ gốc `ORIG_TRAN_NO` · Bộ phận `EXTRA_ID_1` · Nguồn đơn `EXTRA_ID_2` (đều ở đầu phiếu `VOUCHER`) |
| Bán hàng `sale` | Sản phẩm `PRODUCT_ID`+`PRODUCT_NAME` · Nhóm hàng `ITEM_CLASS_ID` · Loại hàng `ITEM_CLASS1_ID` · Nhóm công việc `JOB_CLASS_ID` · Chiết khấu `REAL_DISCOUNT2_AMOUNT` · Hoa hồng `EXPORT_TAX_AMOUNT` · Voucher `LUX_TAX_AMOUNT` · Mã POS `WORKSTATION_ID` |
| Mua hàng `purchase` | Thành tiền `AMOUNT` · Ghi chú `COMMENTS` · TK công nợ `ACCOUNT_ID` · Nhóm hàng `ITEM_CLASS_ID` · Số chứng từ gốc `ORIG_TRAN_NO` · Giá trị nhập kho `COG_AMOUNT` |
| Danh sách PO `po_list` | Nhà cung cấp `PO_DETAIL.PR_DETAIL_ID` (mã + tên) · Thuế suất `VAT_TAX_RATE` · Tiền thuế `VAT_TAX_AMOUNT` · Tài khoản lập phiếu `PO.USER_ID` · Người liên hệ `PO.CONTACT_PERSON` |
| Chứng từ kho `warehouse` | Sản phẩm `PRODUCT_ID`+`PRODUCT_NAME` · Ghi chú `COMMENTS` · Nhóm hàng `ITEM_CLASS_ID` · Số lượng sản phẩm `JOB_QTY` |
| Tồn kho thực tế | **không thêm** |
| Đối chiếu SX BTP | Tài khoản lập phiếu xuất `SALE.USER_ID` |
| Đối chiếu điều chuyển | Số đơn đặt hàng `SALE.SO_TRAN_NO` · Ghi chú phiếu xuất `SALE.COMMENTS` |

- `JOB_QTY` (Chứng từ kho): **Đại Ca chốt 02/11 — lấy thẳng giá trị trên dòng kho, KHÔNG nối về phiếu bán.** (Claude Code đo ngày 10/09/2026:
  ở `XKHO` khớp số món bán 2.702/2.758 cặp đơn vị × món; ở `XKHOSXBTP` = SL bán thành phẩm, có thể ghi theo ĐVT nhập liệu — chỉ để biết.)
- Bộ phận (Chứng từ tiền): danh mục `DM_EXTRA_1` (`EXTRA_ID_1`, `EXTRA_NAME_1`) có thật, đã đọc 02/11.
- **Kế hoạch 3 đợt:** **A** = khung chung + Tổng hợp (mục này) → Claude Code kiểm DB thật → **B** = Tiền, Bán hàng, Mua hàng, PO, Chứng từ kho
  → **C** = 2 màn đối chiếu (CTE phức tạp). Đợt sau chỉ làm khi đợt trước đạt.
- Đợt đầu cột thêm **chỉ để xem + xuất Excel**: KHÔNG sắp xếp, KHÔNG ô tìm, KHÔNG gom nhóm theo cột thêm.

### Hades đọc trước khi làm
`CLAUDE.md` § 1.1 *Cột của 9 bảng* (luật `COT_BANG` / `HangCot` / `veDongCot`) + Bẫy 6, 26. Chỉ sửa **`server.py`** và **`index.html`**.
Số dòng dưới đây đo trên `main` = `e24d138` (02/11/2026) — **khớp bằng CHUỖI, số dòng chỉ để tìm** (Bẫy 26: mỗi chuỗi neo đã kiểm xuất hiện
đúng 1 lần). Sửa xong một điểm thì điểm sau lệch dòng — tìm lại bằng chuỗi.

### Nguyên lý khung (đọc kỹ — đây là chỗ dễ sai)
1. Cột thêm = **nối vào CUỐI `COT_BANG[tab]`** ⇒ ẩn / ghim / vừa khít / kéo giãn / dòng tổng (`veDongCot`) tự chạy, không sửa các hàm đó.
2. Ô của cột thêm **luôn được vẽ** ở mọi hàng (tiêu đề, hàng ô tìm, hàng dữ liệu) — ẩn bằng CSS như cột thường. ⛔ Không vẽ có điều kiện
   (`{x && <td>}`) — luật `HangCot`: đúng 1 ô / cột.
3. **Mặc định ẩn.** Cột thêm đang hiện lưu ở khoá MỚI `them: [khoá]` trong `lr_cot_<tab>`. ⛔ KHÔNG đưa cột thêm vào `an` — máy đã lưu `an`
   cũ (không chứa cột thêm) sẽ tự hiện hết cột thêm.
4. Máy chủ chỉ SELECT cột thêm được xin qua tham số **`cot_them`** (khoá cách dấu phẩy). ⛔ **Không xin ⇒ chuỗi SQL Y HỆT bản cũ.**
5. Khoá cột thêm = tên trường JSON, luôn bắt đầu **`CT_`** (không đè trường đang có — ví dụ `COMMENTS` đã có trong dữ liệu ledger).
6. Tên theo danh mục (Tên nguồn đơn) **map ở Python**, không JOIN thêm: dùng `_sale_dim_info()["extra2"]` (đã có, `server.py` ~5584).

### SERVER — `server.py`

**S1 · thêm khối khai báo + 4 hàm — chèn NGAY TRƯỚC dòng `@app.route("/api/ledger")` (dòng 2052).** Quét trùng tên hàm trước (Bẫy 2).
```python
# ===== CỘT THÊM 9 MÀN DANH SÁCH (việc 54 — Đại Ca chốt 02/11/2026) =====
# Cột lấy THÊM từ iPOS, mặc định ẩn ở trình duyệt; trình duyệt xin qua tham số `cot_them` (khoá cách dấu phẩy) CHỈ những cột đang hiện.
# ⛔ Không xin gì ⇒ câu SQL Y HỆT trước. Khoá = tên trường JSON / khoá cột file xuất, luôn 'CT_…'.
# ⛔ Khoá + thứ tự phải khớp COT_THEM_DS trong index.html.
# Mỗi cột: (khoá, nhãn file xuất, biểu thức SQL theo bí danh bảng chính của endpoint | None, kiểu 'chu'|'so', ten_tu)
#   ten_tu = (khoá cột mã, tên bản đồ) ⇒ cột TÊN điền ở Python từ danh mục; cột mã được SELECT kèm dù không ai xin.
COT_THEM_DS = {
    'ledger': [
        ('CT_COMMENTS',     'Ghi chú',       'L.COMMENTS',   'chu', None),
        ('CT_QUANTITY',     'Số lượng',      'L.QUANTITY',   'so',  None),
        ('CT_EXTRA_ID_2',   'Mã nguồn đơn',  'L.EXTRA_ID_2', 'chu', None),
        ('CT_EXTRA_NAME_2', 'Tên nguồn đơn', None,           'chu', ('CT_EXTRA_ID_2', 'extra2')),
    ],
}


def _cot_them(tab, args):
    """Các cột thêm được xin, theo thứ tự khai báo. Khoá lạ bị bỏ qua."""
    xin = {k.strip() for k in (args.get('cot_them') or '').split(',') if k.strip()}
    return [c for c in COT_THEM_DS.get(tab, []) if c[0] in xin]


def _cot_them_sql(tab, ds):
    """(đoạn ', biểu thức AS khoá, …' nối vào cuối danh sách SELECT, [khoá theo đúng thứ tự đó]).
    ds rỗng ⇒ ('', []) ⇒ câu SQL không đổi."""
    chon, khoa = [], set()
    for k, _n, bt, _kieu, ten_tu in ds:
        if bt and k not in khoa:
            chon.append((k, bt)); khoa.add(k)
        if ten_tu and ten_tu[0] not in khoa:
            goc = next(c for c in COT_THEM_DS[tab] if c[0] == ten_tu[0])
            chon.append((goc[0], goc[2])); khoa.add(goc[0])
    return ''.join(f', {bt} AS {k}' for k, bt in chon), [k for k, _ in chon]


def _ban_do_cot_them(ds):
    """{tên bản đồ: {mã: tên}} — chỉ nạp bản đồ mà ds cần (gọi MỘT lần mỗi request, không gọi trong vòng lặp)."""
    can = {c[4][1] for c in ds if c[4]}
    bd = {}
    if 'extra2' in can:
        bd['extra2'] = _sale_dim_info().get('extra2', {})
    return bd


def _gan_cot_them(row, ds, bd):
    """Chuẩn hoá giá trị cột thêm trong một dòng dict (sửa tại chỗ): tên lấy từ bản đồ, số → float, chữ → strip, None → ''."""
    for k, _n, _bt, kieu, ten_tu in ds:
        if ten_tu:
            row[k] = bd.get(ten_tu[1], {}).get(str(row.get(ten_tu[0]) or '').strip(), '')
            continue
        v = row.get(k)
        if v is None:
            row[k] = ''
        elif kieu == 'so':
            row[k] = float(v)
        elif isinstance(v, str):
            row[k] = v.strip()
    return row


def _noi_cot_them_xuat(cols, transform, ds, alias):
    """File xuất: nối các cột thêm được xin vào CUỐI (cols + [(khoá, nhãn)]). Cột thêm đứng cuối câu SELECT (alias)
    ⇒ transform cũ nhận đúng phần raw gốc (transform cũ unpack cố định số phần tử). ds rỗng ⇒ trả nguyên."""
    if not ds:
        return cols, transform
    n, bd = len(alias), _ban_do_cot_them(ds)

    def tf(raw, c):
        raw = list(raw)
        row = transform(raw[:len(raw) - n], c)
        them = _gan_cot_them(dict(zip(alias, raw[len(raw) - n:])), ds, bd)
        return list(row) + [them[k] for k, *_ in ds]
    return list(cols) + [(k, nhan) for k, nhan, *_ in ds], tf
```

**S2 · `get_ledger` — sau BASE_COLS (dòng 2079).** Cũ:
```python
            L.EXPENSE_ID_CONTRA, L.PR_DETAIL_ID_CONTRA, L.JOB_ID_CONTRA, L.ITEM_ID_CONTRA
        """

        if join_clauses:
```
Mới:
```python
            L.EXPENSE_ID_CONTRA, L.PR_DETAIL_ID_CONTRA, L.JOB_ID_CONTRA, L.ITEM_ID_CONTRA
        """
        # Cột thêm (việc 54): chỉ cột được xin; không xin ⇒ BASE_COLS y cũ.
        ds_them = _cot_them('ledger', request.args)
        sql_them, _alias_them = _cot_them_sql('ledger', ds_them)
        BASE_COLS += sql_them

        if join_clauses:
```
**S3 · `get_ledger` — cuối vòng lặp dựng dòng (dòng 2304).** Cũ: `            rows_append(r)` + `return jsonify({ "status": "ok", "data": rows,`.
Thêm 1 dòng ngay TRƯỚC `rows_append(r)` (cùng thụt lề 12 dấu cách): `            if ds_them: _gan_cot_them(r, ds_them, bd_them)`
và ngay TRƯỚC dòng `        rows = []` của hàm này (dòng ~2292, ngay sau `def _strip(v): …`) thêm: `        bd_them = _ban_do_cot_them(ds_them)`.
⚠️ `rows = []` có ở nhiều hàm — chỉ sửa trong `get_ledger` (khớp đoạn `        def _strip(v):\n            return v.strip() if isinstance(v, str) else (v or '')\n\n        rows = []\n        rows_append = rows.append` — kiểm count == 1).

**S4 · `get_ledger_stream_csv` — BASE_COLS (dòng 3490) + bọc file xuất (dòng 3543).** Cũ:
```python
            L.BANK_ID_CONTRA, B2.BANK_NAME AS BANK_NAME_CONTRA
        """
        joins = [
```
Mới:
```python
            L.BANK_ID_CONTRA, B2.BANK_NAME AS BANK_NAME_CONTRA
        """
        ds_them = _cot_them('ledger', args)   # cột thêm (việc 54) — đứng cuối SELECT, xem _noi_cot_them_xuat
        sql_them, alias_them = _cot_them_sql('ledger', ds_them)
        BASE_COLS += sql_them
        joins = [
```
và cũ: `        headers, transform = _loc_cot_xuat(LEDGER_CSV_COLS, transform, args)   # bỏ cột đang ẩn (25/09/2026)` → mới (2 dòng):
```python
        cols_xuat, transform = _noi_cot_them_xuat(LEDGER_CSV_COLS, transform, ds_them, alias_them)
        headers, transform = _loc_cot_xuat(cols_xuat, transform, args)   # bỏ cột đang ẩn (25/09/2026)
```

**S5 · `get_ledger_export` (xuất chia sheet theo đơn vị) — dòng 6139 + 6178.** Cũ:
```python
            P.ITEM_NAME AS PRODUCT_NAME, B.BANK_NAME, B2.BANK_NAME AS BANK_NAME_CONTRA
        """
```
Mới — thêm ngay sau dòng `"""` đó:
```python
        ds_them = _cot_them('ledger', request.args)   # cột thêm (việc 54)
        sql_them, _alias_them = _cot_them_sql('ledger', ds_them)
        BASE_COLS += sql_them
        bd_them = _ban_do_cot_them(ds_them)
```
và cũ: `            rows.append(r)` + `\n\n        return jsonify({"status": "ok", "data": rows, "total_rows": len(rows)})` → thêm ngay TRƯỚC `rows.append(r)`:
`            if ds_them: _gan_cot_them(r, ds_them, bd_them)`

### TRÌNH DUYỆT — `index.html`

**F1 · khai báo — chèn NGAY TRƯỚC `        const COT_BANG = {` (dòng 5312):**
```javascript
        // ===== CỘT THÊM 9 MÀN DANH SÁCH (việc 54 — Đại Ca chốt 02/11/2026) =====
        // Cột lấy thêm từ iPOS — MẶC ĐỊNH ẨN, nằm cuối hộp Cấu hình cột dưới dòng "Cột thêm". Nối vào CUỐI COT_BANG (dưới) ⇒ ẩn / ghim /
        // vừa khít / kéo giãn chạy như cột thường. Cột đang hiện lưu ở khoá `them` của lr_cot_<tab> (KHÔNG ở `an`). Máy chủ chỉ trả cột
        // đang hiện (tham số cot_them). Đợt đầu: chỉ xem + xuất Excel — không sắp xếp / ô tìm / gom nhóm theo cột thêm.
        // [khoá = trường JSON 'CT_…', nhãn, độ rộng px, kiểu 'chu' | 'so']. ⛔ Khoá + thứ tự khớp COT_THEM_DS trong server.py.
        const COT_THEM_DS = {
            ledger: [['CT_COMMENTS', 'Ghi chú', 220, 'chu'], ['CT_QUANTITY', 'Số lượng', 96, 'so'],
                     ['CT_EXTRA_ID_2', 'Mã nguồn đơn', 112, 'chu'], ['CT_EXTRA_NAME_2', 'Tên nguồn đơn', 180, 'chu']],
        };
        const laCotThem = (tab, k) => (COT_THEM_DS[tab] || []).some(c => c[0] === k);
        // Ô tiêu đề / ô hàng tìm / ô dữ liệu của cột thêm — LUÔN vẽ đủ (ẩn bằng CSS), đúng 1 ô / cột.
        const veThCotThem = (tab) => (COT_THEM_DS[tab] || []).map(([k, nhan]) => <th key={k} className="border-r px-3">{nhan}</th>);
        const veThTimCotThem = (tab) => (COT_THEM_DS[tab] || []).map(([k]) => <th key={k} className="border-r px-1 py-1"></th>);
        const veTdCotThem = (tab, r) => (COT_THEM_DS[tab] || []).map(([k, , , kieu]) => {
            const v = r[k];
            return kieu === 'so'
                ? <td key={k} className="border-r text-right font-mono px-2">{v === '' || v == null ? '' : fmtNum(v)}</td>
                : <td key={k} className="border-r whitespace-nowrap truncate max-w-[250px] px-3">{v == null ? '' : v}</td>;
        });
```
⚠️ Kiểm `fmtNum` khai ở cấp ngoài cùng (đang dùng trong các Row cấp ngoài — dòng ~5161) — nếu không, báo lại, đừng tự viết hàm mới.

**F2 · nối cột thêm vào COT_BANG — chèn ngay SAU dấu `        };` đóng `COT_BANG` (chuỗi neo `        };\n\n        // ===== ĐIỀU HƯỚNG 2 TẦNG`, dòng 5322):**
```javascript
        // Cột thêm (việc 54) đứng CUỐI mỗi bảng — thứ tự này phải đúng thứ tự ô trong JSX (veThCotThem / veThTimCotThem / veTdCotThem).
        Object.keys(COT_THEM_DS).forEach(tab => {
            COT_BANG[tab] = COT_BANG[tab].concat(COT_THEM_DS[tab].map(([k, nhan, rong]) => [k, nhan, rong, [k]]));
        });
```

**F3 · `LedgerRow` — ô cuối (dòng 5211).** Cũ:
```javascript
                <td className="px-4 whitespace-nowrap italic text-teal-700">{r.BANK_NAME_CONTRA}</td>
            </HangCot>
        ));
```
Mới:
```javascript
                <td className="border-r px-4 whitespace-nowrap italic text-teal-700">{r.BANK_NAME_CONTRA}</td>
                {veTdCotThem('ledger', r)}
            </HangCot>
        ));
```

**F4 · tiêu đề + hàng ô tìm bảng ledger (dòng 10162 và ~10173).** Cũ: `className="w-44 px-4" align="left">NH đối ứng</SortableHeader>` + xuống dòng
`                                                </HangCot>` → mới: đổi `className="w-44 px-4"` thành `className="border-r w-44 px-4"` **chỉ ở ô "NH đối
ứng" này**, và chèn dòng `                                                    {veThCotThem('ledger')}` ngay trước `</HangCot>` đó.
Hàng ô tìm: ngay sau khối `.map((key, idx) => ( <th …>…</th> ))}` của hàng `HangCot bang="ledger" className="bg-indigo-50/60 border-b-2
border-indigo-200"` (dòng ~10172 `                                                    ))}`), trước `</HangCot>` của hàng đó, chèn
`                                                    {veThTimCotThem('ledger')}`. ⚠️ Chuỗi `))}` + `</HangCot>` có ở nhiều bảng — neo bằng
đoạn chứa `onChange={e => setColSearch(p => ({...p, [key]: e.target.value}))}` (chỉ ledger dùng `setColSearch` trần — kiểm count).

**F5 · `loadData` của ledger (dòng 7550).** Cũ:
```javascript
                if (ledgerSort.field) { query.set('order_by', ledgerSort.field); query.set('order_dir', ledgerSort.dir); }

                try {
                    const r = await fetch(`/api/ledger?
```
Mới — chèn giữa 2 khối đó: `                const ctLedger = cotThemDangHien('ledger'); if (ctLedger.length) query.set('cot_them', ctLedger.join(','));`
⛔ Chuỗi `if (ledgerSort.field) …` còn 1 bản nữa ở `buildExportQuery` (dòng ~8813) — KHÔNG sửa bản đó (xuất Excel thêm cot_them ở F10).

**F6 · đọc cấu hình đã lưu (dòng 9356).** Cũ: `                            vua: Array.isArray(v.vua) ? v.vua : [] };` → mới:
`                            vua: Array.isArray(v.vua) ? v.vua : [], them: Array.isArray(v.them) ? v.them : [] };`

**F7 · `anCot` + 2 hàm mới (dòng 9391).** Cũ (1 dòng):
```javascript
            const anCot = (tab) => new Set(((cauHinhCot[tab] || {}).an || []).filter(k => k !== '_stt'));   // cột # không bao giờ ẩn
```
Mới:
```javascript
            // Cột đang ẩn = `an` (cột gốc, cột # không bao giờ ẩn) + mọi cột thêm KHÔNG nằm trong `them` (việc 54: cột thêm mặc định ẩn).
            const anCot = (tab) => {
                const c = cauHinhCot[tab] || {};
                const s = new Set((c.an || []).filter(k => k !== '_stt' && !laCotThem(tab, k)));
                const hien = new Set(c.them || []);
                (COT_THEM_DS[tab] || []).forEach(([k]) => { if (!hien.has(k)) s.add(k); });
                return s;
            };
            // Cột thêm đang hiện — đọc qua REF (gọi từ loadData / hẹn giờ, closure có thể cũ). Gửi máy chủ qua tham số cot_them.
            const cotThemDangHien = (tab) => {
                const hien = new Set((cauHinhCotRef.current[tab] || {}).them || []);
                return (COT_THEM_DS[tab] || []).map(c => c[0]).filter(k => hien.has(k));
            };
            // Danh sách cho hộp Cấu hình cột: chèn dòng tiêu đề nhóm '#them' trước cột thêm đầu tiên (CauHinhCot vẽ khoá '#…' thành tiêu đề).
            const dsCauHinhCot = (tab) => {
                const goc = COT_BANG[tab], n = (COT_THEM_DS[tab] || []).length;
                return n ? [...goc.slice(0, goc.length - n), ['#them', 'Cột thêm (mặc định ẩn)'], ...goc.slice(goc.length - n)] : goc;
            };
```
⚠️ `cauHinhCotRef` khai ngay trên `luuCot` (dòng ~9361) — `cotThemDangHien` chỉ được GỌI lúc chạy (không gọi lúc render đầu) nên dùng được.

**F8 · `cssCot` (dòng 9401–9413) — thay cả khối.** Cũ: từ `            const cssCot = Object.keys(COT_BANG).map(tab => {` tới `            }).join('');`
(khối đầu tiên ngay sau `const anXuat = …`). Mới:
```javascript
            const cssCot = Object.keys(COT_BANG).map(tab => {
                const c = cauHinhCot[tab];
                if (!c && !COT_THEM_DS[tab]) return '';   // màn không có cột thêm + chưa cấu hình ⇒ y như trước
                const cc = c || {};
                const an = anCot(tab), rong = cc.rong || {}, vua = new Set(cc.vua || []), b = `table[data-bang="${tab}"]`;
                const tt = thuTuCot(tab);
                let cuoi = 0;
                const css = tt.map((i, vt0) => {
                    const k = COT_BANG[tab][i][0], n = vt0 + 1;
                    if (an.has(k) && k !== '_stt') return `${b}>thead>tr>:nth-child(${n}),${b}>tbody>tr:not(.dong-nhom)>:nth-child(${n}){display:none}`;
                    cuoi = n;
                    // Cột đã "vừa khít": bỏ trần max-width của ô (Diễn giải đang cắt ở 250px) để hiện đủ chữ.
                    return (rong[k] ? `${b}>thead>tr:first-child>:nth-child(${n}){width:${rong[k]}px;min-width:${rong[k]}px}` : '')
                        + (vua.has(k) ? `${b}>tbody>tr:not(.dong-nhom)>:nth-child(${n}){max-width:none!important}` : '');
                }).join('');
                // Tay kéo của cột cuối ĐANG HIỆN phải nằm gọn trong ô (như luật th:last-child ở <style>, việc 50 — lệch 4px). Cột thêm ẩn
                // đứng sau nên :last-child không còn bắt đúng cột đó.
                return css + (cuoi > 1 && cuoi < tt.length
                    ? `${b}>thead>tr:first-child>:nth-child(${cuoi})::after{right:0}`
                      + `${b}>thead>tr:first-child>:nth-child(${cuoi}):hover::after{background:linear-gradient(to right,transparent 5px,#60a5fa 5px,#60a5fa 7px,transparent 7px)}`
                    : '');
            }).join('');
```

**F9 · hộp Cấu hình cột của 9 màn (dòng 9715–9720).** Cũ:
```javascript
                            <CauHinhCot ds={COT_BANG[tab]} an={anCot(tab)}
```
→ mới: `                            <CauHinhCot ds={dsCauHinhCot(tab)} an={anCot(tab)}`
và thêm 2 prop ngay sau dòng `ghiChu={false}`:
```javascript
                                demAn={[...anCot(tab)].filter(k => !laCotThem(tab, k)).length}
                                laMacDinh={!(((cauHinhCot[tab] || {}).an || []).length || ((cauHinhCot[tab] || {}).them || []).length
                                    || Object.keys((cauHinhCot[tab] || {}).rong || {}).length || ctxCotBang[tab])}
```
Cũ (dòng 9720):
```javascript
                                onDoi={an => luuCot(tab, { ...(cauHinhCot[tab] || { rong: {} }), an })} onMacDinh={() => luuCot(tab, { an: [], rong: {}, ghim: { trai: [], phai: [] }, vua: [] })} />
```
Mới:
```javascript
                                onDoi={an => doiCotDs(tab, an)} onMacDinh={() => luuCot(tab, { an: [], rong: {}, ghim: { trai: [], phai: [] }, vua: [], them: [] })} />
```
và khai `doiCotDs` + ref hẹn giờ — chèn ngay SAU khối `const dsCauHinhCot = …` ở F7:
```javascript
            // Tick / bỏ tick trong hộp Cấu hình cột: cột gốc → `an`, cột thêm → `them`. Bật một cột thêm CHƯA có trong số liệu đang có
            // ⇒ tải lại sau 0,7s kể từ lần tick cuối (khuôn henTaiCotRef của báo cáo — máy chủ chạy tuần tự, đừng bắn nhiều câu).
            const henTaiCotDsRef = useRef(null);
            const doiCotDs = (tab, an) => {
                const c = cauHinhCot[tab] || { rong: {} };
                const them = (COT_THEM_DS[tab] || []).map(x => x[0]).filter(k => !an.includes(k));
                luuCot(tab, { ...c, an: an.filter(k => !laCotThem(tab, k)), them });
                const dong0 = (duLieuBangRef.current[tab] || []).find(r => r && !r.isGroup);
                if (dong0 && them.some(k => !(k in dong0))) {
                    clearTimeout(henTaiCotDsRef.current);
                    henTaiCotDsRef.current = setTimeout(() => { if (tab === 'ledger') loadData(filters.page || 1, filters.page_size); }, 700);
                }
            };
```
⚠️ Kiểm `duLieuBangRef.current[tab]` đúng là mảng dữ liệu đang tải của bảng (đang dùng ở `vuaKhitCot`, dòng ~9500) — nếu khác, báo lại.
⚠️ Bỏ tick cột thêm ⇒ **không** gọi máy chủ (chỉ CSS ẩn).

**F10 · xuất Excel — 2 đường.**
(a) Một file qua máy chủ — `startServerExport` (dòng 8846). Cũ: `                    if (boCot.length) q.set('an_cot', boCot.join(','));` → thêm ngay sau:
`                    const ctXuat = cotThemDangHien(kind); if (ctXuat.length) q.set('cot_them', ctXuat.join(','));`
(b) Chia sheet theo đơn vị ở trình duyệt — `doExport`. Cũ (dòng 8911): `                    const countQuery = buildExportQuery(kind);` → thêm ngay sau:
`                    const ctXuat = cotThemDangHien(kind); if (ctXuat.length) countQuery.set('cot_them', ctXuat.join(','));`
(chỉ đường `kind === 'ledger'` dùng `countQuery` cho URL dữ liệu — các màn khác làm ở đợt B). Và cũ (dòng 8969):
```javascript
                    const boXuat = new Set(anXuat(kind));
                    const cols = colsGoc.filter(([k]) => !boXuat.has(k));
```
Mới:
```javascript
                    const boXuat = new Set(anXuat(kind));
                    const cols = colsGoc.concat((COT_THEM_DS[kind] || []).map(([k, nhan]) => [k, nhan])).filter(([k]) => !boXuat.has(k));
```

### Bẫy phải né (Claude Code liệt kê)
1. Vẽ ô cột thêm có điều kiện ⇒ cả hàng lệch cột khi ghim (luật `HangCot`).
2. Dùng `an` cho cột thêm ⇒ máy đã lưu cấu hình cũ hiện hết cột thêm ngay khi cập nhật.
3. Đặt khoá cột thêm trùng trường có sẵn (`COMMENTS`) ⇒ Diễn giải đổi giá trị. Luôn `CT_`.
4. `transform` cũ của stream_csv unpack cố định 34 phần tử — cột thêm phải đứng CUỐI SELECT và đi qua `_noi_cot_them_xuat`, không sửa transform cũ.
5. `_noi_cot_them_xuat` phải chạy TRƯỚC `_loc_cot_xuat`.
6. Gọi `_sale_dim_info()` / dựng bản đồ trong vòng lặp từng dòng ⇒ chậm — chỉ gọi 1 lần / request (`_ban_do_cot_them`).
7. Sửa nhầm bản sao của chuỗi neo (`if (ledgerSort.field)…`, `rows = []`, `))}`+`</HangCot>`) — khớp đúng đoạn dài ghi ở trên, count == 1.
8. Không thêm route mới ⇒ không đụng `PERM_PUBLIC` (Bẫy 30).

### Ca nghiệm thu (Claude Code chạy — Hades không chạy lệnh được)
- M1: `ast.parse(server.py)` + không trùng tên hàm + đếm hàm/route (chỉ +5 hàm, route giữ nguyên) · Babel dịch `index.html` không lỗi.
- M2 (DB thật, `test_client`): `/api/ledger` **không `cot_them` ⇒ chuỗi SQL + JSON trùng khít bản `e24d138`** · có đủ 4 cột ⇒ 4 trường `CT_…`, tên
  nguồn đơn đúng `DM_EXTRA_2` · chỉ xin `CT_EXTRA_NAME_2` vẫn ra tên · `stream_csv` có cột thêm ⇒ 4 cột cuối file, không có ⇒ tiêu đề file y cũ ·
  `/api/ledger/export` có cột thêm.
- Giao diện (Chrome ngầm 1366×768): chưa cấu hình ⇒ 4 cột thêm ẩn, nút Cấu hình cột **không** hiện số, "Về mặc định" mờ · tick ⇒ hiện + **1**
  lần tải sau 0,7s · bỏ tick ⇒ ẩn, không tải · `lr_cot_ledger` cũ `{an:[…]}` ⇒ cột thêm vẫn ẩn · ghim cột thêm sang phải đúng · vừa khít cột thêm ·
  khung cuộn rộng = bảng (không dư 4px) · xuất Excel 1 file + chia sheet có đúng cột thêm đang hiện.

### Việc của Hades — BƯỚC 1 (CHƯA sửa file)
Đọc mục này + code thật ở các chuỗi neo; trả lời: (1) chỗ nào trong đặc tả **không khớp** file thật (chuỗi neo không có / không duy nhất,
`fmtNum` / `duLieuBangRef` / `cauHinhCotRef` khác mô tả) · (2) rủi ro Claude Code bỏ sót · (3) kế hoạch thứ tự sửa. **Không sửa file nào ở bước này.**

---

## 02/11/2026 (tiếp) — Việc 54: đã đo DB thật · trang cho Đại Ca tick cột — ⏳ chờ Đại Ca tick

**Đo xong** (Claude Code, 02/11/2026 ~17:10, chỉ đọc DB, không import server): 13 nguồn của 9 màn — mẫu: `LEDGER` ngày 15/09/2026
(92.664 dòng) · `SALE_VIEW` / `WAREHOUSE_VIEW` / `VOUCHER` tuần 08–14/09/2026 · `PURCHASE_VIEW`, `WAREHOUSE_BALANCE_ACTUAL`, đầu phiếu
`XKHOSXBTP` / `NSP` / `XDCNB` / `NDCNB` cả T09/2026 · `PO` + `PO_DETAIL` cả 2026. Mỗi cột: tỉ lệ dòng có giá trị + 3 giá trị hay gặp.
Kết quả thô: `C:\Users\quang.tran\AppData\Local\Temp\lr_do_cot_them\ket_qua.json` (ngoài repo).

**Lọc tay còn 93 cột ứng viên** (bỏ khoá nội bộ, cột `_ORIG` trùng, cột hằng, cột trống 100%), 20 cột Claude Code gợi ý. Ghi nhận lúc lọc:
- `ledger`: **Ghi chú (`COMMENTS`, 92,6%) chưa bao giờ hiện** — màn vẽ `DESCRIPTION || COMMENTS` mà `DESCRIPTION` có 100%.
- `purchase`: màn có Đơn giá + Tổng tiền nhưng **chưa có Thành tiền** (`AMOUNT`, 99,4%).
- `warehouse_balance`: bảng gốc không có cột nào đáng thêm — ứng viên lấy từ danh mục (Nhóm hàng, Loại hàng, Nhóm kho).
- Tên nhóm theo BC017: `ITEM_CLASS_ID` = **Nhóm hàng**, `ITEM_CLASS1_ID` = **Loại hàng**; tiền bán hàng theo BC015 (Chiết khấu =
  `REAL_DISCOUNT2_AMOUNT`, Hoa hồng = `EXPORT_TAX_AMOUNT`, Voucher = `LUX_TAX_AMOUNT`).
- `JOB_QTY` của Chứng từ kho: chưa chắc nghĩa — phải đối chiếu iPOS trước khi đưa vào đặc tả.

**Trang tick cột (riêng tư):** https://claude.ai/artifact/DnbhfR1Qc6Jqv763PcuLNj — lựa chọn lưu ở collection `chon_cot`, mỗi màn một
tài liệu `{ them: [nguồn.CỘT…], luc }`; Claude Code đọc lại bằng ArtifactData. Màn chưa có tài liệu = **chưa chốt**.

**Nháp khung kỹ thuật** (chưa phải đặc tả): `C:\Users\quang.tran\AppData\Local\Temp\lr_do_cot_them\thiet_ke_khung.md` — cột thêm nối
CUỐI `COT_BANG` (ẩn / ghim / vừa khít tự chạy), mặc định ẩn bằng khoá `them` mới trong `lr_cot_<tab>` (không dùng `an` — máy đã lưu
`an` cũ sẽ tự hiện hết), máy chủ nhận `cot_them` và chỉ SELECT cột được xin (không xin ⇒ SQL y cũ), không thêm route.
**Hades vẫn chưa nhận việc.**

---

## 02/11/2026 — Việc 54: "Chọn thêm cột" cho 9 màn danh sách chứng từ — ⏳ chờ đo DB + Đại Ca tick cột

**Đại Ca yêu cầu (02/11/2026):** *"Trong các danh sách chứng từ t muốn có thêm điều kiện được chọn thêm cột trong bảng danh sách
chứng từ"*. Hiện nút **Cấu hình cột** của 9 màn chỉ ẩn/hiện các cột đang có (`COT_BANG`); chưa có cột mới lấy thêm từ iPOS.

**Đại Ca chốt (02/11/2026, qua câu hỏi):**
- Làm cả **4 phân hệ**: Tổng hợp (`ledger`) · Tiền (`voucher`) · Mua & bán (`sale`, `purchase`, `po_list`) · Kho (`warehouse`,
  `warehouse_balance`, `btp_reconcile`, `dcnb_reconcile`).
- Bộ cột thêm: **Claude Code đo trên DB thật** (tỉ lệ có giá trị + giá trị mẫu), đưa danh sách để **Đại Ca tick**.
- **Hades code**; Claude Code viết đặc tả + duyệt + kiểm lại.

**Khuôn đề xuất** (giống BC017 / việc 50 đợt 1 — CLAUDE.md § 1.2): cột thêm nằm trong hộp Cấu hình cột, **mặc định ẩn**; máy chủ
**chỉ SELECT cột đang tick** (không tick gì ⇒ câu SQL y như cũ, phải so trùng khít); Excel theo cột đang hiện; nhớ trên máy.

**Trạng thái:** chờ Đại Ca điền lại mật khẩu SQL vào `config.json` (đã xoá 05/10) để đo. Script đo (chỉ đọc DB, không import
server) nằm ngoài repo: `C:\Users\quang.tran\AppData\Local\Temp\lr_do_cot_them\do_cot_them.py`. **Hades chưa nhận việc** —
đặc tả gửi sau khi Đại Ca tick xong bộ cột.
