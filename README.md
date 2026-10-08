# 📊 Auto Annotation Report Pipeline (CVAT & GitHub Sync)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![CVAT API](https://img.shields.io/badge/CVAT-REST%20API%20v2-green?logo=opencv)](https://www.cvat.ai/)
[![GitHub API](https://img.shields.io/badge/GitHub-REST%20%26%20GraphQL-black?logo=github)](https://docs.github.com/en/rest)
[![Power BI](https://img.shields.io/badge/Power_BI-Analytics_Dashboard-F2C811?logo=powerbi&logoColor=black)](docs/HYBRID_POWERBI_ARCHITECTURE.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Automation](https://img.shields.io/badge/Workflow-GitHub%20Actions-blueviolet?logo=githubactions)](docs/SCHEDULED_WORKFLOW_GUIDE.md)

> **Hệ sinh thái tự động hóa tổng hợp báo cáo tiến độ & chất lượng gán nhãn dữ liệu (Data Annotation Operations) từ CVAT và GitHub. Ứng dụng mô hình Hybrid kết hợp Python ETL Engine, Dashboard Power BI trực quan và luồng kích hoạt theo lịch định kỳ phục vụ các phiên Mentor & Leader.**


---

## 📌 1. Bối cảnh & Vấn đề giải quyết

Trong các dự án thị giác máy tính (Computer Vision) và gán nhãn dữ liệu quy mô lớn (Data Annotation Operations):
* **Phân mảnh dữ liệu**: Tiến độ gán nhãn nằm trên nền tảng gán nhãn (**CVAT**), trong khi thảo luận kỹ thuật, mã nguồn, báo lỗi và phân chia công việc lại nằm trên **GitHub** (Issues, PRs).
* **Tốn thời gian chuẩn bị họp**: Hàng tuần/hàng kỳ trước buổi họp với Leader hoặc Mentor, nhóm trưởng thường mất **2 đến 4 giờ** để tổng hợp số liệu thủ công: đếm số frame hoàn thành, tính tỷ lệ lỗi, tổng hợp các ca khó (edge cases), và lọc các câu hỏi chưa được giải đáp.
* **Bỏ sót ca khó (Blind Spots)**: Các frame gán nhãn gây tranh cãi hoặc bị gắn cờ lỗi thường bị trôi trên CVAT nếu không được liên kết trực tiếp bằng Deep Link vào tài liệu báo cáo.
* **Thiếu tính định lượng**: Khó đo lường chính xác vận tốc gán nhãn (*velocity*) theo từng thành viên và phân bố loại lỗi (*box lệch, sai nhãn, thiếu đối tượng*).

👉 **Giải pháp**: Xây dựng **Pipeline tự động hóa khép kín (End-to-End Automated Pipeline)**, định kỳ thu thập dữ liệu qua API từ CVAT & GitHub, tổng hợp chỉ số, trích xuất ca khó kèm Deep Link trực tiếp đến từng frame/job, và tạo bản thảo báo cáo chuẩn xác 4 phần cho Leader/Mentor.

---

## 🏗️ 2. Kiến trúc hệ thống (System Architecture)

![Kiến trúc hệ thống](assets/mermaid-diagram.svg)

Hệ thống hoạt động theo quy trình 5 giai đoạn khép kín:

```mermaid
flowchart LR
    subgraph P1["1. KÍCH HOẠT (TRIGGER)"]
        T1["Cron Trigger\n(VD: 24h trước họp)"]
        T2["Kích hoạt thủ công\n(GitHub Actions / CLI)"]
    end

    subgraph P2["2. THU THẬP DỮ LIỆU"]
        CVAT["CVAT REST API\n• /api/tasks & /jobs\n• /api/quality/reports\n• /api/issues & comments"]
        GH["GitHub API\n• Issues (ca-kho, blocker)\n• Commits & PRs"]
    end

    subgraph P3["3. DATA PROCESSING ENGINE"]
        ENG["Xử lý & Liên kết\n• Tính Velocity & % Done\n• Phân bố lỗi & Điểm QA\n• Sinh Deep Link CVAT\n• Phân loại câu hỏi mở"]
    end

    subgraph P4["4. REPORT GENERATOR"]
        GEN["Template Engine (Jinja2) +\nLLM Summarizer\n↓\nMENTOR_REPORT_DRAFT.md"]
    end

    subgraph P5["5. REVIEW & PHIÊN HỌP"]
        REV["Tạo PR/Issue Draft\nThông báo Telegram/Discord\n↓\nLeader tinh chỉnh & Báo cáo"]
    end

    T1 --> CVAT & GH
    T2 --> CVAT & GH
    CVAT --> ENG
    GH --> ENG
    ENG --> GEN
    GEN --> REV

    classDef trigger fill:#E1F5FE,stroke:#0288D1,stroke-width:2px;
    classDef extract fill:#FFF3E0,stroke:#F57C00,stroke-width:2px;
    classDef process fill:#F3E5F5,stroke:#7B1FA2,stroke-width:2px;
    classDef report fill:#E8F5E9,stroke:#388E3C,stroke-width:2px;
    classDef review fill:#FFFDE7,stroke:#FBC02D,stroke-width:2px;

    class T1,T2 trigger;
    class CVAT,GH extract;
    class ENG process;
    class GEN report;
    class REV review;
```

---

## ⚡ 3. Chi tiết 5 Giai đoạn cốt lõi

### Giai đoạn 1: Kích hoạt (Trigger)
* **Cron Trigger**: Thiết lập chạy tự động theo lịch (ví dụ: `0 8 * * 1` - sáng thứ Hai hoặc 24 giờ trước phiên họp Mentor).
* **Manual / Event Trigger**: Cho phép chạy thủ công từ terminal qua CLI hoặc chạy trên giao diện web GitHub Actions (Workflow Dispatch) bất cứ khi nào cần báo cáo khẩn.

### Giai đoạn 2: Thu thập dữ liệu (Data Extraction)
* **CVAT REST API v2**:
  * Trích xuất thông tin Task, Job, phân công (`assignee`) và trạng thái (`annotation`, `validation`, `completed`).
  * Trích xuất báo cáo chất lượng QA/QC: Độ chính xác, tỷ lệ Accept/Reject, các lỗi do reviewer ghi nhận.
  * Thu thập danh sách Issues/Comments gắn tại từng frame hình hoặc object.
* **GitHub API (REST/GraphQL)**:
  * Quét các Issue mở có gắn nhãn: `ca-kho`, `mentor-question`, `blocker`.
  * Thống kê Commit, Pull Request để cập nhật tiến độ phần mềm, pipeline dữ liệu phụ trợ.

### Giai đoạn 3: Động cơ Xử lý & Liên kết (Data Processing Engine)
* **Tiến độ & Vận tốc**: Tính toán tỷ lệ phần trăm hoàn thành, số frame tồn đọng (*backlog*), vận tốc gán nhãn trung bình theo từng thành viên.
* **Phân tích lỗi**: Thống kê ma trận lỗi (*Bounding box lệch/lỏng, gán sai class, bỏ sót nhãn, sai thuộc tính*).
* **Trình tạo Deep Link**: Tự động cấu trúc URL trỏ trực tiếp đến chính xác frame hình đang có tranh chấp trên CVAT (`https://<cvat-host>/tasks/{id}/jobs/{job_id}?frame={idx}`).
* **Phân loại câu hỏi**: Gom nhóm câu hỏi kỹ thuật về quy chuẩn gán nhãn (guideline) hoặc hạ tầng.

### Giai đoạn 4: Sinh bản thảo báo cáo (Report Generator)
* Sử dụng **Jinja2 Template** kết hợp mô hình ngôn ngữ (LLM - Gemini / GPT / Claude) để tóm lược ngắn gọn số liệu thành tài liệu Markdown: `MENTOR_REPORT_DRAFT.md`.
* **Cấu trúc 4 phần chuẩn mực**:
  1. **Tiến độ Batch & KPI**: Tổng frame, % đạt được, vận tốc từng người, tiến độ so với kế hoạch.
  2. **Chất lượng & Điểm QA/QC**: Tỷ lệ Pass/Reject, phân loại lỗi phổ biến, điểm chất lượng trung bình.
  3. **Danh sách Ca khó (Edge Cases)**: Bảng chi tiết kèm hình ảnh, mô tả vấn đề và **Deep Link CVAT trỏ thẳng frame**.
  4. **Câu hỏi mở & Vấn đề cần Mentor gỡ rối**: Các trường hợp guideline chưa bao quát, xung đột nhãn cần Mentor định đoạt.

### Giai đoạn 5: Review & Phiên họp Mentor
* Tự động tạo **Draft Pull Request** hoặc **GitHub Issue** chứa nội dung báo cáo.
* Gửi Webhook thông báo tới **Telegram / Discord / Slack** của Leader.
* Nhóm trưởng review, tinh chỉnh nhanh 5-10 phút trước khi xuất báo cáo gửi Mentor.

---

## 📁 4. Cấu trúc thư mục dự án

```text
├── .github/
│   └── workflows/
│       └── mentor_report_automation.yml  # Lịch chạy định kỳ & Manual trigger
├── assets/
│   └── mermaid-diagram.svg              # Sơ đồ kiến trúc trực quan
├── docs/                                # Thư mục tài liệu chi tiết của dự án
│   ├── ARCHITECTURE.md                  # Tài liệu đặc tả kiến trúc kỹ thuật & Data Flow
│   ├── REPORT_TEMPLATE_SPEC.md          # Chuẩn đặc tả cấu trúc bản báo cáo 4 mục
│   ├── CVAT_INTEGRATION_GUIDE.md        # Hướng dẫn kết nối CVAT REST API & Deep Links
│   ├── GITHUB_INTEGRATION_GUIDE.md      # Hướng dẫn tích hợp GitHub Issues & Actions
│   ├── DEPLOYMENT_AND_WORKFLOW.md       # Hướng dẫn triển khai CI/CD & Bot thông báo
│   └── MENTOR_REPORT_DRAFT_SAMPLE.md    # Báo cáo mẫu minh họa thực tế
├── src/                                 # Mã nguồn Python của hệ thống
│   ├── extractors/                      # Trích xuất dữ liệu từ CVAT và GitHub
│   ├── processors/                      # Tính toán KPI, phân tích QA, sinh Deep Link
│   ├── generators/                      # Render Markdown qua Template & LLM
│   ├── notifiers/                       # Gửi thông báo Telegram/Discord/Slack
│   └── main.py                          # CLI entrypoint điều phối pipeline
├── templates/
│   └── mentor_report_template.j2        # Template Jinja2 cho bản báo cáo
├── .env.example                         # Cấu hình biến môi trường mẫu
├── .gitignore
├── requirements.txt                     # Thư viện phụ thuộc Python
└── README.md                            # Hướng dẫn dự án
```

---

## 🚀 5. Hướng dẫn cài đặt & Chạy thử nghiệm

### 5.1. Yêu cầu môi trường
* Python 3.10 trở lên
* Tài khoản CVAT với Personal Access Token (PAT) hoặc Basic Auth
* GitHub Personal Access Token (với quyền `repo`)

### 5.2. Cài đặt các thư viện

```bash
# Clone repository
git clone https://github.com/nolanminhdinh/Auto-Annotation-Reporter.git
cd Auto-Annotation-Reporter

# Tạo môi trường ảo
python -m venv .venv

# Kích hoạt môi trường (Windows PowerShell)
.\.venv\Scripts\Activate.ps1
# Hoặc trên Linux/macOS:
# source .venv/bin/activate

# Cài đặt thư viện phụ thuộc
pip install -r requirements.txt
```

### 5.3. Cấu hình biến môi trường (`.env`)

Tạo file `.env` từ file mẫu:
```bash
cp .env.example .env
```

Điền các thông số xác thực:
```ini
# CVAT Configuration
CVAT_HOST=https://cvat.example.org
CVAT_USER=your_username
CVAT_PASS=your_password
# hoặc dùng Token:
CVAT_TOKEN=your_cvat_personal_access_token
CVAT_TASK_ID=217

# GitHub Configuration
GITHUB_TOKEN=your_github_token
GITHUB_REPO=your_org/your_repo

# Notifier (Tùy chọn)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

### 5.4. Chạy sinh báo cáo qua CLI

```bash
# Chạy tạo báo cáo cho 1 Task cụ thể
python src/main.py --task-id 217 --output reports/MENTOR_REPORT_DRAFT.md

# Chạy kèm thông báo Telegram
python src/main.py --task-id 217 --notify telegram
```

File báo cáo sau khi sinh sẽ nằm tại `reports/MENTOR_REPORT_DRAFT.md` sẵn sàng để Leader duyệt và gửi Mentor.

---

## 📚 6. Tài liệu chi tiết trong `docs/`

Vui lòng tham khảo các tài liệu chuyên sâu trong thư mục [`docs/`](docs/):
* 🏛️ [Kiến trúc Mô hình Hybrid Power BI](docs/HYBRID_POWERBI_ARCHITECTURE.md) - Chi tiết luồng Python ETL kết hợp Power BI Dashboard.
* ⏰ [Hướng dẫn Vận hành Luồng Theo Lịch](docs/SCHEDULED_WORKFLOW_GUIDE.md) - Cấu hình GitHub Actions Cron & Secrets.
* 🔄 [Tổng hợp 4 Biểu đồ Workflow cốt lõi](docs/WORKFLOWS.md) - 5 giai đoạn, Vòng lặp khép kín, Hybrid Power BI & Scheduled Dispatcher.
* 📖 [Kiến trúc hệ thống chi tiết](docs/ARCHITECTURE.md) - Đặc tả luồng xử lý dữ liệu và Data Flow.
* 📋 [Đặc tả bản báo cáo 4 mục](docs/REPORT_TEMPLATE_SPEC.md) - Quy chuẩn chỉ số và định dạng đầu ra.
* 🔌 [Hướng dẫn tích hợp CVAT REST API](docs/CVAT_INTEGRATION_GUIDE.md) - Endpoint, Authenticate & Deep Linking.
* 🐙 [Hướng dẫn tích hợp GitHub API](docs/GITHUB_INTEGRATION_GUIDE.md) - Labeling, Actions & Pull Request Draft.
* ⚙️ [Hướng dẫn Triển khai & Vận hành](docs/DEPLOYMENT_AND_WORKFLOW.md) - Cron setup, GitHub Actions & Webhook.
* 📝 [Bản báo cáo mẫu thực tế](docs/MENTOR_REPORT_DRAFT_SAMPLE.md) - Mẫu báo cáo hoàn chỉnh được xuất ra.


---

## 💡 7. Gợi ý đổi tên Repository

Tên hiện tại `Automation-Report-For-Leader` có thể đổi thành các tên sau để tăng tính chuyên nghiệp, chuẩn kỹ thuật quốc tế:

| Tên đề xuất | Ý nghĩa & Phù hợp |
| :--- | :--- |
| **`auto-annotation-reporter`** *(Khuyên dùng)* | Tên ngắn gọn, nêu bật chức năng báo cáo tự động cho dự án gán nhãn |
| **`cvat-mentor-report-pipeline`** | Nhấn mạnh trực tiếp vào CVAT và đối tượng nhận báo cáo là Mentor |
| **`annotation-ops-reporter`** | Chuẩn hóa theo xu hướng MLOps / DataOps trong công nghiệp AI |
| **`cvat-github-sync-reporter`** | Nhấn mạnh năng lực đồng bộ hai chiều giữa CVAT và GitHub |

---

## 👥 Nhóm phát triển & Giấy phép
* **Tác giả**: Dinh Cong Minh ([@nolanminhdinh](https://github.com/nolanminhdinh))
* **Giấy phép**: [MIT License](LICENSE)
