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

## 06/11/2026 (chiều) — Việc 58: ô "Loại trừ đơn vị" (mọi báo cáo) + "Loại trừ kho" (BC016, BC017) + "Chọn tất cả" mọi ô — ĐẶC TẢ cho Hades · 4 TAB · ⏳ BƯỚC 1

**Đại Ca 06/11/2026:** *"Chổ bộ lọc cho t thêm cái chọn tất cả, với lại 1 ô loại ra đi, ví dụ thay vì t tích chọn xong t bỏ thì t sễ cùng ô loại trừ các kho
không muốn xuất"*. Chốt qua câu hỏi: ô loại trừ cho **Kho (BC016 + BC017)** và **Đơn vị (mọi báo cáo)** · kiểu **ô riêng** ("Loại trừ kho" / "Loại trừ
đơn vị"), **mặc định nằm trong Bộ lọc nâng cao** · **"Chọn tất cả" ở mọi ô chọn nhiều của Báo cáo TC**. Hades code, giữ 2 bước, `gemini-3.8-flash-medium`.

**Thiết kế (Claude Code đo trước):**
- Máy chủ: mọi báo cáo (18) + mọi đường xuất đều lọc đơn vị qua **một hàm `_org_filter_sql`** (40 chỗ gọi), và mọi đường xuất dựng SQL **trong** yêu cầu rồi mới
  giao luồng nền ⇒ chỉ sửa hàm đó: đọc tham số `org_ids_bo` của yêu cầu đang chạy, bớt các đơn vị đó ở mọi nhánh. **Không gửi ⇒ SQL y hệt bản cũ.**
  Kho: `/api/nxt` (BC016) + `_bc017_where` (BC017 xem + xuất) thêm `NOT IN` theo `wh_ids_bo`.
- ⛔ **Bẫy: 9 màn danh sách dựng yêu cầu bằng `{ ...filters }`** (dòng ~7889/8000/8128/8288 — chung state `filters` với Báo cáo TC) ⇒ **khoá state phải là
  `bc_org_ids_bo` / `bc_wh_ids_bo`** (khác tên tham số), tham số `org_ids_bo` / `wh_ids_bo` CHỈ gửi qua hàm `thamSoLoaiTru` ở các yêu cầu của báo cáo.
  Đặt state tên `org_ids_bo` là 9 màn danh sách tự nhận ô loại trừ của báo cáo (cùng lý do BC017 dùng `bc_wh_ids`).
- ⛔ **Bẫy thứ tự ô:** `oLocCo` sắp theo `THU_TU_O_LOC` bằng `indexOf` ⇒ ô mới không có trong danh sách ra **−1 ⇒ nhảy lên ĐẦU**, chiếm chỗ ô ngoài (BC016 sẽ đẩy
  Hàng hoá vào trong). ⇒ cờ `macDinhTrong` + xếp cuối + `docCauHinhLoc` thêm tham số `trong`.
- "Chọn tất cả": `PremiumDropdown` đã có (`coChonTatCa`, chỉ ô Đơn vị của quản trị dùng) ⇒ bật cho mọi ô. ⛔ **Trần 300 mục**: mỗi mục = 1 tham số SQL (SQL
  Server tối đa 2.100 / câu, nhiều câu dùng lại danh sách 2–3 lần) + URL quá dài ⇒ quá 300 thì hiện dòng nhắc "gõ để thu hẹp" thay cho nút.

### PHẦN G — `server.py` (tab "Hades G") · 4 điểm

**G1** — import (dòng 48). CŨ:
```python
from flask import Flask, jsonify, request, session, send_from_directory
```
MỚI:
```python
from flask import Flask, jsonify, request, session, send_from_directory, has_request_context
```

**G2** — `_org_filter_sql` (~dòng 7980–7998, thay CẢ hàm). CŨ:
```python
def _org_filter_sql(org_ids, col="ORGANIZATION_ID"):
    """Trả (clause, params) cho bộ lọc đơn vị.
    - Có chọn đơn vị  -> col IN (...)  (tôn trọng đúng lựa chọn, kể cả đơn vị ngoài)
    - Không chọn      -> mặc định loại đơn vị ngoài cây 00 (col NOT IN externals)
    """
    # ÉP QUYỀN ĐƠN VỊ theo tài khoản (row-level). Điểm DUY NHẤT — mọi danh sách/báo cáo đi qua đây.
    allowed = _current_allowed_orgs()
    if allowed is not None:
        base = [str(o) for o in org_ids] if org_ids else None
        eff = [o for o in base if o in allowed] if base else sorted(allowed)
        if not eff:
            return "1=0", []                 # chọn toàn đơn vị ngoài quyền → không trả dòng nào
        return f"{col} IN ({','.join(['?'] * len(eff))})", list(eff)
    if org_ids:
        return f"{col} IN ({','.join(['?'] * len(org_ids))})", list(org_ids)
    ext = _get_external_org_ids()
    if ext:
        return f"{col} NOT IN ({','.join(['?'] * len(ext))})", list(ext)
    return "", []
```
MỚI:
```python
def _org_loai_tru():
    """Đơn vị LOẠI TRỪ của yêu cầu đang chạy — ô "Loại trừ đơn vị" của Báo cáo TC (Đại Ca chốt 06/11/2026), tham số `org_ids_bo`.
    CHỈ yêu cầu của Báo cáo TC gửi tham số này (trình duyệt: thamSoLoaiTru; state tên bc_org_ids_bo) ⇒ 9 màn danh sách không bị ảnh hưởng.
    Ngoài ngữ cảnh yêu cầu (luồng nền) ⇒ rỗng — mọi đường xuất đều dựng SQL TRONG yêu cầu rồi mới giao luồng nền (đã kiểm 06/11/2026)."""
    if not has_request_context():
        return set()
    return {v.strip() for v in (request.args.get("org_ids_bo") or "").split(",") if v.strip()}


def _org_filter_sql(org_ids, col="ORGANIZATION_ID"):
    """Trả (clause, params) cho bộ lọc đơn vị.
    - Có chọn đơn vị  -> col IN (...)  (tôn trọng đúng lựa chọn, kể cả đơn vị ngoài)
    - Không chọn      -> mặc định loại đơn vị ngoài cây 00 (col NOT IN externals)
    - Ô "Loại trừ đơn vị" (org_ids_bo, 06/11/2026) -> bớt các đơn vị đó ở MỌI nhánh. Không gửi ⇒ clause + params y hệt bản cũ.
    """
    bo = _org_loai_tru()
    # ÉP QUYỀN ĐƠN VỊ theo tài khoản (row-level). Điểm DUY NHẤT — mọi danh sách/báo cáo đi qua đây.
    allowed = _current_allowed_orgs()
    if allowed is not None:
        base = [str(o) for o in org_ids] if org_ids else None
        eff = [o for o in base if o in allowed] if base else sorted(allowed)
        eff = [o for o in eff if o not in bo]
        if not eff:
            return "1=0", []                 # chọn toàn đơn vị ngoài quyền (hoặc loại trừ hết) → không trả dòng nào
        return f"{col} IN ({','.join(['?'] * len(eff))})", list(eff)
    if org_ids:
        chon = [o for o in org_ids if str(o).strip() not in bo]
        if not chon:
            return "1=0", []                 # loại trừ hết các đơn vị đã chọn → không trả dòng nào
        return f"{col} IN ({','.join(['?'] * len(chon))})", list(chon)
    ext = _get_external_org_ids()
    loai = list(ext) + sorted(b for b in bo if b not in {str(x) for x in ext})
    if loai:
        return f"{col} NOT IN ({','.join(['?'] * len(loai))})", loai
    return "", []
```

**G3** — `/api/nxt` (BC016), sau vòng lọc kho / hàng / nhóm (~dòng 9830–9834). CŨ:
```python
                wparams.extend(vals)

        gkey_sql = "W.WAREHOUSE_ID" if group_by == "warehouse" else "W.ITEM_CLASS_ID"
```
MỚI:
```python
                wparams.extend(vals)
        # Ô "Loại trừ kho" (06/11/2026): NOT IN, đứng sau các IN ⇒ dấu ? vẫn đúng thứ tự wparams (Bẫy 5)
        bo_kho = [v for v in request.args.get("wh_ids_bo", "").split(",") if v]
        if bo_kho:
            where.append(f"W.WAREHOUSE_ID NOT IN ({','.join(['?'] * len(bo_kho))})")
            wparams.extend(bo_kho)

        gkey_sql = "W.WAREHOUSE_ID" if group_by == "warehouse" else "W.ITEM_CLASS_ID"
```

**G4** — `_bc017_where` (BC017 xem + xuất), sau vòng lọc (~dòng 9418–9421). CŨ:
```python
            clauses.append(f"{cot} IN ({','.join(['?'] * len(vals))})")
            params.extend(vals)
    if args.get("an_0d") == "1":
```
MỚI:
```python
            clauses.append(f"{cot} IN ({','.join(['?'] * len(vals))})")
            params.extend(vals)
    # Ô "Loại trừ kho" (06/11/2026): NOT IN sau các IN ⇒ thứ tự dấu ? = thứ tự params
    bo_kho = lay("wh_ids_bo")
    if bo_kho:
        clauses.append(f"S.WAREHOUSE_ID NOT IN ({','.join(['?'] * len(bo_kho))})")
        params.extend(bo_kho)
    if args.get("an_0d") == "1":
```

### PHẦN H — `index.html`, khai báo ô + "Chọn tất cả" (tab "Hades H") · 8 điểm

