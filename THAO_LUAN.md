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

## 05/11/2026 (~14:45) — Việc 56: ✅ M2/M4 DB thật ĐẠT toàn bộ ca nghiệm thu N1–N7

Đại Ca bật VPN ⇒ `kiem_m2_bc018.py` (test_client, DB thật): N1 khớp file 693/693 ô + thứ tự dòng + 8 khu vực + 310.058.331.121 (8,3s) · N2
288.305.680.519 (10,3s) · N3 53.997.961.628 · N4 58.311.193.092 · N5 34.821.910.549 (1,3s) · N6 nhãn qua năm · 2 ca lỗi 400 · N7 quyền đạt ·
metadata `khu_vuc` thật đạt. Lần chạy đầu rớt VPN giữa chừng (N2 lỗi kết nối 08001) — chạy lại đạt hết. **Không ca nào lỗi.**

---

## 05/11/2026 (~14:40) — Việc 56: KẾT QUẢ Claude Code làm theo đặc tả · ✅ M1 + giao diện + quyền · ⏳ M2 DB thật chờ VPN

- Áp đủ S1–S4 + F1–F22 bằng script khớp chuỗi (`ap_bc018.py`, mỗi neo `count == 1`); `git diff` chỉ thay đúng 14 dòng đã nêu trong đặc tả.
- **Khác đặc tả:** K4 thêm `width: auto !important` cho `.bc018-table .col-value` — luật chung `.col-value { width: 130px; }` (`index.html:178`)
  ép mọi cột tháng 130px ⇒ cả năm rộng 2.052px; nay 92px / 1.558px. Đặc tả cũ chỉ đặt `min-width` nên không thắng được luật chung.
- Kiểm: M1 đạt · endpoint thật chạy trên số thật (DB giả) N1–N6 + 2 ca lỗi đạt · N7 quyền đạt · giao diện 1366px + Excel đạt (chi tiết trong
  `NHAT_KY_CONG_VIEC.md` mục 05/11). **M2 trên DB thật chưa chạy** — máy mất VPN (TCP 9001 hết giờ chờ).

---

## 05/11/2026 (~14:00) — Việc 56: Đại Ca đổi — **Claude Code tự code** theo đặc tả bên dưới, Hades KHÔNG sửa file nào

- 11:50 giao BƯỚC 1 bằng `agy -p --mode plan` chạy ngầm ⇒ Đại Ca không thấy cửa sổ, hỏi *"Hades có đang làm không"* ⇒ Đại Ca bảo *"mở trong
  tab orca đi"* ⇒ Claude Code tắt lượt chạy ngầm (chưa ra gì), mở tab Orca "Hades — BC018" (`agy -i … --mode plan`), chọn "trust folder".
- Hades đọc 10 file, nghĩ 8 phút 50 giây rồi **dừng lượt KHÔNG trả lời gì** (13:55 tab đứng ở dấu nhắc trống; tab bị Orca nạp lại, mất chế độ
  plan). Không file nào bị sửa (`git status`: chỉ `THAO_LUAN.md`).
- Đại Ca 05/11: *"m làm luôn đi"* ⇒ Claude Code đóng tab Hades, tự làm S1–S4 + F1–F22 đúng đặc tả mục dưới (khác đặc tả chỗ nào sẽ ghi ở mục
  kết quả).

---

## 05/11/2026 — Việc 56: BC018 · Doanh thu thuần theo chi nhánh — ĐẶC TẢ cho Hades · ⏳ BƯỚC 1 (chỉ trình kế hoạch + diff)

**Đại Ca yêu cầu (05/11/2026):** *"ngoài desktop t có 1 file BC_Doanh_Thu_Thuan_Chi_Nhanh_T1-T10_2026 — t muốn cụ thể hoá nó thành 1 cái
báo cáo trong ledger report"*. File mẫu: `C:\Users\quang.tran\Desktop\BC_Doanh_Thu_Thuan_Chi_Nhanh_T1-T10_2026.xlsx` (1 sheet: STT · Mã ĐV ·
Tên chi nhánh · Tháng 1…10 · Tổng cộng; dòng khu vực in đậm nền `#DCE9F5` = SUBTOTAL; TỔNG CỘNG nền `#FFF2CC`; số `#,##0;(#,##0);"-"`;
A4 ngang; ghi chú cách tính ở cuối).

**Đại Ca chốt (05/11/2026, qua câu hỏi):** ① **Hades code** · ② **Bán hàng nội bộ (BNB): có nút bật/tắt — mặc định TÍNH như file**, chọn
"Bỏ bán nội bộ" thì trừ ra · ③ **có ô lọc Khu vực** cạnh ô Đơn vị.

