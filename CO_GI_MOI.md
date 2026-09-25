# CÓ GÌ MỚI — DATA REPORT

> **App đọc file này** để hiện mục *"Có gì mới"* trong hộp thoại cập nhật (`_doc_co_gi_moi` trong `server.py`).
> Nó đọc **đúng bản file nằm ở tag của bản mới** trên GitHub, nên **phải sửa file này TRƯỚC lần push phát hành**.
>
> Luật viết:
> - Mỗi bản một mục `## vX.Y.Z`, **mới nhất ở trên**. Số bản phải khớp `version.txt` của lần phát hành đó.
> - Mỗi dòng bắt đầu bằng `- ` là **một thay đổi**. Viết cho **nhân viên** đọc: nói cái họ thấy, không nói tên hàm/biến.
> - Tối đa ~5 dòng mỗi bản. App hiện tối đa 8 dòng (gộp mọi bản người dùng nhảy qua), dư thì ghi "… và N thay đổi khác".
> - Dòng không bắt đầu bằng `- ` (như khối ghi chú này) app bỏ qua.

## v2.0.1
- Báo có bản mới rõ hơn: mở app là hiện hộp thoại, ghi luôn bản mới có gì
- Bấm "Để lần sau" thì vẫn còn nút cam trên thanh trên, 2 giờ sau nhắc lại
- Đang mở app mà có bản mới cũng biết (app tự kiểm lại mỗi 2 giờ)

## v2.0.0
- Giao diện mới DATA REPORT: cột phân hệ bên trái, trang chủ, thanh lọc mới cho 9 màn danh sách
- Báo cáo tài chính xuất Excel .xlsx thật, giữ y biểu mẫu đang xem, chữ 11pt
- Bảng danh sách: ẩn/hiện và kéo giãn cột; Excel xuất đúng các cột đang hiện
- Sửa ô Số chứng từ của Sổ tiền mặt & ngân hàng: gõ từng chữ bị lọc ra 0 dòng
- Sửa bảng chỉ hiện khoảng 87 dòng rồi trắng khi đổi qua lại giữa các màn
