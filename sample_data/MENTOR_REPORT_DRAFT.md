# 📋 Bản Nháp Báo Cáo Trước Phiên Họp Mentor

**Phiên họp**: Phiên Mentor Thử Nghiệm
**Thời điểm trích xuất dữ liệu**: 09/10/2026 07:00:00 (UTC+7)
**Thời điểm khởi tạo bản nháp**: 10/10/2026 22:10:09 (UTC+7)
**Snapshot nguồn**: `sample_data`

> 💡 *Bản nháp tự động từ hệ thống CVAT & GitHub Sync. Nhóm trưởng vui lòng rà soát và bổ sung ngữ cảnh (5 phút) trước phiên họp.*

### ⚠️ Thông tin cần lưu ý & Cảnh báo dữ liệu:

- Câu hỏi #3 chưa có tham chiếu task/job được xác minh; có thể là câu hỏi chung của repo.

---

## 1. 📊 Tiến độ Batch & Vận Tốc Gán Nhãn

- **CVAT Task**: **SYNTHETIC DEMO** (ID: `1001`)
- **Tổng số Frame**: **20**
- **Tỷ lệ Job hoàn thành**: **1/2** (50.0%)

> ℹ️ *Ghi chú: Tỷ lệ theo Job phản ánh trạng thái hoàn thành quy trình trên CVAT, chưa đại diện cho % frame đã qua nghiệm thu QA cuối cùng.*

| Mã Job | Loại Job | Giai đoạn (Stage) | Trạng thái (State) | Người phụ trách | Số Frame |
| :---: | :---: | :---: | :---: | :---: | :---: |
| [2001](https://example.com/tasks/1001/jobs/2001) | annotation | annotation | completed | Chưa có | 10 |
| [2002](https://example.com/tasks/1001/jobs/2002) | annotation | annotation | in progress | Chưa có | 10 |
| [2003](https://example.com/tasks/1001/jobs/2003) | ground_truth | acceptance | completed | Chưa có | 1 |

### 📐 Thống kê đối tượng gán nhãn (Annotations):

- Tổng số: **3 shapes**, **1 tracks**, **1 tags** (2 bản ghi shape trong tracks).

| Tên Nhãn (Class) | Mã Label ID | Shapes | Tracks | Tags |
| :--- | :---: | :---: | :---: | :---: |
| **vehicle** | `1` | 3 | 1 | 1 |

---

## 2. 🎯 Chất lượng & Điểm QA/QC

> ⚠️ **Trạng thái**: Chưa thống nhất nguồn điểm và quy tắc chấm QA/QC (hoặc task chưa có Ground Truth).
> *Lưu ý: Hệ thống không coi việc thiếu dữ liệu kiểm thử là điểm 0.*

---

## 3. 🔍 Danh Sách Ca Khó & Trường Hợp Biên (Edge Cases)

### 📍 Issue #2: DEMO: occluded vehicle

- **Người tạo**: `demo-user` | **Vị trí**: **Frame #142**
- [🔗 Xem Issue trên GitHub](https://example.com/issues/2)
- 🎯 **[🔗 Mở trực tiếp Frame 142 trên CVAT](https://example.com/tasks/1001/jobs/2002?frame=142)** *(Đã xác minh liên kết task/job)*

**Mô tả vấn đề & Đề xuất:**
> Synthetic example only.
> CVAT task ID: 1001
> CVAT job ID: 2002
> Frame index (nếu có): 142
> How should the team annotate an occluded vehicle?

---

## 4. 💬 Câu Hỏi Mở Cần Mentor Định Đoạt (Open Questions)

### ❓ Question #3: DEMO: guideline question

- **Người đặt câu hỏi**: `demo-user`
- [🔗 Xem thảo luận trên GitHub](https://example.com/issues/3)

> Synthetic general question: which guideline version should we use?

