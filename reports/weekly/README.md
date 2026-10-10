# 📁 HỆ THỐNG BÁO CÁO TIẾN ĐỘ TUẦN (WEEKLY REPORTS REPOSITORY)

Thư mục này lưu trữ toàn bộ hồ sơ quản lý tiến độ, kế hoạch làm việc và báo cáo tổng kết hàng tuần của dự án **Auto Annotation Report Pipeline (CVAT & GitHub Sync - Power BI Hybrid)**.

---

## 📂 CẤU TRÚC THƯ MỤC BÁO CÁO

```text
reports/weekly/
├── README.md                           <-- Quy chuẩn & Mục lục báo cáo tuần
├── week-01/                            <-- Tuần 1: Khởi động, Nghiệp vụ & Prototype
│   ├── TIMELINE_CONG_VIEC.md           <-- Timeline chi tiết từng ngày của 5 thành viên
│   └── BAO_CAO_TUAN_01.md              <-- Báo cáo: Đã làm, Chưa làm & Cải tiến sản phẩm
└── week-02/                            <-- Tuần 2: Ingestion Pipeline, Data Contract & Frame Deep Link
    ├── TIMELINE_CONG_VIEC.md           <-- Timeline chi tiết từng ngày của 5 thành viên
    └── BAO_CAO_TUAN_02.md              <-- Báo cáo: Nghiệm thu, Refactor & Tích hợp Ingestion API
```

---

## 📋 QUY CHUẨN MẪU BÁO CÁO TUẦN (WEEKLY REPORT STANDARD)

Mỗi tuần, hồ sơ báo cáo bắt buộc bao gồm 2 tài liệu chuẩn hóa:

1. **`TIMELINE_CONG_VIEC.md`**:
   * Phân rã mục tiêu tuần và kế hoạch làm việc từ Thứ Hai đến Chủ Nhật.
   * Chi tiết đầu việc từng ngày của 5 thành viên:
     * **Đinh Công Minh** (Project Lead & BI Architect)
     * **Nguyễn Minh Tú** (Data Integration Engineer)
     * **Vũ Trường Duy** (Data Integration Engineer)
     * **Phạm Nguyễn Tuân** (Analytics & ETL Engineer)
     * **Ngô Duy Ngọc** (DevOps & Automation Engineer)

2. **`BAO_CAO_TUAN_XX.md`**:
   * **Phần 1: Công việc đã hoàn thành**: Liệt kê chi tiết kết quả đạt được, tài liệu và mã nguồn đã hoàn thiện.
   * **Phần 2: Công việc chưa hoàn thành & Lý do**: Nêu rõ nguyên nhân gốc rễ (Root Cause) và giải pháp khắc phục.
   * **Phần 3: Đề xuất & Cải tiến sản phẩm (Product Improvements)**:
     * Nội dung cải tiến mới.
     * Lý do thực hiện cải tiến.
     * Căn cứ kỹ thuật (Technical Grounds) và căn cứ thực tế nghiệp vụ (Operational Grounds).
   * **Phần 4: Đánh giá & Kế hoạch tuần tiếp theo**.
