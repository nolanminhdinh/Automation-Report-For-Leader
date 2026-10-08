# 📋 Đặc Tả Khung Báo Cáo: Mentor & Leader Report Spec

Tài liệu này quy chuẩn cấu trúc, định dạng và các chỉ số đo lường của bản báo cáo tự động **4 mục** chuẩn mực (`MENTOR_REPORT_DRAFT.md`) được sinh ra bởi hệ thống.

---

## 🎯 Mục đích của bản báo cáo 4 mục

Bản báo cáo được thiết kế tối ưu hóa cho các phiên họp định kỳ (Weekly Sync / Milestone Review) giữa Nhóm trưởng (Team Lead) và Mentor / Project Sponsor.
* **Thời gian đọc tối ưu**: Dưới **3 phút** để nắm toàn bộ bức tranh dự án.
* **Tập trung vào tính hành động (Actionable)**: Không chỉ liệt kê số liệu mà chỉ rõ các điểm nghẽn (bottlenecks) và quyết định cần Mentor tháo gỡ.

---

## 📑 Cấu trúc chi tiết 4 Mục chuẩn

### MỤC 1: TIẾN ĐỘ BATCH & KPI (BATCH PROGRESS & VELOCITY)

#### 1.1. Nội dung cần thể hiện:
* **Mã đợt gán nhãn (Batch/Task ID)** & Tổng số lượng khung hình (Frames / Images).
* **Tỷ lệ hoàn thành (% Completed)** so với kế hoạch mốc thời gian (Deadline).
* **Vận tốc thực tế (Velocity)** của toàn đội và phân bổ theo từng nhân sự.
* **Dự báo ngày về đích (Projected Completion Date)**:
  $$\text{Số ngày còn lại} = \frac{\text{Backlog Frames}}{\text{Velocity Trung bình ngày}}$$

#### 1.2. Mẫu bảng biểu quy chuẩn:

| Nhân sự (Assignee) | Số Job nhận | Frames hoàn thành | % Đạt | Vận tốc (Frames/h) | Trạng thái |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Nguyen Van A | 4 | 850 / 850 | 100% | 45 |  Đúng hạn |
| Tran Thi B | 4 | 720 / 850 | 84.7% | 38 |  Đang gán |
| Le Van C | 3 | 510 / 850 | 60.0% | 27 | ⚠️ Chậm tiến độ |
| **Tổng cộng** | **11** | **2,080 / 2,550** | **81.6%** | **36.7 (Avg)** | **ON TRACK** |

---

### MỤC 2: CHẤT LƯỢNG & ĐIỂM QA/QC (QUALITY CONTROL METRICS)

#### 2.1. Nội dung cần thể hiện:
* **Tỷ lệ duyệt lần 1 (First-time Pass Rate)**: Phần trăm Job được Reviewer chấp thuận ngay trong lần thẩm định đầu tiên.
* **Điểm QA trung bình (QA Score)**: Dựa trên báo cáo kiểm thử ngẫu nhiên (Audit) của CVAT hoặc Reviewer chấm.
* **Top 3 - 5 lỗi phổ biến nhất**: Phân loại theo taxonomy lỗi gán nhãn.

#### 2.2. Phân loại lỗi chuẩn (Error Taxonomy):
1. `BOX_LOOSE`: Bounding box quá lỏng hoặc ôm thừa nền quá 10%.
2. `BOX_TIGHT_CLIPPED`: Bounding box cắt lẹm vào chi tiết đối tượng.
3. `MISLABELED`: Gán nhầm nhãn (ví dụ: `car` nhầm thành `truck`, `sedan` nhầm thành `suv`).
4. `MISSED_OBJECT`: Bỏ sót đối tượng trong khung hình (đặc biệt là đối tượng xa, nhỏ, bị che khuất).
5. `ATTRIBUTE_ERROR`: Sai thuộc tính đi kèm (ví dụ: `occluded`, `truncated`, `charging_state`).

#### 2.3. Bảng phân bố lỗi quy chuẩn:

