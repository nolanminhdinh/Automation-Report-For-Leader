# 📊 BÁO CÁO TIẾN ĐỘ TUẦN 2 (WEEK 2 PROGRESS REPORT)

> **Dự án**: Auto Annotation Report Pipeline (CVAT & GitHub Sync - Power BI Hybrid)  
> **Giai đoạn**: Tuần 2 — Triển khai Tầng Ingestion, Hợp nhất Data Contract & Chuẩn hóa Deep Link  
> **Người lập báo cáo**: Đinh Công Minh (Project Lead)  
> **Ngày báo cáo**: 10/10/2026

---

## 📌 I. CÔNG VIỆC ĐÃ HOÀN THÀNH (COMPLETED TASKS)

Trong Tuần 2, toàn đội đã hoàn thành xuất sắc cột mốc tích hợp mã nguồn Tầng Thu Thập & Ingestion vào nhánh chính (`main`), giải quyết trọn vẹn bài toán trích xuất đa nguồn và liên kết dữ liệu:

### 1. Về mặt Quản lý Dự án & Nghiệm thu Kỹ thuật (Đinh Công Minh)
* ✅ **Review & Nghiệm thu mã nguồn của Vũ Trường Duy**:
  * Đánh giá chi tiết repository demo `mentor-report-integration-demo`.
  * Ban hành biên bản nghiệm thu kỹ thuật [reports/NGHIEM_THU_VA_TICH_HOP_API_INGESTION.md](../NGHIEM_THU_VA_TICH_HOP_API_INGESTION.md).
* ✅ **Trực tiếp Tái cấu trúc & Hợp nhất Kiến trúc (Architecture Consolidation)**:
  * Xây dựng cấu trúc thư mục quy chuẩn `src/` gồm 3 tầng rõ ràng: `src/extractors/`, `src/processors/`, `src/generators/`.
  * Nâng cấp logic Deep Link lên cấp Frame (`?frame={idx}`) đáp ứng 100% tiêu chuẩn trong `CVAT_INTEGRATION_GUIDE.md`.
  * Viết bộ kiểm thử 17 Unit Tests tự động hóa đạt tỷ lệ pass 100%.

### 2. Về mặt Tích hợp Dữ liệu & API (Nguyễn Minh Tú & Vũ Trường Duy)
* ✅ **Xây dựng Base HTTP Client hoàn chỉnh (`src/extractors/base_client.py`)**:
  * Tích hợp cơ chế thử lại (Retry) với exponential backoff trên các lỗi HTTP 429/500/502/503/504.
  * Tự động duyệt phân trang an toàn (Safe pagination loop detection).
  * Bảo mật thông tin token và bảo vệ chống tấn công SSRF / Open Redirect.
* ✅ **Hoàn thiện CVAT Extractor (`src/extractors/cvat_extractor.py`)**:
  * Trích xuất đầy đủ thông tin Task, danh sách Jobs, Class Labels, Issues và Comments.
  * Trích xuất dữ liệu Annotations thô theo từng job và hàm tính toán tóm lược (Shapes, Tracks, Tags).
  * Khảo sát và tích hợp kết nối tới endpoint Quality Reports của CVAT.
* ✅ **Hoàn thiện GitHub Extractor (`src/extractors/github_extractor.py`)**:
  * Trích xuất danh sách Issues có gắn các nhãn `ca-kho`, `mentor-question`, `blocker`, `guideline-update`.
  * Thuật toán đối soát chéo liên kết Task/Job, phân loại chi tiết 5 trạng thái liên kết (`verified`, `mismatch`, `unlinked`, `invalid_reference`, `verification_failed`).

### 3. Về mặt Xử lý Dữ liệu & Báo cáo (Phạm Nguyễn Tuân)
* ✅ **Xây dựng Data Normalizer (`src/processors/normalizer.py`)**:
  * Chuẩn hóa dữ liệu đa nguồn thành `report_data.json` theo đúng chuẩn Data Contract v1.
  * Loại bỏ các issue thử nghiệm (`[API test]`) và các issue trỏ nhầm sang task khác.
* ✅ **Hoàn thiện Markdown Generator (`src/generators/markdown_generator.py`)**:
  * Tự động sinh bản thảo báo cáo chuẩn 4 phần `MENTOR_REPORT_DRAFT.md`.
  * Tự động chuyển đổi múi giờ sang giờ Việt Nam (UTC+7).

