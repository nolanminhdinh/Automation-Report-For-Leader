# 🏗️ Kiến Trúc Hệ Thống: Auto Annotation Report Pipeline

Tài liệu này đặc tả chi tiết kiến trúc kỹ thuật, luồng dữ liệu (Data Pipeline), mô hình dữ liệu và các thành phần cốt lõi của hệ sinh thái tự động hóa báo cáo CVAT & GitHub.

---

## 1. Tổng quan kiến trúc (Architecture Overview)

Hệ thống được thiết kế theo kiến trúc **Event-Driven & Pipeline Architecture** (Kiến trúc đường ống hướng sự kiện). Mục tiêu là biến đổi dữ liệu thô, phân tán từ các hệ thống quản trị gán nhãn thành báo cáo nghiệp vụ có tính hành động cao (Actionable Insights).

```mermaid
graph TD
    subgraph TriggerLayer["Tầng 1: Kích hoạt (Trigger Layer)"]
        CRON["Cron Scheduler\n(GitHub Actions Schedule / Systemd)"]
        MANUAL["Manual Trigger\n(Workflow Dispatch / CLI)"]
    end

    subgraph IngestionLayer["Tầng 2: Thu thập (Ingestion Layer)"]
        CVAT_EXTRACTOR["CVAT Extractor\n• Tasks & Jobs Client\n• Quality Reports Client\n• Issues/Comments Client"]
        GH_EXTRACTOR["GitHub Extractor\n• Issue & Labels Client\n• Commits & PRs Client"]
    end

    subgraph ProcessingLayer["Tầng 3: Động cơ xử lý (Processing Engine)"]
        METRICS_CALC["Velocity & Progress Engine"]
        QA_ANALYZER["DQC & Quality Analyzer"]
        DEEP_LINK_GEN["CVAT Deep Link Generator"]
        ISSUE_CLASSIFIER["Technical Issues Classifier"]
    end

    subgraph GenerationLayer["Tầng 4: Sinh báo cáo (Report Generation)"]
        JINJA_ENGINE["Jinja2 Template Engine"]
        LLM_SUMMARIZER["LLM Synthesis (Gemini / Claude / OpenAI)"]
        DRAFT_MD["Bản nháp Markdown:\nMENTOR_REPORT_DRAFT.md"]
    end

    subgraph DeliveryLayer["Tầng 5: Phân phối & Handoff (Delivery Layer)"]
        GH_PR["Tạo GitHub PR / Issue"]
        BOT_NOTIFY["Gửi Webhook Telegram / Discord"]
        LEADER_REVIEW["Leader Review (5 phút)"]
        MENTOR_READY["Báo cáo chính thức gửi Mentor"]
    end

    CRON --> CVAT_EXTRACTOR & GH_EXTRACTOR
    MANUAL --> CVAT_EXTRACTOR & GH_EXTRACTOR

    CVAT_EXTRACTOR --> METRICS_CALC & QA_ANALYZER & DEEP_LINK_GEN
    GH_EXTRACTOR --> ISSUE_CLASSIFIER & METRICS_CALC

    METRICS_CALC --> JINJA_ENGINE
    QA_ANALYZER --> JINJA_ENGINE
    DEEP_LINK_GEN --> JINJA_ENGINE
    ISSUE_CLASSIFIER --> JINJA_ENGINE

    JINJA_ENGINE --> LLM_SUMMARIZER
    LLM_SUMMARIZER --> DRAFT_MD

    DRAFT_MD --> GH_PR & BOT_NOTIFY
    GH_PR --> LEADER_REVIEW
    BOT_NOTIFY --> LEADER_REVIEW
    LEADER_REVIEW --> MENTOR_READY

    classDef c1 fill:#E1F5FE,stroke:#0288D1,stroke-width:2px;
    classDef c2 fill:#FFF3E0,stroke:#F57C00,stroke-width:2px;
    classDef c3 fill:#F3E5F5,stroke:#7B1FA2,stroke-width:2px;
    classDef c4 fill:#E8F5E9,stroke:#388E3C,stroke-width:2px;
    classDef c5 fill:#FFFDE7,stroke:#FBC02D,stroke-width:2px;

    class CRON,MANUAL c1;
    class CVAT_EXTRACTOR,GH_EXTRACTOR c2;
    class METRICS_CALC,QA_ANALYZER,DEEP_LINK_GEN,ISSUE_CLASSIFIER c3;
    class JINJA_ENGINE,LLM_SUMMARIZER,DRAFT_MD c4;
    class GH_PR,BOT_NOTIFY,LEADER_REVIEW,MENTOR_READY c5;
```

---

## 2. Trình tự thực thi (Sequence Diagram)

Sơ đồ trình tự biểu diễn sự tương tác giữa các thành phần từ khi kích hoạt đến khi giao bản báo cáo hoàn chỉnh cho Leader:

