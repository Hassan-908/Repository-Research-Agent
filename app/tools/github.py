import requests

from langchain.tools import tool

from app.core.config import (
    GITHUB_API_URL,
    GITHUB_API_VERSION,
    GITHUB_TOKEN,
)


def _github_headers():
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": GITHUB_API_VERSION,
    }

    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    return headers


def _validate_repo(repo: str):
    repo = repo.strip().strip("/")

    if repo.endswith(".git"):
        repo = repo[:-4]

    parts = repo.split("/")

    if len(parts) != 2 or not all(parts):
        raise ValueError(
            "Repository must be in the format 'owner/repository', "
            "for example 'facebook/react'."
        )

    return repo


def _github_get(endpoint: str, params=None):
    url = f"{GITHUB_API_URL}{endpoint}"

    try:
        response = requests.get(
            url,
            headers=_github_headers(),
            params=params,
            timeout=10,
        )

    except requests.RequestException as exc:
        raise RuntimeError(
            f"GitHub API request failed: {exc}"
        ) from exc

    if response.status_code == 404:
        raise ValueError(
            "Repository or GitHub resource was not found."
        )

    if response.status_code == 403:
        raise RuntimeError(
            "GitHub API access was forbidden or rate limited."
        )

    if response.status_code >= 400:
        try:
            error_data = response.json()
            message = error_data.get("message", "Unknown GitHub API error")
        except ValueError:
            message = response.text or "Unknown GitHub API error"

        raise RuntimeError(
            f"GitHub API returned HTTP {response.status_code}: {message}"
        )

    try:
        return response.json()

    except ValueError as exc:
        raise RuntimeError(
            "GitHub API returned malformed JSON."
        ) from exc


@tool
def get_repository_info(repo: str) -> str:
    """
    Get metadata about a GitHub repository.

    Use this tool when the user asks about repository information,
    description, stars, forks, issues, topics, license, dates,
    primary language, or general repository details.

    The repository must be provided as owner/repository.
    """

    try:
        repo = _validate_repo(repo)

        data = _github_get(f"/repos/{repo}")

        result = {
            "name": data.get("full_name"),
            "description": data.get("description"),
            "language": data.get("language"),
            "stars": data.get("stargazers_count"),
            "forks": data.get("forks_count"),
            "open_issues": data.get("open_issues_count"),
            "topics": data.get("topics", []),
            "license": (
                data.get("license", {}).get("name")
                if data.get("license")
                else None
            ),
            "created_at": data.get("created_at"),
            "updated_at": data.get("updated_at"),
            "default_branch": data.get("default_branch"),
            "html_url": data.get("html_url"),
        }

        return str(result)

    except (ValueError, RuntimeError) as exc:
        return f"ERROR: {exc}"


@tool
def get_repository_languages(repo: str) -> str:
    """
    Get the programming languages used in a GitHub repository.

    Returns the languages reported by GitHub and their byte counts.
    Use this when the user asks about the technology stack,
    programming languages, or language composition.

    The repository must be provided as owner/repository.
    """

    try:
        repo = _validate_repo(repo)

        data = _github_get(f"/repos/{repo}/languages")

        if not isinstance(data, dict):
            return "ERROR: GitHub returned an unexpected languages response."

        return str(data)

    except (ValueError, RuntimeError) as exc:
        return f"ERROR: {exc}"


@tool
def get_recent_commits(repo: str) -> str:
    """
    Get the five most recent commits from a GitHub repository.

    Returns commit messages, authors, dates, and commit URLs.
    Use this when the user asks about recent changes, recent activity,
    or what has changed recently.

    The repository must be provided as owner/repository.
    """

    try:
        repo = _validate_repo(repo)

        data = _github_get(
            f"/repos/{repo}/commits",
            params={"per_page": 5},
        )

        if not isinstance(data, list):
            return "ERROR: GitHub returned an unexpected commits response."

        commits = []

        for commit in data:
            commit_data = commit.get("commit", {})
            author_data = commit_data.get("author") or {}

            commits.append(
                {
                    "sha": commit.get("sha"),
                    "message": commit_data.get("message"),
                    "author": author_data.get("name"),
                    "date": author_data.get("date"),
                    "url": commit.get("html_url"),
                }
            )

        return str(commits)

    except (ValueError, RuntimeError) as exc:
        return f"ERROR: {exc}"