```text
Tổng số lỗi ghi nhận trong kỳ: 48 lỗi
- Bỏ sót đối tượng nhỏ (Missed Small Object): 22 lỗi (45.8%)  [Cần nhắc nhở zoom kỹ]
- Bounding box cắt lẹm (Box Tight/Clipped):  14 lỗi (29.2%)
- Gán nhầm phân lớp xe (Mislabeled):         8 lỗi (16.7%)
- Sai trạng thái cổng sạc (Attribute):       4 lỗi (8.3%)
```

---

### MỤC 3: DANH SÁCH CA KHÓ KÈM DEEP LINK (EDGE CASES & DISPUTES)

Đây là mục quan trọng nhất để Mentor can thiệp trực tiếp mà không cần mở CVAT mò mẫm từng task.

#### 3.1. Yêu cầu bắt buộc:
* Phải có **Deep Link trực tiếp** tới đúng số Frame trong Job CVAT.
* Có ảnh minh họa (Crop ảnh hoặc frame ID cụ thể).
* Mô tả ngắn gọn xung đột giữa các annotators hoặc điểm bất thường của ảnh thực tế.
* Đề xuất phương án của đội kỹ thuật (Option A vs Option B).

#### 3.2. Mẫu bảng biểu quy chuẩn:

| STT | Frame ID | Phân loại ca khó | Mô tả vấn đề | Đề xuất của Team | Deep Link CVAT |
| :---: | :---: | :--- | :--- | :--- | :---: |
| 1 | `#142` (Job 1719) | Cáp vắt qua nóc xe | Dây cáp trụ sạc kéo căng vắt qua nóc ô tô bên cạnh để sạc cho xe thứ 2 | Coi xe 2 là `charging`, xe 1 là `blocked` | [🔗 Mở Frame 142](https://cvat.domain.com/tasks/217/jobs/1719?frame=142) |
| 2 | `#205` (Job 1720) | Xe bị che khuất >70% | Xe tải dừng chắn camera, chỉ thấy 1 góc bánh xe điện ở ô sạc | Kích hoạt quy tắc `Abstain` (không đoán) | [🔗 Mở Frame 205](https://cvat.domain.com/tasks/217/jobs/1720?frame=205) |
| 3 | `#389` (Job 1722) | Đèn LED phản chiếu | Ban đêm đèn đường phản chiếu làm dải LED trụ sạc bị đổi màu xanh giả | Cần thống nhất quy tắc kiểm tra temporal 3 frame | [🔗 Mở Frame 389](https://cvat.domain.com/tasks/217/jobs/1722?frame=389) |

---

### MỤC 4: CÂU HỎI MỞ & VẤN ĐỀ CẦN MENTOR GỠ RỐI (OPEN QUESTIONS & MENTOR CONSULTATION)

#### 4.1. Nội dung cần thể hiện:
* Các câu hỏi vượt thẩm quyền của Lead, liên quan đến thay đổi **Annotation Guideline**, cấu trúc bài toán hoặc tài nguyên dự án.
* Mỗi câu hỏi được liên kết trực tiếp với GitHub Issue tương ứng.
* Trình bày dưới định dạng cấu trúc câu hỏi có kèm phương án lựa chọn:

#### 4.2. Mẫu trình bày chuẩn:

> **Câu hỏi 1 (Guideline Issue #42)**: Với các loại xe máy điện / xe đạp điện vào đỗ chiếm ô sạc của ô tô, nhóm nên gán lớp riêng `two_wheeler_blocking` hay gộp chung vào lớp `obstacle`?
> * **Tác động**: Nếu tạo thêm lớp mới sẽ cần cập nhật lại taxonomy và bổ sung khoảng 500 ảnh mẫu huấn luyện.
> * **Đề xuất của nhóm**: Tạm thời gộp vào `obstacle` cho phiên bản v1.0, tách lớp ở v1.1.
> * 🔗 *GitHub Issue thảo luận*: [#42 - Guideline update for two-wheelers](https://github.com/org/repo/issues/42)

> **Câu hỏi 2 (Hạ tầng / Data Ingestion)**: Nguồn camera trạm sạc tại khu vực Zone 3 đang bị nhiễu sọc ngang sau 18h tối. Mentor có đề xuất thuật toán lọc khử nhiễu tự động trước khi đẩy lên CVAT hay loại bỏ hoàn toàn các khung hình này?
> * 🔗 *GitHub Issue thảo luận*: [#45 - Noise filtering for night cameras](https://github.com/org/repo/issues/45)
