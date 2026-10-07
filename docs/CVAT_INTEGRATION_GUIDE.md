# 🔌 Hướng Dẫn Tích Hợp CVAT REST API (v2)

Tài liệu này hướng dẫn chi tiết cách cấu hình, xác thực và khai thác dữ liệu từ CVAT REST API phục vụ việc trích xuất tự động thông tin tiến độ, chất lượng và tạo Deep Links.

---

## 1. Xác thực (Authentication)

CVAT hỗ trợ 2 hình thức xác thực chính qua HTTP Request:

### 1.1. Personal Access Token (PAT) - Khuyên dùng
Tạo PAT trong giao diện người dùng CVAT: `Profile` $\rightarrow$ `Security` $\rightarrow$ `Create Token`.
Trong HTTP Header, truyền:
```http
Authorization: Token <YOUR_CVAT_PERSONAL_ACCESS_TOKEN>
```

### 1.2. Tổ chức (Organization)
Nếu instance CVAT của bạn được phân chia theo Tổ chức (Organization), bắt buộc phải thêm query parameter `org` hoặc header:
```http
X-Organization: <organization_slug>
```
Hoặc gắn kèm query parameter trong URL: `?org=your-organization`.

---

## 2. Danh mục API Endpoints sử dụng trong Pipeline

| Mục đích | Method & Endpoint | Dữ liệu trích xuất |
| :--- | :--- | :--- |
| **Thông tin Task** | `GET /api/tasks/{task_id}` | Tổng số frame, kích thước, danh sách nhãn, trạng thái task |
| **Tiến độ từng Job** | `GET /api/jobs?task_id={task_id}` | Danh sách Job ID, phân công (`assignee`), trạng thái (`annotation`, `validation`, `completed`) |
| **Báo cáo chất lượng** | `GET /api/quality/reports?task_id={task_id}` | Chỉ số chất lượng QA, số lượng đối tượng sai, tỷ lệ lỗi |
| **Ca khó & Chú thích** | `GET /api/issues?task_id={task_id}` | Các frame bị đánh dấu Issue, vị trí bounding box bị nghi ngờ, bình luận thảo luận |
| **Bình luận chi tiết** | `GET /api/comments?issue_id={issue_id}` | Nội dung trao đổi kỹ thuật giữa annotator và reviewer |

---

## 3. Cấu trúc Deep Link tới Frame cụ thể

Để giúp Mentor hoặc Leader bấm vào liên kết là mở thẳng đúng khung hình đang bị lỗi hoặc ca khó, hệ thống sử dụng quy tắc định dạng Deep Link sau:

```text
{CVAT_HOST}/tasks/{task_id}/jobs/{job_id}?frame={frame_number}
```

* **Ví dụ thực tế**:
  ```text
  https://cvat.example.org/tasks/217/jobs/1719?frame=142
  ```
* **Lưu ý**: Chỉ số frame trong URL bắt đầu từ `0` (0-indexed). Khi người dùng nhấn vào đường link này, giao diện web CVAT sẽ tự động mở đúng Job và tua trực tiếp đến frame đó.

---

## 4. Mã nguồn Python mẫu tích hợp CVAT Client

Dưới đây là module Python mẫu (`cvat_client.py`) sử dụng thư viện `requests` gọn nhẹ:

```python
import os
import requests
from typing import Dict, List, Any

class CVATClient:
    def __init__(self, host: str, token: str, org: str = None):
        self.host = host.rstrip('/')
        self.headers = {
            "Authorization": f"Token {token}",
            "Accept": "application/json"
        }
        if org:
            self.headers["X-Organization"] = org
        self.org = org

    def get_task_details(self, task_id: int) -> Dict[str, Any]:
        """Lấy thông tin tổng quan của Task."""
        url = f"{self.host}/api/tasks/{task_id}"
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def get_task_jobs(self, task_id: int) -> List[Dict[str, Any]]:
        """Lấy danh sách tất cả các Jobs thuộc Task và trạng thái."""
        url = f"{self.host}/api/jobs"
        params = {"task_id": task_id}
        if self.org:
            params["org"] = self.org
        
        jobs = []
        while url:
            resp = requests.get(url, headers=self.headers, params=params)
            resp.raise_for_status()
            data = resp.json()
            jobs.extend(data.get("results", []))
            url = data.get("next")
            params = None  # query params đã được mã hóa trong next url
        return jobs

    def get_task_issues(self, task_id: int) -> List[Dict[str, Any]]:
        """Lấy danh sách các issue/ca khó được gắn trên từng frame."""
        url = f"{self.host}/api/issues"
        params = {"task_id": task_id}
        if self.org:
            params["org"] = self.org
        
        issues = []
        resp = requests.get(url, headers=self.headers, params=params)
        if resp.status_code == 200:
            data = resp.json()
            issues = data.get("results", [])
        return issues

    def build_deep_link(self, task_id: int, job_id: int, frame: int) -> str:
        """Sinh Deep Link chuẩn trỏ thẳng vào frame trong CVAT."""
        return f"{self.host}/tasks/{task_id}/jobs/{job_id}?frame={frame}"
```

---

## 5. Xử lý lỗi thường gặp (Troubleshooting)

1. **`401 Unauthorized`**: Token bị hết hạn hoặc chuỗi Token bị sao chép thiếu ký tự. Kiểm tra biến môi trường `CVAT_TOKEN`.
2. **`403 Forbidden`**: Token không có quyền truy cập vào Project/Task hoặc thiếu header `X-Organization`.
3. **`429 Too Many Requests`**: CVAT Server bị nghẽn do gọi API quá nhanh. Trong mã nguồn cần bổ sung `time.sleep(0.2)` hoặc `backoff` retry strategy.
