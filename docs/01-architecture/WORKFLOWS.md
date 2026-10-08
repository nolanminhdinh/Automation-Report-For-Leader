# 🔄 Tổng Hợp Biểu Đồ Workflow Dự Án (Project Workflows)

Tài liệu này tổng hợp **2 biểu đồ quy trình (Workflow Diagrams)** cốt lõi của hệ thống **Tự động hóa soạn báo cáo trước phiên Mentor (CVAT & GitHub Sync)**.

---

## 📊 Biểu Đồ 1: Quy Trình Pipeline 5 Giai Đoạn Khép Kín (5-Phase End-to-End Pipeline)

Biểu đồ này mô tả chi tiết đường ống dữ liệu từ thời điểm kích hoạt (Trigger), trích xuất API, tính toán chỉ số, sinh văn bản báo cáo cho tới bước Review của Nhóm trưởng.

![Sơ đồ Pipeline 5 Giai đoạn](../assets/mermaid-diagram.svg)

### Mã nguồn Mermaid (Biểu đồ 1):

```mermaid
flowchart TD
    classDef trigger fill:#E1F5FE,stroke:#0288D1,stroke-width:2px;
    classDef fetch fill:#FFF3E0,stroke:#F57C00,stroke-width:2px;
    classDef process fill:#F3E5F5,stroke:#7B1FA2,stroke-width:2px;
    classDef report fill:#E8F5E9,stroke:#388E3C,stroke-width:2px;
    classDef human fill:#FFFDE7,stroke:#FBC02D,stroke-width:2px;

    subgraph Phase1["1. KÍCH HOẠT (TRIGGER)"]
        T1["Lịch định kỳ: Cron Trigger<br/>(VD: 24h trước buổi gặp Mentor)"]:::trigger
        T2["Nhóm trưởng kích hoạt thủ công<br/>(GitHub Actions / CLI / Webhook)"]:::trigger
    end

    subgraph Phase2["2. THU THẬP DỮ LIỆU (DATA EXTRACTION)"]
        direction TB
        subgraph CVAT_Data["CVAT REST API"]
            C1["/api/tasks & /api/jobs<br/>(Tiến độ batch, assignee, trạng thái)"]:::fetch
            C2["/api/quality/reports & analytics<br/>(Điểm QA/QC, tỷ lệ pass/reject)"]:::fetch
            C3["/api/issues & comments<br/>(Ca khó, frame cần review, chú thích)"]:::fetch
        end
        subgraph GitHub_Data["GitHub REST/GraphQL API"]
            G1["Issues & Discussions<br/>(Label: 'ca-kho', 'mentor-question', 'blocker')"]:::fetch
            G2["Commits & PRs<br/>(Tiến độ code, pipeline dữ liệu)"]:::fetch
        end
    end

    subgraph Phase3["3. XỬ LÝ & LIÊN KẾT (DATA PROCESSING ENGINE)"]
        P1["Module tính tiến độ & Velocity<br/>(Tỷ lệ % done, backlog, velocity theo người)"]:::process
        P2["Module thống kê lỗi & QA Score<br/>(Phân bố lỗi: box lệch, thiếu nhãn, sai class)"]:::process
        P3["Bộ tạo Deep Link CVAT<br/>(Sinh link trỏ thẳng frame/job/issue ca khó)"]:::process
        P4["Bộ lọc & phân loại câu hỏi mở<br/>(Phân nhóm thắc mắc về guideline/kỹ thuật)"]:::process
    end

    subgraph Phase4["4. SINH BẢN NHÁP 4 MỤC (REPORT GENERATOR)"]
        R1["Template Engine (Jinja2 / Markdown) + LLM Summarizer"]:::report
        R2["Bản nháp Markdown: MENTOR_REPORT_DRAFT.md<br/>• Mục 1: Tiến độ Batch & KPI<br/>• Mục 2: Chất lượng & Điểm QA<br/>• Mục 3: Danh sách ca khó kèm Link CVAT/GitHub<br/>• Mục 4: Câu hỏi mở & Vấn đề cần Mentor gỡ rối"]:::report
    end

    subgraph Phase5["5. REVIEW & PHIÊN HỌP MENTOR"]
        H1["Tự động tạo GitHub Pull Request / Issue<br/>(Gửi thông báo Telegram/Discord cho Nhóm trưởng)"]:::human
        H2["Nhóm trưởng Review & Tinh chỉnh<br/>(Bổ sung ngữ cảnh, sắp xếp mức ưu tiên)"]:::human
        H3["Báo cáo chính thức gửi Mentor trước buổi họp"]:::human
    end

    T1 --> C1 & C2 & C3 & G1 & G2
    T2 --> C1 & C2 & C3 & G1 & G2

    C1 --> P1
    C2 --> P2
    C3 --> P3
    G1 & G2 --> P4

    P1 & P2 & P3 & P4 --> R1
    R1 --> R2
    R2 --> H1
    H1 --> H2
    H2 --> H3
```

