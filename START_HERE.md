# 👉 ĐỌC FILE NÀY ĐẦU TIÊN

Dự án **iPOS Accounting Ledger Report** (`LedgerReport`) — báo cáo kế toán iPOS ACC.
Flask `server.py` + React single-file `index.html`, đóng gói EXE.

## Đọc gì

**[CLAUDE.md](CLAUDE.md) — nguồn sự thật duy nhất.** Rule, kiến trúc, ma trận BC001–BC014,
12 bẫy đã trả giá, phương án backup, quy trình build/release. Đọc hết file đó là đủ.

`GEMINI.md` và `AGENTS.md` chỉ là con trỏ về `CLAUDE.md` — không có nội dung riêng.
`README.md`, `skill.md`, `KIEN_TRUC_TOAN_TAP.md` là tài liệu cũ, **có thể đã lỗi thời**;
chỗ nào mâu thuẫn thì `CLAUDE.md` thắng.

## 3 điều nhớ trước khi gõ dòng code đầu tiên

1. **Đây là `LedgerReport`, KHÔNG phải `LedgerStudio`.** Hai project song song, kiến trúc giống hệt,
   mã `BC0xx` cùng số nhưng khác nghĩa. Ở đây: `BC011` = LCTT Chú Long, `BC013` = công nợ.
2. **Sửa xong phải chạy `.\Sync-And-Backup.ps1 -Commit`.** Thư mục làm việc và repo con `ledgerreport\`
   là hai bản copy riêng — chỉ repo con mới lên GitHub. Quên đồng bộ = code chưa hề được sao lưu.
3. **Hàm bị mất thì tìm trong git trước, đừng viết lại.** `git show b6553f6:server.py` là bản đầy đủ
   đã chạy thật. Viết lại từ đầu đã một lần cho ra số liệu sai (BC011, 15/08/2026).

## Chạy nhanh

```bash
python server.py                 # dev, mở http://localhost:5050
python build_exe.py              # build EXE (nhớ taskkill EXE cũ trước)
.\Sync-And-Backup.ps1 -Commit    # đồng bộ + push GitHub → Actions tự tạo Release
```