**H1** — `O_LOC_BAO_CAO`, ngay sau ô Nguồn đơn (~dòng 2235). CŨ:
```js
            { id: 'nguondon', ten: 'Nguồn đơn',       khoa: 'source_ids',     co: (t) => t === 'BC015' },
```
MỚI:
```js
            { id: 'nguondon', ten: 'Nguồn đơn',       khoa: 'source_ids',     co: (t) => t === 'BC015' },
            // Ô LOẠI TRỪ (06/11/2026, Đại Ca chốt: ô riêng, mặc định trong Bộ lọc nâng cao). ⛔ Khoá state RIÊNG bc_…_bo: 9 màn danh sách dựng yêu cầu
            // bằng { ...filters } ⇒ đặt trùng tên tham số là danh sách tự lọc theo ô của báo cáo. Gửi máy chủ CHỈ qua thamSoLoaiTru.
            { id: 'donvi_bo', ten: 'Loại trừ đơn vị', khoa: 'bc_org_ids_bo',  co: () => true, macDinhTrong: true },
            { id: 'kho_bo',   ten: 'Loại trừ kho',    khoa: 'bc_wh_ids_bo',   co: (t) => t === 'BC016' || t === 'BC017', macDinhTrong: true },
```

**H2** — `docCauHinhLoc` nhận danh sách ô mặc định nằm trong (~dòng 2335). CŨ:
```js
        const docCauHinhLoc = (bc, dsId, toiDa = TOI_DA_O_NGOAI, macDinh = toiDa) => {
```
MỚI:
```js
        const docCauHinhLoc = (bc, dsId, toiDa = TOI_DA_O_NGOAI, macDinh = toiDa, trong = []) => {
```

**H3** — cùng hàm (~dòng 2340). CŨ:
```js
            const batSan = (luu && Array.isArray(luu.ngoai)) ? luu.ngoai : dsId.slice(0, Math.min(macDinh, toiDa) - 1);
```
MỚI:
```js
            const batSan = (luu && Array.isArray(luu.ngoai)) ? luu.ngoai : dsId.filter(id => !trong.includes(id)).slice(0, Math.min(macDinh, toiDa) - 1);
```

**H4** — `ReportTab`, thứ tự ô (~dòng 2590–2592). CŨ:
```js
            const oLocCo = O_LOC_BAO_CAO.filter(o => o.co(reportType))
                .sort((a, b) => thuTuRieng ? thuTuRieng.indexOf(a.id) - thuTuRieng.indexOf(b.id) : 0);
            const cfgLoc = cauHinhLoc[reportType] || docCauHinhLoc(reportType, oLocCo.map(o => o.id));
```
MỚI:
```js
            // Ô macDinhTrong (ô loại trừ) luôn xếp CUỐI + mặc định trong Bộ lọc nâng cao — không thì indexOf = −1 đưa nó lên ĐẦU, chiếm chỗ ô ngoài.
            const viTriO = (o) => o.macDinhTrong ? 999 : (thuTuRieng ? thuTuRieng.indexOf(o.id) : 0);
            const oLocCo = O_LOC_BAO_CAO.filter(o => o.co(reportType))
                .sort((a, b) => viTriO(a) - viTriO(b));
            const cfgLoc = cauHinhLoc[reportType] || docCauHinhLoc(reportType, oLocCo.map(o => o.id), TOI_DA_O_NGOAI, TOI_DA_O_NGOAI, oLocCo.filter(o => o.macDinhTrong).map(o => o.id));
```

**H5** — `nguonOLoc` (~dòng 2601). CŨ:
```js
khuvuc: meta.khu_vuc || [], nguondon: meta.nguon_don || [] };
```
MỚI:
```js
khuvuc: meta.khu_vuc || [], nguondon: meta.nguon_don || [], donvi_bo: orgsLoc || meta.orgs, kho_bo: meta.warehouses };
```

**H6** — `veOLoc`: bật "Chọn tất cả" cho MỌI ô — (a) ô Đơn vị (~dòng 2626). CŨ:
```js
coChonTatCa={!!dvCuaTk}
```
MỚI:
```js
coChonTatCa
```

**H6b** — (b) ô chung (~dòng 2635). CŨ:
```js
onSelect={v => onToggleFilter(o.khoa, v)} isActive={activeDropdown === o.ten} onToggle={setActiveDropdown} align={trongBang && !canhPhai ? 'left' : 'right'} />
```
MỚI:
```js
onSelect={v => onToggleFilter(o.khoa, v)} isActive={activeDropdown === o.ten} onToggle={setActiveDropdown} align={trongBang && !canhPhai ? 'left' : 'right'} coChonTatCa />
```

**H7** — `PremiumDropdown` (~dòng 1074): hằng trần. CŨ:
```js
        // dauKhung / coChonTatCa (22/10/2026): chỉ ô Đơn vị của Báo cáo TC dùng, khi người xem là quản trị — dòng "Theo tài khoản"
```
MỚI:
```js
        // "Chọn tất cả" (06/11/2026, Đại Ca chốt: mọi ô chọn nhiều của Báo cáo TC) — tối đa CHON_TAT_CA_TOI_DA mục: mỗi mục là 1 tham số SQL
        // (SQL Server tối đa 2.100 / câu, nhiều câu dùng lại danh sách 2–3 lần) + URL quá dài ⇒ quá trần thì nhắc gõ để thu hẹp.
        const CHON_TAT_CA_TOI_DA = 300;
        // dauKhung / coChonTatCa (22/10/2026): chỉ ô Đơn vị của Báo cáo TC dùng, khi người xem là quản trị — dòng "Theo tài khoản"
```

**H7b** — `PremiumDropdown` (~dòng 1104): dòng nhắc khi quá trần. CŨ:
```js
                                {coChonTatCa && filtered.length > 0 && (() => {
```
MỚI:
```js
                                {coChonTatCa && filtered.length > CHON_TAT_CA_TOI_DA && (
                                    <div className="px-3 py-2.5 rounded-xl border border-dashed border-slate-200 text-[10px] font-bold text-slate-400 italic">
                                        Chọn tất cả: tối đa {CHON_TAT_CA_TOI_DA} mục — đang có {filtered.length.toLocaleString()}, gõ để thu hẹp
                                    </div>
                                )}
                                {coChonTatCa && filtered.length > 0 && filtered.length <= CHON_TAT_CA_TOI_DA && (() => {
```

**H7c** — `PremiumDropdown` (~dòng 1111): chữ "mục" (ô loại trừ không ghép được "Chọn tất cả 80 loại trừ kho"). CŨ:
```js
<span className="text-[11px] font-bold leading-none">Chọn tất cả {filtered.length} {label.toLowerCase()} đang hiện</span>
```
MỚI:
```js
<span className="text-[11px] font-bold leading-none">Chọn tất cả {filtered.length} mục đang hiện</span>
```

**H8** — state `filters` mặc định (~dòng 7266). CŨ:
```js
                source_ids: [] });
```
MỚI:
```js
                source_ids: [],
                // Ô loại trừ (06/11/2026) — khoá RIÊNG bc_…_bo, xem O_LOC_BAO_CAO
                bc_org_ids_bo: [], bc_wh_ids_bo: [] });
```

**H8b** — `toggleFilter` chịu được khoá thiếu (~dòng 9536). CŨ:
```js
                    setFilters(p => ({ ...p, [key]: p[key].includes(id) ? p[key].filter(x => x!==id) : [...p[key], id] }));
```
MỚI:
```js
                    setFilters(p => { const cu = p[key] || []; return { ...p, [key]: cu.includes(id) ? cu.filter(x => x!==id) : [...cu, id] }; });
```

### PHẦN I — `index.html`, gắn tham số loại trừ vào MỌI yêu cầu của Báo cáo TC (tab "Hades I") · 16 điểm

**Luật:** I3–I16 chỉ CHÈN `...thamSoLoaiTru(filters),` ngay sau dấu `{` đầu tiên của `URLSearchParams({` / `const base = {` — không đổi gì khác.
`thamSoLoaiTru` trả `{}` khi không chọn ⇒ **URL y hệt bản cũ**. `base` (5 đường xuất đủ dòng) + `thamSoBC017` (BC017 xem + xuất) phủ nhiều chỗ qua 1 điểm.

**I1** — hàm mới, ngay TRƯỚC `thamSoBC017` (~dòng 2247). CŨ:
```js
        const thamSoBC017 = (f, an0d, kieu, xem, anCot) => ({
```
MỚI:
```js
        // Ô "Loại trừ đơn vị" / "Loại trừ kho" (Đại Ca chốt 06/11/2026) — gắn vào MỌI yêu cầu xem + xuất của Báo cáo TC. Khoá state RIÊNG bc_…_bo
        // (9 màn danh sách dựng yêu cầu bằng { ...filters }) ⇒ tham số org_ids_bo / wh_ids_bo chỉ đi qua đây. Không chọn ⇒ {} ⇒ URL y cũ.
        const thamSoLoaiTru = (f) => {
            const m = {};
            if ((f.bc_org_ids_bo || []).length) m.org_ids_bo = f.bc_org_ids_bo.join(',');
            if ((f.bc_wh_ids_bo || []).length) m.wh_ids_bo = f.bc_wh_ids_bo.join(',');
            return m;
        };
        const thamSoBC017 = (f, an0d, kieu, xem, anCot) => ({
```

**I2** — `thamSoBC017` (~dòng 2253). CŨ:
```js
            job_ids: (f.job_ids || []).join(','), tran_ids: (f.bc_tran_ids || []).join(','), an_0d: an0d ? '1' : '0',
```
MỚI:
```js
            job_ids: (f.job_ids || []).join(','), tran_ids: (f.bc_tran_ids || []).join(','), an_0d: an0d ? '1' : '0',
            ...thamSoLoaiTru(f),
```