---

## 🔄 Biểu Đồ 2: Kiến Trúc Vòng Lặp Khép Kín & Điều Phối Đa Kênh (Closed-Loop Pipeline & Multi-Channel Delivery)

Biểu đồ này tập trung vào kiến trúc tổng thể của hệ thống, vòng lặp phản hồi (*closed feedback loop*) giữa quyết định của Mentor và việc cập nhật ngược lại nền tảng gán nhãn, cùng cơ chế thông báo đa kênh.

![Sơ đồ Vòng lặp Khép kín & Đa kênh](../assets/workflow-closed-loop-delivery.svg)

### Mã nguồn Mermaid (Biểu đồ 2):

```mermaid
flowchart TD
    classDef source fill:#E1F5FE,stroke:#0288D1,stroke-width:2px;
    classDef engine fill:#FFF3E0,stroke:#F57C00,stroke-width:2px;
    classDef output fill:#E8F5E9,stroke:#388E3C,stroke-width:2px;
    classDef channel fill:#FFFDE7,stroke:#FBC02D,stroke-width:2px;
    classDef loop fill:#F3E5F5,stroke:#7B1FA2,stroke-width:2px;

    subgraph Layer1 ["1. NGUỒN DỮ LIỆU ĐẦU VÀO (DATA SOURCES)"]
        CVAT["CVAT REST API v2<br/>• Tiến độ Tasks & Jobs<br/>• Báo cáo chất lượng QA/QC<br/>• Issues & Frame Annotations"]:::source
        GH["GitHub REST / GraphQL API<br/>• Pull Requests & Commits<br/>• Thảo luận & Issue kỹ thuật<br/>• Nhãn: ca-kho, mentor-question"]:::source
    end

    subgraph Layer2 ["2. BỘ XỬ LÝ TRUNG TÂM (CORE PROCESSING & ANALYTICS)"]
        Aggregator["Aggregator & Metric Calculator<br/>• Tính Velocity & Tỷ lệ % Batch<br/>• Phân tích ma trận lỗi QA/QC<br/>• Bộ sinh Deep Link (Frame-level)"]:::engine
        AIAssistant["Guideline Matcher & LLM Summarizer<br/>• Đối chiếu quy chuẩn gán nhãn<br/>• Tóm lược số liệu & gợi ý câu hỏi"]:::engine
    end

    subgraph Layer3 ["3. ĐẦU RA & BÁO CÁO (OUTPUTS & ARTIFACTS)"]
        Dashboard["Interactive Dashboard<br/>(Trực quan hóa số liệu tiến độ)"]:::output
        ReportGen["Report Engine (Jinja2)<br/>• Bản nháp MENTOR_REPORT_DRAFT.md<br/>• Khung chuẩn 4 mục hành động"]:::output
    end

    subgraph Layer4 ["4. ĐA KÊNH PHÂN PHỐI & THÔNG BÁO (MULTI-CHANNEL DELIVERY)"]
        Telegram["📱 Telegram Bot Alert<br/>(Gửi tóm tắt KPI & link bản nháp)"]:::channel
        DiscordSlack["💬 Discord / Slack Webhook<br/>(Ping Team Lead kèm rich embed)"]:::channel
        GHIssue["🐙 GitHub Pull Request / Issue<br/>(Mở PR bản thảo báo cáo tự động)"]:::channel
    end

    subgraph Layer5 ["5. VÒNG LẶP KHÉP KÍN (CLOSED FEEDBACK LOOP)"]
        MentorReview["Phiên Họp Mentor & Quyết Định<br/>• Mentor giải đáp ca khó<br/>• Chốt phương án xử lý tranh chấp"]:::loop
        SyncBack["Cập Nhật Ngược Hệ Thống<br/>• Đồng bộ nhãn sửa đổi vào CVAT<br/>• Tự động mở PR cập nhật Guideline"]:::loop
    end

    CVAT --> Aggregator
    GH --> Aggregator
    Aggregator --> AIAssistant
    AIAssistant --> Dashboard
    Aggregator --> ReportGen

    ReportGen --> Telegram & DiscordSlack & GHIssue
    Telegram & DiscordSlack & GHIssue --> MentorReview
    Dashboard --> MentorReview

    MentorReview --> SyncBack
    SyncBack -.->|Cập nhật quy chuẩn| GH
    SyncBack -.->|Đồng bộ ground-truth| CVAT
```

