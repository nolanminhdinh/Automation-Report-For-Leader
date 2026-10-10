"""GitHub REST API Extractor for Issues, Discussions, and CVAT Cross-Verification."""
from datetime import datetime, timezone
import re
from typing import Any, Dict, List, Optional, Tuple

import requests

from .base_client import BaseClient
from .cvat_extractor import CVATExtractor


def extract_cvat_references(body: Optional[str]) -> Tuple[Optional[int], Optional[int], Optional[int]]:
    """
    Extract CVAT Task ID, Job ID, and optional Frame Index from issue markdown body.
    
    Returns:
        (task_id, job_id, frame_idx) as integers or None.
    Raises:
        ValueError: If duplicate or conflicting IDs are found.
    """
    text = body or ""
    results: Dict[str, Optional[int]] = {"task": None, "job": None, "frame": None}

    # Extract Task and Job IDs
    for kind in ("task", "job"):
        pattern = rf"^CVAT {kind} ID:[ \t]*(\d+)[ \t]*\r?$"
        matches = re.findall(pattern, text, re.MULTILINE | re.IGNORECASE)
        if len(matches) > 1:
            raise ValueError(f"Issue contains ambiguous multiple CVAT {kind} IDs: {matches}")
        if len(matches) == 1:
            val = int(matches[0])
            if val <= 0:
                raise ValueError(f"CVAT {kind} ID must be a positive integer: {val}")
            results[kind] = val

    # Extract Frame Index (e.g., 'Frame index (nếu có): 142', 'Frame index: 142', 'Frame: 142')
    frame_patterns = [
        r"^Frame index(?:[ \t]*\(nếu có\))?:[ \t]*(\d+)[ \t]*\r?$",
        r"^Frame(?: ID)?:[ \t]*(\d+)[ \t]*\r?$",
        r"^Khung hình:[ \t]*(\d+)[ \t]*\r?$",
    ]
    for pat in frame_patterns:
        frame_matches = re.findall(pat, text, re.MULTILINE | re.IGNORECASE)
        if frame_matches:
            results["frame"] = int(frame_matches[0])
            break

    return results["task"], results["job"], results["frame"]


def verify_issue_link(
    github_client: BaseClient,
    cvat_client: BaseClient,
    repo: str,
    issue_number: int,
) -> Dict[str, Any]:
    """Verify CVAT task/job integrity for a specific GitHub issue."""
    issue = github_client.get(f"repos/{repo}/issues/{issue_number}").json()
    if "pull_request" in issue:
        raise ValueError("Expected an issue, received a pull request")

    body = issue.get("body") or ""
    task_id, job_id, frame_idx = extract_cvat_references(body)

    if task_id is None or job_id is None:
        return {
            "github_issue": issue["number"],
            "github_url": issue["html_url"],
            "github_issue_updated_at": issue.get("updated_at"),
            "status": "unlinked",
            "relationship_verified": False,
            "frame": frame_idx,
        }

    job = cvat_client.get(f"api/jobs/{job_id}").json()
    actual_task_id = job.get("task_id")
    if not isinstance(actual_task_id, int):
        raise ValueError("CVAT response is missing an integer task_id")

    is_verified = (actual_task_id == task_id)
    return {
        "github_repo": repo,
        "github_issue": issue["number"],
        "github_url": issue["html_url"],
        "github_issue_updated_at": issue.get("updated_at"),
        "cvat_task_id": task_id,
        "cvat_job_id": job_id,
        "frame": frame_idx,
        "actual_cvat_task_id": actual_task_id,
        "relationship_verified": is_verified,
        "status": "verified" if is_verified else "mismatch",
        "verified_at": datetime.now(timezone.utc).isoformat(),
    }


class GitHubExtractor:
    """Extractor for GitHub Issues, Labels, and Comments."""

    DEFAULT_LABELS = ["ca-kho", "mentor-question", "blocker", "guideline-update"]

    def __init__(self, token: Optional[str] = None):
        self.token = token.strip() if token else None
        self.client = BaseClient(
            base_url="https://api.github.com",
            token=self.token,
            auth_prefix="Bearer",
        )
        if not self.token:
            self.client.session.headers.pop("Authorization", None)

    def get_issues(self, repo: str, state: str = "all") -> List[Dict[str, Any]]:
        """Fetch repository issues excluding pull requests."""
        root = f"repos/{repo}/issues"
        params = {"state": state, "per_page": 100}
        issues = self.client.listing(root, params=params, is_github=True)
        return [row for row in issues if "pull_request" not in row]

    def get_labels(self, repo: str) -> List[Dict[str, Any]]:
        """Fetch repository labels."""
        return self.client.listing(f"repos/{repo}/labels", {"per_page": 100}, is_github=True)

    def get_comments(self, repo: str, issue_number: int) -> List[Dict[str, Any]]:
        """Fetch discussion comments for an issue."""
        return self.client.listing(
            f"repos/{repo}/issues/{issue_number}/comments",
            {"per_page": 100},
            is_github=True,
        )

    def extract_snapshot(self, repo: str) -> Dict[str, Any]:
        """Collect all issues, labels, and issue comments for a snapshot."""
        issues = self.get_issues(repo, state="all")
        labels = self.get_labels(repo)
        comments: List[Dict[str, Any]] = []

        for issue in issues:
            try:
                num = issue.get("number")
                if num:
                    comments.extend(self.get_comments(repo, num))
            except Exception:
                pass

        return {
            "issues": issues,
            "labels": labels,
            "comments": comments,
        }

    def link_issues(
        self,
        issues: List[Dict[str, Any]],
        cvat_extractor: Optional[CVATExtractor],
        cvat_jobs: Optional[List[Dict[str, Any]]] = None,
    ) -> List[Dict[str, Any]]:
        """Verify cross-system links between GitHub issues and CVAT jobs."""
        cache: Dict[int, Dict[str, Any]] = {
            job["id"]: job for job in (cvat_jobs or []) if "id" in job
        }
        links: List[Dict[str, Any]] = []

        for issue in issues:
            row: Dict[str, Any] = {
                "github_issue": issue["number"],
                "github_url": issue["html_url"],
                "github_issue_updated_at": issue.get("updated_at"),
            }
            body = issue.get("body") or ""

            try:
                task_id, job_id, frame_idx = extract_cvat_references(body)
            except ValueError as err:
                row.update(status="invalid_reference", error=str(err))
                links.append(row)
                continue

            if task_id is None and job_id is None:
                row.update(status="unlinked", frame=frame_idx)
                links.append(row)
                continue

            if task_id is None or job_id is None:
                row.update(
                    status="invalid_reference",
                    error="Issue must contain both CVAT task ID and CVAT job ID",
                    frame=frame_idx,
                )
                links.append(row)
                continue

            row.update(cvat_task_id=task_id, cvat_job_id=job_id, frame=frame_idx)

            if cvat_extractor is None:
                row.update(status="verification_failed", error="CVAT extractor unavailable")
                links.append(row)
                continue

            try:
                if job_id not in cache:
                    cache[job_id] = cvat_extractor.client.get(f"api/jobs/{job_id}").json()

                actual = cache[job_id].get("task_id")
                if not isinstance(actual, int):
                    raise ValueError("Job response missing integer task_id")

                is_verified = (actual == task_id)
                row.update(
                    actual_cvat_task_id=actual,
                    relationship_verified=is_verified,
                    status="verified" if is_verified else "mismatch",
                )
            except (requests.RequestException, RuntimeError, ValueError, KeyError) as error:
                row.update(status="verification_failed", error_type=type(error).__name__)

            links.append(row)

        return links
