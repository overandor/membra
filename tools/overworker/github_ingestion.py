"""GitHub repo ingestion - fetches public repo text files using git."""
import subprocess
import tempfile
import shutil
import os
from typing import List, Optional
import re
from dataclasses import dataclass


@dataclass
class RepoFile:
    path: str
    content: str
    size: int


@dataclass
class RepoStructure:
    owner: str
    repo: str
    files: List[RepoFile]
    readme: Optional[str] = None


class GitHubIngestor:
    """Fetches and parses GitHub repositories using git."""
    
    def __init__(self):
        pass
    
    async def close(self):
        pass
    
    def parse_repo_url(self, url: str) -> tuple[str, str]:
        patterns = [
            r"github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$",
            r"github\.com/([^/]+)/([^/]+)$",
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                owner, repo = match.groups()
                return owner, repo
        raise ValueError(f"Invalid GitHub URL: {url}")
    
    def is_text_file(self, path: str) -> bool:
        text_extensions = {
            '.py', '.js', '.ts', '.tsx', '.jsx', '.md', '.txt', '.json', '.yaml', '.yml',
            '.toml', '.cfg', '.ini', '.sh', '.bash', '.zsh', '.rs', '.go', '.java',
            '.c', '.cpp', '.h', '.hpp', '.css', '.html', '.xml', '.sql', '.rb', '.php'
        }
        for ext in text_extensions:
            if path.endswith(ext):
                return True
        text_filenames = {'README', 'LICENSE', 'CONTRIBUTING', 'CHANGELOG', 'Makefile'}
        if any(path.upper().endswith(name) for name in text_filenames):
            return True
        return False
    
    async def ingest_repo(self, url: str, max_files: int = 1000, max_total_bytes: int = 50_000_000) -> RepoStructure:
        owner, repo = self.parse_repo_url(url)
        temp_dir = tempfile.mkdtemp()
        try:
            repo_url = f"https://github.com/{owner}/{repo}.git"
            subprocess.run(
                ["git", "clone", "--depth", "1", repo_url, temp_dir],
                check=True, capture_output=True, timeout=60
            )
            files = []
            readme_content = None
            total_bytes = 0
            
            for root, dirs, dir_files in os.walk(temp_dir):
                dirs[:] = [d for d in dirs if d != '.git']
                for file in dir_files:
                    if len(files) >= max_files:
                        break
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, temp_dir)
                    if self.is_text_file(rel_path):
                        try:
                            size = os.path.getsize(full_path)
                            if size > 100000 or total_bytes + size > max_total_bytes:
                                continue
                            total_bytes += size
                            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                            files.append(RepoFile(path=rel_path, content=content, size=len(content)))
                            if "README" in rel_path.upper():
                                readme_content = content
                        except (OSError, UnicodeDecodeError):
                            pass
            
            return RepoStructure(owner=owner, repo=repo, files=files, readme=readme_content)
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