---

## 🏛️ Biểu Đồ 3: Mô Hình Hybrid — Python ETL Engine & Power BI Analytics Dashboard

Biểu đồ này mô tả chi tiết sự phân công phối hợp giữa **Python Engine** (phụ trách trích xuất API, tính toán logic và soạn thảo văn bản) và **Power BI Dashboard** (phụ trách trực quan hóa số liệu KPI, drill-down và hiển thị danh mục ca khó kèm link):

![Sơ đồ Mô hình Hybrid Power BI](../assets/workflow-hybrid-powerbi.svg)

### Mã nguồn Mermaid (Biểu đồ 3):

```mermaid
flowchart TD

    classDef src fill:#E1F5FE,stroke:#0288D1,stroke-width:2px;
    classDef py fill:#FFF3E0,stroke:#F57C00,stroke-width:2px;
    classDef pbi fill:#FFFDE7,stroke:#FBC02D,stroke-width:2px;
    classDef out fill:#E8F5E9,stroke:#388E3C,stroke-width:2px;

    subgraph Layer1 ["1. NGUỒN DỮ LIỆU ĐẦU VÀO"]
        CVAT["CVAT REST API v2<br/>(Tasks, Jobs, QA Scores, Issues)"]:::src
        GH["GitHub REST API<br/>(Issues ca-kho, Commits, PRs)"]:::src
    end

    subgraph Layer2 ["2. PYTHON BACKEND & ETL ENGINE"]
        Extractor["API Extractor Module<br/>(Xử lý phân trang & Bearer Auth)"]:::py
        Processor["Metric Processor & Aggregator<br/>• Gom tiến độ theo Batch<br/>• Tính QA Score & Vận tốc<br/>• Sinh Deep Link CVAT Job/Frame"]:::py
        ReportGen["Report Generator (Jinja2 / LLM)<br/>• Bản nháp MENTOR_REPORT_DRAFT.md"]:::py
        CSVExport["Power BI Data Exporter<br/>• Xuất data/processed/*.csv"]:::py
    end

    subgraph Layer3 ["3. POWER BI DASHBOARD (DATA VIZ LAYER)"]
        Page1["Page 1: Tổng Quan Tiến Độ Batch<br/>(KPI Cards, Gauge, Velocity)"]:::pbi
        Page2["Page 2: Phân Tích Điểm QA/QC<br/>(Leaderboard, Ma trận 4 loại lỗi)"]:::pbi
        Page3["Page 3: Ca Khó & Deep-Link Explorer<br/>(Bảng ca khó + URL mở CVAT trực tiếp)"]:::pbi
    end

    subgraph Layer4 ["4. ĐẦU RA PHỤC VỤ PHIÊN MENTOR"]
        DraftDoc["Văn Bản Báo Cáo (.md / .pdf)<br/>• Gửi trước cho Leader & Mentor"]:::out
        LiveViz["Giao Diện Trực Quan Power BI<br/>• Trình chiếu số liệu trong buổi họp"]:::out
    end

    CVAT & GH --> Extractor
    Extractor --> Processor
    Processor --> ReportGen & CSVExport
    CSVExport -->|Nạp dữ liệu sạch| Page1 & Page2 & Page3
    ReportGen --> DraftDoc
    Page1 & Page2 & Page3 --> LiveViz
```

