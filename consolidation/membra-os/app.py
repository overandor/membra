"""
MEMBRA OS — Proof-to-Payout Assetification Demo.

Safe boundary: this demo records proof, consent, attribution, estimates, and payout eligibility.
It does not custody funds, guarantee revenue, issue bearer money, execute tokenomics, or settle payments.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import io
import json
import os
import re
import uuid
from pathlib import Path
from typing import Any, Dict, List, Tuple

import gradio as gr
import pandas as pd
from PIL import Image, ImageDraw

try:
    import qrcode
except Exception:
    qrcode = None

APP_NAME = "MEMBRA OS"
DATA_DIR = Path(os.getenv("MEMBRA_DATA_DIR", "data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)
PROOFBOOK_PATH = DATA_DIR / "proofbook.jsonl"
SCAN_PATH = DATA_DIR / "scan_events.jsonl"
SAFE_DISCLOSURE = (
    "MEMBRA records proof, consent, attribution, estimates, and payout eligibility. "
    "It does not custody funds, guarantee revenue, issue bearer money, or execute tokenomics."
)

SCENARIOS = [
    {"key": "window_ad", "label": "Window / storefront ad inventory", "keywords": "window storefront glass shop retail front signage street", "base": 180, "unit": "campaign_month", "risk": "medium"},
    {"key": "vehicle_ad", "label": "Vehicle wrap / mobile ad inventory", "keywords": "car vehicle van truck delivery fleet uber taxi", "base": 240, "unit": "campaign_month", "risk": "medium"},
    {"key": "storage_space", "label": "Underused storage / micro-warehouse", "keywords": "garage storage basement warehouse shelf closet empty room space", "base": 120, "unit": "month", "risk": "medium"},
    {"key": "tool_rental", "label": "Tool / equipment rental", "keywords": "tool drill saw ladder equipment camera printer machine", "base": 65, "unit": "day", "risk": "low"},
    {"key": "event_booth", "label": "Event booth / activation surface", "keywords": "event booth festival table venue market pop-up activation", "base": 350, "unit": "event_day", "risk": "medium"},
    {"key": "creator_asset", "label": "Creator/media monetization asset", "keywords": "photo video content creator media art post influencer", "base": 95, "unit": "campaign", "risk": "low"},
    {"key": "relay_point", "label": "Local relay / pickup point", "keywords": "pickup relay dropoff porch locker counter delivery", "base": 75, "unit": "month", "risk": "medium"},
]


def now_iso() -> str:
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def normalize(text: str | None) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def stable_hash(payload: Any) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()


def file_digest(file_obj: Any) -> Tuple[str, str]:
    if not file_obj:
        return "", "no_file"
    path = getattr(file_obj, "name", None) or str(file_obj)
    try:
        data = Path(path).read_bytes()
        return hashlib.sha256(data).hexdigest(), f"file:{Path(path).name}:{len(data)}bytes"
    except Exception:
        raw = str(file_obj).encode()
        return hashlib.sha256(raw).hexdigest(), "file_reference_only"


def choose_scenario(text: str) -> Dict[str, Any]:
    lower = text.lower()
    ranked = []
    for item in SCENARIOS:
        words = item["keywords"].split()
        hits = [w for w in words if w in lower]
        score = len(hits) or 0.25
        ranked.append({**item, "hits": hits, "score": score})
    ranked.sort(key=lambda x: x["score"], reverse=True)
    top = ranked[0]
    second = ranked[1]["score"] if len(ranked) > 1 else 0
    top["confidence"] = round(min(0.93, 0.44 + top["score"] * 0.12 + max(0, top["score"] - second) * 0.05), 2)
    return top


def estimate_value(base: int, confidence: float, consent: str) -> Tuple[int, int, bool]:
    approved = consent == "Owner approved"
    factor = 1.0 if approved else 0.45
    low = int(base * 0.55 * factor)
    high = int(base * (1.15 + confidence * 0.35) * factor)
    return low, max(high, low + 1), approved


def make_sku(label: str, scenario_key: str) -> str:
    clean = re.sub(r"[^A-Z0-9]+", "", label.upper())[:8] or "ASSET"
    return f"MBR-{scenario_key[:3].upper()}-{clean}-{uuid.uuid4().hex[:6].upper()}"


def append_jsonl(path: Path, row: Dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def read_jsonl(path: Path, limit: int = 200) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    rows: List[Dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            rows.append(json.loads(line))
        except Exception:
            pass
    return rows[-limit:]


def make_qr(url: str) -> Image.Image:
    if qrcode:
        return qrcode.make(url).convert("RGB")
    img = Image.new("RGB", (420, 420), "white")
    draw = ImageDraw.Draw(img)
    draw.rectangle((40, 40, 380, 380), outline="black", width=8)
    draw.text((70, 190), "QR dependency missing", fill="black")
    return img


def assetify(owner_alias: str, asset_label: str, description: str, consent: str, public_base_url: str, upload: Any):
    owner_alias = normalize(owner_alias) or "anonymous-owner"
    asset_label = normalize(asset_label) or "Untitled Asset"
    description = normalize(description)
    base_url = normalize(public_base_url).rstrip("/") or "https://membra.local"
    file_hash, file_note = file_digest(upload)

    text = " ".join([owner_alias, asset_label, description, file_note])
    scenario = choose_scenario(text)
    low, high, eligible = estimate_value(scenario["base"], scenario["confidence"], consent)
    proof_id = uuid.uuid4().hex
    sku = make_sku(asset_label, scenario["key"])
    qr_url = f"{base_url}/g/{proof_id}"
    claim_url = f"{base_url}/claim/{proof_id}"
    source_hash = stable_hash({"owner": owner_alias, "asset": asset_label, "description": description, "file_hash": file_hash})
    proof_hash = stable_hash({"proof_id": proof_id, "sku": sku, "scenario": scenario["key"], "source_hash": source_hash, "created_at": now_iso()})
    record = {
        "proof_id": proof_id,
        "created_at": now_iso(),
        "owner_alias": owner_alias,
        "asset_label": asset_label,
        "scenario_key": scenario["key"],
        "scenario_label": scenario["label"],
        "sku": sku,
        "confidence": scenario["confidence"],
        "estimated_value_low": low,
        "estimated_value_high": high,
        "value_unit": scenario["unit"],
        "risk": scenario["risk"],
        "payout_eligible": eligible,
        "consent_status": consent,
        "source_hash": source_hash,
        "proof_hash": proof_hash,
        "claim_url": claim_url,
        "qr_url": qr_url,
        "disclosure": SAFE_DISCLOSURE,
    }
    append_jsonl(PROOFBOOK_PATH, record)
    summary = f"""
