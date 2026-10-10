import unittest
from unittest.mock import Mock

from src.extractors.github_extractor import (
    GitHubExtractor,
    extract_cvat_references,
    verify_issue_link,
)


class GitHubExtractorTests(unittest.TestCase):
    def test_extract_references_with_frame(self):
        body = (
            "Tham chiếu:\r\n"
            "CVAT task ID: 2592622\r\n"
            "CVAT job ID: 4475446\r\n"
            "Frame index (nếu có): 142\r\n"
            "Mô tả lỗi: Xe bị che khuất."
        )
        task_id, job_id, frame_idx = extract_cvat_references(body)
        self.assertEqual(task_id, 2592622)
        self.assertEqual(job_id, 4475446)
        self.assertEqual(frame_idx, 142)

    def test_extract_references_without_frame(self):
        body = "CVAT task ID: 1001\nCVAT job ID: 2002\n"
        task_id, job_id, frame_idx = extract_cvat_references(body)
        self.assertEqual(task_id, 1001)
        self.assertEqual(job_id, 2002)
        self.assertIsNone(frame_idx)

    def test_extract_references_ambiguous_raises(self):
        body = "CVAT task ID: 1\nCVAT task ID: 2\nCVAT job ID: 3\n"
        with self.assertRaises(ValueError):
            extract_cvat_references(body)

    def test_verify_issue_link_success(self):
        gh_client = Mock()
        cvat_client = Mock()

        gh_client.get.return_value.json.return_value = {
            "number": 10,
            "html_url": "https://github.com/org/repo/issues/10",
            "body": "CVAT task ID: 100\nCVAT job ID: 200\nFrame index: 55",
            "updated_at": "2026-10-10T12:00:00Z",
        }
        cvat_client.get.return_value.json.return_value = {
            "id": 200,
            "task_id": 100,
        }

        res = verify_issue_link(gh_client, cvat_client, "org/repo", 10)
        self.assertTrue(res["relationship_verified"])
        self.assertEqual(res["status"], "verified")
        self.assertEqual(res["frame"], 55)

    def test_verify_issue_link_mismatch(self):
        gh_client = Mock()
        cvat_client = Mock()

        gh_client.get.return_value.json.return_value = {
            "number": 11,
            "html_url": "https://github.com/org/repo/issues/11",
            "body": "CVAT task ID: 100\nCVAT job ID: 200",
            "updated_at": "2026-10-10T12:00:00Z",
        }
        cvat_client.get.return_value.json.return_value = {
            "id": 200,
            "task_id": 999,  # Mismatch!
        }

        res = verify_issue_link(gh_client, cvat_client, "org/repo", 11)
        self.assertFalse(res["relationship_verified"])
        self.assertEqual(res["status"], "mismatch")


if __name__ == "__main__":
    unittest.main()
