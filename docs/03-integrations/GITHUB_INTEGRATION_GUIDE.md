# 🐙 Hướng Dẫn Tích Hợp GitHub API & Actions

Tài liệu này hướng dẫn cách cấu hình GitHub API để thu thập các câu hỏi mở, theo dõi tiến độ mã nguồn và thiết lập GitHub Actions tự động sinh báo cáo.

---

## 1. Chuẩn hóa Quy ước Nhãn (Labeling Conventions)

Để hệ thống tự động nhận diện và gom nhóm các vấn đề cần Mentor giải đáp, toàn bộ thành viên trong nhóm thống nhất sử dụng bộ nhãn chuẩn trên GitHub Issues:

| Nhãn (Label) | Màu sắc (Color) | Ý nghĩa nghiệp vụ |
| :--- | :---: | :--- |
| `ca-kho` | `#d93f0b` (Đỏ cam) | Khung hình có trường hợp biên đặc thù cần tranh biện |
| `mentor-question` | `#0075ca` (Xanh dương) | Câu hỏi trực tiếp gửi tới Mentor trong buổi họp |
| `blocker` | `#b60205` (Đỏ đậm) | Sự cố hạ tầng/quy trình làm ngưng trệ việc gán nhãn |
| `guideline-update` | `#fbca04` (Vàng) | Đề xuất sửa đổi hoặc bổ sung văn bản hướng dẫn gán nhãn |

---

## 2. Trích xuất dữ liệu qua GitHub API (v3)

Sử dụng GitHub REST API để lấy danh sách các Issue đang mở có gắn nhãn liên quan:

```http
GET https://api.github.com/repos/{owner}/{repo}/issues?state=open&labels=mentor-question,ca-kho
Authorization: Bearer <GITHUB_TOKEN>
Accept: application/vnd.github+json
```

### Python Code mẫu trích xuất GitHub Issues:

```python
import requests
from typing import List, Dict, Any

class GitHubExtractor:
    def __init__(self, token: str, repo: str):
        self.base_url = f"https://api.github.com/repos/{repo}"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json"
        }

    def get_mentor_questions(self) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/issues"
        params = {
            "state": "open",
            "labels": "mentor-question,ca-kho",
            "sort": "created",
            "direction": "desc"
        }
        resp = requests.get(url, headers=self.headers, params=params)
        resp.raise_for_status()
        
        results = []
        for issue in resp.json():
            # Bỏ qua pull requests nếu có
            if "pull_request" in issue:
                continue
            results.append({
                "number": issue["number"],
                "title": issue["title"],
                "url": issue["html_url"],
                "labels": [lbl["name"] for lbl in issue.get("labels", [])],
                "created_at": issue["created_at"],
                "body_preview": issue.get("body", "")[:200]
            })
        return results
```

---

## 3. Tự động hóa qua GitHub Actions Workflow

File cấu hình GitHub Actions nằm tại `.github/workflows/mentor_report_automation.yml`:

```yaml
name: Automated Mentor Report Generator

on:
  schedule:
    # Chạy vào 20:00 Chủ Nhật hàng tuần (UTC 13:00)
    - cron: '0 13 * * 0'
  workflow_dispatch:
    inputs:
      task_id:
        description: 'CVAT Task ID to generate report for'
        required: true
        default: '217'

jobs:
  build-report:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run Report Pipeline
        env:
          CVAT_HOST: ${{ secrets.CVAT_HOST }}
          CVAT_TOKEN: ${{ secrets.CVAT_TOKEN }}
          CVAT_TASK_ID: ${{ github.event.inputs.task_id || secrets.DEFAULT_TASK_ID }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        run: |
          python src/main.py --output reports/MENTOR_REPORT_DRAFT.md --notify telegram

      - name: Create Pull Request with Report Draft
        uses: peter-evans/create-pull-request@v6
        with:
          commit-message: "docs(report): Automated Weekly Mentor Report Draft"
          title: "📋 [Report Draft] Báo cáo tiến độ chuẩn bị gặp Mentor"
          body: |
            Bản báo cáo tự động đã được khởi tạo thành công từ số liệu CVAT & GitHub.
            Nhóm trưởng vui lòng review và bổ sung ngữ cảnh trước phiên họp!
          branch: "automated-mentor-report"
          base: "main"
```
