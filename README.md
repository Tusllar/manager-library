# 🎓 Hệ Thống Quản Lý Nộp Đồ Án - Sinh viên & Giảng viên

Dự án xây dựng hệ thống web hỗ trợ **sinh viên nộp đồ án** và **giảng viên quản lý, phê duyệt và nhận xét đồ án**, giúp quá trình làm việc và chấm điểm trở nên **hiệu quả và số hóa**. Hệ thống được xây dựng bằng **Python Flask** và **MySQL**.

---

## 🚀 Tính năng chính

### 👩‍🎓 Đối với sinh viên
- Đăng ký và đăng nhập tài khoản
- Điền thông tin cá nhân và đề tài đồ án
- Upload file đồ án (PDF, DOCX, ZIP,...)
- Xem lại lịch sử nộp và trạng thái phê duyệt
- Nhận phản hồi từ giảng viên

### 👨‍🏫 Đối với giảng viên
- Đăng nhập tài khoản
- Xem danh sách sinh viên và đồ án đã nộp
- Tải file đồ án để kiểm tra
- Gửi phản hồi, đánh giá, hoặc yêu cầu chỉnh sửa


### ⚙️ Hệ thống và quản lý
- Quản trị viên có thể quản lý người dùng, phân quyền
- Kiểm tra định dạng và dung lượng file khi upload
- Quản lý file lưu trữ theo từng sinh viên/đợt
- Duyệt hoặc từ chối đồ án
---

## 🏗️ Kiến trúc hệ thống

- **Backend**: Python Flask (RESTful API)
- **Database**: MySQL
- **Frontend**: HTML + CSS 
- **File Upload**: Lưu trữ nội bộ hoặc máy tính + drive
- **Thư viện phụ trợ**: Flask-Login, Flask-WTF, SQLAlchemy/MySQL Connector