**I3** — ~dòng 2849. CŨ:
```js
                const query = new URLSearchParams({ 
                    report_type:
```
MỚI:
```js
                const query = new URLSearchParams({ ...thamSoLoaiTru(filters), 
                    report_type:
```

**I4** — ~dòng 3252. CŨ:
```js
                const q = new URLSearchParams({ report_type: 'BC007', mode, journal_view_mode: journalViewMode, 
```
MỚI:
```js
                const q = new URLSearchParams({ ...thamSoLoaiTru(filters), report_type: 'BC007', mode, journal_view_mode: journalViewMode, 
```

**I5** — ~dòng 3268. CŨ:
```js
                const q = new URLSearchParams({ report_type: 'BC007', mode, journal_view_mode: journalViewMode,
                    from_date:
```
MỚI:
```js
                const q = new URLSearchParams({ ...thamSoLoaiTru(filters), report_type: 'BC007', mode, journal_view_mode: journalViewMode,
                    from_date:
```

**I6** — ~dòng 3466. CŨ:
```js
                const base = { from_date: filters.from_
```
MỚI:
```js
                const base = { ...thamSoLoaiTru(filters), from_date: filters.from_
```

**I7** — ~dòng 3495. CŨ:
```js
                    const q = new URLSearchParams({ report_type: 'BC008', fr
```
MỚI:
```js
                    const q = new URLSearchParams({ ...thamSoLoaiTru(filters), report_type: 'BC008', fr
```

**I8** — ~dòng 3500. CŨ:
```js
                    const q = new URLSearchParams({ from_date: filters.from_
```
MỚI:
```js
                    const q = new URLSearchParams({ ...thamSoLoaiTru(filters), from_date: filters.from_
```

**I9** — ~dòng 5117. CŨ:
```js
                                                const q = new URLSearchParams({ report_type: 'BC014', mo
```
MỚI:
```js
                                                const q = new URLSearchParams({ ...thamSoLoaiTru(filters), report_type: 'BC014', mo
```

**I10** — ~dòng 9319. CŨ:
```js
                const query = new URLSearchParams({ from_date: filters.from_
```
MỚI:
```js
                const query = new URLSearchParams({ ...thamSoLoaiTru(filters), from_date: filters.from_
```

**I11** — ~dòng 9375. CŨ:
```js
                        const q2 = new URLSearchParams({ from_date: filters.from_date, to_date: filters.to_date, org_ids: filters.org_ids.join(','), acc_ids: filters.acc_ids.join(','), p
```
MỚI:
```js
                        const q2 = new URLSearchParams({ ...thamSoLoaiTru(filters), from_date: filters.from_date, to_date: filters.to_date, org_ids: filters.org_ids.join(','), acc_ids: filters.acc_ids.join(','), p
```

**I12** — ~dòng 9387. CŨ:
```js
                        const q2 = new URLSearchParams({ from_date: filters.from_date, to_date: filters.to_date, org_ids: filters.org_ids.join(','), acc_ids: filters.acc_ids.join(','), m
```
MỚI:
```js
                        const q2 = new URLSearchParams({ ...thamSoLoaiTru(filters), from_date: filters.from_date, to_date: filters.to_date, org_ids: filters.org_ids.join(','), acc_ids: filters.acc_ids.join(','), m
```

**I13** — ~dòng 9400. CŨ:
```js
                        const q2 = new URLSearchParams({ from_date: filters.from_date, to_date: filters.to_date, org_ids: filters.org_ids.join(','), kv
```
MỚI:
```js
                        const q2 = new URLSearchParams({ ...thamSoLoaiTru(filters), from_date: filters.from_date, to_date: filters.to_date, org_ids: filters.org_ids.join(','), kv
```

**I14** — ~dòng 9413. CŨ:
```js
                        const q2 = new URLSearchParams({ from_date: filters.from_date, to_date: filters.to_date, org_ids: filters.org_ids.join(','), so
```
MỚI:
```js
                        const q2 = new URLSearchParams({ ...thamSoLoaiTru(filters), from_date: filters.from_date, to_date: filters.to_date, org_ids: filters.org_ids.join(','), so
```

**I15** — ~dòng 9444. CŨ:
```js
                        const q2 = new URLSearchParams({ from_date: filters.from_date, to_date: filters.to_date, org_ids: filters.org_ids.join(','), wh
```
MỚI:
```js
                        const q2 = new URLSearchParams({ ...thamSoLoaiTru(filters), from_date: filters.from_date, to_date: filters.to_date, org_ids: filters.org_ids.join(','), wh
```

**I16** — ~dòng 9459. CŨ:
```js
                        const q2 = new URLSearchParams({ from_date: filters.from_date, to_date: filters.to_date, org_ids: filters.org_ids.join(','), acc_ids: filters.acc_ids.join(','), c
```
MỚI:
```js
                        const q2 = new URLSearchParams({ ...thamSoLoaiTru(filters), from_date: filters.from_date, to_date: filters.to_date, org_ids: filters.org_ids.join(','), acc_ids: filters.acc_ids.join(','), c
```

### PHẦN J — `index.html`, dòng "Loại trừ …" trên giấy + tiêu đề file Excel (tab "Hades J") · 2 điểm

**J1** — dòng phụ tiêu đề Excel (~dòng 3111–3114). CŨ:
```js
                dongPhu.push('Đơn vị: ' + (filters.org_ids && filters.org_ids.length > 0 ? filters.org_ids.map(id => {
                    const org = meta.orgs.find(o => o.id === id);
                    return org ? `${id} - ${org.name}` : id;
                }).join(', ') : 'Tất cả'));
```
MỚI:
```js
                dongPhu.push('Đơn vị: ' + (filters.org_ids && filters.org_ids.length > 0 ? filters.org_ids.map(id => {
                    const org = meta.orgs.find(o => o.id === id);
                    return org ? `${id} - ${org.name}` : id;
                }).join(', ') : 'Tất cả'));
                // Ô loại trừ (06/11/2026): chỉ in khi có chọn — để trống thì file y như cũ
                if ((filters.bc_org_ids_bo || []).length) dongPhu.push('Loại trừ đơn vị: ' + filters.bc_org_ids_bo.map(id => { const org = (meta.orgs || []).find(o => o.id === id); return org ? `${id} - ${org.name}` : id; }).join(', '));
                if (['BC016', 'BC017'].includes(reportType) && (filters.bc_wh_ids_bo || []).length) dongPhu.push('Loại trừ kho: ' + filters.bc_wh_ids_bo.map(id => { const w = (meta.warehouses || []).find(x => x.id === id); return w ? w.name : id; }).join(', '));
```

**J2** — dòng phụ trên giấy (~dòng 3828–3831). CŨ:
```jsx
                                <div className="text-[10px] font-bold text-slate-600 uppercase">Đơn vị: {filters.org_ids.length > 0 ? filters.org_ids.map(id => {
                                    const org = meta.orgs.find(o => o.id === id);
                                    return org ? `${id} - ${org.name}` : id;
                                }).join(', ') : 'Tất cả'}</div>
```
MỚI:
```jsx
                                <div className="text-[10px] font-bold text-slate-600 uppercase">Đơn vị: {filters.org_ids.length > 0 ? filters.org_ids.map(id => {
                                    const org = meta.orgs.find(o => o.id === id);
                                    return org ? `${id} - ${org.name}` : id;
                                }).join(', ') : 'Tất cả'}</div>
                                {(filters.bc_org_ids_bo || []).length > 0 && (
                                    <div className="text-[10px] font-bold text-slate-600 uppercase">Loại trừ đơn vị: {filters.bc_org_ids_bo.map(id => { const org = (meta.orgs || []).find(o => o.id === id); return org ? `${id} - ${org.name}` : id; }).join(', ')}</div>
                                )}
                                {['BC016', 'BC017'].includes(reportType) && (filters.bc_wh_ids_bo || []).length > 0 && (
                                    <div className="text-[10px] font-bold text-slate-600 uppercase">Loại trừ kho: {filters.bc_wh_ids_bo.map(id => { const w = (meta.warehouses || []).find(x => x.id === id); return w ? w.name : id; }).join(', ')}</div>
                                )}
```

### ➡️ BƯỚC 1 cho mỗi tab (chỉ ĐỌC — CHƯA sửa file)
Mở `index.html` / `server.py` theo đúng dải dòng Claude Code đưa trong lệnh (KHÔNG dùng công cụ tìm kiếm, KHÔNG đọc nguyên file), so từng chuỗi CŨ của phần mình,
trả lời tối đa 15 dòng: mỗi điểm khớp đúng 1 lần không, thay y hệt MỚI hay cần chỉnh gì. **Không sửa file.** Thứ tự BƯỚC 2: G ∥ H → I → J (3 tab cùng sửa `index.html`).

### Ca nghiệm thu (Claude Code chạy)
M1 `ast` + Babel · code trùng khít bản áp thử · **không chọn loại trừ ⇒ JSON y hệt bản cũ** ở các endpoint báo cáo (chạy code cũ từ git cùng lúc) · **có loại trừ X ⇒
= chọn tường minh "mọi đơn vị trừ ngoài cây và X"** (DB thật) · tài khoản giới hạn {A, B} + loại trừ B ⇒ chỉ A · loại trừ kho BC016 / BC017 = chọn tường minh các
kho còn lại · 9 màn danh sách: có `bc_org_ids_bo` trong state vẫn trả y cũ · giao diện: 2 ô loại trừ nằm trong Bộ lọc nâng cao (ô ngoài BC016 không đổi), số trên nút
phễu đếm ô loại trừ đang có giá trị, dòng "Loại trừ …" trên giấy, "Chọn tất cả" ở mọi ô + dòng nhắc khi > 300 · mọi yêu cầu xem (18 báo cáo) mang `org_ids_bo` khi
có chọn (bắt yêu cầu trên Chrome ngầm).

