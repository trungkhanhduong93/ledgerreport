# AGENTS.md — con trỏ

Context cho mọi AI agent (Cursor, Copilot, Codex, Windsurf, Antigravity…) làm việc trên project
**LedgerReport**: đọc **[CLAUDE.md](CLAUDE.md)**.

Ba việc phải nắm trước khi sửa bất cứ dòng nào:

1. **Khoá ngữ cảnh** — thư mục này là `LedgerReport`, KHÔNG phải `LedgerStudio`. Mã `BC0xx` cùng số
   nhưng khác nghĩa giữa hai project.
2. **Sửa xong phải đồng bộ** — chạy `.\Sync-And-Backup.ps1 -Commit`. Thư mục làm việc và repo git con
   là hai bản copy riêng; quên đồng bộ là code không hề được sao lưu.
3. **Đừng viết lại hàm đã mất** — tìm trong `git show b6553f6:server.py` trước. Viết lại từ đầu đã
   một lần cho ra số liệu sai.

> Đừng chép nội dung CLAUDE.md sang đây. Một nguồn sự thật thôi.