```mermaid
sequenceDiagram
    autonumber
    actor Leader as Nhóm Trưởng (Leader)
    participant Cron as GitHub Actions (Cron)
    participant Extractor as Extractor Module
    participant CVAT as CVAT REST API
    participant GH as GitHub API
    participant Engine as Processing Engine
    participant Generator as Report Generator (Jinja2+LLM)
    participant Notifier as Telegram/Discord Bot

    alt Tự động định kỳ
        Cron->>Extractor: Kích hoạt pipeline theo lịch (VD: Chủ nhật 20:00)
    else Thủ công
        Leader->>Cron: Chạy lệnh CLI / Workflow Dispatch
        Cron->>Extractor: Kích hoạt pipeline
    end

    activate Extractor
    Extractor->>CVAT: GET /api/tasks/{id}, /api/jobs
    CVAT-->>Extractor: Danh sách Job, trạng thái, assignees
    Extractor->>CVAT: GET /api/quality/reports?task_id={id}
    CVAT-->>Extractor: Điểm QA, phân bố lỗi, tỷ lệ Pass/Reject
    Extractor->>CVAT: GET /api/issues?task_id={id}
    CVAT-->>Extractor: Frame có comment lỗi / ca khó

    Extractor->>GH: GET /repos/{owner}/{repo}/issues?labels=ca-kho,blocker
    GH-->>Extractor: Danh sách Issue thảo luận kỹ thuật
    deactivate Extractor

    activate Engine
    Extractor->>Engine: Truyền dữ liệu thô (Raw Data Payload)
    Engine->>Engine: Tính Velocity (frames/member/ngày)
    Engine->>Engine: Tổng hợp Top 5 loại lỗi QA
    Engine->>Engine: Sinh Deep Links CVAT (frame-level URL)
    Engine->>Engine: Chuẩn hóa Schema báo cáo
    deactivate Engine

    activate Generator
    Engine->>Generator: Context Data Dict
    Generator->>Generator: Render Jinja2 Template
    opt LLM Tóm lược (Optional)
        Generator->>Generator: LLM tóm tắt insight & hành động khuyến nghị
    end
    Generator-->>Generator: Xuất MENTOR_REPORT_DRAFT.md
    deactivate Generator

    activate Notifier
    Generator->>Notifier: Đẩy tóm tắt KPI + Link báo cáo
    Notifier->>Leader: Gửi tin nhắn Telegram/Discord: "Bản nháp báo cáo đã sẵn sàng!"
    deactivate Notifier

    Leader->>Leader: Đọc, tinh chỉnh ngữ cảnh (5-10 phút)
    Leader->>Leader: Xuất báo cáo chính thức gửi Mentor trong buổi họp
```

---

## 3. Các module thành phần cốt lõi

### 3.1. Extractor Layer (`src/extractors/`)
* **`CVATExtractor`**:
  * Sử dụng thư viện `requests` hoặc `cvat-sdk` chính thức.
  * Hỗ trợ xác thực qua Token Header (`Authorization: Token <key>`) hoặc Basic Auth.
  * Cơ chế tự động phân trang (Pagination handling) khi danh sách Jobs hoặc Issues vượt quá 100 items.
* **`GitHubExtractor`**:
  * Sử dụng GitHub REST API v3 và Octokit/PyGithub.
  * Lọc issues theo bộ nhãn quy ước: `ca-kho`, `mentor-question`, `blocker`.
  * Trích xuất các PR liên quan đến data tool hoặc annotation guideline changes.

### 3.2. Processing Engine Layer (`src/processors/`)
* **`VelocityCalculator`**:
  $$\text{Velocity} = \frac{\text{Số frames đã chuyển sang completed trong kỳ}}{\text{Số annotators tham gia} \times \text{Số ngày}}$$
  $$\text{Progress Rate (\%)} = \frac{\sum \text{Frames Completed}}{\text{Tổng số frames của Task}} \times 100\%$$
* **`QAMetricsAnalyzer`**:
  * Đọc Quality Report từ CVAT: trích xuất độ lệch IoU trung bình, lỗi sai label, lỗi vẽ box thiếu hoặc thừa.
  * Phân loại lỗi theo mức độ nghiêm trọng: `CRITICAL` (ảnh hưởng trực tiếp đến ground-truth), `WARNING` (sai sót nhỏ về bounding box padding).
* **`DeepLinkBuilder`**:
  * Xây dựng URL trực tiếp đến frame cụ thể:
    $$\text{URL} = \texttt{\{CVAT\_HOST\}/tasks/\{task\_id\}/jobs/\{job\_id\}?frame=\{frame\_number\}}$$

### 3.3. Generator Layer (`src/generators/`)
* Sử dụng thư viện **Jinja2** để ánh xạ số liệu vào khung Markdown chuẩn hóa.
* Hỗ trợ cắm module LLM (`Gemini Flash / OpenAI GPT-4o-mini`) với prompt tối ưu để:
  * Viết phần tóm tắt điều hành (Executive Summary) 3 câu.
  * Đề xuất 3 câu hỏi sắc bén nhất cho Leader hỏi Mentor.

### 3.4. Notifier Layer (`src/notifiers/`)
* Gửi payload tóm tắt dạng Rich Text tới:
  * **Telegram Bot API**: Tin nhắn Markdown kèm inline button trỏ đến file Draft.
  * **Discord Webhook**: Embed message màu sắc trực quan (Xanh nếu đạt KPI, Đỏ nếu trễ hạn hoặc QA thấp).

---

## 4. An toàn dữ liệu & Quản lý Token (Security)

1. **Tuân thủ Bảo vệ Dữ liệu**:
   * Hệ thống chỉ trích xuất metadata số lượng, điểm số, ID của job/frame và nội dung ghi chú kỹ thuật.
   * Không lưu trữ hoặc tải về hình ảnh thô có chứa thông tin nhận dạng cá nhân (PII như mặt người, biển số xe) lên máy chủ báo cáo.
2. **Quản trị Bí mật (Secrets Management)**:
   * Mọi Token (`CVAT_TOKEN`, `GITHUB_TOKEN`, `TELEGRAM_BOT_TOKEN`) tuyệt đối không hardcode trong mã nguồn.
   * Chỉ được nạp thông qua biến môi trường (`.env` trên local hoặc `GitHub Secrets` trên CI/CD).