### 4. Về mặt Tự động hóa & DevOps (Ngô Duy Ngọc)
* ✅ **Triển khai GitHub Issue Templates**:
  * Tạo 2 templates `.github/ISSUE_TEMPLATE/edge-case.yml` và `mentor-question.yml`.
* ✅ **Chuẩn hóa script điều phối (`src/sync.py`)**:
  * Hỗ trợ chạy cả 2 chế độ: Online Live Sync và Offline Snapshot Replay.

---

## ⚠️ II. CÔNG VIỆC CHƯA HOÀN THÀNH & NGUYÊN NHÂN

| Công Việc Chưa Hoàn Thành | Mức Độ | Người Phụ Trách | Nguyên Nhân Gốc Rễ | Kế Hoạch Khắc Phục |
| :--- | :---: | :---: | :--- | :--- |
| **1. Tính toán điểm QA tự động từ Ground Truth** | Thấp | Vũ Trường Duy | Instance CVAT của nhóm chưa có Job Ground Truth mẫu nên endpoint `/api/quality/reports` trả về rỗng. | Duy trì cơ chế trả về `scores.status = "unavailable"` kèm lý do rõ ràng. Tiếp tục phát triển nhánh đánh giá qua Reviewer (Tuân). |
| **2. Tích hợp trích xuất CSV trực tiếp cho Power BI** | Vừa | Phạm Nguyễn Tuân | Tuần 2 tập trung hoàn thiện tầng Ingestion & Data Contract `report_data.json`. Các file CSV sẽ được sinh ở tầng ETL tiếp theo. | Tuân sẽ hoàn thiện các module tính Vận tốc, QA và xuất 4 file CSV sạch vào đầu Tuần 3. |

---

## 💡 III. CÁC ĐIỂM CẢI TIẾN TRONG SẢN PHẨM (PRODUCT IMPROVEMENTS)

### 🌟 CẢI TIẾN 1: Tự động Bóc tách Frame Index & Sinh Deep Link Frame-Level
* **Nội dung cải tiến**:
  * Thay vì chỉ mở chung chung vào trang chính của Job, hệ thống tự động bóc tách chỉ số Frame từ nội dung mô tả của issue trên GitHub (ví dụ: `Frame index (nếu có): 142`).
  * Đường dẫn Deep Link được tạo tự động dưới dạng:
    `{CVAT_HOST}/tasks/{task_id}/jobs/{job_id}?frame={frame_idx}`
* **Lý do & Căn cứ nghiệp vụ**:
  * Giúp Mentor hoặc Leader bấm vào liên kết trong báo cáo là trình duyệt lập tức mở đúng khung hình bị tranh chấp gán nhãn, tiết kiệm 100% thời gian tìm kiếm thủ công trong các job hàng trăm frame.

### 🌟 CẢI TIẾN 2: Cơ chế Snapshot Bất biến & Hỗ trợ Replay Offline
* **Nội dung cải tiến**:
  * Mỗi lần chạy pipeline, dữ liệu thô từ CVAT và GitHub được đóng băng thành một snapshot tại `data/raw/<timestamp>/` kèm file kiểm toán `manifest.json`.
  * Hỗ trợ cờ `--offline sample_data/` cho phép chạy và kiểm thử toàn trình pipeline offline không cần kết nối mạng hoặc token thật.
* **Lý do & Căn cứ kỹ thuật**:
  * Bảo đảm tính toàn vẹn dữ liệu (Data Lineage & Reproducibility). Tránh rủi ro khi số liệu trên CVAT bị thay đổi giữa chừng trong lúc họp.

---

## 🎯 IV. KẾ HOẠCH TUẦN 3 (NEXT SPRINT OBJECTIVES)

1. **Phạm Nguyễn Tuân**: Hoàn thành module ETL (`src/processors/velocity.py`, `quality.py`, `geometry.py`) và xuất 4 file CSV sạch vào `data/processed/`.
2. **Đinh Công Minh**: Nạp dữ liệu vào Power BI Desktop, xây dựng quan hệ Star Schema và thiết kế 5 trang visual trực quan.
3. **Ngô Duy Ngọc**: Tích hợp lệnh `python src/sync.py` vào GitHub Actions Workflow định kỳ và cấu hình Bot Telegram thông báo.
