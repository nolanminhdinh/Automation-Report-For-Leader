import unittest

from src.generators.markdown_generator import format_vn_time, render_mentor_report


class ReportGeneratorTests(unittest.TestCase):
    def test_format_vn_time(self):
        utc_ts = "2026-10-10T12:00:00Z"
        vn_time = format_vn_time(utc_ts)
        self.assertIn("19:00:00", vn_time)
        self.assertIn("10/10/2026", vn_time)
        self.assertIn("(UTC+7)", vn_time)

    def test_render_four_sections(self):
        mock_data = {
            "metadata": {
                "mentor_session": "Phiên 1",
                "snapshot": "data/raw/123",
                "snapshot_started_at": "2026-10-10T00:00:00Z",
                "generated_at": "2026-10-10T01:00:00Z",
                "warnings": ["Warning test"],
            },
            "batch_progress": {
                "status": "available",
                "task_id": 1001,
                "task_name": "Batch A",
                "total_frames": 200,
                "jobs": [
                    {
                        "job_id": 1,
                        "type": "annotation",
                        "stage": "annotation",
                        "state": "completed",
                        "assignee": "tuan",
                        "frame_count": 100,
                        "source_url": "https://cvat/tasks/1001/jobs/1",
                    }
                ],
                "annotation_job_count": 1,
                "completed_annotation_job_count": 1,
                "completed_annotation_job_percent": 100.0,
            },
            "scores": {
                "status": "unavailable",
                "reason": "Chưa có điểm.",
            },
            "annotations": {
                "status": "available",
                "totals": {"shapes": 10, "tracks": 2, "tags": 0, "track_shape_records": 4},
                "by_label": [{"label_id": 1, "label_name": "car", "shapes": 10, "tracks": 2, "tags": 0}],
            },
            "edge_cases": {
                "status": "available",
                "items": [
                    {
                        "number": 5,
                        "title": "Xe bị lấp",
                        "author": "minh",
                        "frame": 142,
                        "source_url": "https://github/issue/5",
                        "cvat_job_url": "https://cvat/tasks/1001/jobs/1?frame=142",
                        "description": "Chi tiết lỗi xe",
                    }
                ],
            },
            "open_questions": {
                "status": "available",
                "items": [
                    {
                        "number": 6,
                        "title": "Hỏi guideline",
                        "author": "duy",
                        "source_url": "https://github/issue/6",
                        "description": "Câu hỏi về guideline",
                    }
                ],
            },
        }

        md = render_mentor_report(mock_data)
        self.assertIn("## 1. 📊 Tiến độ Batch & Vận Tốc Gán Nhãn", md)
        self.assertIn("## 2. 🎯 Chất lượng & Điểm QA/QC", md)
        self.assertIn("## 3. 🔍 Danh Sách Ca Khó & Trường Hợp Biên (Edge Cases)", md)
        self.assertIn("## 4. 💬 Câu Hỏi Mở Cần Mentor Định Đoạt (Open Questions)", md)
        self.assertIn("Frame 142", md)
        self.assertIn("https://cvat/tasks/1001/jobs/1?frame=142", md)


if __name__ == "__main__":
    unittest.main()