### Số đo DB thật (Claude Code, `IACC_CHULONG`, chỉ đọc, 05/11/2026) — đã chốt cách tính
- **Doanh thu thuần = PS Có 511 − PS Nợ 521, không tính kết chuyển** (Có 511 đối ứng 911 · Nợ 521 đối ứng 511/911). Khớp file **693/693 ô
  T1–T9** (77 đơn vị × 9 tháng, từng đồng) + đúng thứ tự dòng. Cùng công thức dòng *Doanh thu thuần* (mã 03) của BC001 (đã thử 4 công thức —
  ra y nhau). Đối chiếu chéo: tổng T1–T9 = **310.058.331.121** = đúng số bút toán KC Nợ 511 / Có 911 cùng kỳ.
- T10 lệch 26/78 đơn vị (đơn vị `83` mới có 27,5 triệu, `76` −1,27 triệu, `42` +1,42 triệu…) — số T10 trên DB đổi sau ngày lập file 03/11
  (chưa kiểm chứng nguyên nhân). **Ca nghiệm thu dùng T1–T9.**
- **Khu vực = đơn vị CHA trong `DM_ORGANIZATION`** (8/8 nhóm của file khớp `PARENT_ORGANIZATION_ID`: 001 HCM · 003 Đà Nẵng · 004 Hà Nội ·
  005 Kiên Giang · 006 Quảng Ngãi · 007 Huế · 009 Các quán ngoài · `00` ⇒ "Trực thuộc công ty"). Thứ tự nhóm = mã cha, `00` cuối; trong
  nhóm = mã đơn vị (chuỗi). Chỉ hiện đơn vị có doanh thu trong kỳ (T1–T9 thì `82` ẩn — đúng như file "chỉ liệt kê đơn vị có doanh thu").
- BNB (`SYS_TRAN`: "Bán hàng nội bộ") T1–T9 = **21.752.650.602** (đơn vị `01` + 150.000 ở `48`).
- ⛔ **Tốc độ — chỉ mục quyết định:** `IX_LEDGER_ACC_DATE` (khoá `ACCOUNT_ID, TRAN_DATE`; INCLUDE `DEBIT_CREDIT, ORGANIZATION_ID,
  ACCOUNT_ID_CONTRA, AMOUNT`…) **phủ đủ câu chính nhưng KHÔNG có `TRAN_ID`**. Câu chính T1–T9 **5,7s** (1 tháng 1,2–1,8s). Nhắc tới `TRAN_ID`
  trong câu chính (WHERE hay CASE) ⇒ **27–40s**. Bỏ BNB = **câu riêng** `WHERE L.TRAN_ID = 'BNB'` (đi `IX_LEDGER_TRAN_ID_DATE`, 17.692 dòng)
  **2,2s** rồi trừ ở Python ⇒ 288.305.680.519, trùng khít cách lọc WHERE.

### Máy chủ — `server.py` (4 điểm; khớp chuỗi, `count == 1`, KHÔNG dò số dòng — Bẫy 26)

**S1 — dòng 171** (mã quyền mới; app tự gửi mã mới lên Google — Bẫy 22, không sửa `Code.gs`):
```python
PERM_REPORTS = ['BC%03d' % i for i in range(1, 18)]          # BC001..BC017
```
→
```python
PERM_REPORTS = ['BC%03d' % i for i in range(1, 19)]          # BC001..BC018
```

**S2 — dòng 254** (khai quyền route — thiếu là nhân viên 403, ADMIN không thấy lỗi — Bẫy 30): ngay SAU dòng
`    '/api/sale_detail': 'BC017', '/api/sale_detail/export': 'BC017',` thêm:
```python
    '/api/dt_thuan_chi_nhanh': 'BC018',          # BC018 Doanh thu thuần theo chi nhánh (05/11/2026)
```

**S3 — `/api/metadata`: danh sách Khu vực.** (a) Ngay SAU 2 dòng (1794–1795):
```python
            logger.warning('Metadata: khong doc duoc danh muc nhom (BC017): %s', e)
            cursor = conn.cursor()
```
thêm:
```python

        # Khu vực cho ô lọc BC018 (05/11/2026) = đơn vị CHA của các đơn vị đang dùng; '00' (công ty) ⇒ "Trực thuộc công ty".
        # Câu riêng, hỏng thì danh sách rỗng — đừng kéo chết cả màn hình vì 1 ô lọc.
        khu_vuc = []
        try:
            cursor.execute("""
                SELECT DISTINCT ISNULL(O.PARENT_ORGANIZATION_ID, ''), P.ORGANIZATION_NAME
                FROM dbo.DM_ORGANIZATION O WITH (NOLOCK)
                LEFT JOIN dbo.DM_ORGANIZATION P WITH (NOLOCK) ON P.ORGANIZATION_ID = O.PARENT_ORGANIZATION_ID
                WHERE O.ACTIVE = 1 AND ISNULL(O.PARENT_ORGANIZATION_ID, '') <> ''
            """)
            for cha, ten in cursor.fetchall():
                cha = (cha or '').strip()
                khu_vuc.append({"id": cha, "name": 'Trực thuộc công ty' if cha == '00' else ((ten or '').strip() or cha)})
            khu_vuc.sort(key=lambda k: (k["id"] == '00', k["id"]))
        except Exception as e:
            logger.warning('Metadata: khong doc duoc danh sach khu vuc (BC018): %s', e)
            cursor = conn.cursor()
```
(b) dòng 1834 `            "job_classes": lop_nhom['job_class'],` → thêm ngay sau: `            "khu_vuc": khu_vuc,`

