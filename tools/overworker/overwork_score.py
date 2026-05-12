"""Overwork Score - weakest-link readiness scoring."""
from typing import Dict, List
from dataclasses import dataclass
from enum import Enum


class ReadinessBand(Enum):
    PRODUCTION_READY = "production_ready"
    DEMO_READY = "demo_ready"
    SCAFFOLD = "scaffold"
    PROVENANCE = "provenance"
    FRAGMENT = "fragment"


@dataclass
class OverworkScoreResult:
    score: float
    band: ReadinessBand
    weakest_link: str
    component_scores: Dict[str, float]
    recommendations: List[str]


class OverworkScorer:
    def __init__(self):
        self.weights = {
            "documentation": 0.15, "code_quality": 0.20, "security": 0.20,
            "testing": 0.15, "configuration": 0.10, "claims_verification": 0.10, "file_structure": 0.10
        }
    
    def compute_score(self, files, readme, secret_summary, gate_summary, claim_summary):
        component_scores = {
            "documentation": self._score_documentation(files, readme),
            "code_quality": self._score_code_quality(gate_summary),
            "security": self._score_security(secret_summary),
            "testing": self._score_testing(gate_summary),
            "configuration": self._score_configuration(gate_summary),
            "claims_verification": self._score_claims(claim_summary),
            "file_structure": self._score_structure(files),
        }
        total_score = sum(component_scores[k] * self.weights[k] for k in self.weights)
        weakest_link = min(component_scores, key=component_scores.get)
        band = self._get_band(total_score)
        recommendations = self._generate_recommendations(component_scores)
        return OverworkScoreResult(score=round(total_score, 3), band=band, weakest_link=weakest_link, component_scores=component_scores, recommendations=recommendations)
    
    def _score_documentation(self, files, readme):
        score = 0.0
        if readme and len(readme.strip()) > 50: score += 0.4
        if readme and len(readme.split()) > 200: score += 0.3
        if readme and any(m in readme for m in ["##", "---", "###"]): score += 0.2
        doc_files = [f for f, _ in files if f.endswith(('.md', '.rst', '.txt'))]
        if len(doc_files) > 1: score += 0.1
        return min(score, 1.0)
    
    def _score_code_quality(self, gate_summary):
        score = 1.0
        for gate in gate_summary.get("gates", []):
            if gate["name"] == "has_code" and gate["status"] == "warn": score -= 0.3
            if gate["name"] == "file_count" and gate["status"] == "warn": score -= 0.2
        return max(score, 0.0)
    
    def _score_security(self, secret_summary):
        by_severity = secret_summary.get("by_severity", {})
        if by_severity.get("CRITICAL", 0) > 0: return 0.0
        if by_severity.get("HIGH", 0) > 0: return 0.3
        if by_severity.get("MEDIUM", 0) > 0: return 0.6
        if by_severity.get("LOW", 0) > 0: return 0.8
        return 1.0
    
    def _score_testing(self, gate_summary):
        for gate in gate_summary.get("gates", []):
            if gate["name"] == "has_tests":
                if gate["status"] == "pass": return 1.0
                elif gate["status"] == "warn": return 0.5
        return 0.0
    
    def _score_configuration(self, gate_summary):
        for gate in gate_summary.get("gates", []):
            if gate["name"] == "has_config":
                if gate["status"] == "pass": return 1.0
                elif gate["status"] == "warn": return 0.5
        return 0.0
    
    def _score_claims(self, claim_summary):
        if not claim_summary: return 0.5
        return claim_summary.get("verified_ratio", 0.0)
    
    def _score_structure(self, files):
        n = len(files)
        if n < 3: return 0.2
        if n < 5: return 0.5
        if n < 10: return 0.8
        return 1.0
    
    def _get_band(self, score):
        if score >= 0.85: return ReadinessBand.PRODUCTION_READY
        elif score >= 0.70: return ReadinessBand.DEMO_READY
        elif score >= 0.50: return ReadinessBand.SCAFFOLD
        elif score >= 0.30: return ReadinessBand.PROVENANCE
        else: return ReadinessBand.FRAGMENT
    
    def _generate_recommendations(self, component_scores):
        recs = []
        if component_scores["documentation"] < 0.7: recs.append("Expand README with installation instructions and usage examples")
        if component_scores["security"] < 0.8: recs.append("Remove or redact API keys and secrets from code")
        if component_scores["testing"] < 0.7: recs.append("Add test files to verify functionality")
        if component_scores["configuration"] < 0.7: recs.append("Add configuration files (requirements.txt, package.json, etc.)")
        if component_scores["claims_verification"] < 0.5: recs.append("Add code evidence to support README claims")
        if component_scores["file_structure"] < 0.7: recs.append("Add more implementation files")
        return recs
