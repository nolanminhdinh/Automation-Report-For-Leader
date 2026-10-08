# ⏱️ TIMELINE CÔNG VIỆC TUẦN 1 (WEEK 1 DETAILED TIMELINE)

> **Dự án**: Auto Annotation Report Pipeline (CVAT & GitHub Sync - Power BI Hybrid)  
> **Thời gian**: Tuần 1 (Giai đoạn Khởi động, Khảo sát Nghiệp vụ, Kiến trúc & Prototype)  
> **Người duyệt**: Đinh Công Minh (Project Lead)

---

## 🎯 MỤC TIÊU CỐT LÕI TUẦN 1
1. Làm rõ 100% yêu cầu nghiệp vụ: định nghĩa các chỉ số Vận tốc, Chất lượng (Ground Truth vs Reviewer), Phân bổ class, Hình học vật thể.
2. Thiết lập kiến trúc Hybrid (Python ETL + Power BI) và Data Model (Star Schema).
3. Kết nối thành công API thử nghiệm với CVAT REST API v2 và GitHub API.
4. Chuẩn hóa môi trường làm việc, Git Flow và khung tự động hóa GitHub Actions.

---

## 📅 BẢNG TIMELINE CÔNG VIỆC CHI TIẾT TỪNG NGÀY CHO 5 THÀNH VIÊN

### 1. Đinh Công Minh (Project Lead & BI Architect)
* **Thứ Hai**:
  * Họp Kick-off dự án, khảo sát yêu cầu thực tế từ các phiên họp Mentor và Leader.
  * Phác thảo Mindmap nghiệp vụ và kiến trúc tổng thể 5 giai đoạn khép kín.
* **Thứ Ba**:
  * Xây dựng cấu trúc tài liệu kiến trúc hệ thống (`ARCHITECTURE.md`, `HYBRID_POWERBI_ARCHITECTURE.md`).
  * Định nghĩa Data Contract 3 bảng đầu ra cơ bản phục vụ nạp vào Power BI.
* **Thứ Tư**:
  * Soạn thảo chi tiết tài liệu đặc tả dữ liệu và chỉ số (`PROJECT_ANALYTICS_SPEC.md`).
  * Xây dựng danh mục Data Dictionary cho 9 bảng quan hệ và 20 công thức DAX Measures.
* **Thứ Năm**:
  * Thiết lập Kế hoạch Quản lý Dự án (`PROJECT_MANAGEMENT_PLAN.md`), phân chia WBS và ma trận RACI cho 4 thành viên.
  * Review kết quả kết nối thử nghiệm API CVAT & GitHub của Tú và Duy.
* **Thứ Sáu**:
  * Phác thảo wireframe giao diện 5 trang báo cáo Power BI: Executive 360, QA Deep-Dive, Annotator Matrix, Data Geometry, Edge-Cases.
  * Thống nhất bộ quy tắc phân loại nhân sự (Final Annotator Segmentation) cùng Tuân.
* **Thứ Bảy & Chủ Nhật**:
  * Kiểm tra chéo toàn bộ tài liệu dự án, đảm bảo tính đồng bộ trên GitHub repository.
  * Tổng kết tuần 1, chuẩn bị kế hoạch chạy Sprint MVP cho tuần 2.

---

### 2. Nguyễn Minh Tú (Data Integration Engineer - CVAT API)
* **Thứ Hai**:
  * Đọc tài liệu CVAT REST API v2, tìm hiểu cơ chế xác thực Token (PAT) và phân quyền Organization.
* **Thứ Ba**:
  * Khởi tạo Personal Access Token trên hệ thống CVAT, kiểm thử endpoint `GET /api/tasks` và `GET /api/tasks/{id}`.
* **Thứ Tư**:
  * Viết script thử nghiệm trích xuất danh sách Jobs (`GET /api/jobs?task_id={id}`) và trường dữ liệu `assignee`.
* **Thứ Năm**:
  * Nghiên cứu cấu trúc dữ liệu annotations của Job (`GET /api/jobs/{id}/annotations`).
  * Phân tích cách bóc tách tọa độ hình học (Rectangle `[x1, y1, x2, y2]` và Polygon points).
* **Thứ Sáu**:
  * Viết module `src/extractors/cvat_extractor.py` gom toàn bộ dữ liệu Tasks, Jobs và Annotations thành JSON thô.
