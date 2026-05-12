"""Overworker - AI execution layer for GitHub repo verification."""
import os
import subprocess
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel
import stripe
from github_ingestion import GitHubIngestor, RepoStructure
from secret_scanner import SecretScanner, SecretMatch
from claim_labeler import ClaimLabeler, Claim
from verification_firewall import VerificationFirewall
from overwork_score import OverworkScorer
from tokenization import TokenizedRepo
from kpi_computation import KPIEngine, KPIReport
from endpoint_appraisal import EndpointAppraiser, EServiceAppraisal
from inverse_derivative import DerivativePortfolio, InverseDerivativeEngine
from report_generator import ReportGenerator
from zip_exporter import ZIPExporter


class RepoRequest(BaseModel):
    url: str

    def validate_github_url(self):
        import re
        pattern = r'^https://github\.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+/?$'
        if not re.match(pattern, self.url):
            raise ValueError("URL must be a valid GitHub repository URL (e.g., https://github.com/owner/repo)")
        return True


app = FastAPI()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_placeholder")
STRIPE_PRICE_ID = os.getenv("STRIPE_PRICE_ID", "price_placeholder")


@app.get("/", response_class=HTMLResponse)
async def dashboard():
    template_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/features", response_class=HTMLResponse)
async def features():
    template_path = os.path.join(os.path.dirname(__file__), "templates", "features.html")
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/pricing", response_class=HTMLResponse)
async def pricing():
    template_path = os.path.join(os.path.dirname(__file__), "templates", "pricing.html")
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/about", response_class=HTMLResponse)
async def about():
    template_path = os.path.join(os.path.dirname(__file__), "templates", "about.html")
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/contact", response_class=HTMLResponse)
async def contact():
    template_path = os.path.join(os.path.dirname(__file__), "templates", "contact.html")
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/docs-page", response_class=HTMLResponse)
async def docs():
    template_path = os.path.join(os.path.dirname(__file__), "templates", "docs.html")
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/static/styles.css")
async def styles_css():
    css_path = os.path.join(os.path.dirname(__file__), "templates", "styles.css")
    from fastapi.responses import FileResponse
    return FileResponse(css_path, media_type="text/css")


class CheckoutRequest(BaseModel):
    plan_id: str


@app.post("/create-checkout-session")
async def create_checkout_session(request_data: CheckoutRequest):
    try:
        plans = {
            "starter": {"price": 0, "name": "Starter"},
            "professional": {"price": 2900, "name": "Professional"},
            "enterprise": {"price": 9900, "name": "Enterprise"}
        }
        plan = plans.get(request_data.plan_id)
        if not plan:
            raise HTTPException(status_code=400, detail="Invalid plan ID")
        if plan["price"] == 0:
            return {"url": None, "free": True}
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price_data": {"currency": "usd", "product_data": {"name": f"Overworker {plan['name']} Plan"}, "unit_amount": plan["price"]}, "quantity": 1}],
            mode="payment",
            success_url="https://huggingface.co/spaces/luguog/overworker?success=true",
            cancel_url="https://huggingface.co/spaces/luguog/overworker?canceled=true",
        )
        return {"url": checkout_session.url, "free": False}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def is_local_directory(path: str) -> bool:
    return os.path.isdir(path) and not path.startswith("http")


def extract_readme(files: list) -> str:
    for file in files:
        if "README" in file.path.upper():
            return file.content
    return None


# In-memory ZIP storage
zip_storage = {}


@app.post("/analyze")
async def analyze_repo(request: RepoRequest):
    try:
        request.validate_github_url()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    ingestor = GitHubIngestor()
    secret_scanner = SecretScanner()
    claim_labeler = ClaimLabeler()
    firewall = VerificationFirewall()
    score_engine = OverworkScorer()
    report_gen = ReportGenerator()
    zip_exporter = ZIPExporter()
    kpi_engine = KPIEngine()
    endpoint_appraiser = EndpointAppraiser()
    derivative_engine = InverseDerivativeEngine()

    try:
        repo_structure: RepoStructure = await ingestor.ingest_repo(request.url)
        files = [(f.path, f.content) for f in repo_structure.files]

        secret_matches = secret_scanner.scan_repo(files)
        secret_summary = secret_scanner.summarize(secret_matches)

        claims = claim_labeler.label_all_claims(repo_structure.readme, files)
        claim_summary = claim_labeler.summarize(claims)

        firewall.run_all_gates(files, repo_structure.readme, secret_matches, claims)
        gate_summary = firewall.get_summary()

        score_result = score_engine.compute_score(files, repo_structure.readme, secret_summary, gate_summary, claim_summary)

        from tokenization import RepoTokenizer
        tokenizer = RepoTokenizer()
        tokenized_repo: TokenizedRepo = tokenizer.tokenize_repo(files)

        kpi_report: KPIReport = kpi_engine.compute_kpis(files, tokenized_repo, repo_structure.readme)
        e_service_appraisal: EServiceAppraisal = endpoint_appraiser.appraise_endpoints(files, tokenized_repo)
        derivative_portfolio: DerivativePortfolio = derivative_engine.create_inverse_derivatives(e_service_appraisal)

        report = report_gen.generate_report(
            request.url, repo_structure.owner, repo_structure.repo,
            repo_structure.readme, secret_summary, claim_summary,
            gate_summary, score_result, len(files), secret_matches
        )

        zip_data = zip_exporter.export(
            request.url, repo_structure.owner, repo_structure.repo,
            report, secret_matches, claims, gate_summary, score_result, files
        )

        zip_filename = f"{repo_structure.repo}_overworker_package_{int(time.time())}.zip"
        zip_storage[zip_filename] = {"data": zip_data, "timestamp": time.time(), "repo_url": request.url}

        return {
            "score": score_result.score,
            "band": score_result.band.value,
            "weakest_link": score_result.weakest_link,
            "component_scores": score_result.component_scores,
            "recommendations": score_result.recommendations,
            "files_analyzed": len(files),
            "secret_summary": secret_summary,
            "claim_summary": claim_summary,
            "kpi_report": {"kpis": [{"name": k.name, "value": k.value, "unit": k.unit, "category": k.category} for k in kpi_report.kpis], "overall_score": kpi_report.overall_score},
            "e_service_appraisal": {"total_endpoints": e_service_appraisal.metadata.get("total_endpoints", 0), "total_value": e_service_appraisal.total_value, "avg_value": e_service_appraisal.avg_value, "liquidity_index": e_service_appraisal.liquidity_index},
            "derivative_portfolio": {"total_tokens": len(derivative_portfolio.tokens), "total_notional": derivative_portfolio.total_notional, "weighted_inverse_value": derivative_portfolio.weighted_inverse_value, "risk_score": derivative_portfolio.risk_score, "pricing": derivative_engine.compute_derivative_pricing(derivative_portfolio)},
            "zip_url": f"/download/{zip_filename}",
            "filename": zip_filename
        }
    except Exception as e:
        import traceback
        return {"error": f"Analysis failed: {str(e)}", "details": traceback.format_exc()}
    finally:
        try:
            await ingestor.close()
        except Exception:
            pass


@app.get("/download/{filename}")
async def download_zip(filename: str):
    current_time = time.time()
    for key in [k for k, v in zip_storage.items() if current_time - v["timestamp"] > 3600]:
        del zip_storage[key]
    if filename not in zip_storage:
        raise HTTPException(status_code=404, detail="ZIP not found.")
    zip_entry = zip_storage[filename]
    return Response(content=zip_entry["data"], media_type="application/zip", headers={"Content-Disposition": f"attachment; filename={filename}"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
