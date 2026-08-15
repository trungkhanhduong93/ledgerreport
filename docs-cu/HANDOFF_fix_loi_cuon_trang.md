# HANDOFF — Sửa lỗi "load được vài chục dòng rồi bên dưới trắng" (Danh sách chứng từ tiền)

> Lỗi: vào tab **Danh sách chứng từ tiền**, TRUY VẤN xong chỉ thấy vài chục dòng, cuộn xuống thì **trắng toàn bộ** dù tổng (RESULTS) báo cả trăm nghìn dòng. Sửa ở **frontend `index.html`**, áp cho **CẢ 2 folder** (LedgerReport + LedgerStudio).

---

## 1. Nguyên nhân (đã chẩn đoán xong)

- **KHÔNG phải lỗi dữ liệu.** Backend `/api/voucher?page_size=10000` trả về **đủ 10.000 dòng đầy đủ** (đã kiểm dòng 0/100/5000/9999 đều có TK Nợ/Có, số tiền, diễn giải). Vậy `voucherData` có đủ dữ liệu.
- Lỗi nằm ở **virtual-scroll** (hook `useVirtualScroll` trong `index.html`). Bảng chỉ render những dòng trong khung nhìn; vị trí khối render tính bằng `topPadding = startIndex * eff`, với `eff` = **chiều cao 1 dòng đo từ DOM**.
- Bản hook CŨ đo chiều cao dòng **2 lần rồi DỪNG hẳn** (`if (calibRef.current >= 2) return;`). Bảng chứng từ tiền **rất rộng (29 cột, có cuộn ngang)** nên layout ổn định CHẬM → hook đo trúng lúc dòng đang cao bất thường → `eff` **bị kẹt ở giá trị sai** và không bao giờ đo lại → `topPadding` lệch dần → khối dòng render **trôi ra ngoài viewport** → nhìn thấy trắng.
- Tab "bán hàng" (SALE) layout ổn định sớm hơn nên không dính → dễ tưởng chỉ tab tiền lỗi, nhưng gốc là ở **hook dùng chung**.

---

## 2. CÁCH SỬA — đổi phần đo chiều cao dòng trong `useVirtualScroll`

Mở `index.html`, tìm hàm `function useVirtualScroll(totalItems, itemHeight, containerRef) {` (khoảng dòng **200**). Bên trong có 1 `React.useLayoutEffect` đo chiều cao dòng. **Thay nguyên block đó.**

### TÌM (bản CŨ bị lỗi):
```jsx
            React.useLayoutEffect(() => {
                if (calibRef.current >= 2) return;        // đã hiệu chỉnh ổn định → bỏ qua
                const c = containerRef.current;
                if (!c) return;
                const rows = [...c.querySelectorAll('tbody tr')].filter(tr => tr.children.length > 1);
                const hs = rows.slice(0, 12).map(tr => tr.getBoundingClientRect().height).filter(h => h > 4 && h < 200);
                if (hs.length) {
                    const avg = hs.reduce((a, b) => a + b, 0) / hs.length;
                    if (avg > 4 && Math.abs(avg - rowH) > 0.4) { setRowH(avg); calibRef.current = 0; }
                    else calibRef.current += 1;           // đã khớp → tăng đếm để dừng
                }
            });
```

### THAY BẰNG (bản ĐÚNG — luôn đo lại + dùng trung vị):
```jsx
            React.useLayoutEffect(() => {
                const c = containerRef.current;
                if (!c) return;
                const rows = [...c.querySelectorAll('tbody tr')].filter(tr => tr.children.length > 1);
                const hs = rows.slice(0, 16).map(tr => tr.getBoundingClientRect().height).filter(h => h > 4 && h < 200);
                if (hs.length) {
                    hs.sort((a, b) => a - b);
                    const med = hs[Math.floor(hs.length / 2)];   // trung vị: bền với dòng lẻ cao bất thường
                    if (med > 4 && Math.abs(med - rowH) > 0.5) setRowH(med);   // LUÔN đo lại → tự khớp, không kẹt ở giá trị sai
                }
            });
```