### Nhật ký chạy (mới nhất ở dưới cùng của mục này)
- **~18:10** Claude Code áp thử đặc tả lên bản sao `lr_viec57\v58\` (34/34 neo khớp 1 lần, `ast` + Babel OK) + thử riêng `_org_filter_sql` mới 8 trường hợp
  (không chọn / loại trừ / chọn + loại trừ / loại trừ hết ⇒ `1=0` / tài khoản giới hạn / ngoài yêu cầu ⇒ rỗng) đúng hết. Mở 4 tab Orca "Hades G/H/I/J - viec 58"
  (`--mode plan`, số dòng đưa sẵn). Tab để mở tới khi báo Đại Ca xong.
- **~18:23 cả 4 tab trình BƯỚC 1**: G 4/4 · H 12/12 · I 16/16 · J 2/2 khớp đúng 1 lần, thay y hệt MỚI, không đề nghị chỉnh.
  ✅ **Claude Code duyệt BƯỚC 2 cả 4 phần theo quyền Đại Ca trao** — mọi neo khớp, đặc tả đã áp thử + kiểm cú pháp đạt. Thứ tự: G ∥ H → I → J; chế độ thường
  (Hades hỏi từng lần sửa, Claude Code soát rồi "Yes").
- **~18:27 G BƯỚC 2 XONG** (G3, G4, G2, G1 — soát từng lần; G2 dài, 9 dòng cuối khuất ⇒ soát bằng so file): `server.py` **trùng khít** bản áp thử `v58\server.py`
  (0 dòng khác) · `ast` OK.
- ⏸️ **~18:31 Đại Ca: "tạm ngưng đi, tối làm tiếp giờ về m"** ⇒ dừng giữa PHẦN H. Đã áp H: **H8b, H8, H6b, H6, H5, H4, H3, H2, H1** (H2 phải duyệt trước khi dừng —
  H3 đã dùng biến `trong` của H2). Ngắt tab H (Esc lúc Hades đang soạn điểm kế, sau khi đã "Yes" H1). **CÒN: H7, H7b, H7c** (trần "Chọn tất cả") → **I1–I16** → **J1–J2**.
  Trạng thái dừng an toàn: Babel + `ast` OK, không tham chiếu treo (`CHON_TAT_CA_TOI_DA`, `thamSoLoaiTru` chưa ai gọi). Chưa commit. Tab G đã đóng (xong);
  tab H, I, J để mở (I, J đã duyệt BƯỚC 2 nhưng CHƯA gửi lệnh sửa).
  **Làm tiếp:** tab H gửi lệnh áp H7c, H7b, H7 (số dòng hiện tại: tính lại bằng `dong_58.json` cách cũ) → so `index.html` với bản áp thử từng phần → tab I → tab J →
  so trùng khít `v58\index.html` → Babel → giao diện (server thử 5052) → M2 DB thật `kiem_m2_v58.py` (cần VPN + mật khẩu `config.json`).
- **~18:35 Đại Ca: "coi hades còn tab nào đang chạy xem nó chạy xong rồi dừng lun"** ⇒ kiểm: tab H, I, J đều RẢNH (không chạy) ⇒ **đóng cả 3**. Không còn tab
  Hades nào của LedgerReport. Tối làm tiếp: mở tab mới cho H (H7, H7b, H7c), I, J — đưa số dòng hiện tại.
- **13/11/2026 ~11:56 Đại Ca: "bữa đang làm gì dang dỡ làm tiếp đi m"** ⇒ kiểm hiện trạng: `server.py` **trùng khít** bản áp thử `v58\server.py` (chỉ khác
  CRLF/LF) · `index.html` còn đúng 21 điểm chưa áp = H7, H7b, H7c, I1–I16, J1–J2 (diff với `v58\index.html`, không lệch gì khác). BƯỚC 1 của H/I/J đã duyệt
  06/11 ⇒ mở tab Orca MỚI giao thẳng BƯỚC 2, lần lượt H → I → J (cùng sửa `index.html`), chế độ thường (Hades hỏi từng lần sửa, Claude Code soát rồi "Yes").
  Số dòng hiện tại: H7 1074 · H7b 1104 · H7c 1111 (sửa từ dưới lên). Sau H (+8 dòng): I1 2259 · I2 2265 · I3 2863 · I4 3266 · I5 3282 · I6 3480 · I7 3509 ·
  I8 3514 · I9 5131 · I10 9335 · I11 9391 · I12 9403 · I13 9416 · I14 9429 · I15 9460 · I16 9475. Sau H + I (+17): J1 3134–3137 · J2 3851–3854.
- **~11:58** ⛔ Bộ lọc an toàn của Claude Code **chặn `orca terminal create`** (đúng luật chung: không thêm quyền sẵn cho lệnh mở Hades) ⇒ hỏi Đại Ca: *"Em tự áp
  luôn"* hay *"Đại Ca tự mở tab Hades"* ⇒ **Đại Ca chọn "Em tự áp luôn"** ⇒ **Claude Code tự áp 21 điểm còn lại** (Hades không sửa gì thêm ở phần này):
  script đọc CŨ/MỚI thẳng từ mục này, mỗi neo khớp đúng 1 lần, ghi CRLF. Kết quả: `index.html` **trùng khít** `v58\index.html` (bỏ CR) · CRLF 11.874/11.874 ·
  Babel OK · `ast` OK · `thamSoLoaiTru(` 15 lần (thamSoBC017 + I3–I16).
- **~12:10 Giao diện (server thử 5052, DB giả, Chrome ngầm 1366×768) — ĐẠT:** BC016 ô ngoài **không đổi** (Thời gian · Đơn vị · Kho · Hàng hoá), 2 ô loại trừ
  nằm trong Bộ lọc nâng cao · chọn đơn vị 35 + kho KTONG ⇒ phễu *"2 ô đang áp dụng"* · `/api/nxt` mang `org_ids_bo=35&wh_ids_bo=KTONG`, SQL có
  `ORGANIZATION_ID NOT IN` (có 35) + `W.WAREHOUSE_ID NOT IN` (KTONG) · giấy in *"Loại trừ đơn vị: 35 - …"* + *"Loại trừ kho: Kho tổng"* · "Chọn tất cả 94 /
  3 mục đang hiện" ở ô loại trừ · ô Hàng hoá 353 mục ⇒ dòng nhắc *"tối đa 300 mục — đang có 353"*, gõ thu hẹp ⇒ "Chọn tất cả 10 mục" · BC017 ô ngoài không đổi,
  loại trừ xếp CUỐI trong bảng, `/api/sale_detail` mang 2 tham số · BC001 chỉ có ô Loại trừ đơn vị, phễu *"1 ô"*, giấy chỉ in dòng đơn vị · BC007 / BC012 /
  BC018 mang `org_ids_bo` · màn Chứng từ bán hàng chỉ mang `bc_org_ids_bo` / `bc_wh_ids_bo` (tên state, máy chủ bỏ qua), **không** mang `org_ids_bo` · không tràn
  ngang. ⚠️ 2 hộp lỗi *"tuple index out of range"* (BC012, Chứng từ bán hàng) = **do DB giả** — gọi y câu đó KHÔNG có tham số loại trừ cũng ra 500 y hệt.
  ⏳ **Chưa thử:** J1 (dòng "Loại trừ…" ở tiêu đề file Excel) — nút xuất khoá khi báo cáo 0 dòng (DB giả) ⇒ thử trên DB thật. ⏳ **M2 DB thật**
  (`lr_viec57\kiem_m2_v58.py`) chờ Đại Ca bật VPN + điền mật khẩu `config.json`.
- **~12:30 Đại Ca điền mật khẩu + VPN ⇒ M2 DB thật lần 1 (`kiem_m2_v58.py`, kỳ T09/2026, loại trừ {01, 35}): ĐẠT 31 · LỖI 4.**
  ĐẠT: R (không loại trừ MỚI = CŨ) BC006/012/015/016/018 · E (loại trừ = chọn tường minh 93 đơn vị) BC001/002/006/007/008/009/013/014/015/016/017/018 ·
  P (giới hạn {02,35} + loại trừ 35 = giới hạn {02}) BC012/015/018 · K (loại trừ kho = chọn tường minh 89 kho) BC016/017 · L sale · X CSV BC007 (10.055.695 B
  trùng từng byte) + BC012.
  🔴 **LỖI THẬT — đặc tả của Claude Code SÓT 2 bộ nhớ đệm kết quả** (không phải lỗi Hades): `_ledger_cum_cache` (số dư luỹ kế BC005 + BC011, giữ 180s) và
  `_cashbook_cache` (BC012) — khoá nhớ chỉ có `org_ids`, không có `org_ids_bo` ⇒ bấm loại trừ ngay sau khi xem không loại trừ là **trả lại số cũ** (đo: loại trừ
  0,0–0,3s, JSON y hệt không loại trừ). Lúc thiết kế em chỉ rà `_org_filter_sql` (40 chỗ gọi) mà không rà bộ nhớ đệm.
  **Sửa (Claude Code, nối tiếp quyền "em tự áp" Đại Ca chọn ~11:58):** khoá `_ledger_cum_cache` thêm `_lc, tuple(_lp)` (mệnh đề đơn vị THẬT — gồm loại trừ +
  quyền tài khoản); khoá `_cashbook_cache` thêm `tuple(sorted(_org_loai_tru()))`. Không gửi loại trừ ⇒ kết quả y cũ (chỉ khoá nhớ dài thêm). Chỉ 2 bộ nhớ đệm
  kết quả trong `server.py` (đã rà mọi `_…cache` cấp module). `ast` OK, không hàm trùng, CRLF giữ nguyên.
  ⚠️ LỖI L ledger (dòng đầu khác) — nghi thứ tự `ORDER BY` không duy nhất (có từ trước) ⇒ chạy lại so TẬP dòng.
- **~12:45 M2 chạy lại sau khi sửa (`kiem_m2_v58_lai.py`, cùng thứ tự gọi: KHÔNG loại trừ trước để nạp bộ nhớ đệm) — ĐẠT HẾT:** BC005 · BC011 · BC012 đều:
  R không loại trừ MỚI = CŨ · E loại trừ {01,35} = chọn tường minh · D có loại trừ ⇒ KHÁC không loại trừ · E2 gọi lại lần 2 vẫn = tường minh; P BC012 giới hạn
  {02,35} + loại trừ 35 (sau khi nạp đệm) = giới hạn {02}.
  **Ledger** (`kiem_ledger_v58.py`): `/api/ledger/count` có / không `bc_…` = 89.628 / 89.628 · đơn vị 35 (906 dòng) và 02 (1.878 dòng) — đủ dòng trong 1 trang —
  có / không `bc_…` **trùng khít tập dòng** · `_build_where` chỉ đọc danh sách tham số cố định (không có `bc_…`). ⇒ lần 1 lệch là do cắt trang 10.000 / 89.628 dòng
  trên `ORDER BY TRAN_DATE DESC, TRAN_NO` không duy nhất — **có từ trước, không do việc 58**.
- **~12:52 J1 trên DB thật** (server thử 5052 nối DB thật, Chrome ngầm): BC016 T01/2026 loại trừ đơn vị 35 + kho KTONGHN ⇒ 297 dòng, 9,6s · file `.xlsx` thật dòng 7
  *"Loại trừ đơn vị: 35 - CPMCL-KG-446 …"*, dòng 8 *"Loại trừ kho: Kho tổng Hà Nội"* · ô Loại trừ đơn vị "Chọn tất cả 96 mục", Loại trừ kho "Chọn tất cả 91 mục".
  ✅ **Việc 58: M1 + giao diện + M2 DB thật ĐẠT.** Server thử đã tắt; mật khẩu `config.json` **đã xoá lại**. Chưa commit · chưa phát hành (chờ Đại Ca).

---

## 06/11/2026 — Việc 57: BC015 thêm ô lọc "Nguồn đơn" (DM_EXTRA_2) — ĐẶC TẢ cho Hades · 3 TAB SONG SONG · ⏳ BƯỚC 1

**Đại Ca 06/11/2026:** *"Chổ báo cáo BC015 t muốn có thêm bộ lọc theo danh mục DM_EXTRA_2 … việc lần này giao cho hades làm, với t thấy
tốc độ nó làm chậm quá, m làm sao cho nó làm nhanh hơn xem"* + *"chia nhỏ các mục đó ra, cho phép m mở nhiều tab hades … mỗi tab chạy 1 phần
xong ráp lại"*. Chốt qua câu hỏi: **giữ 2 bước** (BƯỚC 1 trình diff, CHƯA sửa → Claude Code duyệt → BƯỚC 2 sửa) · việc này chạy
**`gemini-3.8-flash-medium`** (đặc tả có sẵn code, không cần nghĩ nhiều; việc khó vẫn High).

**Vì sao lần trước chậm (Claude Code rút ra):** đặc tả việc 56 dài ~360 dòng / 26 điểm, Hades đọc cả `CLAUDE.md` + `index.html` (~1 MB) +
`server.py` (~10.000 dòng) rồi phải viết diff cho 26 điểm trong 1 lượt ⇒ nghĩ 9 phút rồi dừng không trả lời. Lần này: mỗi tab **2–4 điểm**,
code mới viết sẵn, ⛔ **KHÔNG đọc nguyên file lớn** — tìm chuỗi neo rồi chỉ xem ±20 dòng quanh đó; KHÔNG đọc `CLAUDE.md` / phần dưới của file
này (mọi luật cần biết ghi ngay ở đây).

**Nền:** máy chủ BC015 (`get_sale_by_source`, `server.py`) **đã nhận sẵn `source_ids`** (`AND S.EXTRA_ID_2 IN (?,…)`, params đúng thứ tự) —
chỉ thiếu danh mục cho ô chọn + ô lọc trên giao diện. Khuôn y ô **Khu vực** của BC018 (việc 56).

**Luật chung cho cả 3 tab:**
- Mỗi neo "CŨ" dưới đây đã kiểm **xuất hiện đúng 1 lần** (06/11). Sửa = **thay đúng chuỗi CŨ bằng chuỗi MỚI**, giữ nguyên thụt lề. Không dò theo
  số dòng (số dòng chỉ để tham khảo — 2 tab cùng sửa `index.html` nên số dòng sẽ trôi).
- Chỉ sửa điểm của **phần mình**. Không sửa file nào khác. ⛔ Không chạy lệnh shell, không `git`, không đụng `config.json`.
- Tiếng Việt trong code / chú thích giữ nguyên dấu (file UTF-8).

### PHẦN A — `server.py` (tab "Hades A") · 2 điểm

**A1** — `/api/metadata`: thêm danh mục nguồn đơn ngay SAU khối khu vực (~dòng 1811–1814).
CŨ:
```python
        except Exception as e:
            logger.warning('Metadata: khong doc duoc danh sach khu vuc (BC018): %s', e)
            cursor = conn.cursor()
```
MỚI:
```python
        except Exception as e:
            logger.warning('Metadata: khong doc duoc danh sach khu vuc (BC018): %s', e)
            cursor = conn.cursor()

        # Nguồn đơn cho ô lọc BC015 (06/11/2026) = danh mục DM_EXTRA_2, CAST y BC015 (SALE_VIEW.EXTRA_ID_2 là chuỗi).
        # KHÔNG lọc ACTIVE (Bẫy 16: mã ngưng dùng vẫn còn chứng từ cũ). Câu riêng, hỏng thì danh sách rỗng.
        nguon_don = []
        try:
            cursor.execute("SELECT CAST(EXTRA_ID_2 AS NVARCHAR(100)), EXTRA_NAME_2 FROM dbo.DM_EXTRA_2 WITH (NOLOCK)")
            for ma, ten in cursor.fetchall():
                ma = (ma or '').strip()
                if ma:
                    nguon_don.append({"id": ma, "name": (ten or '').strip() or ma})
            nguon_don.sort(key=lambda k: k["id"])
        except Exception as e:
            logger.warning('Metadata: khong doc duoc danh muc nguon don DM_EXTRA_2 (BC015): %s', e)
            cursor = conn.cursor()
```

**A2** — kết quả trả về (~dòng 1854). CŨ: `            "khu_vuc": khu_vuc,` → MỚI: `            "khu_vuc": khu_vuc, "nguon_don": nguon_don,`

### PHẦN B — `index.html`, khai báo ô lọc (tab "Hades B") · 4 điểm

**B1** — `O_LOC_BAO_CAO` (~dòng 2232). CŨ:
```js
            { id: 'khuvuc',   ten: 'Khu vực',         khoa: 'kv_ids',         co: (t) => t === 'BC018' },
```
MỚI:
```js
            { id: 'khuvuc',   ten: 'Khu vực',         khoa: 'kv_ids',         co: (t) => t === 'BC018' },
            // BC015 (06/11/2026): Nguồn đơn = danh mục DM_EXTRA_2 (/api/metadata trả nguon_don); máy chủ nhận source_ids từ trước
            { id: 'nguondon', ten: 'Nguồn đơn',       khoa: 'source_ids',     co: (t) => t === 'BC015' },
```

**B2** — `THU_TU_O_LOC` (~dòng 2236). CŨ: `        const THU_TU_O_LOC = {` → MỚI (thêm 1 dòng ngay dưới):
```js
        const THU_TU_O_LOC = {
            BC015: ['nguondon', 'donvi'],
```

**B3** — `nguonOLoc` trong `ReportTab` (~dòng 2596). CŨ: `khuvuc: meta.khu_vuc || [] };` → MỚI: `khuvuc: meta.khu_vuc || [], nguondon: meta.nguon_don || [] };`

**B4** — state `filters` mặc định trong `App` (~dòng 7244). CŨ: `                kv_ids: [] });` → MỚI:
```js
                kv_ids: [],
                // BC015 (06/11/2026): ô Nguồn đơn
                source_ids: [] });