## MEMBRA Proof Created

**Proof ID:** `{proof_id}`  
**SKU:** `{sku}`  
**Scenario:** {scenario['label']}  
**Confidence:** {scenario['confidence']}  
**Estimated range:** ${low:,}–${high:,} per {scenario['unit']}  
**Consent:** {consent}  
**Payout eligible:** {'Yes' if eligible else 'No'}

**Claim URL:** {claim_url}  
**Gateway URL:** {qr_url}

**Proof hash:** `{proof_hash}`

{SAFE_DISCLOSURE}
"""
    df = pd.DataFrame([record])
    return summary, df, make_qr(qr_url)


def record_scan(proof_id: str, channel: str, note: str):
    proof_id = normalize(proof_id)
    if not proof_id:
        return "Provide a proof_id first.", pd.DataFrame(read_jsonl(SCAN_PATH))
    event = {"event_id": uuid.uuid4().hex, "proof_id": proof_id, "channel": channel, "note": normalize(note), "created_at": now_iso()}
    append_jsonl(SCAN_PATH, event)
    return f"Recorded {channel} event for `{proof_id}`.", pd.DataFrame(read_jsonl(SCAN_PATH))


def dashboard():
    proofs = read_jsonl(PROOFBOOK_PATH)
    scans = read_jsonl(SCAN_PATH)
    if not proofs:
        return "No proof records yet.", pd.DataFrame(), pd.DataFrame()
    p = pd.DataFrame(proofs)
    s = pd.DataFrame(scans)
    approved = int(p.get("payout_eligible", pd.Series(dtype=bool)).sum())
    value_low = int(p.get("estimated_value_low", pd.Series(dtype=int)).sum())
    value_high = int(p.get("estimated_value_high", pd.Series(dtype=int)).sum())
    text = f"""