**Khác biệt cốt lõi:**
1. **Bỏ `if (calibRef.current >= 2) return;`** → hook ĐO LẠI mỗi lần render. Nếu lỡ đo sai một lần, lần render kế tiếp tự đo lại đúng → không còn kẹt.
2. **Dùng TRUNG VỊ (median)** thay vì trung bình → nếu có vài dòng cao bất thường (chữ xuống dòng), trung vị vẫn ra chiều cao chuẩn.
3. Vì dòng cao đều nhau, sau khi hội tụ `med` không đổi → không gọi `setRowH` nữa → không gây render thừa.

> Không cần xóa biến `calibRef` (vẫn được dùng ở effect `[totalItems]` để reset khi đổi dữ liệu — để nguyên, vô hại).

---

## 3. Phòng lỗi tái phát — giữ chiều cao dòng ĐỀU

Hook chỉ chạy đúng khi mọi dòng cao bằng nhau. Trong component `VoucherRow` (khoảng dòng 1997), **mọi ô chữ phải có `whitespace-nowrap`** để không xuống dòng (làm dòng cao gấp đôi → lệch lại). Ô số (`text-right font-mono`) không có khoảng trắng nên an toàn. Khi thêm cột mới cũng phải giữ quy tắc này.

---

## 4. Kiểm tra sau khi sửa

1. Mở tab **Danh sách chứng từ tiền** → TRUY VẤN.
2. Cuộn xuống tới đáy: phải thấy **đủ dòng liên tục, không có khoảng trắng**, số thứ tự (#) tăng đều tới hết trang (vd 10.000).
3. Đổi "Hiển thị" / đổi trang / cuộn nhanh: vẫn không trắng.
4. Kiểm tab **bán hàng (SALE)** vẫn chạy bình thường (hook dùng chung).

---

## 5. Áp cho cả 2 folder + build lại

- Sửa GIỐNG HỆT trong:
  - `D:\IACC HCM\iPOS ACC\ACC PMKT\LedgerReport\index.html`
  - `D:\IACC HCM\iPOS ACC\ACC PMKT\LedgerStudio\index.html`
  (block `useLayoutEffect` này GIỐNG NHAU 100% ở cả 2 file.)
- Đóng app đang chạy (EXE bị khóa thì không build đè được), rồi build lại từng folder:

**LedgerReport:**
```powershell
cd "D:\IACC HCM\iPOS ACC\ACC PMKT\LedgerReport"
python -m PyInstaller --noconsole --onefile --clean --noconfirm --name "iPOS_Accounting_Report" --icon icon.ico --add-data "index.html;." --add-data "install_driver.ps1;." --add-data "manifest.json;." --add-data "icon.svg;." --collect-submodules flask --collect-submodules flask_cors --collect-submodules pyodbc --hidden-import pyodbc --hidden-import flask --hidden-import flask_cors server.py
```
**LedgerStudio:** y hệt nhưng `cd ...\LedgerStudio` và đổi `--name "iPOS_Ledger_Studio"`. EXE ra ở `dist\`.

---

## Ghi chú: lỗi "Unexpected end of JSON input" (nếu gặp khi xem tab tổng hợp)
Lỗi KHÁC, không liên quan virtual-scroll. Nguyên nhân: 6 hàm load (ledger/sale/voucher/...) dùng **chung 1 `abortRef`**; khi một request đang `r.json()` đọc body 10MB mà bị một load khác hủy ngang → ném `"Unexpected end of JSON input"` (không phải `AbortError`) → hiện alert dù dữ liệu thật vẫn ổn. Sửa: mỗi hàm load đổi `abortRef.current = new AbortController();` thành `const _ctrl = new AbortController(); abortRef.current = _ctrl;` và trong `catch` đổi `if (err.name === 'AbortError') return;` thành `if (err.name === 'AbortError' || _ctrl.signal.aborted) return;`.