* **Thứ Bảy & Chủ Nhật**:
  * Tối ưu hóa hàm xử lý phân trang (Pagination) để không bị sót jobs trên các task lớn.
  * Xuất file mẫu `data/raw/cvat_raw_sample.json` bàn giao cho Tuân.

---

### 3. Vũ Trường Duy (Data Integration Engineer - Quality API & GitHub)
* **Thứ Hai**:
  * Khảo sát luồng phản hồi ca khó và gắn cờ lỗi trên GitHub Issues (label `ca-kho`, `blocker`).
* **Thứ Ba**:
  * Tạo GitHub Personal Access Token (classic) với quyền `repo`, kiểm thử gọi GitHub REST API v3 lấy danh sách Issues.
* **Thứ Tư**:
  * Nghiên cứu CVAT Quality Management API (`GET /api/quality/reports?task_id={id}`) để trích xuất điểm mIoU, conflicts.
* **Thứ Năm**:
  * Nghiên cứu CVAT Issues & Comments API (`GET /api/issues`, `GET /api/comments`) để lấy nội dung lỗi từ Reviewer.
* **Thứ Sáu**:
  * Xây dựng hàm sinh **Deep Link CVAT** tự động: `{CVAT_HOST}/tasks/{task_id}/jobs/{job_id}?frame={frame_idx}`.
* **Thứ Bảy & Chủ Nhật**:
  * Viết module `src/extractors/github_extractor.py`, xuất file mẫu `data/raw/github_issues_sample.json`.
  * Phối hợp cùng Tú đồng bộ cấu trúc dữ liệu thô bàn giao cho tầng ETL.

---

### 4. Phạm Nguyễn Tuân (Analytics & ETL Engineer)
* **Thứ Hai**:
  * Nghiên cứu tài liệu các công thức tính toán: Vận tốc (Velocity), Thời gian xử lý trung bình (AHT), Mật độ lỗi (Defect Density).
* **Thứ Ba**:
  * Tìm hiểu thuật toán Shoelace (Gauss's area formula) để tính toán diện tích các đa giác polygon bất kỳ trong dữ liệu CVAT.
* **Thứ Tư**:
  * Nghiên cứu tiêu chuẩn phân loại kích thước đối tượng theo bộ dữ liệu chuẩn COCO (Small < 32x32, Medium, Large > 96x96).
* **Thứ Năm**:
  * Tiếp nhận file dữ liệu JSON mẫu từ Tú và Duy, phân tích các trường hợp dữ liệu bị khuyết thiếu (NULL, thiếu frame_count).
* **Thứ Sáu**:
  * Viết prototype script Python thử nghiệm tính toán Vận tốc (Frames/h) và phân loại đối tượng theo COCO Scale.
* **Thứ Bảy & Chủ Nhật**:
  * Thiết lập cấu trúc thư mục module `src/processors/` (chia tách `velocity.py`, `quality.py`, `geometry.py`).
  * Chuẩn bị logic xuất ra 4 file CSV mẫu theo chuẩn Star Schema đã thống nhất.

---

### 5. Ngô Duy Ngọc (DevOps & Automation Engineer)
* **Thứ Hai**:
  * Khởi tạo và chuẩn hóa cấu trúc repository Git, cấu hình file `.gitignore` cho Python và môi trường ảo.
* **Thứ Ba**:
  * Tạo file `.env.example` và danh sách phụ thuộc thư viện `requirements.txt` (requests, pandas, jinja2).
* **Thứ Tư**:
  * Tìm hiểu cơ chế GitHub Actions Workflow, cách cấu hình chạy theo lịch định kỳ bằng biểu thức Cron (`cron: '0 8 * * 1'`).
* **Thứ Năm**:
  * Thiết lập mẫu workflow `workflows/scheduled_report.yml`, cấu hình checkout repo và cài đặt môi trường Python.
* **Thứ Sáu**:
  * Nghiên cứu cơ chế bảo mật GitHub Actions Secrets (`CVAT_TOKEN`, `GH_PAT`, `TELEGRAM_BOT_TOKEN`).
* **Thứ Bảy & Chủ Nhật**:
  * Tạo Telegram Bot qua BotFather, lấy Token và Chat ID để kiểm thử gửi tin nhắn văn bản tự động qua Webhook.
  * Viết script mẫu `src/notifiers/bot.py` gửi thông báo thử nghiệm thành công.