**S4 — endpoint mới.** Ngay SAU 2 dòng cuối của `get_sale_by_source` (khớp chuỗi):
```python
        logger.error(f"Error in BC015 get_sale_by_source: {msg}")
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500
```
thêm (giữ 2 dòng trống trước khối `# BC017 …` phía dưới):
```python


# =====================================================================
# BC018 — DOANH THU THUẦN THEO CHI NHÁNH (Đại Ca chốt 05/11/2026, theo file BC_Doanh_Thu_Thuan_Chi_Nhanh_T1-T10_2026.xlsx)
# =====================================================================
# Doanh thu thuần = PS Có 511 − PS Nợ 521, KHÔNG tính kết chuyển (Có 511 đối ứng 911 · Nợ 521 đối ứng 511/911) — cùng số dòng
# "Doanh thu thuần" (mã 03) của BC001. Đo 05/11/2026: khớp file 693/693 ô T1–T9; tổng T1–T9 = đúng bút toán KC 511→911.
# Khu vực = đơn vị CHA trong DM_ORGANIZATION ('00' ⇒ "Trực thuộc công ty") ⇒ mở chi nhánh mới tự vào đúng nhóm.
# ⛔ Câu chính KHÔNG được nhắc tới TRAN_ID: IX_LEDGER_ACC_DATE phủ đủ cột của nó nhưng không có TRAN_ID — nhắc tới là SQL phải tra
#    từng dòng (đo T1–T9: 5,7s → 27–40s). Bỏ bán nội bộ = câu RIÊNG theo IX_LEDGER_TRAN_ID_DATE (2,2s) rồi trừ ở Python.
BC018_DT_SQL = """CASE WHEN L.ACCOUNT_ID LIKE '511%' AND L.DEBIT_CREDIT = 'CRD'
                       AND ISNULL(L.ACCOUNT_ID_CONTRA, '') NOT LIKE '911%' THEN L.AMOUNT
                  WHEN L.ACCOUNT_ID LIKE '521%' AND L.DEBIT_CREDIT = 'DEB'
                       AND ISNULL(L.ACCOUNT_ID_CONTRA, '') NOT LIKE '511%'
                       AND ISNULL(L.ACCOUNT_ID_CONTRA, '') NOT LIKE '911%' THEN -L.AMOUNT
                  ELSE 0 END"""
BC018_TRAN_NOI_BO = 'BNB'      # SYS_TRAN "Bán hàng nội bộ" — gần như chỉ Kho Tổng 01
BC018_TOI_DA_THANG = 36


@app.route("/api/dt_thuan_chi_nhanh")
@with_db_lock
def get_dt_thuan_chi_nhanh():
    """BC018 — dòng = đơn vị (nhóm theo khu vực = đơn vị cha), cột = từng tháng trong kỳ. bo_bnb=1 ⇒ trừ bán hàng nội bộ."""
    try:
        f_date = request.args.get("from_date")
        t_date = request.args.get("to_date")
        if not f_date or not t_date:
            return jsonify({"status": "error", "message": "Thiếu từ ngày / đến ngày"}), 400
        org_ids = [v for v in request.args.get("org_ids", "").split(",") if v]
        kv_ids = {v.strip() for v in request.args.get("kv_ids", "").split(",") if v.strip()}
        bo_bnb = request.args.get("bo_bnb") == "1"
        tu = datetime.strptime(f_date, "%d/%m/%Y")
        den = datetime.strptime(t_date, "%d/%m/%Y")
        if den < tu:
            return jsonify({"status": "error", "message": "Đến ngày phải sau Từ ngày"}), 400

        # Cột = MỌI tháng trong kỳ, kể cả tháng chưa có số (như file mẫu).
        thang = []
        y, m = tu.year, tu.month
        while (y, m) <= (den.year, den.month):
            thang.append((y, m))
            y, m = (y + 1, 1) if m == 12 else (y, m + 1)
        if len(thang) > BC018_TOI_DA_THANG:
            return jsonify({"status": "error", "message": f"Kỳ báo cáo tối đa {BC018_TOI_DA_THANG} tháng"}), 400
        mot_nam = len({a for a, _ in thang}) == 1
        cot = {k: i for i, k in enumerate(thang)}

        f_dt = tu.strftime("%Y%m%d")
        t_dt = (den + timedelta(days=1)).strftime("%Y%m%d")      # TRAN_DATE là smalldatetime: "< ngày kế tiếp"
        _oc, _op = _org_filter_sql(org_ids, "L.ORGANIZATION_ID")   # quyền đơn vị + loại đơn vị ngoài cây
        org_where = (" AND " + _oc) if _oc else ""
        dk = "L.TRAN_DATE >= ? AND L.TRAN_DATE < ? AND (L.ACCOUNT_ID LIKE '511%' OR L.ACCOUNT_ID LIKE '521%')"
        gom = " GROUP BY L.ORGANIZATION_ID, YEAR(L.TRAN_DATE), MONTH(L.TRAN_DATE)"
        params = [f_dt, t_dt] + list(_op)                         # đúng thứ tự dấu ? (Bẫy 5)

        so = {}   # đơn vị -> [số từng tháng]

        def cong(rows, dau):
            for org, yy, mm, v in rows:
                i = cot.get((int(yy), int(mm)))
                if i is None:
                    continue
                o = (str(org) if org is not None else "").strip()
                so.setdefault(o, [0.0] * len(thang))[i] += dau * float(v or 0)

        cur = get_connection().cursor()
        cur.execute(f"SELECT L.ORGANIZATION_ID, YEAR(L.TRAN_DATE), MONTH(L.TRAN_DATE), SUM({BC018_DT_SQL}) "
                    f"FROM dbo.LEDGER L WITH (NOLOCK) WHERE {dk}{org_where}{gom}", params)
        cong(cur.fetchall(), 1)
        if bo_bnb:
            cur.execute(f"SELECT L.ORGANIZATION_ID, YEAR(L.TRAN_DATE), MONTH(L.TRAN_DATE), SUM({BC018_DT_SQL}) "
                        f"FROM dbo.LEDGER L WITH (NOLOCK) WHERE L.TRAN_ID = ? AND {dk}{org_where}{gom}",
                        [BC018_TRAN_NOI_BO] + params)
            cong(cur.fetchall(), -1)

        cur.execute("SELECT ORGANIZATION_ID, ORGANIZATION_NAME, ISNULL(PARENT_ORGANIZATION_ID, '') FROM dbo.DM_ORGANIZATION WITH (NOLOCK)")
        dm = {(r[0] or '').strip(): ((r[1] or '').strip(), (r[2] or '').strip()) for r in cur.fetchall()}

        nhom = {}
        for o, ds in so.items():
            if all(round(x, 2) == 0 for x in ds):
                continue                                          # chỉ đơn vị có doanh thu trong kỳ (như file)
            cha = dm.get(o, ('', ''))[1]
            if kv_ids and cha not in kv_ids:
                continue                                          # ô Khu vực: lọc ở Python, KHÔNG thêm vào SQL
            nhom.setdefault(cha, []).append(o)

        tong = [0.0] * len(thang)
        ket = []
        for cha in sorted(nhom, key=lambda c: (c == '', c == '00', c)):   # mã cha tăng dần, "Trực thuộc công ty" rồi "ngoài cây" cuối
            cong_kv = [0.0] * len(thang)
            dong = []
            for o in sorted(nhom[cha]):
                ds = so[o]
                for i, x in enumerate(ds):
                    cong_kv[i] += x
                dong.append({"org_id": o, "org_name": dm.get(o, ('', ''))[0] or o,
                             "so": [round(x, 2) for x in ds], "tong": round(sum(ds), 2)})
            for i, x in enumerate(cong_kv):
                tong[i] += x
            ten = 'Trực thuộc công ty' if cha == '00' else (dm.get(cha, ('', ''))[0] or 'Ngoài cây đơn vị')
            ket.append({"kv": cha, "ten": ten, "so": [round(x, 2) for x in cong_kv], "tong": round(sum(cong_kv), 2), "dong": dong})

        return jsonify({
            "status": "ok",
            "bo_bnb": bo_bnb,
            "thang": [{"nam": a, "thang": b, "nhan": f"Tháng {b}" if mot_nam else f"T{b}/{a}"} for a, b in thang],
            "nhom": ket,
            "tong": {"so": [round(x, 2) for x in tong], "tong": round(sum(tong), 2)},
        })
    except Exception as e:
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()
        logger.error(f"Error in BC018 get_dt_thuan_chi_nhanh: {msg}")
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500
```

