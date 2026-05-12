"""Report generator - creates Markdown reports from analysis results."""
from typing import Dict, Optional, List
from datetime import datetime


class ReportGenerator:
    def redact_secrets(self, text, secret_matches):
        if not secret_matches: return text
        redacted = text
        for match in secret_matches:
            if hasattr(match, 'secret_value') and match.secret_value in redacted:
                redacted = redacted.replace(match.secret_value, "***REDACTED***")
        return redacted
    
    def generate_report(self, repo_url, owner, repo, readme, secret_summary, claim_summary, gate_summary, overwork_score_result, files_analyzed, secret_matches=None):
        if readme and secret_matches:
            readme = self.redact_secrets(readme, secret_matches)
        
        lines = []
        lines.extend(["# Overworker Verification Report", "", f"**Repository:** {owner}/{repo}", f"**URL:** {repo_url}", f"**Generated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}", "", "---", ""])
        lines.extend(["## Executive Summary", "", f"**Overwork Score:** {overwork_score_result.score:.3f}/1.0", f"**Readiness Band:** `{overwork_score_result.band.value.upper()}`", f"**Weakest Link:** `{overwork_score_result.weakest_link}`", f"**Files Analyzed:** {files_analyzed}", ""])
        lines.extend(["### Component Scores", ""])
        for component, score in overwork_score_result.component_scores.items():
            lines.append(f"- **{component}:** {score:.2f}")
        lines.extend(["", "---", ""])
        lines.extend(["## Verification Firewall Results", "", f"**Total Gates:** {gate_summary['total_gates']}", f"**Passed:** {gate_summary['passed']}", f"**Failed:** {gate_summary['failed']}", f"**Warnings:** {gate_summary['warned']}", ""])
        for gate in gate_summary["gates"]:
            icons = {"pass": "PASS", "fail": "FAIL", "warn": "WARN", "skip": "SKIP"}
            lines.append(f"- {icons.get(gate['status'], '?')} **{gate['name']}:** {gate['message']}")
        lines.extend(["", "---", ""])
        lines.extend(["## Secret Scan Results", "", f"**Total Matches:** {secret_summary['total_matches']}", f"**Files Affected:** {secret_summary['files_affected']}", ""])
        lines.extend(["## Claim Analysis", "", f"**Total Claims:** {claim_summary.get('total_claims', 0)}", f"**Verified Ratio:** {claim_summary.get('verified_ratio', 0):.1%}", "", "---", ""])
        lines.extend(["## About Overworker", "", "Overworker is an AI execution layer that converts messy repositories into verified, inspectable, saleable assets.", ""])
        return "\n".join(lines)
