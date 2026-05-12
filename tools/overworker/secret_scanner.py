"""Secret scanner - detects API keys and sensitive data."""
import re
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class SecretMatch:
    file_path: str
    line_number: int
    secret_type: str
    matched_text: str
    context: str


class SecretScanner:
    PATTERNS = {
        "AWS Access Key": r'AKIA[0-9A-Z]{16}',
        "AWS Secret Key": r'[A-Za-z0-9/+=]{40}',
        "GitHub Token": r'ghp_[a-zA-Z0-9]{36}',
        "GitHub OAuth": r'(gho|ghu|ghs|ghr)_[a-zA-Z0-9]{36}',
        "Slack Token": r'xox[baprs]-[a-zA-Z0-9-]+',
        "Stripe API Key": r'sk_(live|test)_[0-9a-zA-Z]{24,}',
        "API Key (generic)": r'(?i)api[_-]?key["\']?\s*[:=]\s*["\']?[a-zA-Z0-9_\-]{20,}',
        "Secret (generic)": r'(?i)secret["\']?\s*[:=]\s*["\']?[a-zA-Z0-9_\-]{20,}',
        "Password (in code)": r'(?i)password["\']?\s*[:=]\s*["\'][^"\']{8,}["\']',
        "Private Key": r'-----BEGIN (RSA )?PRIVATE KEY-----',
        "Database URL": r'(?i)(mongodb|mysql|postgres)://[^\s"\']+',
        "JWT Token": r'eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+',
        "Email (potential contact)": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
    }
    
    def __init__(self):
        self.compiled_patterns = {name: re.compile(pattern) for name, pattern in self.PATTERNS.items()}
    
    def scan_file(self, file_path, content):
        matches = []
        lines = content.split('\n')
        for line_num, line in enumerate(lines, 1):
            for secret_type, pattern in self.compiled_patterns.items():
                match = pattern.search(line)
                if match:
                    context_start = max(0, line_num - 2)
                    context_end = min(len(lines), line_num + 3)
                    context = '\n'.join(lines[context_start:context_end])
                    matches.append(SecretMatch(file_path=file_path, line_number=line_num, secret_type=secret_type, matched_text=match.group(), context=context))
        return matches
    
    def scan_repo(self, files):
        all_matches = []
        for file_path, content in files:
            all_matches.extend(self.scan_file(file_path, content))
        return all_matches
    
    def get_severity(self, secret_type):
        critical = {"AWS Access Key", "AWS Secret Key", "GitHub Token", "Private Key", "Stripe API Key"}
        high = {"GitHub OAuth", "Slack Token", "Database URL", "JWT Token"}
        medium = {"API Key (generic)", "Secret (generic)", "Password (in code)"}
        if secret_type in critical: return "CRITICAL"
        elif secret_type in high: return "HIGH"
        elif secret_type in medium: return "MEDIUM"
        else: return "LOW"
    
    def summarize(self, matches):
        by_type = {}
        by_severity = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for match in matches:
            by_type.setdefault(match.secret_type, []).append(match.file_path)
            by_severity[self.get_severity(match.secret_type)] += 1
        return {
            "total_matches": len(matches),
            "by_type": {k: len(set(v)) for k, v in by_type.items()},
            "by_severity": by_severity,
            "files_affected": len(set(m.file_path for m in matches))
        }
