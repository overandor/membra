"""Tests for GitHub URL parsing."""
import pytest
from github_ingestion import GitHubIngestor


def test_parse_github_url():
    ingestor = GitHubIngestor()
    test_cases = [
        ("https://github.com/owner/repo", ("owner", "repo")),
        ("https://github.com/owner/repo.git", ("owner", "repo")),
        ("https://github.com/owner/repo/", ("owner", "repo")),
    ]
    for url, expected in test_cases:
        result = ingestor.parse_repo_url(url)
        assert result == expected


def test_parse_invalid_url():
    ingestor = GitHubIngestor()
    invalid_urls = [
        "https://notgithub.com/owner/repo",
        "https://github.com/owner",
        "invalid-url",
        "",
    ]
    for url in invalid_urls:
        with pytest.raises(ValueError):
            ingestor.parse_repo_url(url)
