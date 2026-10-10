"""Base HTTP Client with robust retry logic, pagination handling, and security safeguards."""
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin, urlsplit

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class BaseClient:
    """Robust, authenticated HTTP client for REST APIs (CVAT, GitHub)."""

    def __init__(
        self,
        base_url: str,
        token: Optional[str] = None,
        auth_prefix: str = "Bearer",
        org: Optional[str] = None,
        timeout: tuple = (10, 60),
    ):
        self.base_url = base_url.rstrip("/") + "/"
        self.org = org
        self.timeout = timeout
        self.session = requests.Session()

        if token:
            self.session.headers.update({"Authorization": f"{auth_prefix} {token}".strip()})

        self.session.headers.setdefault("Accept", "application/json")
        if self.org:
            self.session.headers["X-Organization"] = self.org

        # Configure connection pooling & exponential backoff retry
        retries = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
            respect_retry_after_header=True,
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """Execute a secure GET request with host verification."""
        url = urljoin(self.base_url, path)
        split_url = urlsplit(url)
        split_base = urlsplit(self.base_url)

        if split_url.scheme not in ("https", "http") or split_url.netloc != split_base.netloc:
            raise ValueError(f"Unsafe API URL redirect/traversal detected: {url}")

        req_params = dict(params or {})
        if self.org is not None and "org" not in req_params:
            req_params["org"] = self.org

        response = self.session.get(
            url,
            params=req_params,
            timeout=self.timeout,
            allow_redirects=False,
        )
        if response.status_code != 200:
            raise RuntimeError(f"GET {split_url.path} failed with HTTP {response.status_code}")
        return response

    def listing(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        is_github: bool = False,
    ) -> List[Dict[str, Any]]:
        """Traverse paginated API responses safely without duplicate loops."""
        rows: List[Dict[str, Any]] = []
        seen = set()

        curr_path: Optional[str] = path
        curr_params = params

        while curr_path:
            if curr_path in seen:
                raise ValueError("Infinite pagination loop detected")
            seen.add(curr_path)

            response = self.get(curr_path, curr_params)
            payload = response.json()

            if is_github:
                if not isinstance(payload, list):
                    raise ValueError("Expected GitHub API list response")
                rows.extend(payload)
                curr_path = response.links.get("next", {}).get("url")
            else:
                if not isinstance(payload, dict) or not isinstance(payload.get("results"), list):
                    raise ValueError("Expected CVAT paginated 'results' dictionary")
                rows.extend(payload["results"])
                curr_path = payload.get("next")

            curr_params = None  # Next URL already includes required parameters

        return rows
