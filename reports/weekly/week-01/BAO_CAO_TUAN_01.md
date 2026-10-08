# 📊 BÁO CÁO TIẾN ĐỘ TUẦN 1 (WEEK 1 PROGRESS REPORT)

> **Dự án**: Auto Annotation Report Pipeline (CVAT & GitHub Sync - Power BI Hybrid)  
> **Giai đoạn**: Tuần 1 — Khảo sát Nghiệp vụ, Kiến trúc Hệ thống & Prototype  
> **Người lập báo cáo**: Đinh Công Minh (Project Lead)  
> **Ngày báo cáo**: 08/10/2026

---

## 📌 I. CÔNG VIỆC ĐÃ HOÀN THÀNH (COMPLETED TASKS)

Trong Tuần 1, toàn đội đã hoàn thành xuất sắc các mục tiêu nền tảng về nghiệp vụ, kiến trúc và kết nối kỹ thuật:

### 1. Về mặt Nghiệp vụ & Quản lý Dự án (Đinh Công Minh chủ trì)
* ✅ **Hoàn thiện Bộ Tài liệu Kỹ thuật Dự án (`PROJECT_ANALYTICS_SPEC.md`)**:
  * Xây dựng Mindmap phân rã 4 trụ cột nghiệp vụ gán nhãn: Tiến độ, Chất lượng (Ground Truth vs Reviewer), Hình học dữ liệu, Phân khúc nhân sự.
  * Thiết lập mô hình dữ liệu **Star Schema** cho Power BI gồm 4 bảng Fact và 4 bảng Dimension.
  * Hoàn thành **Data Dictionary** chi tiết cho 9 bảng dữ liệu (mô tả, kiểu dữ liệu, khóa chính/ngoại, nguồn trích xuất API).
  * Xây dựng danh mục **20 Measures DAX** chuẩn xác phục vụ trực quan hóa các chỉ số hiệu năng và chất lượng.
  * Đặc tả chi tiết giao diện và mục tiêu phân tích của **5 Trang Báo Cáo Power BI**.
* ✅ **Hoàn thiện Kế hoạch Quản lý Dự án (`PROJECT_MANAGEMENT_PLAN.md`)**:
  * Phân công nhiệm vụ chi tiết (WBS), ma trận trách nhiệm RACI cho cả 5 thành viên.
  * Thiết lập quy tắc hợp đồng dữ liệu (Data Contract), chiến lược phân nhánh Git (Git Flow) và tiêu chuẩn nghiệm thu của Lead.

### 2. Về mặt Tích hợp Dữ liệu & API (Nguyễn Minh Tú & Vũ Trường Duy)
* ✅ **Kết nối thành công CVAT REST API v2**:
  * Thực hiện xác thực thành công qua Personal Access Token (PAT) và phân quyền tổ chức (Organization).
  * Gọi thành công các endpoint trích xuất: Danh sách Task (`/api/tasks`), danh sách Jobs (`/api/jobs`), và phân bổ nhân sự (`assignee`).
  * Xây dựng cơ chế vượt phân trang (Pagination handling) đảm bảo không sót dữ liệu khi task có hàng trăm jobs.
* ✅ **Kết nối GitHub REST API v3 & CVAT Quality**:
  * Trích xuất danh sách Issues trên GitHub có gắn nhãn `ca-kho` và `blocker`.
  * Khảo sát endpoint `/api/quality/reports` trên CVAT để lấy dữ liệu đối soát chất lượng.
  * Xây dựng thuật toán sinh URL **Deep Link CVAT** tự động trỏ thẳng tới từng frame hình.

