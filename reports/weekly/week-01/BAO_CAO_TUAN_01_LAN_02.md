# 📊 BÁO CÁO TIẾN ĐỘ TUẦN 1 — LẦN 2 (WEEK 1 PROGRESS REPORT - SESSION 2)

> **Dự án**: Auto Annotation Report Pipeline (CVAT & GitHub Sync - Power BI Hybrid)  
> **Giai đoạn**: Tuần 1 — Khảo sát Nghiệp vụ, Kiến trúc Hệ thống & Tích hợp Prototype Ingestion  
> **Phiên báo cáo**: Phiên 2 — Tối Chủ Nhật (11/10/2026)  
> **Người lập báo cáo**: Đinh Công Minh (Project Lead & BI Architect)  
> **Ngày phê duyệt**: 11/10/2026  

---

## 📌 I. CÔNG VIỆC ĐÃ HOÀN THÀNH (COMPLETED TASKS)

Trong giai đoạn nửa cuối Tuần 1 (từ Thứ Sáu đến Chủ Nhật), sau phiên báo cáo Lần 1 (Tối Thứ Năm), toàn đội đã tập trung nghiệm thu, kiểm thử chéo và tích hợp thành công module **Data Ingestion & Verification Pipeline** vào nhánh chính (`main`) của repository:

