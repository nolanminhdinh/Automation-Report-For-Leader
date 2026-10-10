# 📑 BIÊN BẢN ĐÁNH GIÁ & NGHIỆM THU TÍCH HỢP KỸ THUẬT
## (TECHNICAL ACCEPTANCE & INTEGRATION REPORT)

* **Dự án**: [auto-annotation-reporter](file:///c:/Users/MINH/vinai/Build%20phase/README.md) — Pipeline Tự Động Hóa Báo Cáo Gán Nhãn Dữ Liệu (CVAT & GitHub Sync)
* **Người chủ trì đánh giá**: **Đinh Công Minh** (Project Lead & BI Architect)
* **Đối tượng nghiệm thu**: Repository prototype [`DuyWebdev/mentor-report-integration-demo`](https://github.com/DuyWebdev/mentor-report-integration-demo) do **Vũ Trường Duy** (Data Integration Engineer) xây dựng.
* **Thời điểm nghiệm thu**: 10/10/2026
* **Trạng thái**:  **APPROVED & INTEGRATED (Đã nghiệm thu và tích hợp thành công vào nhánh main)**

---

## 🎯 I. MỤC TIÊU & BỐI CẢNH ĐÁNH GIÁ

Nhằm phục vụ Sprint Tuần 2 về việc hoàn thiện Tầng Thu Thập & Tích Hợp Dữ Liệu (Data Ingestion Layer), Project Lead Đinh Công Minh đã tiến hành rà soát chéo (Peer Review & Architecture Inspection) toàn bộ mã nguồn tại repository demo của thành viên Vũ Trường Duy (`DuyWebdev`).

### Yêu cầu ban đầu (theo Kế hoạch WBS 1.3):
1. Kết nối GitHub REST API v3 trích xuất danh sách Issues thảo luận kỹ thuật có gắn nhãn `ca-kho`, `mentor-question`, `blocker`.
2. Đối soát chéo giữa GitHub Issue và CVAT Job/Task để loại bỏ các ca khó rác hoặc tham chiếu nhầm task.
3. Tạo sinh đường dẫn Deep Link chuẩn trỏ trực tiếp tới giao diện CVAT.

---

## 📊 II. ĐÁNH GIÁ KỸ THUẬT SẢN PHẨM CỦA DUY (PROS & CONS)

### 1. Điểm mạnh nổi bật (Strengths)
* **Tư duy Quản trị Dữ liệu (Data Governance)**: Xây dựng cơ chế snapshot bất biến lưu tại `data/raw/<timestamp>/` kèm file metadata `manifest.json`. Phân định rõ ràng giữa `null` (chưa có) và `0` (số đếm thực tế), `unavailable` (nguồn lỗi) và rỗng.
* **Độ ổn định & Khả năng phục hồi (Resilience)**: Client HTTP cấu hình `requests.Session` với `urllib3.util.retry.Retry` (backoff factor = 1, tự động thử lại khi gặp mã lỗi 429, 500, 502, 503, 504).
* **An toàn & Bảo mật (Security)**: Kiểm tra cấu trúc URL phân trang chống tấn công SSRF / Open Redirect; loại bỏ hoàn toàn Token/Credentials khi log lỗi.
* **Kiểm định liên kết chéo (Cross-System Verification)**: Module `verify_link.py` giải quyết xuất sắc việc phân loại trạng thái liên kết (`verified`, `mismatch`, `unlinked`, `invalid_reference`, `verification_failed`).
* **Tài liệu & Unit Tests bài bản**: Soạn thảo tài liệu bàn giao `TomTat.md` và `DATA_CONTRACT.md` cực kỳ chi tiết, kèm bộ 5 file unit test mô phỏng các ca biên.

### 2. Các điểm hạn chế & Điểm lệch kiến trúc so với dự án chính
* **Deep Link chưa hỗ trợ cấp Frame**: Mã nguồn của Duy mới chỉ dừng ở mức link Job (`.../tasks/{task_id}/jobs/{job_id}`). Trường `frame` bị gán cứng `None`, chưa đạt tiêu chuẩn trỏ trực tiếp tới khung hình lỗi (`?frame={idx}`) theo đặc tả [CVAT_INTEGRATION_GUIDE.md](file:///c:/Users/MINH/vinai/Build%20phase/docs/03-integrations/CVAT_INTEGRATION_GUIDE.md).
* **Cấu trúc thư mục độc lập**: Mã nguồn demo đặt phẳng ở thư mục gốc (`src/collect.py`, `src/sync.py`, `src/verify_link.py`), chưa khớp cấu trúc phân tầng của dự án chính (`src/extractors/`, `src/processors/`, `src/generators/`).
* **Chồng lấn phân công công việc**: Duy tự viết thêm phần CVAT API (vốn thuộc WBS của Tú) và Markdown render (thuộc WBS của Ngọc/Tuân).

---

## 🛠️ III. CHI TIẾT CÔNG VIỆC TÁI CẤU TRÚC & TÍCH HỢP ĐÃ THỰC HIỆN

Project Lead đã trực tiếp triển khai quy trình **Tái cấu trúc và Tích hợp có chọn lọc (Selective Refactor & Modular Integration)**:

### 1. Chuẩn hóa cấu trúc thư mục quy chuẩn (`src/`)
* [`src/extractors/base_client.py`](file:///c:/Users/MINH/vinai/Build%20phase/src/extractors/base_client.py): Trích xuất lớp `BaseClient` chuẩn hóa cho cả dự án, hỗ trợ retry backoff, connection pooling, phân trang an toàn cho cả CVAT và GitHub.
* [`src/extractors/cvat_extractor.py`](file:///c:/Users/MINH/vinai/Build%20phase/src/extractors/cvat_extractor.py): Module trích xuất toàn diện CVAT Tasks, Jobs, Labels, Annotations summary (shapes, tracks, tags) và Quality Reports.
* [`src/extractors/github_extractor.py`](file:///c:/Users/MINH/vinai/Build%20phase/src/extractors/github_extractor.py): Module trích xuất GitHub Issues, Labels, Comments và đối soát liên kết task/job.
* [`src/processors/normalizer.py`](file:///c:/Users/MINH/vinai/Build%20phase/src/processors/normalizer.py): Động cơ chuẩn hóa dữ liệu thành `report_data.json` theo đúng Data Contract v1.
* [`src/generators/markdown_generator.py`](file:///c:/Users/MINH/vinai/Build%20phase/src/generators/markdown_generator.py): Động cơ render bản thảo báo cáo 4 mục chuẩn (`MENTOR_REPORT_DRAFT.md`), chuyển đổi múi giờ sang Việt Nam (UTC+7).
* [`src/sync.py`](file:///c:/Users/MINH/vinai/Build%20phase/src/sync.py): CLI Runner điều phối toàn bộ pipeline, hỗ trợ cả 2 chế độ:
  * **Online Mode**: Gọi trực tiếp API CVAT và GitHub theo lịch Cron.
  * **Offline Mode (`--offline`)**: Replay dữ liệu snapshot mẫu để kiểm thử và demo tức thì mà không cần mạng.

### 2. Nâng cấp bộ phân giải Frame Index & Deep Link
* Bổ sung parser Regex linh hoạt nhận diện:
  * `Frame index (nếu có): 142`
  * `Frame index: 142`
  * `Frame ID: 142`
  * `Khung hình: 142`
* Tự động tạo URL Deep Link chuẩn frame-level:
  ```text
  https://<cvat-host>/tasks/{task_id}/jobs/{job_id}?frame={frame_idx}
  ```
* Báo cáo Markdown hiển thị rõ ràng:  
  `🎯 [🔗 Mở trực tiếp Frame 142 trên CVAT](...)`

### 3. Đưa GitHub Issue Templates vào dự án
* Đã cấu hình và đưa 2 templates vào `.github/ISSUE_TEMPLATE/`:
  * [`edge-case.yml`](file:///c:/Users/MINH/vinai/Build%20phase/.github/ISSUE_TEMPLATE/edge-case.yml): Báo ca khó có sẵn các dòng nhập ID và `Frame index (nếu có):`.
  * [`mentor-question.yml`](file:///c:/Users/MINH/vinai/Build%20phase/.github/ISSUE_TEMPLATE/mentor-question.yml): Câu hỏi định hướng gửi Mentor.

---

## 🧪 IV. KẾT QUẢ KIỂM THỬ NGHIỆM THU

### 1. Kiểm thử Unit Test (`pytest tests/`)
Đã xây dựng bộ 17 test cases bao quát toàn bộ logic hệ thống:
* `tests/test_base_client.py`: 3 tests (Init headers, SSRF redirect rejection, Pagination loop safety).
* `tests/test_cvat_extractor.py`: 4 tests (Deep link format, Annotations summary success/partial/unavailable).
* `tests/test_github_extractor.py`: 5 tests (Frame parsing regex, ambiguous IDs, issue link verification).
* `tests/test_normalizer.py`: 3 tests (Other task filtering, Ground Truth exclusion, Frame query parameter).
* `tests/test_report_generator.py`: 2 tests (4 sections render, Vietnam time UTC+7 conversion).

👉 **Kết quả**: **17/17 tests PASS 100% trong 0.14 giây.**

### 2. Kiểm thử chạy toàn trình (End-to-End Pipeline)
Chạy thử nghiệm lệnh:
```powershell
.\.venv\Scripts\python.exe src/sync.py --offline sample_data/ --session "Phiên Mentor Thử Nghiệm"
```
* Pipeline chạy trơn tru không lỗi.
* Sinh thành công `sample_data/report_data.json` và bản thảo `sample_data/MENTOR_REPORT_DRAFT.md`.
* Deep Link tới Frame 142 trên CVAT hoạt động chuẩn xác theo đúng nghiệp vụ.

---

## 📋 V. KẾ HOẠCH BÀN GIAO TIẾP THEO

1. **Bàn giao cho Nguyễn Minh Tú (Data Integration Eng - CVAT)**:
   * Tái sử dụng lớp `BaseClient` và `CVATExtractor` để hoàn thiện module trích xuất chuyên sâu của CVAT.
2. **Bàn giao cho Phạm Nguyễn Tuân (Analytics & ETL Eng)**:
   * Sử dụng file `report_data.json` và raw JSON snapshot từ pipeline làm đầu vào chính thức để viết các module tính chỉ số Vận tốc, Chất lượng và xuất bộ file CSV nạp vào Power BI.
3. **Bàn giao cho Ngô Duy Ngọc (DevOps & Automation Eng)**:
   * Tích hợp lệnh `python src/sync.py` vào GitHub Actions Workflow (`scheduled_report.yml`) và kết nối Bot Telegram thông báo trước phiên họp.