```

### PHẦN C — `index.html`, gửi tham số + dòng phụ trên giấy (tab "Hades C") · 4 điểm

**C1** — dòng phụ (tiêu đề file Excel) (~dòng 3091). CŨ: `                if (reportType === 'BC015') dongPhu.push('Nguồn đơn: Tất cả');` → MỚI:
```js
                if (reportType === 'BC015') {
                    const ndDs = meta.nguon_don || [];
                    dongPhu.push('Nguồn đơn: ' + ((filters.source_ids || []).length ? filters.source_ids.map(id => { const n = ndDs.find(x => x.id === id); return n ? n.name : id; }).join(', ') : 'Tất cả'));
                }
```

**C2** — xuất Excel đủ dòng, `buildFullExportReq` (~dòng 3465). CŨ:
`                    const q = new URLSearchParams({ ...base, mode: modeArg || saleSourceMode || 'summary', page: 1, page_size: 0 });` → MỚI:
`                    const q = new URLSearchParams({ ...base, source_ids: (filters.source_ids || []).join(','), mode: modeArg || saleSourceMode || 'summary', page: 1, page_size: 0 });`

**C3** — dòng phụ trên giấy (~dòng 3772). CŨ:
```jsx
                                    <div className="text-[10px] font-bold text-slate-600 uppercase">Nguồn đơn: Tất cả</div>
