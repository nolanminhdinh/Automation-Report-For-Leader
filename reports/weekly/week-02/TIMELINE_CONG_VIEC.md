# ⏱️ TIMELINE CÔNG VIỆC TUẦN 2 (WEEK 2 DETAILED TIMELINE)

> **Dự án**: Auto Annotation Report Pipeline (CVAT & GitHub Sync - Power BI Hybrid)  
> **Thời gian**: Tuần 2 (Giai đoạn Triển khai Tầng Ingestion, ETL Engine & Chuẩn hóa Data Contract)  
> **Người duyệt**: Đinh Công Minh (Project Lead)

---

## 🎯 MỤC TIÊU CỐT LÕI TUẦN 2
1. Nghiệm thu, chuẩn hóa và tích hợp module Ingestion API (CVAT REST API v2 & GitHub API v3) vào nhánh chính.
2. Xây dựng Data Contract v1 (`report_data.json`) làm cầu nối vững chắc giữa Tầng Thu Thập và Tầng Phân Tích (ETL).
3. Triển khai thuật toán trích xuất Frame Index từ GitHub Issue và sinh Deep Link CVAT chính xác tới từng khung hình.
4. Xây dựng bộ Unit Test tự động hóa (17 test cases) và bộ mẫu Issue Templates trên GitHub.

---

## 📅 BẢNG TIMELINE CÔNG VIỆC CHI TIẾT TỪNG NGÀY CHO 5 THÀNH VIÊN

### 1. Đinh Công Minh (Project Lead & BI Architect)
* **Thứ Hai - Thứ Ba**:
  * Đánh giá và nghiệm thu chéo repository demo của Vũ Trường Duy (`mentor-report-integration-demo`).
  * Ban hành biên bản nghiệm thu kỹ thuật `reports/NGHIEM_THU_VA_TICH_HOP_API_INGESTION.md`.
* **Thứ Tư - Thứ Năm**:
  * Tái cấu trúc mã nguồn thành kiến trúc phân tầng chuẩn: `src/extractors/`, `src/processors/`, `src/generators/`.
  * Nâng cấp logic Deep Link hỗ trợ chỉ số frame (`?frame={idx}`).
  * Viết bộ 17 Unit Tests tự động hóa và chạy kiểm thử toàn trình (End-to-End Offline Replay).
* **Thứ Sáu - Chủ Nhật**:
  * Handoff Data Contract v1 cho Phạm Nguyễn Tuân phục vụ việc tính toán các chỉ số Vận tốc, Chất lượng và xuất CSV.
  * Phối hợp cùng Ngô Duy Ngọc tích hợp script `src/sync.py` vào GitHub Actions Workflow.

### 2. Nguyễn Minh Tú (Data Integration Engineer - CVAT API)
* **Thứ Hai - Thứ Ba**:
  * Khảo sát endpoint trích xuất Annotations theo từng Job trên CVAT Cloud.
* **Thứ Tư - Thứ Năm**:
  * Phối hợp cùng Lead Minh và Duy để thống nhất sử dụng lớp nền `BaseClient` và `CVATExtractor`.
* **Thứ Sáu - Chủ Nhật**:
  * Tối ưu hóa hàm trích xuất Annotations summary theo shapes, tracks, tags và danh mục label.

### 3. Vũ Trường Duy (Data Integration Engineer - Quality API & GitHub)
* **Thứ Hai - Thứ Ba**:
  * Hoàn thiện repository demo độc lập `mentor-report-integration-demo` và viết tài liệu `TomTat.md`, `DATA_CONTRACT.md`.
* **Thứ Tư - Thứ Năm**:
  * Bàn giao mã nguồn cho Lead Minh để review và refactor vào nhánh chính của dự án.
* **Thứ Sáu - Chủ Nhật**:
  * Hỗ trợ kiểm thử thực tế việc đối soát chéo liên kết task/job trên các issue thật của repository.

### 4. Phạm Nguyễn Tuân (Analytics & ETL Engineer)
* **Thứ Hai - Thứ Tư**:
  * Tiếp nhận Data Contract v1 (`report_data.json`) từ tầng Ingestion.
* **Thứ Năm - Chủ Nhật**:
  * Bắt đầu xây dựng các module xử lý chỉ số trong `src/processors/`: tính Vận tốc (Frames/h, Objects/h), FTPR %, Rework % và thuật toán phân khúc thành viên.

### 5. Ngô Duy Ngọc (DevOps & Automation Engineer)
* **Thứ Hai - Thứ Tư**:
  * Chuẩn hóa môi trường Python ảo `.venv`, cấu hình dependencies trong `requirements.txt`.
* **Thứ Năm - Chủ Nhật**:
  * Cập nhật file `.github/workflows/scheduled_report.yml` để gọi lệnh `python src/sync.py`.
  * Cấu hình secrets trên GitHub Actions (`CVAT_TOKEN`, `GITHUB_TOKEN`, `TELEGRAM_BOT_TOKEN`).
