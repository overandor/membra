"""Verification Firewall - quality gate layer for repo analysis."""
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class GateStatus(Enum):
    PASS = "pass"
    FAIL = "fail"
    WARN = "warn"
    SKIP = "skip"


@dataclass
class VerificationGate:
    name: str
    description: str
    status: GateStatus
    message: str
    score_impact: float


class VerificationFirewall:
    def __init__(self):
        self.gates: List[VerificationGate] = []
    
    def run_all_gates(self, files, readme, secret_matches, claims):
        self.gates = []
        self._check_has_readme(readme)
        if readme: self._check_readme_substance(readme)
        self._check_has_code(files)
        self._check_critical_secrets(secret_matches)
        self._check_has_license(files)
        self._check_has_tests(files)
        self._check_has_documentation(files)
        if claims: self._check_claim_verification(claims)
        self._check_file_count(files)
        self._check_has_config(files)
        return self.gates
    
    def _check_has_readme(self, readme):
        if readme and len(readme.strip()) > 50:
            self.gates.append(VerificationGate(name="has_readme", description="Repository has a README file", status=GateStatus.PASS, message="README present with content", score_impact=0.0))
        else:
            self.gates.append(VerificationGate(name="has_readme", description="Repository has a README file", status=GateStatus.FAIL, message="README missing or too short", score_impact=-0.15))
    
    def _check_readme_substance(self, readme):
        word_count = len(readme.split())
        has_sections = any(m in readme for m in ["##", "---", "###"])
        if word_count > 100 and has_sections:
            self.gates.append(VerificationGate(name="readme_substance", description="README has substantial content", status=GateStatus.PASS, message=f"README has {word_count} words with sections", score_impact=0.0))
        else:
            self.gates.append(VerificationGate(name="readme_substance", description="README has substantial content", status=GateStatus.WARN, message=f"README has {word_count} words, could be more detailed", score_impact=-0.05))
    
    def _check_has_code(self, files):
        code_extensions = {'.py', '.js', '.ts', '.tsx', '.jsx', '.rs', '.go', '.java', '.c', '.cpp'}
        has_code = any(any(f.endswith(ext) for ext in code_extensions) for f, _ in files)
        status = GateStatus.PASS if has_code else GateStatus.WARN
        msg = "Found code files in repository" if has_code else "No code files found"
        self.gates.append(VerificationGate(name="has_code", description="Repository has code files", status=status, message=msg, score_impact=0.0 if has_code else -0.1))
    
    def _check_critical_secrets(self, secret_matches):
        critical_count = sum(1 for m in secret_matches if hasattr(m, 'secret_type') and any(x in m.secret_type for x in ['AWS', 'Key', 'Token']))
        if critical_count == 0:
            self.gates.append(VerificationGate(name="no_critical_secrets", description="No critical secrets detected", status=GateStatus.PASS, message="No critical secrets found", score_impact=0.0))
        else:
            self.gates.append(VerificationGate(name="no_critical_secrets", description="No critical secrets detected", status=GateStatus.FAIL, message=f"Found {critical_count} potential critical secrets", score_impact=-0.25))
    
    def _check_has_license(self, files):
        has_license = any(name in path.upper() for path, _ in files for name in ['LICENSE', 'COPYING'])
        status = GateStatus.PASS if has_license else GateStatus.WARN
        self.gates.append(VerificationGate(name="has_license", description="Repository has a license file", status=status, message="License file present" if has_license else "No license file found", score_impact=0.0 if has_license else -0.05))
    
    def _check_has_tests(self, files):
        has_tests = any(indicator in path.lower() for path, _ in files for indicator in ['test', 'spec', '__tests__'])
        status = GateStatus.PASS if has_tests else GateStatus.WARN
        self.gates.append(VerificationGate(name="has_tests", description="Repository has test files", status=status, message="Test files present" if has_tests else "No test files found", score_impact=0.0 if has_tests else -0.1))
    
    def _check_has_documentation(self, files):
        doc_files = [f for f, _ in files if any(f.endswith(ext) for ext in ['.md', '.rst', '.txt'])]
        if len(doc_files) > 1:
            self.gates.append(VerificationGate(name="has_documentation", description="Repository has documentation", status=GateStatus.PASS, message=f"Found {len(doc_files)} documentation files", score_impact=0.0))
        else:
            self.gates.append(VerificationGate(name="has_documentation", description="Repository has documentation", status=GateStatus.WARN, message="Limited documentation beyond README", score_impact=-0.05))
    
    def _check_claim_verification(self, claims):
        verified_count = sum(1 for c in claims if hasattr(c, 'evidence_level') and c.evidence_level.value in ['verified', 'partial'])
        ratio = verified_count / len(claims)
        status = GateStatus.PASS if ratio >= 0.5 else GateStatus.WARN
        self.gates.append(VerificationGate(name="claim_verification", description="Claims have supporting evidence", status=status, message=f"{verified_count}/{len(claims)} claims have evidence ({ratio:.0%})", score_impact=0.0 if ratio >= 0.5 else -0.1))
    
    def _check_file_count(self, files):
        n = len(files)
        status = GateStatus.PASS if n >= 5 else GateStatus.WARN
        self.gates.append(VerificationGate(name="file_count", description="Repository has sufficient files", status=status, message=f"Repository has {n} file(s)", score_impact=0.0 if n >= 5 else -0.1))
    
    def _check_has_config(self, files):
        config_files = ['package.json', 'requirements.txt', 'setup.py', 'pyproject.toml', 'Cargo.toml', 'go.mod']
        has_config = any(config in path for path, _ in files for config in config_files)
        status = GateStatus.PASS if has_config else GateStatus.WARN
        self.gates.append(VerificationGate(name="has_config", description="Repository has configuration files", status=status, message="Configuration files present" if has_config else "No configuration files found", score_impact=0.0 if has_config else -0.05))
    
    def get_summary(self):
        passed = sum(1 for g in self.gates if g.status == GateStatus.PASS)
        failed = sum(1 for g in self.gates if g.status == GateStatus.FAIL)
        warned = sum(1 for g in self.gates if g.status == GateStatus.WARN)
        skipped = sum(1 for g in self.gates if g.status == GateStatus.SKIP)
        return {
            "total_gates": len(self.gates), "passed": passed, "failed": failed, "warned": warned, "skipped": skipped,
            "score_impact": sum(g.score_impact for g in self.gates),
            "gates": [{"name": g.name, "status": g.status.value, "message": g.message, "score_impact": g.score_impact} for g in self.gates]
        }