```
MỚI:
```jsx
                                    <div className="text-[10px] font-bold text-slate-600 uppercase">Nguồn đơn: {(filters.source_ids || []).length > 0 ? filters.source_ids.map(id => {
                                        const n = (meta.nguon_don || []).find(x => x.id === id);
                                        return n ? n.name : id;
                                    }).join(', ') : 'Tất cả'}</div>
```

**C4** — màn xem, `loadReportData` nhánh BC015 (~dòng 9389). CŨ:
`org_ids: filters.org_ids.join(','), mode: activeMode, page: _page, page_size: rptPageSize });` → MỚI:
`org_ids: filters.org_ids.join(','), source_ids: (filters.source_ids || []).join(','), mode: activeMode, page: _page, page_size: rptPageSize });`

**Ghi chú cố ý:** dòng không có nguồn đơn (EXTRA_ID_2 trống — nhóm cuối của BC015) **không chọn riêng được**; để trống ô = tất cả, như cũ.
`(filters.source_ids || [])` ở mọi chỗ để máy cũ / state thiếu khoá không vỡ.

### PHẦN D — BC016 thêm ô lọc Kho + Hàng hoá, `index.html` (tab "Hades D") · 7 điểm *(Đại Ca 06/11 ~15:30, gửi ảnh: "Với cái báo cáo BC016, cho thông tin lọc theo kho và lọc theo hàng hóa nữa m")*

**Nền:** `/api/nxt` (BC016) **đã nhận sẵn** `wh_ids` + `item_ids` (`server.py` ~dòng 9811, `W.WAREHOUSE_ID IN` / `W.ITEM_ID IN`). Ô **Kho**
(`bc_wh_ids`) + **Hàng hoá** (`item_ids`) đã có cho BC017, `nguonOLoc` đã có `kho` / `hanghoa` ⇒ chỉ bật cho BC016 + gửi tham số + in lên giấy.
⚠️ PHẦN D sửa **cùng file** với B, C ⇒ BƯỚC 2 của D chạy **SAU** C (Claude Code điều phối). Neo của D không trùng neo của B/C.

**D1** (~dòng 2225). CŨ:
```js
            { id: 'kho',      ten: 'Kho',             khoa: 'bc_wh_ids',      co: (t) => t === 'BC017' },
```
MỚI:
```js
            // BC016 (06/11/2026): Kho + Hàng hoá dùng chung ô của BC017 — /api/nxt nhận wh_ids / item_ids từ trước
            { id: 'kho',      ten: 'Kho',             khoa: 'bc_wh_ids',      co: (t) => t === 'BC017' || t === 'BC016' },
```

**D2** (~dòng 2227). CŨ:
```js
            { id: 'hanghoa',  ten: 'Hàng hoá',        khoa: 'item_ids',       co: (t) => t === 'BC017' },
```
MỚI:
```js
            { id: 'hanghoa',  ten: 'Hàng hoá',        khoa: 'item_ids',       co: (t) => t === 'BC017' || t === 'BC016' },
```

**D3** (~dòng 2238). CŨ:
```js
            BC018: ['khuvuc', 'donvi'],
```
MỚI:
```js
            BC018: ['khuvuc', 'donvi'],
            BC016: ['donvi', 'kho', 'hanghoa'],
