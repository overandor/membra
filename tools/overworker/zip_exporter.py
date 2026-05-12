"""ZIP exporter - packages analysis results into downloadable ZIP."""
import zipfile
import io
from typing import Dict, List
from datetime import datetime


class ZIPExporter:
    def export(self, repo_url, owner, repo, report_markdown, secret_matches, claims, gate_summary, overwork_score_result, files):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.writestr(f"{repo}_overworker_report.md", report_markdown)
            zipf.writestr(f"{repo}_summary.json", self._create_json_summary(repo_url, owner, repo, gate_summary, overwork_score_result))
            if secret_matches:
                zipf.writestr(f"{repo}_secrets.txt", self._create_secret_report(secret_matches))
            if claims:
                zipf.writestr(f"{repo}_claims.txt", self._create_claims_report(claims))
            zipf.writestr(f"{repo}_gates.txt", self._create_gate_report(gate_summary))
            zipf.writestr(f"{repo}_files.txt", self._create_file_inventory(files))
            zipf.writestr("metadata.txt", self._create_metadata(repo_url, owner, repo))
        zip_buffer.seek(0)
        return zip_buffer.getvalue()
    
    def _create_json_summary(self, repo_url, owner, repo, gate_summary, overwork_score_result):
        import json
        return json.dumps({"repository": {"url": repo_url, "owner": owner, "name": repo}, "timestamp": datetime.utcnow().isoformat(), "overwork_score": {"score": overwork_score_result.score, "band": overwork_score_result.band.value, "weakest_link": overwork_score_result.weakest_link, "component_scores": overwork_score_result.component_scores}, "verification_firewall": {"total_gates": gate_summary["total_gates"], "passed": gate_summary["passed"], "failed": gate_summary["failed"], "warned": gate_summary["warned"]}}, indent=2)
    
    def _create_secret_report(self, secret_matches):
        lines = ["SECRET SCAN RESULTS", "=" * 50, ""]
        for match in secret_matches:
            redacted = match.matched_text[:4] + "****" + match.matched_text[-4:] if len(match.matched_text) > 10 else "*" * len(match.matched_text)
            lines.extend([f"File: {match.file_path}", f"Line: {match.line_number}", f"Type: {match.secret_type}", f"Matched: {redacted}", "-" * 30, ""])
        return "\n".join(lines)
    
    def _create_claims_report(self, claims):
        lines = ["CLAIM ANALYSIS", "=" * 50, ""]
        for claim in claims:
            lines.extend([f"Line {claim.line_number}: {claim.text}", f"Category: {claim.category.value}", f"Evidence: {claim.evidence_level.value}", ""])
        return "\n".join(lines)
    
    def _create_gate_report(self, gate_summary):
        lines = ["VERIFICATION FIREWALL RESULTS", "=" * 50, "", f"Total Gates: {gate_summary['total_gates']}", f"Passed: {gate_summary['passed']}", f"Failed: {gate_summary['failed']}", f"Warned: {gate_summary['warned']}", "", "Gate Details:", "-" * 30, ""]
        for gate in gate_summary["gates"]:
            lines.extend([f"{gate['name']}: {gate['status'].upper()}", f"  {gate['message']}", ""])
        return "\n".join(lines)
    
    def _create_file_inventory(self, files):
        lines = ["FILE INVENTORY", "=" * 50, ""]
        for file_path, content in files:
            lines.append(f"{file_path} ({len(content)} bytes)")
        lines.extend(["", f"Total files: {len(files)}"])
        return "\n".join(lines)
    
    def _create_metadata(self, repo_url, owner, repo):
        return "\n".join(["OVERWORKER PACKAGE METADATA", "=" * 50, "", f"Repository: {owner}/{repo}", f"URL: {repo_url}", f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}"])