### Giao diện — `index.html` (22 điểm, theo thứ tự dòng; mọi chuỗi neo đã kiểm: xuất hiện ĐÚNG 1 lần)

⚠️ Trong bảng dưới, `\|\|` là **`||`** (dấu `|` phải thoát cho bảng Markdown) — trong code viết `||`, KHÔNG có dấu `\`. Số dòng là của file
TRƯỚC khi sửa; sửa xong điểm trên là điểm dưới lệch dòng ⇒ **luôn tìm theo chuỗi neo**.

| # | Dòng | Neo (code cũ) | Sửa |
|---|---|---|---|
| F1 | 1546 | dòng `{ id: 'BC017', name: 'BÁO CÁO BÁN HÀNG', …` | thêm NGAY SAU: `{ id: 'BC018', name: 'BÁO CÁO DOANH THU THUẦN THEO CHI NHÁNH', ten: 'Doanh thu thuần theo chi nhánh', mo_ta: 'Doanh thu thuần từng chi nhánh theo tháng, cộng theo khu vực' },` |
| F2 | 2190 | dòng `{ id: 'loaict',   ten: 'Loại chứng từ', …co: (t) => t === 'BC017' },` | thêm NGAY SAU: `// BC018 (05/11/2026): Khu vực = đơn vị CHA trong danh mục đơn vị (danh sách do /api/metadata trả — khu_vuc)` + `{ id: 'khuvuc',   ten: 'Khu vực',         khoa: 'kv_ids',         co: (t) => t === 'BC018' },` |
| F3 | 2195 | `BC017: ['donvi', 'kho', …, 'loaict'],` (trong `THU_TU_O_LOC`) | thêm NGAY SAU: `BC018: ['khuvuc', 'donvi'],` |
| F4 | 2510 | trong chữ ký `ReportTab`: `saleSourceMode, setSaleSourceMode, nxtData, nxtGroupBy` | → `saleSourceMode, setSaleSourceMode, bc18BoBnb = false, setBc18BoBnb, nxtData, nxtGroupBy` |
| F5 | 2553 | `nhomcv: meta.job_classes \|\| [], loaict: (meta.tran_ids_by_tab && meta.tran_ids_by_tab.sale) \|\| meta.tran_ids \|\| [] };` | → giữ nguyên, thay `[] };` cuối bằng `[], khuvuc: meta.khu_vuc \|\| [] };` |
| F6 | 2822 | `BC016: 'BC016_Nhap_Xuat_Ton_Nha_Hang'` (trong `REPORT_FILE`) | → `BC016: 'BC016_Nhap_Xuat_Ton_Nha_Hang',` + dòng mới `BC018: 'BC018_Doanh_Thu_Thuan_Chi_Nhanh'` |
| F7 | 2999 | `BC015: '', BC016: ''` (trong `REPORT_PATTERNS`) | → `BC015: '', BC016: '', BC018: ''` (không có thì xuất ra chữ "Mẫu B02 - DN") |
| F8 | 3015 | `else if (reportType === 'BC016') reportTitle = 'BÁO CÁO NHẬP XUẤT TỒN NHÀ HÀNG';` | thêm NGAY SAU: `else if (reportType === 'BC018') reportTitle = 'BÁO CÁO DOANH THU THUẦN THEO CHI NHÁNH';` |
| F9 | 3046 | `if (reportType === 'BC015') dongPhu.push('Nguồn đơn: Tất cả');` | thêm NGAY SAU khối **K1** (dưới bảng) |
| F10 | 3088–3089 | `landscape: reportType === 'BC015' \|\| reportType === 'BC016',` · `fit_width: reportType === 'BC016',` | → `landscape: reportType === 'BC015' \|\| reportType === 'BC016' \|\| reportType === 'BC018',` · `fit_width: reportType === 'BC016' \|\| reportType === 'BC018',` (giữ chú thích cuối dòng) |
| F11 | 3575–3576 | `onDoi={(k, an, x) => { setBc17Kieu(k); … }} />` + dòng kế `)}` | thêm NGAY SAU `)}` đó khối **K2** (nút bán nội bộ) |
| F12 | 3661 | `<NutXuat khongCoSo={reportType === 'BC017' ? ` | → `<NutXuat khongCoSo={reportType === 'BC018' ? !(initialReportData && initialReportData.nhom && initialReportData.nhom.length) : reportType === 'BC017' ? ` |
| F13 | 3667 | `'BC014', 'BC015', 'BC016', 'BC017'].includes(reportType) ? 'paper-landscape'` | → `'BC014', 'BC015', 'BC016', 'BC017', 'BC018'].includes(reportType) ? 'paper-landscape'` |
| F14 | 3680 | `(reportType === 'BC015' \|\| reportType === 'BC016' \|\| reportType === 'BC017') ? ''` | → `(reportType === 'BC015' \|\| reportType === 'BC016' \|\| reportType === 'BC017' \|\| reportType === 'BC018') ? ''` |
| F15 | 3684 | `reportType === 'BC017' ? 'BÁO CÁO BÁN HÀNG' :` | → `reportType === 'BC017' ? 'BÁO CÁO BÁN HÀNG' : reportType === 'BC018' ? 'BÁO CÁO DOANH THU THUẦN THEO CHI NHÁNH' :` |
| F16 | 3712–3714 | `{reportType === 'BC015' && (` + `<div …>Nguồn đơn: Tất cả</div>` + `)}` | thêm NGAY SAU khối **K3** (dòng phụ trên giấy) |
| F17 | 3753 | `{reportType === 'BC015' && (` + dòng kế `<style>{\`` + `.bc015-table { width: 100% …` | chèn NGAY TRƯỚC khối **K4** (style) |
| F18 | 3885 | `${reportType === 'BC017' ? 'bc017-table' : ''}` | → `${reportType === 'BC017' ? 'bc017-table' : ''} ${reportType === 'BC018' ? 'bc018-table' : ''}` |
| F19 | 4245 | `) : reportType === 'BC016' ? (` | → khối **K5** rồi mới tới `) : reportType === 'BC016' ? (` |
| F20 | 7059 | `const [saleSourceMode, setSaleSourceMode] = useState('summary');     // BC015: …` | thêm NGAY SAU: `const [bc18BoBnb, setBc18BoBnb] = useState(false);              // BC018: true = bỏ bán hàng nội bộ (BNB)` |
| F21 | 7117 | `bc_wh_ids: [], item_class_ids: [], pr_class_ids: [], job_class_ids: [], bc_tran_ids: [] });` | → `… bc_tran_ids: [],` + dòng `// BC018 (05/11/2026): ô Khu vực` + `kv_ids: [] });` (thiếu là `toggleFilter` gọi `.includes` trên undefined ⇒ văng) |
| F22 | 9246 | `} else if (reportType === 'BC015') {` (trong `loadReportData`) | chèn NGAY TRƯỚC khối **K6** · và dòng 11512 `setSaleSourceMode={setSaleSourceMode}` thêm ngay sau: `bc18BoBnb={bc18BoBnb}` + `setBc18BoBnb={setBc18BoBnb}` |

**K1 — dòng phụ file Excel (F9):**
```jsx
                if (reportType === 'BC018') {
                    const kvDs = meta.khu_vuc || [];
                    dongPhu.push('Khu vực: ' + ((filters.kv_ids || []).length ? filters.kv_ids.map(id => { const k = kvDs.find(x => x.id === id); return k ? k.name : id; }).join(', ') : 'Tất cả'));
                    dongPhu.push((initialReportData && initialReportData.bo_bnb) ? 'Không tính bán hàng nội bộ (BNB)' : 'Có tính bán hàng nội bộ (BNB)');
                    dongPhu.push('Doanh thu thuần = PS Có TK 511 − PS Nợ TK 521, không tính bút toán kết chuyển');
                }
```
**K2 — nút bán nội bộ (F11):**
```jsx
                            {reportType === 'BC018' && (
                                // Bán hàng nội bộ (BNB) — Đại Ca chốt 05/11/2026: mặc định TÍNH như file mẫu; "Bỏ bán nội bộ" để xem doanh thu bán ra
                                // ngoài. Có số liệu rồi thì đổi là tải lại luôn — giá trị MỚI đi qua modeArg (bẫy stale closure BC014/BC015).
                                <div className="flex bg-slate-100 p-0.5 rounded-lg border border-slate-200 shrink-0 h-[32px] items-center">
                                    <button disabled={loading} onClick={() => { if (!bc18BoBnb || loading) return; setBc18BoBnb(false); if (initialReportData && initialReportData.nhom) loadReportData(1, { boBnb: false }); }} className={`px-3 py-1 rounded-md text-[10px] font-bold transition-all ${!bc18BoBnb ? 'bg-white text-indigo-700 shadow-sm' : 'text-slate-500 hover:text-slate-800'} disabled:opacity-50`}>Gồm bán nội bộ</button>
                                    <button disabled={loading} onClick={() => { if (bc18BoBnb || loading) return; setBc18BoBnb(true); if (initialReportData && initialReportData.nhom) loadReportData(1, { boBnb: true }); }} className={`px-3 py-1 rounded-md text-[10px] font-bold transition-all ${bc18BoBnb ? 'bg-white text-indigo-700 shadow-sm' : 'text-slate-500 hover:text-slate-800'} disabled:opacity-50`}>Bỏ bán nội bộ</button>
                                </div>
                            )}
```
**K3 — dòng phụ trên giấy (F16):**
```jsx
                                {reportType === 'BC018' && (<>
                                    <div className="text-[10px] font-bold text-slate-600 uppercase">Khu vực: {(filters.kv_ids || []).length > 0 ? filters.kv_ids.map(id => {
                                        const k = (meta.khu_vuc || []).find(x => x.id === id);
                                        return k ? k.name : id;
                                    }).join(', ') : 'Tất cả'}</div>
                                    <div className="text-[10px] font-bold text-slate-600 uppercase">{(initialReportData && initialReportData.bo_bnb) ? 'Không tính bán hàng nội bộ (BNB)' : 'Có tính bán hàng nội bộ (BNB)'}</div>
                                    <div className="text-[9px] text-slate-500 italic">Doanh thu thuần = PS Có TK 511 − PS Nợ TK 521, không tính bút toán kết chuyển</div>
                                </>)}
```
**K4 — style (F17):**
```jsx
                                {reportType === 'BC018' && (
                                    <style>{`
                                        .bc018-table { border-collapse: collapse !important; }
                                        .bc018-table th, .bc018-table td { border: 1px solid #cbd5e1 !important; font-size: 11px !important; padding: 4px 6px !important; white-space: nowrap !important; }
                                        .bc018-table .col-value { min-width: 92px !important; text-align: right !important; }
                                        .bc018-table th.col-value { text-align: center !important; }
                                        .bc018-table tr.dong-kv td { background-color: #DCE9F5 !important; }
                                        .bc018-table tr.dong-tong td { background-color: #FFF2CC !important; }
                                    `}</style>
                                )}
```
**K5 — thân bảng (F19)** — chèn trước `) : reportType === 'BC016' ? (`, nối chuỗi ba ngôi y như nhánh BC017 (`})() : …`):
```jsx
                                    ) : reportType === 'BC018' ? (() => {
                                        // BC018 (05/11/2026) — y file mẫu Đại Ca: STT · Mã ĐV · Tên chi nhánh · từng tháng · Tổng cộng; dòng khu vực tô
                                        // xanh = cộng các chi nhánh bên dưới; TỔNG CỘNG tô vàng. Số âm trong ngoặc, 0 ⇒ "-" (formatNum — cùng định dạng file).
                                        const d18 = initialReportData || {};
                                        const th18 = d18.thang || [], nh18 = d18.nhom || [];
                                        let stt = 0;
                                        return (<>
                                            <thead>
                                                <tr>
                                                    <th className="text-center">STT</th>
                                                    <th className="text-center">Mã ĐV</th>
                                                    <th className="text-center">Tên chi nhánh</th>
                                                    {th18.map(t => <th key={`${t.nam}-${t.thang}`} className="col-value">{t.nhan}</th>)}
                                                    <th className="col-value">Tổng cộng</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {nh18.map(n => (
                                                    <React.Fragment key={'kv' + n.kv}>
                                                        <tr className="dong-kv font-black">
                                                            <td colSpan={3}>{n.ten}</td>
                                                            {n.so.map((v, i) => <td key={i} className="col-value">{formatNum(v)}</td>)}
                                                            <td className="col-value">{formatNum(n.tong)}</td>
                                                        </tr>
                                                        {n.dong.map(r => (
                                                            <tr key={r.org_id} className="hover:bg-slate-50">
                                                                <td className="text-center">{++stt}</td>
                                                                <td className="text-center">{r.org_id}</td>
                                                                <td>{r.org_name}</td>
                                                                {r.so.map((v, i) => <td key={i} className="col-value">{formatNum(v)}</td>)}
                                                                <td className="col-value font-bold">{formatNum(r.tong)}</td>
                                                            </tr>
                                                        ))}
                                                    </React.Fragment>
                                                ))}
                                                {nh18.length === 0 && (
                                                    <tr><td colSpan={4 + th18.length} className="text-center py-8 text-slate-400 text-xs italic">Không có doanh thu trong kỳ báo cáo đã chọn</td></tr>
                                                )}
                                                {nh18.length > 0 && d18.tong && (
                                                    <tr className="dong-tong font-black">
                                                        <td colSpan={3} className="text-center uppercase">Tổng cộng</td>
                                                        {d18.tong.so.map((v, i) => <td key={i} className="col-value">{formatNum(v)}</td>)}
                                                        <td className="col-value">{formatNum(d18.tong.tong)}</td>
                                                    </tr>
                                                )}
                                            </tbody>
                                        </>);
                                    })() : reportType === 'BC016' ? (
```
**K6 — tải số liệu (F22, trong `loadReportData` ở App):**
```jsx
                    } else if (reportType === 'BC018') {
                        // modeArg { boBnb } = giá trị MỚI của nút bán nội bộ (state vừa set chưa vào closure — bẫy stale closure BC014/BC015).
                        const boBnb = (modeArg && typeof modeArg === 'object' && modeArg.boBnb !== undefined) ? modeArg.boBnb : bc18BoBnb;
                        const q2 = new URLSearchParams({ from_date: filters.from_date, to_date: filters.to_date, org_ids: filters.org_ids.join(','), kv_ids: (filters.kv_ids || []).join(','), bo_bnb: boBnb ? '1' : '0' });
                        const r = await fetch(`/api/dt_thuan_chi_nhanh?${q2.toString()}`, { signal: abortRef.current.signal });
                        if (r.status === 401) { setIsLoggedIn(false); return; }
                        const res = await r.json();
                        if (res.status === 'ok') {
                            setReportData(res);
                        } else {
                            alert('Lỗi xem báo cáo doanh thu thuần theo chi nhánh: ' + (res.message || 'không có dữ liệu'));
                        }
```
(khối K6 kết thúc ở đây; dòng `} else if (reportType === 'BC015') {` cũ đứng ngay sau, giữ nguyên.)

### Bẫy phải né
1. ⛔ **Không nhắc `TRAN_ID` trong câu chính** (kể cả `CASE`) — tụt 5,7s → 27–40s (đo 05/11). BNB chỉ ở câu riêng khi `bo_bnb=1`.
2. ⛔ Ô Khu vực lọc **ở Python** sau khi gom, đừng thêm `IN (SELECT … DM_ORGANIZATION)` vào SQL (đo: 7,7–13,4s, không lợi, rủi ro kế hoạch).
3. Quyền đơn vị đi **duy nhất** qua `_org_filter_sql` — áp cho CẢ câu BNB (cùng `org_where` + `params`). Đừng tự lọc `app_orgs`.
4. Thứ tự params = thứ tự dấu `?` (Bẫy 5): câu BNB là `[BC018_TRAN_NOI_BO] + params` vì `L.TRAN_ID = ?` đứng ĐẦU WHERE.
5. `kv_ids: []` phải có trong state `filters` mặc định (F21) — thiếu là bấm ô Khu vực văng (`toggleFilter` gọi `p[key].includes`).
6. K5 là nhánh ba ngôi giữa chuỗi `reportType === …` — sai một ngoặc là trắng cả màn Báo cáo TC. Đừng thêm `{x && <td>}` có điều kiện trong hàng.
7. `server.py` **không import `Decimal`** — giữ `float` như đặc tả (số tới 9 triệu tỷ vẫn chính xác từng đồng; trả `round(…, 2)`).
8. Không đụng `CO_GI_MOI.md`, `version.txt`, `build_exe.py`, `release.yml`, `Code.gs` — Claude Code lo phần phát hành.

### Ca nghiệm thu (Claude Code chạy — M1 `ast` + Babel · M2 `test_client` DB thật · M4 so file mẫu)
| Ca | Gọi | Phải ra |
|---|---|---|
| N1 | `from_date=01/01/2026&to_date=30/09/2026` | 9 cột "Tháng 1…9" · 8 nhóm `001,003,004,005,006,007,009,00` (53·3·7·1·1·3·6·2 đơn vị) · **TỔNG 310.058.331.121** · khớp file 693/693 ô, đúng thứ tự dòng |
| N2 | N1 + `bo_bnb=1` | **288.305.680.519** · đơn vị `01` giảm đúng phần BNB · thời gian ≤ câu N1 + ~3s |
| N3 | N1 + `kv_ids=004` | 1 nhóm Hà Nội 7 đơn vị · **53.997.961.628** |
| N4 | N1 + `kv_ids=009,00` | 2 nhóm (6 + 2 đơn vị) · **58.311.193.092** |
| N5 | `01/09/2026–30/09/2026` | 1 cột "Tháng 9" · **34.821.910.549** |
| N6 | `01/12/2025–31/01/2026` | cột "T12/2025", "T1/2026" |
| N7 | tài khoản giới hạn đơn vị `02` (gieo phiên, KHÔNG phải ADMIN) | 200 · chỉ 1 nhóm, 1 đơn vị `02` · không có quyền BC018 ⇒ **403** |
| N8 | quét route chưa khai quyền (Bẫy 30) | `[]` |
| N9 | giao diện 1366px (Chrome ngầm) | BC018 có trong trang liệt kê + Ctrl+F · hàng điều kiện 1 dòng · nút bán nội bộ tải lại 1 lần · xuất Excel: tiêu đề + 3 dòng phụ, nền xanh/vàng, số âm âm thật |

### ➡️ BƯỚC 1 cho Hades (chỉ ĐỌC — chưa sửa file nào)
Đọc `CLAUDE.md` + mục này, mở đúng các dòng nêu trên, rồi trình: (a) xác nhận từng neo S1–S4, F1–F22 khớp file thật (neo nào lệch thì ghi
rõ); (b) diff dự kiến cho từng điểm; (c) rủi ro / chỗ nghi đặc tả sai. **Chưa sửa file.** Claude Code soát xong mới ghi lệnh duyệt BƯỚC 2.

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