### 3. Về mặt Tính toán Chỉ số & ETL (Phạm Nguyễn Tuân)
* ✅ **Nghiên cứu & Prototype thuật toán tính toán**:
  * Xây dựng công thức tính Vận tốc (Frames/giờ, Objects/giờ) và thời gian xử lý trung bình (AHT per Frame).
  * Nghiên cứu thuật toán Shoelace (Gauss's area formula) tính toán diện tích hình học đa giác (Polygon).
  * Xây dựng quy chuẩn phân loại kích thước vật thể theo chuẩn quốc tế COCO Scale (`Small`, `Medium`, `Large`).
  * Phác thảo cấu trúc 4 bảng CSV đầu ra phục vụ nạp vào Power BI: `batch_progress.csv`, `qa_metrics.csv`, `annotator_segments.csv`, `edge_cases.csv`.

### 4. Về mặt Tự động hóa & Hạ tầng (Ngô Duy Ngọc)
* ✅ **Thiết lập Repository & Luồng CI/CD ban đầu**:
  * Khởi tạo khung repository, file cấu hình `.gitignore`, `.env.example`, `requirements.txt`.
  * Viết khung file GitHub Actions Workflow (`workflows/scheduled_report.yml`) hỗ trợ chạy kích hoạt tự động theo lịch Cron và chạy thủ công qua `workflow_dispatch`.
  * Tạo thành công Telegram Bot thử nghiệm và kiểm thử gửi tin nhắn văn bản thông báo qua Webhook.

---

## ⚠️ II. CÔNG VIỆC CHƯA HOÀN THÀNH & NGUYÊN NHÂN (PENDING TASKS & ROOT CAUSE)

| Công Việc Chưa Hoàn Thành | Mức Độ | Người Phụ Trách | Nguyên Nhân Gốc Rễ (Root Cause) | Giải Pháp Khắc Phục (Action Plan) |
| :--- | :---: | :---: | :--- | :--- |
| **1. Parse toàn diện mảng tọa độ Polygon phức tạp** | Vừa | Nguyễn Minh Tú & Phạm Nguyễn Tuân | Tọa độ Polygon trên CVAT trả về dạng mảng 1 chiều phẳng `[x1, y1, x2, y2, x3, y3...]` thay vì danh sách cặp điểm `[[x, y], ...]`. Khi gặp đa giác có hàng trăm đỉnh hoặc đối tượng bị che khuất (Occluded), việc phân tách bị chậm. | **Giải pháp**: Tuân viết một hàm tiền xử lý dùng thư viện `numpy` để định hình lại mảng thành ma trận $N \times 2$ trước khi đưa vào công thức Shoelace. Sẽ hoàn thành vào Thứ Bảy tuần này. |
| **2. Kiểm thử thực tế endpoint Ground Truth của CVAT** | Thấp | Vũ Trường Duy | Instance CVAT thử nghiệm hiện tại chưa gắn sẵn "Ground Truth Job" đối chứng trên task mẫu, dẫn đến endpoint `/api/quality/reports` trả về rỗng. | **Giải pháp**: Chuyển hướng ưu tiên kiểm thử nhánh **Đánh giá chất lượng qua Reviewer (Rejection count & Issues)** trước, đồng thời đề nghị tạo 1 Job chuẩn 50 frames để test lại endpoint GT vào đầu tuần 2. |
| **3. Tích hợp tự động Git Commit trong GitHub Actions** | Vừa | Ngô Duy Ngọc | Workflow GitHub Actions gặp lỗi quyền ghi (`403 Permission Denied`) khi cố gắng tự động commit đè các file CSV mới sinh ra ngược trở lại repo. | **Giải pháp**: Cần cấp quyền `permissions: contents: write` trong file `scheduled_report.yml` và sử dụng `GITHUB_TOKEN` có quyền ghi. Ngọc sẽ cập nhật và test lại trong Thứ Sáu. |

---

## 💡 III. CÁC ĐIỂM CẢI TIẾN TRONG SẢN PHẨM (PRODUCT IMPROVEMENTS)

Trong quá trình khảo sát nghiệp vụ thực tế tại Tuần 1, nhóm đã chủ động đưa ra **3 cải tiến quan trọng** so với ý tưởng ban đầu:

### 🌟 CẢI TIẾN 1: Bổ sung Cơ chế Đánh giá Chất lượng Kép (Dual Quality Evaluation Framework)
* **Nội dung cải tiến**: 
  * Thay vì chỉ hỗ trợ đánh giá chất lượng qua việc so sánh với Ground Truth (đo IoU/F1), hệ thống bổ sung thêm nhánh **Đánh giá chất lượng qua Quy trình Kiểm định (Reviewer Audit)**.
  * Chỉ số bổ sung: Số lần job bị trả về sửa lỗi (`rejection_count`), Tỷ lệ hoàn thành ngay lần đầu (`First-Time Pass Rate - FTPR`), Mật độ lỗi trên 100 frame (`Defect Density`), và phân loại ma trận 4 nhóm lỗi phổ biến.
* **Lý do thực hiện**:
  * Trong các dự án gán nhãn thực tế quy mô lớn, **hơn 90% số task không có sẵn tập Ground Truth** (do tốn chi phí và thời gian tạo nhãn chuẩn trước).
  * Nếu hệ thống chỉ phụ thuộc vào Ground Truth, phần lớn các task và thành viên sẽ không có điểm số chất lượng.
* **Căn cứ kỹ thuật & thực tế nghiệp vụ**:
  * *Căn cứ thực tế*: Mọi quy trình gán nhãn chuẩn công nghiệp đều có khâu QA/Reviewer kiểm tra trước khi bàn giao. Khi một job không đạt, Reviewer sẽ chuyển trạng thái từ `validation` về lại `annotation` kèm ghi chú lỗi.
  * *Căn cứ kỹ thuật*: CVAT lưu trữ đầy đủ lịch sử trạng thái của job và hỗ trợ tạo issue gắn kèm tọa độ và comment lỗi (`/api/issues`). Việc khai thác dữ liệu này giúp theo dõi chất lượng tức thời mà không tốn công gán nhãn chuẩn trước.

---

### 🌟 CẢI TIẾN 2: Chuẩn hóa Đo lường Độ khó Dữ liệu theo COCO Scale & Diện tích Đa giác (Shoelace Formula)
* **Nội dung cải tiến**:
  * Tích hợp công thức Shoelace để tính diện tích thực tế của Bounding Box và Polygon ($px^2$ và tỷ lệ % diện tích frame).
  * Tự động gắn thẻ phân loại kích thước đối tượng theo tiêu chuẩn quốc tế COCO:
    * `Small`: Diện tích $< 32^2 = 1024\text{ px}^2$.
    * `Medium`: Diện tích từ $1024\text{ px}^2 \to 9216\text{ px}^2$.
    * `Large`: Diện tích $> 96^2 = 9216\text{ px}^2$.
* **Lý do thực hiện**:
  * Tránh việc đánh giá phiến diện, thiếu công bằng đối với năng suất của người gán nhãn.
* **Căn cứ kỹ thuật & thực tế nghiệp vụ**:
  * *Căn cứ kỹ thuật*: Một bức ảnh chứa 20 vật thể siêu nhỏ (như xe máy ở xa) hoặc đa giác uốn lượn phức tạp đòi hỏi thời gian căn chỉnh gấp 5-10 lần so với bức ảnh chỉ có 1 chiếc xe tải to choán hết màn hình.
  * *Căn cứ nghiệp vụ*: Bằng cách đưa tỷ lệ `% Vật thể nhỏ (Small %)` vào báo cáo, Leader và Mentor có cơ sở khoa học để hiểu tại sao một số batch có vận tốc gán nhãn chậm hơn bình thường, từ đó phân bổ khối lượng công việc công bằng và chuẩn xác.

---

### 🌟 CẢI TIẾN 3: Tích hợp Deep Link Trực Tiếp tới từng Frame CVAT trên Báo Cáo & Power BI
* **Nội dung cải tiến**:
  * Toàn bộ danh sách ca khó (Edge Cases) và danh sách lỗi nghiêm trọng (Blocker Defects) đều được hệ thống tự động sinh trường `cvat_deep_link` theo quy tắc:
    $$\text{URL} = \text{CVAT\_HOST} + \text{/tasks/\{task\_id\}/jobs/\{job\_id\}?frame=\{frame\_idx\}}$$
  * Cột này được định dạng kiểu `Web URL` trong Power BI.
* **Lý do thực hiện**:
  * Xóa bỏ hoàn toàn "Điểm mù" (Blind Spots) và rút ngắn thời gian chuẩn bị họp giữa Leader và Mentor từ 2-4 giờ xuống còn vài giây.
* **Căn cứ kỹ thuật & thực tế nghiệp vụ**:
  * *Căn cứ kỹ thuật*: CVAT Web Frontend hỗ trợ tham số query `?frame={index}` trong URL để tua thẳng đến frame tương ứng.
  * *Căn cứ nghiệp vụ*: Trong các phiên Mentor, thay vì phải mở CVAT, tìm Task, tìm Job rồi lướt từng frame để tìm chỗ gây tranh cãi, Mentor và Leader chỉ cần **nhấp chuột 1 lần trực tiếp trên Power BI** là giao diện gán nhãn tự động mở ra đúng khung hình đó để giải quyết ngay lập tức.

---

## 📈 IV. ĐÁNH GIÁ CHUNG & KẾ HOẠCH TUẦN 2 (HƯỚNG TỚI MVP)

### 1. Đánh giá chung Tuần 1
* **Tiến độ tổng thể**: Đạt **95%** kế hoạch đề ra cho Tuần 1.
* **Tình trạng phối hợp**: Nhóm giao tiếp hiệu quả, phân vai rõ ràng, tài liệu đặc tả chuẩn chỉ và không có xung đột kỹ thuật lớn.
* **Độ sẵn sàng**: Đã sẵn sàng bước vào giai đoạn tăng tốc hoàn thiện MVP.

### 2. Kế hoạch trọng tâm Tuần 2 (Hạn chót Thứ Năm: 15/10/2026)
* **Thứ 6 - Thứ 7**: Hoàn thiện toàn bộ code extractor API (Tú, Duy) và script tính toán ETL xuất 4 file CSV (Tuân).
* **Chủ Nhật - Thứ 2**: Thiết kế hoàn chỉnh 3 trang cốt lõi Power BI MVP và tích hợp Bot Notifier (Minh, Ngọc).
* **Thứ 3**: Kết nối toàn trình End-to-End từ GitHub Actions $\to$ CSV $\to$ Power BI $\to$ Telegram Bot.
* **Thứ 4**: Họp tổng duyệt nội bộ (Internal Dry Run) và chuẩn bị kịch bản UAT.
* **Thứ 5 (15/10/2026)**: **Bảo vệ và nghiệm thu chính thức sản phẩm MVP cùng Mentor!**