## Portfolio KPI

**Proof records:** {len(p)}  
**Scan/claim events:** {len(s)}  
**Payout eligible records:** {approved}  
**Estimated portfolio range:** ${value_low:,}–${value_high:,}

{SAFE_DISCLOSURE}
"""
    return text, p.tail(50), s.tail(50)


def export_proofbook():
    return str(PROOFBOOK_PATH) if PROOFBOOK_PATH.exists() else None


with gr.Blocks(title=APP_NAME, theme=gr.themes.Soft()) as demo:
    gr.Markdown("# MEMBRA OS\n### Proof-to-Payout Assetification Infrastructure\n" + SAFE_DISCLOSURE)
    with gr.Tab("Assetify"):
        owner = gr.Textbox(label="Owner alias", value="local-owner")
        label = gr.Textbox(label="Asset label", value="Storefront window ad slot")
        desc = gr.Textbox(label="Description/context", lines=5, value="Retail storefront window facing a busy street. Owner wants QR proof and scan attribution before public listing.")
        consent = gr.Radio(["Draft only", "Owner approved"], value="Draft only", label="Consent status")
        base_url = gr.Textbox(label="Public base URL", value="https://membra.example")
        upload = gr.File(label="Optional image or KPI file")
        run = gr.Button("Create ProofBook record")
        out = gr.Markdown()
        out_df = gr.Dataframe(label="Proof record")
        out_qr = gr.Image(label="Gateway QR")
        run.click(assetify, [owner, label, desc, consent, base_url, upload], [out, out_df, out_qr])
    with gr.Tab("Record QR/SMS Event"):
        proof_id = gr.Textbox(label="Proof ID")
        channel = gr.Radio(["qr_scan", "sms_claim", "email_claim", "admin_review"], value="qr_scan", label="Event channel")
        note = gr.Textbox(label="Note")
        event_btn = gr.Button("Record event")
        event_msg = gr.Markdown()
        event_df = gr.Dataframe(label="Events")
        event_btn.click(record_scan, [proof_id, channel, note], [event_msg, event_df])
    with gr.Tab("KPI Dashboard"):
        refresh = gr.Button("Refresh dashboard")
        kpi = gr.Markdown()
        proofs_df = gr.Dataframe(label="ProofBook")
        scans_df = gr.Dataframe(label="Scan/claim events")
        download = gr.File(label="Download proofbook JSONL")
        refresh.click(dashboard, None, [kpi, proofs_df, scans_df])
        refresh.click(export_proofbook, None, download)
    with gr.Tab("Consolidation Map"):
        gr.Markdown("""
| Repo | Role |
|---|---|
| `membra` | canonical parent, SDK, docs, registry |
| `Membra_kpi` | flagship KPI and assetification SaaS |
| `membra-qr-gateway` | QR/NFC proof rail |
| `sms` | SMS/email/QR claim-link rail |
| `membramoney-protocol` | devnet-only protocol research lab |

Production focus: assetification, ProofBook, QR/SMS attribution, owner consent, KPI reports, marketplace drafts, and external settlement eligibility.
""")

if __name__ == "__main__":
    demo.launch()