### 1. Về mặt Quản lý Dự án & Nghiệm thu Kỹ thuật (Đinh Công Minh)
* ✅ **Review & Nghiệm thu chéo mã nguồn của Vũ Trường Duy**:
  * Đánh giá toàn diện repository prototype [`DuyWebdev/mentor-report-integration-demo`](https://github.com/DuyWebdev/mentor-report-integration-demo).
  * Ban hành biên bản nghiệm thu kỹ thuật chính thức: [`reports/NGHIEM_THU_VA_TICH_HOP_API_INGESTION.md`](../NGHIEM_THU_VA_TICH_HOP_API_INGESTION.md).
* ✅ **Trực tiếp Tái cấu trúc & Hợp nhất Kiến trúc (Architecture Consolidation)**:
  * Quy hoạch cấu trúc thư mục quy chuẩn `src/` gồm 3 tầng rõ ràng:
    * `src/extractors/`: Thu thập API đa nguồn (CVAT & GitHub).
    * `src/processors/`: Chuẩn hóa dữ liệu theo Data Contract v1 (`report_data.json`).
    * `src/generators/`: Động cơ kết xuất báo cáo Markdown 4 mục (`MENTOR_REPORT_DRAFT.md`).
  * Nâng cấp logic Deep Link lên cấp Frame (`?frame={idx}`), thỏa mãn 100% tiêu chí đặc tả trong `CVAT_INTEGRATION_GUIDE.md`.
  * Viết bộ kiểm thử tự động **17 Unit Tests** với tỷ lệ pass **100%**.

### 2. Về mặt Tích hợp Dữ liệu & API (Nguyễn Minh Tú & Vũ Trường Duy)
* ✅ **Xây dựng Base HTTP Client hoàn chỉnh (`src/extractors/base_client.py`)**:
  * Tích hợp cơ chế tự động thử lại (Retry) với exponential backoff trên các lỗi HTTP 429/500/502/503/504.
  * Tự động duyệt phân trang an toàn, ngăn chặn vòng lặp URL vô tận (Safe pagination traversal).
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
  * Tự động loại bỏ các issue thử nghiệm (`[API test]`) và các issue trỏ nhầm sang task khác.
* ✅ **Hoàn thiện Markdown Generator (`src/generators/markdown_generator.py`)**:
  * Tự động sinh bản thảo báo cáo chuẩn 4 phần `MENTOR_REPORT_DRAFT.md`.
  * Tự động chuyển đổi múi giờ sang giờ Việt Nam (UTC+7).

### 4. Về mặt Tự động hóa & DevOps (Ngô Duy Ngọc)
* ✅ **Triển khai GitHub Issue Templates**:
  * Tạo 2 templates `.github/ISSUE_TEMPLATE/edge-case.yml` và `mentor-question.yml` để chuẩn hóa dữ liệu đầu vào từ đội ngũ annotators.
* ✅ **Chuẩn hóa script điều phối (`src/sync.py`)**:
  * Hỗ trợ chạy cả 2 chế độ: Online Live Sync và Offline Snapshot Replay.

---

## ⚠️ II. CÔNG VIỆC CHƯA HOÀN THÀNH & NGUYÊN NHÂN (PENDING TASKS & ROOT CAUSE)

| Công Việc Chưa Hoàn Thành | Mức Độ | Người Phụ Trách | Nguyên Nhân Gốc Rễ (Root Cause) | Giải Pháp Khắc Phục (Action Plan) |
| :--- | :---: | :---: | :--- | :--- |
| **1. Tính toán điểm QA tự động từ Ground Truth API** | Thấp | Vũ Trường Duy & Đinh Công Minh | Instance CVAT thử nghiệm của nhóm chưa gắn sẵn Job Ground Truth mẫu, dẫn đến endpoint `/api/quality/reports` trả về rỗng. | Duy trì cơ chế trả về `scores.status = "unavailable"` kèm lý do rõ ràng. Trong Tuần 2 sẽ tạo 1 Ground Truth Job mẫu trên CVAT và ưu tiên nhánh đánh giá qua Reviewer do Tuân phụ trách. |
| **2. Tích hợp trích xuất CSV trực tiếp cho Power BI** | Vừa | Phạm Nguyễn Tuân | Phạm vi Tuần 1 tập trung hoàn thiện tầng Ingestion & Data Contract `report_data.json`. Các bảng CSV quan hệ thuộc về nhiệm vụ của tầng ETL. | Tuân tiếp nhận `report_data.json` và raw snapshot từ Duy để hoàn thiện các module tính Vận tốc, QA và xuất 4 file CSV sạch vào đầu Tuần 2. |

---

## 💡 III. CÁC ĐIỂM CẢI TIẾN TRONG SẢN PHẨM (PRODUCT IMPROVEMENTS)

Trong đợt nghiệm thu và tích hợp cuối Tuần 1, nhóm đã bổ sung **2 cải tiến kỹ thuật quan trọng**:

### 🌟 CẢI TIẾN 1: Tự động Bóc tách Frame Index & Sinh Deep Link Frame-Level
* **Nội dung cải tiến**:
  * Thay vì chỉ mở chung chung vào trang chính của Job, hệ thống tự động bóc tách chỉ số Frame từ nội dung mô tả của issue trên GitHub (ví dụ: `Frame index (nếu có): 142`, `Frame: 142`, `Khung hình: 142`).
  * Đường dẫn Deep Link được tạo tự động dưới dạng:
    $$\text{URL} = \text{CVAT\_HOST} + \text{/tasks/\{task\_id\}/jobs/\{job\_id\}?frame=\{frame\_idx\}}$$
* **Lý do & Căn cứ nghiệp vụ**:
  * *Căn cứ thực tế*: Trong các job có hàng trăm hoặc hàng nghìn frames, nếu liên kết chỉ trỏ đến Job, Mentor và Leader phải mất nhiều phút dò tìm thủ công khung hình gây tranh chấp.
  * *Căn cứ kỹ thuật*: CVAT Web Frontend hỗ trợ trực tiếp query parameter `?frame={index}` để tua thẳng tới vị trí frame. Bằng cách hiển thị `🎯 [🔗 Mở trực tiếp Frame 142 trên CVAT]`, thời gian tra cứu được rút ngắn xuống chỉ còn 1 cú click chuột.

### 🌟 CẢI TIẾN 2: Cơ chế Snapshot Bất biến & Hỗ trợ Replay Offline
* **Nội dung cải tiến**:
  * Mỗi lần chạy pipeline, dữ liệu thô từ CVAT và GitHub được đóng băng thành một thư mục snapshot độc lập tại `data/raw/<timestamp>/` kèm file kiểm toán `manifest.json`.
  * Hỗ trợ cờ `--offline sample_data/` cho phép chạy và kiểm thử toàn trình pipeline offline không cần mạng hoặc token thật.
* **Lý do & Căn cứ kỹ thuật**:
  * *Căn cứ kỹ thuật*: Bảo đảm tính toàn vẹn dữ liệu (Data Lineage & Reproducibility). Số liệu báo cáo luôn có bằng chứng gốc đối chiếu.
  * *Căn cứ nghiệp vụ*: Giúp các thành viên khác trong nhóm (Tuân làm ETL, Ngọc làm DevOps, Minh làm Power BI) có thể phát triển và kiểm thử code độc lập mà không bị phụ thuộc vào tính sẵn sàng của server CVAT Cloud.

---

## 🎯 IV. KẾ HOẠCH SPRINT TUẦN 2 (WEEK 2 SPRINT PLAN)

Khép lại Tuần 1 với 100% mục tiêu Ingestion & Data Contract hoàn tất, nhóm chuyển trọng tâm sang **Sprint Tuần 2: ETL Engine & Power BI Dashboard Modeling**:

1. **Phạm Nguyễn Tuân (Analytics & ETL Eng)**:
   * Xây dựng các module xử lý chỉ số trong `src/processors/`: Vận tốc (`velocity.py`), Chất lượng (`quality.py`), Diện tích Shoelace & COCO Scale (`geometry.py`).
   * Cài đặt logic ma trận phân khúc nhân sự (Final Annotator Segmentation).
   * Xuất bộ 4 file CSV chuẩn hóa vào thư mục `data/processed/`.
2. **Đinh Công Minh (Project Lead & BI Architect)**:
   * Nạp 4 file CSV vào Power BI Desktop, thiết lập mô hình quan hệ hình sao (Star Schema).
   * Viết và kiểm thử bộ 20 công thức DAX Measures.
   * Thiết kế trực quan 5 Trang Báo Cáo trên Power BI (Executive 360, QA Deep-Dive, Annotator Matrix, Data Geometry, Edge-Cases).
3. **Nguyễn Minh Tú & Vũ Trường Duy (Data Integration Eng)**:
   * Kiểm thử tải dữ liệu trên task CVAT thực tế với số lượng frames lớn (>1,000 frames).
   * Hỗ trợ Tuân đối chiếu số liệu kiểm tra chéo (Data Reconciliation).
4. **Ngô Duy Ngọc (DevOps & Automation Eng)**:
   * Cập nhật file `.github/workflows/scheduled_report.yml` để kích hoạt định kỳ pipeline `python src/sync.py`.
   * Hoàn thiện Bot Telegram bắn thông báo tóm tắt KPI trước các buổi họp.
