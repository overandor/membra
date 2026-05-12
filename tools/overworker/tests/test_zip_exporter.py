"""Tests for ZIPExporter."""
import pytest
import zipfile
import io
from zip_exporter import ZIPExporter


def test_zip_exporter_initialization():
    exporter = ZIPExporter()
    assert exporter is not None


def test_export_creates_zip():
    exporter = ZIPExporter()
    repo_url = "https://github.com/test/repo"
    owner = "test"
    repo = "repo"
    report = "# Test Report\n\nThis is a test report."
    secret_matches = []
    claims = []
    gate_summary = {"total_gates": 5, "passed": 3, "failed": 1, "warned": 1, "gates": []}
    
    class MockScoreResult:
        score = 0.75
        band = type('Band', (), {'value': 'DEMO_READY'})()
        weakest_link = "tests"
        component_scores = {"code_quality": 0.8, "documentation": 0.6}
    
    files = [("test.py", "print('hello')"), ("README.md", "# Test")]
    zip_data = exporter.export(repo_url, owner, repo, report, secret_matches, claims, gate_summary, MockScoreResult(), files)
    assert zip_data is not None
    zf = zipfile.ZipFile(io.BytesIO(zip_data))
    assert len(zf.namelist()) > 0
    assert any("report.md" in f for f in zf.namelist())