---

## ⏰ Biểu Đồ 4: Luồng Hoạt Động Tự Động Hóa Theo Lịch (Scheduled Pipeline Automation)

Biểu đồ này mô tả luồng thực thi tự động định kỳ qua **GitHub Actions Cron Scheduler**, từ thời điểm kích hoạt không người lái đến khi đẩy dữ liệu lên repo và phát thông báo qua Telegram/Discord:

![Sơ đồ Luồng Hoạt Động Theo Lịch](../assets/workflow-scheduled-automation.svg)

### Mã nguồn Mermaid (Biểu đồ 4):

```mermaid
flowchart TD

    classDef trigger fill:#E1F5FE,stroke:#0288D1,stroke-width:2px;
    classDef runner fill:#FFF3E0,stroke:#F57C00,stroke-width:2px;
    classDef data fill:#F3E5F5,stroke:#7B1FA2,stroke-width:2px;
    classDef notify fill:#E8F5E9,stroke:#388E3C,stroke-width:2px;

    subgraph TriggerZone ["1. BỘ ĐẾM GIỜ & KÍCH HOẠT"]
        CronWk["⏰ Cron Schedule: Thứ 6 (17:00 ICT) & Chủ Nhật (20:00 ICT)"]:::trigger
        ManualWk["👆 Workflow Dispatch: Kích hoạt thủ công khi cần gấp"]:::trigger
    end

    subgraph CloudRunner ["2. GITHUB ACTIONS CLOUD RUNNER"]
        Setup["Setup Python 3.10 & Cài đặt requirements.txt"]:::runner
        FetchRun["Gọi CVAT REST API & GitHub API với Secrets an toàn"]:::runner
        Compute["Xử lý số liệu, tính điểm QA & gom danh sách ca khó"]:::runner
    end

    subgraph ArtifactSync ["3. ĐỒNG BỘ HIỆN VẬT & POWER BI"]
        SaveCSVs["Cập nhật data/processed/*.csv cho Power BI"]:::data
        SaveReport["Sinh file reports/MENTOR_REPORT_DRAFT.md"]:::data
        GitCommit["Auto Git Commit & Push lên branch main [skip ci]"]:::data
    end

    subgraph DispatchNotice ["4. PHÂN PHỐI THÔNG BÁO TỨC THỜI"]
        TgBot["📱 Telegram Bot: Bắn tóm tắt KPI & Link báo cáo"]:::notify
        DcBot["💬 Discord Webhook: Ping kênh thông báo nhóm"]:::notify
        LeadAction["👤 Nhóm Trưởng: Xem báo cáo, mở Power BI, sẵn sàng họp Mentor"]:::notify
    end

    CronWk & ManualWk --> Setup
    Setup --> FetchRun
    FetchRun --> Compute
    Compute --> SaveCSVs & SaveReport
    SaveCSVs & SaveReport --> GitCommit
    GitCommit --> TgBot & DcBot
    TgBot & DcBot --> LeadAction
```

---

## 🛡️ Cam Kết Bảo Mật & Toàn Vẹn Dữ Liệu

1. **Không chứa thông tin mật bên thứ ba**: Mọi dữ liệu mẫu, đường dẫn máy chủ và thông số định danh trong biểu đồ đều được chuẩn hóa theo chuẩn mở tổng quát (Generic Open Standards), không chứa token, bí mật doanh nghiệp, mã học viên hay thông tin nội bộ của bất kỳ tổ chức nào.
2. **Tuân thủ quy chuẩn bảo mật**: Quá trình trích xuất chỉ đọc metadata thống kê, không lưu giữ dữ liệu nhận dạng cá nhân (PII) trên đường ống báo cáo.