```

**D4** — màn xem, `loadReportData` nhánh BC016 (~dòng 9420). CŨ:
`org_ids: filters.org_ids.join(','), group_by: gb, page: _page, page_size: 1000 });` → MỚI:
`org_ids: filters.org_ids.join(','), wh_ids: (filters.bc_wh_ids || []).join(','), item_ids: (filters.item_ids || []).join(','), group_by: gb, page: _page, page_size: 1000 });`

**D5** — xuất Excel, `buildFullExportReq` (~dòng 3470). CŨ:
`const q = new URLSearchParams({ ...base, group_by: modeArg || nxtGroupBy || 'class', page: 1, page_size: 0 });` → MỚI:
`const q = new URLSearchParams({ ...base, wh_ids: (filters.bc_wh_ids || []).join(','), item_ids: (filters.item_ids || []).join(','), group_by: modeArg || nxtGroupBy || 'class', page: 1, page_size: 0 });`

**D6** — dòng phụ tiêu đề file Excel (~dòng 3092, chèn TRƯỚC khối BC018). CŨ:
```js
                if (reportType === 'BC018') {
```
MỚI:
```js
                if (reportType === 'BC016') {
                    // Ô Kho / Hàng hoá (06/11/2026): chỉ in khi có chọn — để trống thì giấy y như cũ
                    if ((filters.bc_wh_ids || []).length) dongPhu.push('Kho: ' + filters.bc_wh_ids.map(id => { const w = (meta.warehouses || []).find(x => x.id === id); return w ? w.name : id; }).join(', '));
                    if ((filters.item_ids || []).length) dongPhu.push('Hàng hoá: ' + filters.item_ids.map(id => { const h = (meta.items || []).find(x => x.id === id); return h ? `${id} - ${h.name}` : id; }).join(', '));
                }
                if (reportType === 'BC018') {
```

**D7** — dòng phụ trên giấy (~dòng 3774, chèn TRƯỚC khối BC018). CŨ:
```jsx
                                {reportType === 'BC018' && (<>
```
MỚI:
```jsx
                                {reportType === 'BC016' && (filters.bc_wh_ids || []).length > 0 && (
                                    <div className="text-[10px] font-bold text-slate-600 uppercase">Kho: {filters.bc_wh_ids.map(id => { const w = (meta.warehouses || []).find(x => x.id === id); return w ? w.name : id; }).join(', ')}</div>
                                )}
                                {reportType === 'BC016' && (filters.item_ids || []).length > 0 && (
                                    <div className="text-[10px] font-bold text-slate-600 uppercase">Hàng hoá: {filters.item_ids.map(id => { const h = (meta.items || []).find(x => x.id === id); return h ? `${id} - ${h.name}` : id; }).join(', ')}</div>
                                )}
                                {reportType === 'BC018' && (<>
```

**Ca nghiệm thu D (Claude Code chạy):** M1 Babel · D-N1 BC016 chọn 1 kho ⇒ chỉ dòng của kho đó, số = đúng các dòng kho đó ở bản không lọc (gom
theo Kho) · D-N2 chọn vài hàng hoá ⇒ chỉ các mã đó · D-N3 để trống ⇒ JSON y bản cũ · D-N4 Excel có lọc = số trên màn + dòng "Kho: …" · D-N5 giao
diện 1366: Đơn vị · Kho · Hàng hoá đứng ngoài (cùng Thời gian = 4 ô, tối đa). ⚠️ Ô Kho / Hàng hoá **dùng chung giá trị với BC017** (cùng khoá
`bc_wh_ids` / `item_ids` — như ô Đơn vị dùng chung mọi báo cáo): chọn ở BC017 rồi sang BC016 thì ô vẫn giữ lựa chọn.

### PHẦN E — BC015 mục "Không có nguồn đơn" trong ô Nguồn đơn, `server.py` (tab "Hades E") · 3 điểm *(Đại Ca chốt 06/11 ~16:45: "Thêm mục, giao Hades")*

**Vì sao:** M2 DB thật — chứng từ 2026 để trống nguồn đơn **25.514 phiếu, 25 tỷ = 7,26% doanh thu, 81 đơn vị**; ô Nguồn đơn chưa chọn riêng được nhóm này.
**Cách làm:** chỉ sửa máy chủ. `/api/metadata` trả thêm mục đầu danh sách mã giả `(TRONG)` tên "Không có nguồn đơn" ⇒ ô chọn + dòng phụ trên giấy
tự có (map tên theo `meta.nguon_don`), **`index.html` không sửa gì**. BC015 gặp mã giả ⇒ thêm nhánh `ISNULL(S.EXTRA_ID_2, '') = ''` nối `OR` với
`IN (…)` của các mã thật; dấu `?` của `IN` vẫn đứng sau tham số đơn vị ⇒ thứ tự params không đổi (Bẫy 5). Mã có dấu ngoặc ⇒ không trùng mã thật.

**E1** — hằng mới, ngay TRƯỚC `SALE_SOURCE_MONEY_COLS` (~dòng 8974). CŨ:
```python
SALE_SOURCE_MONEY_COLS = [
```
MỚI:
```python
# Mã giả của mục "Không có nguồn đơn" trong ô lọc Nguồn đơn (Đại Ca chốt 06/11/2026): chứng từ để trống EXTRA_ID_2
# (2026: 25.514 phiếu = 7,26% doanh thu). Có dấu ngoặc ⇒ không trùng mã thật của DM_EXTRA_2.
BC015_NGUON_TRONG = '(TRONG)'
SALE_SOURCE_MONEY_COLS = [
```

**E2** — `/api/metadata`, khối nguồn đơn (~dòng 1825). CŨ:
```python
            nguon_don.sort(key=lambda k: k["id"])
```
MỚI:
```python
            nguon_don.sort(key=lambda k: k["id"])
            nguon_don.insert(0, {"id": BC015_NGUON_TRONG, "name": "Không có nguồn đơn"})
```

**E3** — `get_sale_by_source`, lọc nguồn (~dòng 9013–9015). CŨ:
```python
        if source_ids:
            src_where = " AND S.EXTRA_ID_2 IN (" + ",".join(["?"] * len(source_ids)) + ")"
            src_params = list(source_ids)
```
MỚI:
```python
        if source_ids:
            # BC015_NGUON_TRONG = mục "Không có nguồn đơn" (06/11/2026) ⇒ thêm nhánh EXTRA_ID_2 trống, nối OR với danh sách mã.
            ma_nguon = [v for v in source_ids if v != BC015_NGUON_TRONG]
            dk_nguon = []
            if ma_nguon:
                dk_nguon.append("S.EXTRA_ID_2 IN (" + ",".join(["?"] * len(ma_nguon)) + ")")
                src_params = ma_nguon
            if BC015_NGUON_TRONG in source_ids:
                dk_nguon.append("ISNULL(S.EXTRA_ID_2, '') = ''")
            src_where = " AND (" + " OR ".join(dk_nguon) + ")"
```

**Ca nghiệm thu E (Claude Code chạy, DB thật T09/2026):** E-N1 metadata: mục đầu = `(TRONG)` · E-N2 chỉ `(TRONG)` ⇒ đúng khối nhóm trống của bản không
lọc · E-N3 `(TRONG)` + 1 nguồn thật ⇒ đúng 2 khối · E-N4 chi tiết (đường xuất Excel) chỉ `(TRONG)` = đúng khối · chạy lại N2–N5 (không hồi quy).

### PHẦN F — BC015 bỏ phiếu XDCNB (xuất điều chuyển nội bộ), `server.py` (tab "Hades E" dùng tiếp) · 2 điểm *(Đại Ca chốt 06/11 ~16:55: "PHần này bắt buộc loại phiếu XDCNB ra á")*

**Vì sao:** `SALE_VIEW` có cả `XDCNB` (điều chuyển nội bộ — không phải bán hàng). T1–T9/2026 phiếu này toàn 0 đồng nên không thấy; **từ T10/2026 mang tiền**
(T10 1.606.989.769 · T11 tới 06/11 495.988.059) ⇒ lọt vào tổng BC015, nằm trong nhóm "Không có nguồn đơn". Bỏ bằng 1 điều kiện **hằng** trong WHERE
(không phải tham số ⇒ thứ tự `?` không đổi — Bẫy 5). Kèm sửa câu chú thích E1 ("7,26% doanh thu" là sai cách gọi — xem đính chính ở Nhật ký chạy).

**F1** — hằng (~dòng 8974–8976). CŨ:
```python
# Mã giả của mục "Không có nguồn đơn" trong ô lọc Nguồn đơn (Đại Ca chốt 06/11/2026): chứng từ để trống EXTRA_ID_2
# (2026: 25.514 phiếu = 7,26% doanh thu). Có dấu ngoặc ⇒ không trùng mã thật của DM_EXTRA_2.
BC015_NGUON_TRONG = '(TRONG)'
```
MỚI:
```python
# Mã giả của mục "Không có nguồn đơn" trong ô lọc Nguồn đơn (Đại Ca chốt 06/11/2026): chứng từ để trống EXTRA_ID_2
# (2026: gần như toàn chứng từ nội bộ — BNB bán nội bộ của Kho tổng). Có dấu ngoặc ⇒ không trùng mã thật của DM_EXTRA_2.
BC015_NGUON_TRONG = '(TRONG)'
# BC015 KHÔNG tính phiếu xuất điều chuyển nội bộ (Đại Ca chốt 06/11/2026: "bắt buộc loại phiếu XDCNB ra") — điều chuyển không phải bán hàng.
# T1–T9/2026 phiếu XDCNB toàn 0 đồng; từ T10/2026 mang tiền (T10 ~1,6 tỷ) nên từng lọt vào tổng BC015 ở nhóm "Không có nguồn đơn".
BC015_BO_LOAI_CT = 'XDCNB'
```

**F2** — `get_sale_by_source`, WHERE (~dòng 9043). CŨ:
```python
            WHERE S.STATUS = ? AND S.TRAN_DATE >= ? AND S.TRAN_DATE < ?{org_where}{src_where}
```
MỚI:
```python
            WHERE S.STATUS = ? AND S.TRAN_DATE >= ? AND S.TRAN_DATE < ? AND S.TRAN_ID <> '{BC015_BO_LOAI_CT}'{org_where}{src_where}
```

**Ca nghiệm thu F (Claude Code chạy, DB thật — so với JSON chụp TRƯỚC khi sửa `lr_viec57\bc015_truoc_F.json`):** F-N1 T09 (XDCNB 0 đồng) ⇒ JSON
**y hệt** trước · F-N2 T10: tổng mới = tổng cũ − tổng XDCNB T10 (tra thẳng SQL) · mọi nguồn có tên **y hệt** · nhóm trống mới = cũ − XDCNB · F-N3 T10 chi tiết
cùng luật · F-N4 T1–T10 cùng luật · hồi quy lọc nguồn / `(TRONG)`.

### ➡️ BƯỚC 1 cho mỗi tab (chỉ ĐỌC — CHƯA sửa file)
Tìm từng chuỗi CŨ của phần mình, xem ±20 dòng xung quanh, rồi trả lời **ngắn, tối đa 25 dòng**: với mỗi điểm — tìm thấy đúng 1 lần không (dòng
hiện tại), sẽ thay đúng như MỚI hay cần chỉnh gì (chép phần chỉnh), rủi ro thấy được. **Không sửa file.** Claude Code soát xong ghi lệnh duyệt BƯỚC 2.

### Ca nghiệm thu (Claude Code chạy)
M1 `ast.parse` + Babel · N1 `/api/metadata` có `nguon_don` (mỗi mục `{id, name}`, khớp DM_EXTRA_2) · N2 BC015 chọn 1 nguồn ⇒ chỉ còn nhóm đó, số
= đúng nhóm đó ở bản không lọc · N3 chọn 2 nguồn · N4 để trống ⇒ JSON y bản cũ · N5 Excel có lọc = số trên màn, dòng "Nguồn đơn: …" đúng tên ·
N6 giao diện 1366: ô Nguồn đơn đứng ngoài cạnh Đơn vị · N7 tài khoản giới hạn đơn vị vẫn chỉ thấy đơn vị của mình. N1–N5, N7 cần DB thật (VPN).

### Nhật ký chạy (mới nhất ở dưới cùng của mục này)
- **~15:10** mở 3 tab Orca "Hades A/B/C - viec 57" (`gemini-3.8-flash-medium`, `--mode plan`, lệnh qua `lr_viec57\hades_X.cmd` vì PowerShell làm
  vỡ dấu ngoặc kép lồng nhau). Không tab nào hỏi "trust folder".
- **~15:18 Hades A trình BƯỚC 1** (nghĩ 3m28s + 34s): A1 neo đúng 1 lần dòng 1812–1814, A2 đúng 1 lần dòng 1854, thay đúng như MỚI, không rủi ro.
  ✅ **Claude Code duyệt BƯỚC 2 PHẦN A theo quyền Đại Ca trao** — lý do: 2 neo khớp đúng đặc tả, khối MỚI đã áp thử lên bản sao + `ast.parse` đạt;
  PHẦN A chỉ sửa `server.py`, không đụng `index.html` của tab B/C ⇒ cho chạy ngay, không chờ B/C.
- **~15:21 A BƯỚC 2 XONG** (chế độ thường — Hades hỏi từng lần sửa, Claude Code chọn "Yes" từng lần, KHÔNG bật tự duyệt). Claude Code kiểm độc lập:
  `server.py` bỏ khác biệt xuống dòng thì **trùng khít bản áp thử** (0 dòng khác) · `ast.parse` OK.
- **~15:25 B, C quá 15 phút vẫn "Reading file…"** (công cụ tìm của Hades đọc cả `index.html` ~1 MB) ⇒ Claude Code ngắt (Esc), giao lại BƯỚC 1 kèm
  **đúng dải dòng** cần mở, cấm tìm kiếm.
- **~15:30 Đại Ca thêm việc BC016 (Kho + Hàng hoá)** ⇒ PHẦN D (đặc tả trên, áp thử lên bản sao + Babel OK) ⇒ mở tab "Hades D".
- **~15:31 B trình BƯỚC 1** (nghĩ 40s sau khi có dải dòng): B1–B4 khớp đúng 1 lần, thay y hệt MỚI, không rủi ro.
  ✅ **Claude Code duyệt BƯỚC 2 PHẦN B theo quyền Đại Ca trao** — 4 neo khớp, khối MỚI đã áp thử + Babel đạt. Thứ tự sửa `index.html`: B → C → D
  (cùng file, không cho 2 tab sửa cùng lúc).
- **~15:33 C trình BƯỚC 1**: C1–C4 khớp đúng 1 lần, thay y hệt MỚI. ✅ **Claude Code duyệt BƯỚC 2 PHẦN C theo quyền Đại Ca trao** (chạy sau B).
- **~15:44 B BƯỚC 2 XONG** (4 lần hỏi, Claude Code soát diff từng lần rồi "Yes"; `git diff` +7/−2, dòng `khuvuc` không đổi) ⇒ giao C.
- **~15:44 D trình BƯỚC 1** (nghĩ 6m13s + 1m38s): D1–D7 khớp đúng 1 lần, thay y hệt MOI. ✅ **Claude Code duyệt BƯỚC 2 PHẦN D theo quyền Đại Ca
  trao** — 7 neo khớp, khối MỚI đã áp thử + Babel đạt; chạy sau C.
- **~15:51 C BƯỚC 2 XONG** (4 lần hỏi, soát từng lần) ⇒ giao D. Mỗi lần sửa `index.html` Hades mất ~1–2 phút (file ~1 MB).
- **~15:53–16:00 D đọc lại cả `index.html` ~6 phút không sửa** ⇒ Claude Code ngắt, gửi **số dòng HIỆN TẠI** của 7 neo ⇒ D hỏi duyệt ngay.
  **~16:07 D BƯỚC 2 XONG** (6 lần hỏi — D1+D2 gộp 1 lần, thứ tự D1/2 → D3 → D6 → D5 → D7 → D4; soát từng lần rồi "Yes").
- **Claude Code kiểm độc lập (~16:10):** `index.html` + `server.py` **trùng khít bản áp thử** A+B+C+D (bỏ khác biệt xuống dòng: 0 dòng khác) ·
  `ast` OK · Babel OK · không hàm trùng · 219 hàm / 81 route (không thêm route ⇒ Bẫy 30 không đổi).
  Giao diện (Chrome ngầm 1366, server thử 5052 = code thật + DB giả, `lr_viec57\cdp_viec57*.py`): `/api/metadata` THẬT trả `nguon_don` · BC015 ô
  ngoài Thời gian · Nguồn đơn · Đơn vị 1 hàng · để trống ⇒ `source_ids=` rỗng, SQL không có `EXTRA_ID_2 IN` · chọn 2 nguồn ⇒ `source_ids=GRAB,SHOPEE`,
  SQL `EXTRA_ID_2 IN (?,?)`, tham số đúng thứ tự (`POSTED, từ, đến, 66, GRAB, SHOPEE`), giấy "Nguồn đơn: GrabFood, ShopeeFood" · xuất Excel mang
  `source_ids` · BC016 ô ngoài Thời gian · Đơn vị · Kho · Hàng hoá · chọn ⇒ `wh_ids=KTONG&item_ids=SUA-DAC`, SQL `W.WAREHOUSE_ID IN` + `W.ITEM_ID IN`,
  giấy "Kho: Kho tổng" / "Hàng hoá: SUA-DAC - Sữa đặc" · BC017 ô ngoài y cũ. Hàng điều kiện BC016: **1 hàng ở 1536 / 1920 / 1366 thu gọn cột**;
  1366 cột mở rộng ⇒ cụm nút rớt hàng 2 (y BC017/BC018 — đã ghi CLAUDE.md).
- ⏳ **Còn M2 DB thật** (`lr_viec57\kiem_m2_viec57.py`, so "có lọc" với đúng phần tương ứng của "không lọc", T09/2026) — cần VPN + mật khẩu `config.json`.
  4 tab Hades đã đóng.
- ✅ **~16:40 M2 DB THẬT ĐẠT** (Đại Ca điền mật khẩu, VPN có; T09/2026):
  - BC015 8/8: metadata `nguon_don` 23 mục = đúng 23 mã DM_EXTRA_2 (12,4s cả metadata) · lọc 1 nguồn (`10000171`, 72 dòng) = đúng khối của nguồn đó + tổng
    = dòng nguồn · lọc 2 nguồn = đúng 2 khối · `source_ids=` rỗng = y không lọc · chi tiết theo ngày (đường xuất Excel, 2.049 dòng) = đúng khối · nhân viên
    giới hạn đơn vị `02` + lọc nguồn ⇒ chỉ `02`.
  - BC016 6/6 (`kiem_bc016_chuan.py`): lọc kho `CH.2.36QT` (82 mã) / `KTONG` (266) / kho nhỏ nhất (7) = đúng nhóm kho (dòng + tổng nhóm) · lọc 2 và 3 hàng
    hoá = đúng các dòng · kho + hàng = đúng 1 dòng · tham số rỗng = y không lọc. ⚠️ Lần chạy đầu báo 3 LỖI — **do cách so của kịch bản**, không phải code:
    BC016 có **cột động theo loại CT có phát sinh** ⇒ lọc thì bớt cột toàn 0 (7 nhập / 12 xuất → 2 / 1 khi lọc 2 mã). So lại bỏ cột toàn 0: 0 chỗ lệch.
  - **Phát hiện dữ liệu:** chứng từ 2026 có 4 mã nguồn KHÔNG có trong DM_EXTRA_2 (`1000169`, `RYO`, `SOURCE-145`, `SOURRCE-M145` — ~50 phiếu, tổng
    ≈ −2,5 triệu, không đáng kể) và **nguồn TRỐNG: 25.514 phiếu, 25.027.727.503 = 7,26% doanh thu 2026, 81 đơn vị** — ô Nguồn đơn hiện chưa chọn riêng
    được nhóm trống (đặc tả ghi "cố ý") ⇒ hỏi Đại Ca.
- **~16:45 Đại Ca chốt thêm mục "Không có nguồn đơn", giao Hades** ⇒ PHẦN E (áp thử lên bản sao + `ast` OK) ⇒ mở tab "Hades E - viec 57" (`--focus`,
  để mở cho Đại Ca theo dõi — Đại Ca hỏi *"hades nó vẫn đang làm không, t thấy các tab đóng nên t không theo dõi được"*).
- **~16:33 E trình BƯỚC 1** (đã đưa sẵn số dòng ⇒ ~5 phút): E1–E3 khớp đúng 1 lần, thay y hệt MỚI. ✅ **Claude Code duyệt BƯỚC 2 PHẦN E theo quyền
  Đại Ca trao** — 3 neo khớp, khối MỚI áp thử + `ast` đạt.
- **~16:36 E BƯỚC 2 XONG** (3 lần hỏi, soát từng lần): `server.py` trùng khít bản áp thử A+E · `ast` OK. **M2 DB thật E đạt 6/6** (`kiem_m2_E.py`, T09):
  metadata mục đầu `(TRONG)` "Không có nguồn đơn" (24 mục) · chỉ `(TRONG)` = đúng khối nhóm trống (2.318.162.779) · `(TRONG)` + `10000171` = đúng 2 khối ·
  chi tiết = đúng khối · hồi quy N2, N4 đạt.
- ⚠️ **ĐÍNH CHÍNH cách gọi ở mục trên:** "25 tỷ = 7,26% doanh thu" là 7,26% **tổng của BC015**, KHÔNG phải doanh thu bán cho khách. Tách theo loại CT
  (SALE_VIEW, POSTED, 2026, nguồn trống): **BNB** bán nội bộ ~2,3–2,6 tỷ/tháng (1 đơn vị — Kho tổng) · **BH** ~40 triệu/tháng (1 đơn vị) · **XDCNB** điều
  chuyển nội bộ ~2.000–2.700 phiếu/tháng ở 50–65 đơn vị, **T1–T9 tiền = 0 nhưng từ T10/2026 có tiền: T10 1.606.989.769, T11 (tới 06/11) 495.988.059**
  (cùng lúc BNB T10 tụt còn 750 triệu) · BHVAT/BHK ≈ 0 (39,8 triệu BHVAT T1 bị HDDC trừ đúng −39,78 triệu). ⇒ Từ T10 tổng BC015 đang cộng cả điều
  chuyển nội bộ — hỏi Đại Ca. Chú thích E1 trong `server.py` còn ghi "7,26% doanh thu" ⇒ sẽ sửa câu chữ.
- **~16:40 Đại Ca chốt: "PHần này bắt buộc loại phiếu XDCNB ra á"** ⇒ PHẦN F (áp thử + `ast` OK). Chụp JSON BC015 bản hiện tại trên DB thật TRƯỚC khi sửa
  (`lr_viec57\bc015_truoc_F.json`: T09 tổng 33.711.229.223 · T10 36.360.789.074 · T10 nhóm trống 2.401.788.545 · T1–T10 338.917.669.482).
- **~16:44 Hades E (dùng tiếp tab, chuyển lại plan) trình BƯỚC 1 PHẦN F** (~1,5 phút): F1, F2 khớp đúng 1 lần, thay y hệt MỚI.
  ✅ **Claude Code duyệt BƯỚC 2 PHẦN F theo quyền Đại Ca trao** — 2 neo khớp, khối MỚI áp thử + `ast` đạt; điều kiện là hằng, không thêm tham số.
- **~16:46 F BƯỚC 2 XONG** (2 lần hỏi, soát từng lần): `server.py` trùng khít bản áp thử A+E+F · `ast` OK.
  **M2 DB thật F đạt 13/13** (`kiem_m2_F.py`, so JSON chụp trước): T09 y hệt trước · T10 tổng 36.360.789.074 − XDCNB 1.606.989.769 (tra thẳng SQL)
  = 34.753.799.305 cả 8 cột tiền · 15 nguồn có tên y hệt · nhóm trống 2.401.788.545 → 794.798.776 · chi tiết T10 cùng luật · T1–T10 338.917.669.482 −
  1.607.137.769 = 337.310.531.713, 25 nguồn y hệt · mục `(TRONG)` cùng luật.
- ⚠️ Claude Code sơ suất: 2 file kết quả (`bc015_truoc_F.json`, `kq_m2_E.json`) bị ghi vào THƯ MỤC REPO (kịch bản `os.chdir(REPO)` rồi ghi theo đường
  dẫn tương đối) — chưa vào git (chưa `git add`), đã chuyển ra `lr_viec57\`. Kịch bản sau dùng đường dẫn tuyệt đối.
- **~17:00 Đại Ca bấm thử trên server xem 5051 (code mới, DB thật) ⇒ "ok rồi chơi đi"** ⇒ phát hành `v2.1.13` (ghi kết quả ở `NHAT_KY_CONG_VIEC.md`).

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
