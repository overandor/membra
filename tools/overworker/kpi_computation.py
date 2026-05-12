"""KPI computation engine."""
from typing import List, Dict, Tuple
from dataclasses import dataclass
import re


@dataclass
class KPI:
    name: str
    value: float
    unit: str
    description: str
    category: str


@dataclass
class KPIReport:
    kpis: List[KPI]
    overall_score: float
    metadata: Dict


class KPIEngine:
    def compute_kpis(self, files, tokenized_repo, readme=None):
        kpis = []
        kpis.extend(self._compute_code_quality_kpis(files))
        kpis.extend(self._compute_activity_kpis(files))
        kpis.extend(self._compute_complexity_kpis(files, tokenized_repo))
        kpis.extend(self._compute_documentation_kpis(files, readme))
        kpis.extend(self._compute_maintainability_kpis(files))
        kpis.append(self._compute_liquidity_kpi(files, tokenized_repo))
        kpis.append(self._compute_endpoint_kpi(tokenized_repo))
        overall_score = self._compute_overall_score(kpis)
        return KPIReport(kpis=kpis, overall_score=overall_score, metadata={"total_kpis": len(kpis), "categories": set(k.category for k in kpis)})
    
    def _compute_code_quality_kpis(self, files):
        total_loc = sum(len(c.split('\n')) for _, c in files)
        code_files = [f for f, _ in files if self._is_code_file(f)]
        code_density = len(code_files) / len(files) if files else 0
        return [
            KPI(name="lines_of_code", value=total_loc, unit="lines", description="Total lines of code", category="code_quality"),
            KPI(name="code_density", value=code_density, unit="ratio", description="Ratio of code files", category="code_quality"),
        ]
    
    def _compute_activity_kpis(self, files):
        total_size = sum(len(c) for _, c in files)
        avg_size = total_size / len(files) if files else 0
        return [
            KPI(name="file_count", value=len(files), unit="files", description="Total files", category="activity"),
            KPI(name="avg_file_size", value=avg_size, unit="bytes", description="Average file size", category="activity"),
        ]
    
    def _compute_complexity_kpis(self, files, tokenized_repo):
        kpis = []
        if tokenized_repo and tokenized_repo.unique_tokens > 0:
            diversity = tokenized_repo.unique_tokens / tokenized_repo.total_tokens
            kpis.append(KPI(name="token_diversity", value=diversity, unit="ratio", description="Token diversity", category="complexity"))
        func_count = sum(1 for _, c in files for line in c.split('\n') if re.search(r'def\s+\w+|function\s+\w+', line))
        kpis.append(KPI(name="function_count", value=func_count, unit="functions", description="Total functions", category="complexity"))
        return kpis
    
    def _compute_documentation_kpis(self, files, readme=None):
        has_readme = 1.0 if readme and len(readme) > 100 else 0.0
        doc_files = [f for f, _ in files if f.endswith(('.md', '.rst', '.txt'))]
        doc_ratio = len(doc_files) / len(files) if files else 0
        return [
            KPI(name="readme_coverage", value=has_readme, unit="ratio", description="Has README", category="documentation"),
            KPI(name="documentation_ratio", value=doc_ratio, unit="ratio", description="Doc files ratio", category="documentation"),
        ]
    
    def _compute_maintainability_kpis(self, files):
        test_files = [f for f, _ in files if 'test' in f.lower()]
        test_ratio = len(test_files) / len(files) if files else 0
        config_files = [f for f, _ in files if f.endswith(('.json', '.yaml', '.yml', '.toml'))]
        has_config = 1.0 if config_files else 0.0
        return [
            KPI(name="test_coverage_indicator", value=test_ratio, unit="ratio", description="Test files ratio", category="maintainability"),
            KPI(name="has_config", value=has_config, unit="ratio", description="Has config files", category="maintainability"),
        ]
    
    def _compute_liquidity_kpi(self, files, tokenized_repo):
        test_files = [f for f, _ in files if 'test' in f.lower()]
        test_score = min(len(test_files) / max(len(files), 1) * 2, 1.0)
        doc_files = [f for f, _ in files if f.endswith(('.md', '.rst'))]
        doc_score = min(len(doc_files) / max(len(files), 1) * 3, 1.0)
        config_files = [f for f, _ in files if f.endswith(('.json', '.yaml', '.yml'))]
        config_score = 1.0 if config_files else 0.5
        endpoint_score = 0.0
        if tokenized_repo:
            endpoints = [t for t in tokenized_repo.tokens if t.type == 'endpoint']
            endpoint_score = min(len(endpoints) / 10, 1.0)
        liquidity = test_score * 0.3 + doc_score * 0.3 + config_score * 0.2 + endpoint_score * 0.2
        return KPI(name="liquidity_score", value=liquidity, unit="ratio", description="Liquidity score", category="liquidity")
    
    def _compute_endpoint_kpi(self, tokenized_repo):
        if not tokenized_repo:
            return KPI(name="endpoint_count", value=0, unit="endpoints", description="API endpoints", category="e_service")
        endpoints = [t for t in tokenized_repo.tokens if t.type == 'endpoint']
        return KPI(name="endpoint_count", value=len(endpoints), unit="endpoints", description="API endpoints", category="e_service")
    
    def _compute_overall_score(self, kpis):
        if not kpis: return 0.0
        category_weights = {"code_quality": 0.2, "activity": 0.15, "complexity": 0.15, "documentation": 0.2, "maintainability": 0.15, "liquidity": 0.15}
        weighted_sum = 0.0
        total_weight = 0.0
        for kpi in kpis:
            weight = category_weights.get(kpi.category, 0.1)
            normalized = min(kpi.value, 1.0) if kpi.unit == "ratio" else min(kpi.value / 1000, 1.0)
            weighted_sum += normalized * weight
            total_weight += weight
        return weighted_sum / total_weight if total_weight > 0 else 0.0
    
    def _is_code_file(self, file_path):
        return any(file_path.endswith(e) for e in ['.py', '.js', '.ts', '.tsx', '.jsx', '.rs', '.go', '.java', '.rb', '.php'])
