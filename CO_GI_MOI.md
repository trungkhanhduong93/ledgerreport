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
>   Mở đầu bằng **tên màn hình / báo cáo** (vd *"Nhật ký chung: …"*), nói **việc họ làm được**. ⛔ Đừng dùng chữ kiểu
>   *"thật / giả"*, *"để trống thật"*, *".xlsx thật"* — người đọc không hiểu (Đại Ca nhắc 28/09/2026).
> - ⚠️ App đọc file này **tại tag** của bản mới ⇒ phát hành rồi mới sửa câu thì **phải ra bản kế tiếp** mới có tác dụng.
> - Tối đa ~5 dòng mỗi bản. App gộp mọi bản người dùng nhảy qua, **bỏ dòng trùng** (nên "Cập nhật hệ thống" chỉ hiện
>   một lần), hiện tối đa 8 dòng, dư thì ghi "… và N thay đổi khác".
> - Dòng không bắt đầu bằng `- ` (như khối ghi chú này) app bỏ qua.

## v2.1.1
- Báo cáo TC: thêm BC017 Báo cáo bán hàng — xem theo đơn vị, theo ngày hoặc theo nguồn đơn, từng dòng hàng hoặc chỉ dòng tổng, để đối chiếu doanh thu
- Sổ nhật ký chung, Sổ chi tiết tài khoản, Sổ tiền mặt & ngân hàng, Bán hàng theo nguồn đơn, Nhập xuất tồn: nút Cấu hình cột để thêm / bớt cột, xuất Excel đúng các cột đang hiện
- Các màn danh sách chứng từ: ghim cột bất kỳ sát lề trái hoặc phải, cuộn ngang cột đó vẫn đứng yên
- Các màn danh sách chứng từ: bấm đúp mép phải tiêu đề cột để cột vừa khít nội dung, hoặc bấm "Vừa khít tất cả cột"
- Sổ tiền mặt & ngân hàng: bấm sang trang một lần là chuyển, không phải bấm hai lần

## v2.1.0
- Mở ứng dụng nhanh hơn hẳn, không cần Internet để tải giao diện — không còn màn trắng chờ 7–13 giây
- Nhật ký chung: bấm Hủy xuất hiện hộp hỏi giữa màn; trong lúc hỏi việc xuất tạm dừng, chọn Không là xuất tiếp
- Nút Tải lại: kiểm lại quyền và nạp lại giao diện, không tự lọc số liệu; quyền vừa bị đổi thì tự đăng xuất để đăng nhập lại
- Cột bên trái: mỗi danh sách chứng từ có biểu tượng riêng, dễ nhận ra
- Màn đăng nhập: số phiên bản hiện nổi màu xanh, dễ nhìn; không còn bật khung Google Dịch ở góc màn hình
- Cập nhật hệ thống

## v2.0.9
- Mở ứng dụng nhanh hơn hẳn, không cần Internet để tải giao diện — không còn màn trắng chờ 7–13 giây
- Nhật ký chung: bấm Hủy xuất hiện hộp hỏi giữa màn; trong lúc hỏi việc xuất tạm dừng, chọn Không là xuất tiếp
- Nút Tải lại: kiểm lại quyền và nạp lại giao diện, không tự lọc số liệu; quyền vừa bị đổi thì tự đăng xuất để đăng nhập lại
- Cột bên trái: mỗi danh sách chứng từ có biểu tượng riêng, dễ nhận ra
- Màn đăng nhập: số phiên bản hiện nổi màu xanh, dễ nhìn; không còn bật khung Google Dịch ở góc màn hình
- Cập nhật hệ thống

## v2.0.8
- Nhật ký chung: bấm Hủy xuất là dừng ngay, thư mục xuất không còn thoáng hiện file đang làm dở
- Xuất Excel: nếu file cùng tên đang mở trong Excel, app báo rõ cần đóng file đó rồi xuất lại

## v2.0.7
- Nhật ký chung: hộp xuất Excel hiện số dòng đã ghi, tốc độ, thời gian đã chạy và thời gian còn lại
- Nhật ký chung: có nút Hủy xuất để dừng giữa chừng, không để lại file dở

## v2.0.6
- Nhật ký chung: xuất Excel có đồng hồ đếm ngược thời gian còn lại, thanh tiến trình chạy đúng phần trăm công việc
- Sửa lỗi thỉnh thoảng bị đăng xuất giữa chừng khi nhiều người mở app cùng lúc

## v2.0.5
- Màn đăng nhập mới: chia rõ 2 phần Máy chủ SQL và Tài khoản ứng dụng, chữ tiếng Việt hết
- Màn đăng nhập: bấm hình con mắt để xem lại mật khẩu vừa gõ
- Màn đăng nhập: các ô để trống sạch, không còn chữ mờ ví dụ dễ tưởng là đã điền sẵn

## v2.0.4
- Báo cáo tài chính: file Excel xuất ra giữ đúng mẫu đang xem — tiêu đề cột canh giữa, cột Chỉ tiêu canh trái

## v2.0.3
- Nhật ký chung: file Excel chi tiết có thêm 2 cột Mã mục chi phí và Tên mục chi phí
- Nhật ký chung: lọc ô trống ở cột Công việc, Tên đối tượng trong file Excel nay ra đủ dòng

## v2.0.2
- Sửa lỗi nhân viên không xuất được Excel ở Báo cáo tài chính (báo "Route chưa khai báo quyền")
- Ô lọc Đơn vị chỉ hiện các đơn vị bạn được xem
- Bỏ trống tài khoản ứng dụng khi đăng nhập thì báo ngay, không phải chờ
- Bị đăng xuất giữa chừng (đổi mật khẩu, bị khoá, đổi quyền) thì màn đăng nhập nói rõ lý do

## v2.0.1
- Cập nhật hệ thống

## v2.0.0
- Giao diện mới DATA REPORT: cột phân hệ bên trái, trang chủ, thanh lọc mới cho 9 màn danh sách
- Báo cáo tài chính xuất Excel (.xlsx) giống hệt mẫu đang xem: tiêu đề cột canh giữa, cột Chỉ tiêu canh trái, chữ cỡ 11
- Bảng danh sách: ẩn/hiện và kéo giãn cột; Excel xuất đúng các cột đang hiện
- Sửa ô Số chứng từ của Sổ tiền mặt & ngân hàng: gõ từng chữ bị lọc ra 0 dòng
- Sửa bảng chỉ hiện khoảng 87 dòng rồi trắng khi đổi qua lại giữa các màn
