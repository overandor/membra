"""Endpoint appraisal - detects and appraises endpoints as e-services."""
import re
from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class EndpointCategory(Enum):
    DATA = "data"
    AUTH = "auth"
    COMPUTE = "compute"
    STORAGE = "storage"
    NOTIFICATION = "notification"
    WEBHOOK = "webhook"
    ADMIN = "admin"
    UNKNOWN = "unknown"


@dataclass
class AppraisedEndpoint:
    path: str
    method: HttpMethod
    category: EndpointCategory
    complexity_score: float
    value_score: float
    liquidity_score: float
    appraisal_value: float
    metadata: Dict


@dataclass
class EServiceAppraisal:
    endpoints: List[AppraisedEndpoint]
    total_value: float
    avg_value: float
    liquidity_index: float
    metadata: Dict


class EndpointAppraiser:
    """Detects and appraises endpoints as e-services."""
    
    def __init__(self):
        self.patterns = {
            'flask': [
                r'@app\.route\([\'"]([\'"]+)[\'"]\)',
                r'@app\.(get|post|put|delete)\([\'"]([\'"]+)[\'"]\)',
            ],
            'fastapi': [
                r'@app\.(get|post|put|delete|patch)\([\'"]([\'"]+)[\'"]\)',
            ],
            'express': [
                r'app\.(get|post|put|delete|patch)\([\'"]([\'"]+)[\'"]\)',
            ],
            'django': [
                r'path\([\'"]([\'"]+)[\'"]\)',
            ],
        }
    
    def appraise_endpoints(self, files, tokenized_repo):
        endpoints = []
        for file_path, content in files:
            file_endpoints = self._detect_endpoints_in_file(file_path, content)
            endpoints.extend(file_endpoints)
        
        unique_endpoints = self._deduplicate_endpoints(endpoints)
        appraised = [self._appraise_endpoint(e, files, tokenized_repo) for e in unique_endpoints]
        
        total_value = sum(e.appraisal_value for e in appraised)
        avg_value = total_value / len(appraised) if appraised else 0
        liquidity_index = sum(e.liquidity_score for e in appraised) / len(appraised) if appraised else 0
        
        return EServiceAppraisal(
            endpoints=appraised,
            total_value=total_value,
            avg_value=avg_value,
            liquidity_index=liquidity_index,
            metadata={"total_endpoints": len(appraised), "categories": set(e.category.value for e in appraised)}
        )
    
    def _detect_endpoints_in_file(self, file_path, content):
        endpoints = []
        lines = content.split('\n')
        for line_num, line in enumerate(lines, 1):
            for framework, patterns in self.patterns.items():
                for pattern in patterns:
                    match = re.search(pattern, line)
                    if match:
                        if framework in ('fastapi', 'express'):
                            method_str = match.group(1)
                            path = match.group(2)
                            method = HttpMethod(method_str.upper())
                        else:
                            path = match.group(1) if match.groups() else match.group(0)
                            method = HttpMethod.GET
                        endpoints.append({"path": path, "method": method, "file": file_path, "line": line_num})
                        break
        return endpoints
    
    def _deduplicate_endpoints(self, endpoints):
        seen = set()
        unique = []
        for e in endpoints:
            key = (e["path"], e["method"])
            if key not in seen:
                seen.add(key)
                unique.append(e)
        return unique
    
    def _appraise_endpoint(self, endpoint, files, tokenized_repo):
        path = endpoint["path"]
        method = endpoint["method"]
        category = self._categorize_endpoint(path)
        complexity = min(path.count('/') / 5 + (0.2 if '{' in path else 0), 1.0)
        
        category_values = {
            EndpointCategory.AUTH: 0.8, EndpointCategory.DATA: 0.6,
            EndpointCategory.COMPUTE: 0.7, EndpointCategory.STORAGE: 0.5,
            EndpointCategory.NOTIFICATION: 0.4, EndpointCategory.ADMIN: 0.3,
            EndpointCategory.UNKNOWN: 0.2,
        }
        value = min(category_values.get(category, 0.2) * (1 + complexity * 0.5), 1.0)
        
        high_liq = {EndpointCategory.DATA, EndpointCategory.COMPUTE, EndpointCategory.AUTH}
        liquidity = 0.8 if category in high_liq else (0.6 if category == EndpointCategory.STORAGE else 0.5 if category == EndpointCategory.NOTIFICATION else 0.3)
        
        return AppraisedEndpoint(
            path=path, method=method, category=category,
            complexity_score=complexity, value_score=value,
            liquidity_score=liquidity, appraisal_value=value * complexity * liquidity,
            metadata={"file": endpoint.get("file"), "line": endpoint.get("line")}
        )
    
    def _categorize_endpoint(self, path):
        p = path.lower()
        if any(x in p for x in ['login', 'register', 'auth', 'token', 'oauth']): return EndpointCategory.AUTH
        elif any(x in p for x in ['data', 'query', 'search', 'list', 'get']): return EndpointCategory.DATA
        elif any(x in p for x in ['compute', 'process', 'calculate', 'transform']): return EndpointCategory.COMPUTE
        elif any(x in p for x in ['upload', 'download', 'file', 'storage', 's3']): return EndpointCategory.STORAGE
        elif any(x in p for x in ['notify', 'webhook', 'callback', 'event']): return EndpointCategory.NOTIFICATION
        elif any(x in p for x in ['admin', 'manage', 'config', 'settings']): return EndpointCategory.ADMIN
        else: return EndpointCategory.UNKNOWN
