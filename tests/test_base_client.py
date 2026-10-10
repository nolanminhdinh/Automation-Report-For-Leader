import unittest
from unittest.mock import Mock, patch

from src.extractors.base_client import BaseClient


class BaseClientTests(unittest.TestCase):
    def test_client_init_headers(self):
        client = BaseClient(base_url="https://api.cvat.ai", token="test-token", auth_prefix="Token", org="vinai")
        self.assertEqual(client.session.headers.get("Authorization"), "Token test-token")
        self.assertEqual(client.session.headers.get("X-Organization"), "vinai")

    def test_unsafe_redirect_rejected(self):
        client = BaseClient(base_url="https://api.cvat.ai", token="test-token")
        with self.assertRaises(ValueError):
            client.get("https://malicious.site/api/jobs")

    def test_cvat_pagination(self):
        client = BaseClient(base_url="https://api.cvat.ai", token="test-token")
        with patch.object(client, "get") as mock_get:
            res1 = Mock()
            res1.json.return_value = {"results": [{"id": 1}], "next": "api/jobs?page=2"}
            res2 = Mock()
            res2.json.return_value = {"results": [{"id": 2}], "next": None}
            mock_get.side_effect = [res1, res2]

            items = client.listing("api/jobs")
            self.assertEqual(len(items), 2)
            self.assertEqual([i["id"] for i in items], [1, 2])


if __name__ == "__main__":
    unittest.main()
