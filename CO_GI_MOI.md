# CÓ GÌ MỚI — DATA REPORT

> **App đọc file này** để hiện mục *"Có gì mới"* trong hộp thoại cập nhật (`_doc_co_gi_moi` trong `server.py`).
> Nó đọc **đúng bản file nằm ở tag của bản mới** trên GitHub, nên **phải sửa file này TRƯỚC lần push phát hành**.
>
> Luật viết (Đại Ca chốt 26/09/2026):
> - **Chỉ ghi TÍNH NĂNG** người dùng thấy được khi làm việc (màn hình mới, báo cáo mới, nút mới, lỗi họ từng gặp đã sửa).
> - Thay đổi phía **hệ thống / code / cách thông báo cập nhật** ⇒ **KHÔNG kể chi tiết**, gộp thành đúng MỘT dòng
>   `- Cập nhật hệ thống`. Bản chỉ có loại này thì mục đó chỉ có dòng ấy.
> - Mỗi bản một mục `## vX.Y.Z`, **mới nhất ở trên**. Số bản phải khớp `version.txt` của lần phát hành đó.
> - Mỗi dòng bắt đầu bằng `- ` là **một thay đổi**. Viết cho **nhân viên** đọc: nói cái họ thấy, không nói tên hàm/biến.
> - Tối đa ~5 dòng mỗi bản. App gộp mọi bản người dùng nhảy qua, **bỏ dòng trùng** (nên "Cập nhật hệ thống" chỉ hiện
>   một lần), hiện tối đa 8 dòng, dư thì ghi "… và N thay đổi khác".
> - Dòng không bắt đầu bằng `- ` (như khối ghi chú này) app bỏ qua.

## v2.0.2
- Sửa lỗi nhân viên không xuất được Excel ở Báo cáo tài chính (báo "Route chưa khai báo quyền")
- Ô lọc Đơn vị chỉ hiện các đơn vị bạn được xem
- Bỏ trống tài khoản ứng dụng khi đăng nhập thì báo ngay, không phải chờ
- Bị đăng xuất giữa chừng (đổi mật khẩu, bị khoá, đổi quyền) thì màn đăng nhập nói rõ lý do

## v2.0.1
- Cập nhật hệ thống

## v2.0.0
- Giao diện mới DATA REPORT: cột phân hệ bên trái, trang chủ, thanh lọc mới cho 9 màn danh sách
- Báo cáo tài chính xuất Excel .xlsx thật, giữ y biểu mẫu đang xem, chữ 11pt
- Bảng danh sách: ẩn/hiện và kéo giãn cột; Excel xuất đúng các cột đang hiện
- Sửa ô Số chứng từ của Sổ tiền mặt & ngân hàng: gõ từng chữ bị lọc ra 0 dòng
- Sửa bảng chỉ hiện khoảng 87 dòng rồi trắng khi đổi qua lại giữa các màn
