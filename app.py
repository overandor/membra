'''
Membra Institutional KPI Generator — Hugging Face Spaces app.py

Single-file FastAPI + Gradio production runtime with Groq KPI generation,
Stripe webhook entitlement hooks, SQLite quota tracking, dataset profiling,
and JSON/CSV exports.

Recommended requirements.txt:
  gradio>=4.44.1
  fastapi>=0.111.0
  uvicorn>=0.30.0
  pandas>=2.2.0
  groq>=0.9.0
  stripe>=10.0.0
  openpyxl>=3.1.0
  pyarrow>=15.0.0
  python-multipart>=0.0.9

Required Hugging Face Space secrets:
  GROQ_API_KEY
  STRIPE_SECRET_KEY
  STRIPE_WEBHOOK_SECRET
  STRIPE_PRICE_ID
  APP_BASE_URL

Optional:
  GROQ_MODEL, REQUIRE_STRIPE, FREE_DAILY_KPI_LIMIT, PAID_DAILY_KPI_LIMIT,
  APP_DB_PATH, APP_EXPORT_DIR, ADMIN_API_TOKEN, AUTO_INSTALL_DEPS
'''

from __future__ import annotations

import datetime as dt
import hashlib
import importlib.util
import json
import logging
import os
import re
import sqlite3
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Any


def ensure_runtime_dependencies() -> None:
    required = {
        'gradio': 'gradio>=4.44.1',
        'fastapi': 'fastapi>=0.111.0',
        'uvicorn': 'uvicorn>=0.30.0',
        'pandas': 'pandas>=2.2.0',
        'groq': 'groq>=0.9.0',
        'stripe': 'stripe>=10.0.0',
        'openpyxl': 'openpyxl>=3.1.0',
        'pyarrow': 'pyarrow>=15.0.0',
        'multipart': 'python-multipart>=0.0.9',
    }
    missing = [pkg for module, pkg in required.items() if importlib.util.find_spec(module) is None]
    if not missing:
        return
    if os.getenv('AUTO_INSTALL_DEPS', 'true').strip().lower() not in {'1', 'true', 'yes', 'on'}:
        raise RuntimeError('Missing dependencies: ' + ', '.join(missing))
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--quiet', *missing])


ensure_runtime_dependencies()

import gradio as gr
import pandas as pd
import stripe
import uvicorn
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from groq import Groq
from pydantic import BaseModel

APP_NAME = 'Membra Institutional KPI Generator'
APP_VERSION = '1.0.0'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
log = logging.getLogger('membra-kpi')

DB_PATH = Path(os.getenv('APP_DB_PATH', '/tmp/membra_kpi.sqlite3'))
EXPORT_DIR = Path(os.getenv('APP_EXPORT_DIR', '/tmp/membra_kpi_exports'))
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama3-70b-8192')
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', '')
STRIPE_PRICE_ID = os.getenv('STRIPE_PRICE_ID', '')
APP_BASE_URL = os.getenv('APP_BASE_URL', 'http://localhost:7860').rstrip('/')
REQUIRE_STRIPE = os.getenv('REQUIRE_STRIPE', 'false').strip().lower() in {'1', 'true', 'yes', 'on'}
FREE_DAILY_KPI_LIMIT = int(os.getenv('FREE_DAILY_KPI_LIMIT', '25'))
PAID_DAILY_KPI_LIMIT = int(os.getenv('PAID_DAILY_KPI_LIMIT', '1000'))
ADMIN_API_TOKEN = os.getenv('ADMIN_API_TOKEN', '')
stripe.api_key = STRIPE_SECRET_KEY or None

api = FastAPI(title=APP_NAME, version=APP_VERSION)


class CheckoutRequest(BaseModel):
    email: str
    success_url: str | None = None
    cancel_url: str | None = None


class PortalRequest(BaseModel):
    email: str
    return_url: str | None = None


class AdminGrantRequest(BaseModel):
    email: str
    tier: str = 'pro'
    status: str = 'active'
    daily_limit: int | None = None


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def today_key() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d')


def normalize_email(email: str) -> str:
    email = (email or '').strip().lower()
    if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
        raise ValueError('A valid email address is required.')
    return email


def db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=30, isolation_level=None)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with db() as conn:
        conn.executescript('''
            PRAGMA journal_mode=WAL;
            CREATE TABLE IF NOT EXISTS entitlements (
                email TEXT PRIMARY KEY,
                tier TEXT NOT NULL DEFAULT 'free',
                status TEXT NOT NULL DEFAULT 'inactive',
                daily_limit INTEGER NOT NULL DEFAULT 25,
                stripe_customer_id TEXT,
                stripe_subscription_id TEXT,
                current_period_end TEXT,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS usage_daily (
                email TEXT NOT NULL,
                day TEXT NOT NULL,
                kpis_generated INTEGER NOT NULL DEFAULT 0,
                updated_at TEXT NOT NULL,
                PRIMARY KEY(email, day)
            );
            CREATE TABLE IF NOT EXISTS generation_events (
                id TEXT PRIMARY KEY,
                email TEXT NOT NULL,
                dataset_fingerprint TEXT,
                kpi_count INTEGER NOT NULL,
                model TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_entitlements_customer ON entitlements(stripe_customer_id);
            CREATE INDEX IF NOT EXISTS idx_entitlements_subscription ON entitlements(stripe_subscription_id);
        ''')


init_db()


def get_entitlement(email: str) -> dict[str, Any]:
    email = normalize_email(email)
    with db() as conn:
        row = conn.execute('SELECT * FROM entitlements WHERE email=?', (email,)).fetchone()
        used = conn.execute('SELECT kpis_generated FROM usage_daily WHERE email=? AND day=?', (email, today_key())).fetchone()
    if row:
        ent = dict(row)
    else:
        ent = {
            'email': email,
            'tier': 'free',
            'status': 'active' if not REQUIRE_STRIPE else 'inactive',
            'daily_limit': FREE_DAILY_KPI_LIMIT,
            'stripe_customer_id': None,
            'stripe_subscription_id': None,
            'current_period_end': None,
            'updated_at': None,
        }
    ent['used_today'] = int(used['kpis_generated']) if used else 0
    ent['remaining_today'] = max(0, int(ent['daily_limit']) - ent['used_today'])
    ent['require_stripe'] = REQUIRE_STRIPE
    return ent


def upsert_entitlement(
    email: str,
    *,
    tier: str,
    status: str,
    daily_limit: int,
    stripe_customer_id: str | None = None,
    stripe_subscription_id: str | None = None,
    current_period_end: str | None = None,
) -> None:
    email = normalize_email(email)
    with db() as conn:
        conn.execute(
            '''
            INSERT INTO entitlements(email, tier, status, daily_limit, stripe_customer_id,
                                     stripe_subscription_id, current_period_end, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(email) DO UPDATE SET
              tier=excluded.tier,
              status=excluded.status,
              daily_limit=excluded.daily_limit,
              stripe_customer_id=COALESCE(excluded.stripe_customer_id, entitlements.stripe_customer_id),
              stripe_subscription_id=COALESCE(excluded.stripe_subscription_id, entitlements.stripe_subscription_id),
              current_period_end=COALESCE(excluded.current_period_end, entitlements.current_period_end),
              updated_at=excluded.updated_at
            ''',
            (email, tier, status, daily_limit, stripe_customer_id, stripe_subscription_id, current_period_end, now_utc()),
        )


def increment_usage(email: str, kpi_count: int) -> None:
    with db() as conn:
        conn.execute(
            '''
            INSERT INTO usage_daily(email, day, kpis_generated, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(email, day) DO UPDATE SET
              kpis_generated = usage_daily.kpis_generated + excluded.kpis_generated,
              updated_at = excluded.updated_at
            ''',
            (normalize_email(email), today_key(), int(kpi_count), now_utc()),
        )


def require_admin(authorization: str | None) -> None:
    if not ADMIN_API_TOKEN:
        raise HTTPException(404, 'Admin endpoint disabled. Set ADMIN_API_TOKEN to enable it.')
    if authorization != f'Bearer {ADMIN_API_TOKEN}':
        raise HTTPException(401, 'Invalid admin token')


def subscription_period_end(subscription: Any) -> str | None:
    raw = None
    if subscription is not None:
        raw = subscription.get('current_period_end') if hasattr(subscription, 'get') else getattr(subscription, 'current_period_end', None)
    if not raw:
        return None
    return dt.datetime.fromtimestamp(int(raw), tz=dt.timezone.utc).isoformat()


def set_subscription_entitlement(email: str, customer_id: str | None, subscription: Any | None, active: bool) -> None:
    sub_id = subscription.get('id') if subscription is not None and hasattr(subscription, 'get') else getattr(subscription, 'id', None)
    status = subscription.get('status') if subscription is not None and hasattr(subscription, 'get') else getattr(subscription, 'status', 'inactive')
    if active and status in {'active', 'trialing'}:
        upsert_entitlement(
            email,
            tier='pro',
            status=status,
            daily_limit=PAID_DAILY_KPI_LIMIT,
            stripe_customer_id=customer_id,
            stripe_subscription_id=sub_id,
            current_period_end=subscription_period_end(subscription),
        )
    else:
        upsert_entitlement(
            email,
            tier='free',
            status=status or 'inactive',
            daily_limit=FREE_DAILY_KPI_LIMIT,
            stripe_customer_id=customer_id,
            stripe_subscription_id=sub_id,
            current_period_end=subscription_period_end(subscription),
        )


def load_dataframe(file_path: str) -> pd.DataFrame:
    if not file_path:
        raise ValueError('Upload a CSV, Excel, JSON, JSONL, or Parquet file first.')
    p = Path(file_path)
    suffix = p.suffix.lower()
    if suffix == '.csv':
        df = pd.read_csv(p)
    elif suffix in {'.xlsx', '.xls'}:
        df = pd.read_excel(p)
    elif suffix == '.jsonl':
        df = pd.read_json(p, lines=True)
    elif suffix == '.json':
        df = pd.read_json(p)
    elif suffix == '.parquet':
        df = pd.read_parquet(p)
    else:
        raise ValueError(f'Unsupported file type: {suffix}')
    if df.empty:
        raise ValueError('Dataset is empty.')
    if len(df) > 250_000:
        df = df.sample(250_000, random_state=7)
    if len(df.columns) > 150:
        df = df.iloc[:, :150]
    df.columns = [str(c).strip()[:120] or f'column_{i}' for i, c in enumerate(df.columns)]
    return df


def dataframe_profile(df: pd.DataFrame) -> str:
    sample = df.head(10).to_dict(orient='records')
    cols: list[dict[str, Any]] = []
    for col in df.columns:
        s = df[col]
        entry: dict[str, Any] = {
            'name': col,
            'dtype': str(s.dtype),
            'null_pct': round(float(s.isna().mean() * 100), 2),
            'unique': int(s.nunique(dropna=True)),
        }
        if pd.api.types.is_numeric_dtype(s):
            desc = s.describe(percentiles=[0.25, 0.5, 0.75]).to_dict()
            entry['stats'] = {k: round(float(v), 4) for k, v in desc.items() if pd.notna(v)}
        else:
            entry['top_values'] = {str(k)[:80]: int(v) for k, v in s.dropna().astype(str).value_counts().head(5).to_dict().items()}
        cols.append(entry)
    return '\n\n'.join([
        f'Rows: {len(df):,}',
        f'Columns: {len(df.columns):,}',
        'Column profile JSON:\n' + json.dumps(cols, ensure_ascii=False, default=str),
        'Sample rows JSON:\n' + json.dumps(sample, ensure_ascii=False, default=str),
    ])


def fingerprint_df(df: pd.DataFrame) -> str:
    h = hashlib.sha256()
    h.update(str(df.shape).encode())
    h.update('|'.join(map(str, df.columns)).encode())
    h.update(pd.util.hash_pandas_object(df.head(1000), index=True).values.tobytes())
    return h.hexdigest()[:16]


def extract_json(text: str) -> dict[str, Any]:
    text = (text or '').strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', text, flags=re.S)
        if not match:
            raise ValueError('Model did not return JSON.')
        return json.loads(match.group(0))


def groq_client() -> Groq:
    if not GROQ_API_KEY:
        raise RuntimeError('GROQ_API_KEY is not configured in Space secrets.')
    return Groq(api_key=GROQ_API_KEY)


def generate_kpi_payload(profile: str, business_context: str, kpi_count: int) -> list[dict[str, Any]]:
    system = (
        'You are an institutional KPI designer. Return only valid compact JSON. '
        'No markdown. No prose outside JSON. Create metrics that are auditable, calculable, '
        'non-duplicative, and useful for executives, operators, finance, risk, compliance, and product leaders.'
    )
    user = {
        'task': 'Generate production-grade KPIs from this dataset profile.',
        'kpi_count': int(kpi_count),
        'business_context': business_context or 'General institutional operations and performance management.',
        'required_output_schema': {
            'kpis': [
                {
                    'name': 'string',
                    'category': 'growth|finance|operations|risk|quality|customer|workforce|compliance',
                    'definition': 'string',
                    'formula': 'string using dataset columns where possible',
                    'required_columns': ['column names'],
                    'calculation_notes': 'string',
                    'owner': 'string',
                    'frequency': 'daily|weekly|monthly|quarterly',
                    'decision_use': 'string',
                    'thresholds': {'green': 'string', 'yellow': 'string', 'red': 'string'},
                    'risk_notes': 'string',
                }
            ]
        },
        'dataset_profile': profile,
    }
    res = groq_client().chat.completions.create(
        model=GROQ_MODEL,
        temperature=0.25,
        max_tokens=4096,
        messages=[{'role': 'system', 'content': system}, {'role': 'user', 'content': json.dumps(user, ensure_ascii=False)}],
        response_format={'type': 'json_object'},
    )
    data = extract_json(res.choices[0].message.content or '{}')
    kpis = data.get('kpis', [])
    if not isinstance(kpis, list):
        raise ValueError('Model JSON had no kpis array.')
    return [k for k in kpis if isinstance(k, dict) and k.get('name')]


def safe_csv_value(value: Any) -> Any:
    if isinstance(value, str) and value[:1] in {'=', '+', '-', '@'}:
        return "'" + value
    return value


def flatten_kpi(k: dict[str, Any], csv_safe: bool = False) -> dict[str, Any]:
    row = {
        'name': k.get('name', ''),
        'category': k.get('category', ''),
        'definition': k.get('definition', ''),
        'formula': k.get('formula', ''),
        'required_columns': ', '.join(map(str, k.get('required_columns', []))) if isinstance(k.get('required_columns'), list) else str(k.get('required_columns', '')),
        'calculation_notes': k.get('calculation_notes', ''),
        'owner': k.get('owner', ''),
        'frequency': k.get('frequency', ''),
        'decision_use': k.get('decision_use', ''),
        'thresholds': json.dumps(k.get('thresholds', {}), ensure_ascii=False),
        'risk_notes': k.get('risk_notes', ''),
    }
    return {key: safe_csv_value(value) for key, value in row.items()} if csv_safe else row


def dedupe(kpis: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for k in kpis:
        key = re.sub(r'[^a-z0-9]+', '', str(k.get('name', '')).lower())
        if key and key not in seen:
            seen.add(key)
            out.append(k)
    return out


def export_files(kpis: list[dict[str, Any]]) -> tuple[str, str]:
    stem = f"kpis_{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    json_path = EXPORT_DIR / f'{stem}.json'
    csv_path = EXPORT_DIR / f'{stem}.csv'
    json_path.write_text(json.dumps(kpis, indent=2, ensure_ascii=False), encoding='utf-8')
    pd.DataFrame([flatten_kpi(k, csv_safe=True) for k in kpis]).to_csv(csv_path, index=False)
    return str(json_path), str(csv_path)


def gradio_load(file_path: str) -> tuple[str, str]:
    try:
        df = load_dataframe(file_path)
        return dataframe_profile(df), f'Loaded dataset: {len(df):,} rows x {len(df.columns):,} columns'
    except Exception as e:
        return '', f'Load error: {e}'


def gradio_generate(email: str, file_path: str, business_context: str, kpi_count: int) -> tuple[pd.DataFrame, str, str, str, list[dict[str, Any]]]:
    try:
        email = normalize_email(email)
    except Exception as e:
        return pd.DataFrame(), str(e), '', '', []
    ent = get_entitlement(email)
    desired = max(1, min(int(kpi_count or 10), 50))
    if REQUIRE_STRIPE and ent['status'] not in {'active', 'trialing'}:
        return pd.DataFrame(), 'Stripe entitlement required. Use checkout or disable REQUIRE_STRIPE.', '', '', []
    if ent['remaining_today'] < desired:
        return pd.DataFrame(), f"Daily quota exceeded. Remaining today: {ent['remaining_today']} KPI(s).", '', '', []
    try:
        df = load_dataframe(file_path)
        kpis = dedupe(generate_kpi_payload(dataframe_profile(df), business_context, desired))[:desired]
        if not kpis:
            raise RuntimeError('No KPIs returned by model.')
        increment_usage(email, len(kpis))
        with db() as conn:
            conn.execute(
                'INSERT INTO generation_events(id, email, dataset_fingerprint, kpi_count, model, created_at) VALUES (?, ?, ?, ?, ?, ?)',
                (uuid.uuid4().hex, email, fingerprint_df(df), len(kpis), GROQ_MODEL, now_utc()),
            )
        json_path, csv_path = export_files(kpis)
        status = f"Generated {len(kpis)} KPI(s). Tier={ent['tier']}; remaining before run={ent['remaining_today']}."
        return pd.DataFrame([flatten_kpi(k) for k in kpis]), status, json_path, csv_path, kpis
    except Exception as e:
        log.exception('generation failed')
        return pd.DataFrame(), f'Generation error: {e}', '', '', []


def gradio_checkout_link(email: str) -> str:
    try:
        email = normalize_email(email)
    except Exception as e:
        return str(e)
    if not STRIPE_SECRET_KEY or not STRIPE_PRICE_ID:
        return 'Stripe checkout is not configured. Set STRIPE_SECRET_KEY and STRIPE_PRICE_ID.'
    session = stripe.checkout.Session.create(
        mode='subscription',
        customer_email=email,
        line_items=[{'price': STRIPE_PRICE_ID, 'quantity': 1}],
        success_url=f'{APP_BASE_URL}/?checkout=success&session_id={{CHECKOUT_SESSION_ID}}',
        cancel_url=f'{APP_BASE_URL}/?checkout=cancelled',
        metadata={'email': email},
    )
    return f'Checkout URL: {session.url}'


@api.get('/api/health')
def health() -> dict[str, Any]:
    return {
        'ok': True,
        'app': APP_NAME,
        'version': APP_VERSION,
        'model': GROQ_MODEL,
        'require_stripe': REQUIRE_STRIPE,
        'stripe_configured': bool(STRIPE_SECRET_KEY and STRIPE_WEBHOOK_SECRET and STRIPE_PRICE_ID),
        'groq_configured': bool(GROQ_API_KEY),
    }


@api.get('/api/entitlement')
def entitlement(email: str) -> dict[str, Any]:
    try:
        return get_entitlement(email)
    except ValueError as e:
        raise HTTPException(400, str(e))


@api.post('/api/admin/grant')
def admin_grant(payload: AdminGrantRequest, authorization: str | None = Header(default=None)) -> dict[str, Any]:
    require_admin(authorization)
    if payload.tier not in {'free', 'pro'}:
        raise HTTPException(400, 'tier must be free or pro')
    limit = payload.daily_limit if payload.daily_limit is not None else (PAID_DAILY_KPI_LIMIT if payload.tier == 'pro' else FREE_DAILY_KPI_LIMIT)
    upsert_entitlement(payload.email, tier=payload.tier, status=payload.status, daily_limit=limit)
    return {'ok': True, 'entitlement': get_entitlement(payload.email)}


@api.post('/api/stripe/create-checkout-session')
def create_checkout_session(payload: CheckoutRequest) -> dict[str, Any]:
    if not STRIPE_SECRET_KEY or not STRIPE_PRICE_ID:
        raise HTTPException(500, 'Stripe checkout is not configured.')
    try:
        email = normalize_email(payload.email)
    except ValueError as e:
        raise HTTPException(400, str(e))
    session = stripe.checkout.Session.create(
        mode='subscription',
        customer_email=email,
        line_items=[{'price': STRIPE_PRICE_ID, 'quantity': 1}],
        success_url=payload.success_url or f'{APP_BASE_URL}/?checkout=success&session_id={{CHECKOUT_SESSION_ID}}',
        cancel_url=payload.cancel_url or f'{APP_BASE_URL}/?checkout=cancelled',
        metadata={'email': email},
    )
    return {'url': session.url, 'id': session.id}


@api.post('/api/stripe/create-portal-session')
def create_portal_session(payload: PortalRequest) -> dict[str, Any]:
    if not STRIPE_SECRET_KEY:
        raise HTTPException(500, 'Stripe is not configured.')
    ent = get_entitlement(payload.email)
    customer_id = ent.get('stripe_customer_id')
    if not customer_id:
        raise HTTPException(404, 'No Stripe customer is linked to that email yet.')
    session = stripe.billing_portal.Session.create(customer=customer_id, return_url=payload.return_url or APP_BASE_URL)
    return {'url': session.url, 'id': session.id}


@api.post('/api/stripe/webhook')
async def stripe_webhook(request: Request, stripe_signature: str | None = Header(default=None)) -> JSONResponse:
    if not STRIPE_WEBHOOK_SECRET:
        raise HTTPException(500, 'STRIPE_WEBHOOK_SECRET is not configured.')
    body = await request.body()
    try:
        event = stripe.Webhook.construct_event(body, stripe_signature, STRIPE_WEBHOOK_SECRET)
    except Exception as e:
        raise HTTPException(400, f'Invalid Stripe webhook: {e}')

    event_type = event['type']
    obj = event['data']['object']
    log.info('stripe webhook received: %s', event_type)

    if event_type == 'checkout.session.completed':
        email = normalize_email(obj.get('customer_details', {}).get('email') or obj.get('customer_email') or obj.get('metadata', {}).get('email', ''))
        customer_id = obj.get('customer')
        sub_id = obj.get('subscription')
        subscription = stripe.Subscription.retrieve(sub_id) if sub_id else None
        set_subscription_entitlement(email, customer_id, subscription, active=True)

    elif event_type in {'customer.subscription.created', 'customer.subscription.updated', 'customer.subscription.deleted'}:
        customer_id = obj.get('customer')
        customer = stripe.Customer.retrieve(customer_id) if customer_id else None
        email = normalize_email((customer or {}).get('email', ''))
        set_subscription_entitlement(email, customer_id, obj, active=event_type != 'customer.subscription.deleted')

    elif event_type in {'invoice.payment_succeeded', 'invoice.paid'}:
        customer_id = obj.get('customer')
        sub_id = obj.get('subscription')
        customer = stripe.Customer.retrieve(customer_id) if customer_id else None
        email = normalize_email((customer or {}).get('email', ''))
        subscription = stripe.Subscription.retrieve(sub_id) if sub_id else None
        set_subscription_entitlement(email, customer_id, subscription, active=True)

    return JSONResponse({'received': True})


@api.get('/api')
def api_index() -> PlainTextResponse:
    return PlainTextResponse('\n'.join([
        'Membra Institutional KPI Generator API',
        'GET  /api/health',
        'GET  /api/entitlement?email=user@example.com',
        'POST /api/stripe/create-checkout-session',
        'POST /api/stripe/create-portal-session',
        'POST /api/stripe/webhook',
        'POST /api/admin/grant',
    ]))


def build_ui() -> gr.Blocks:
    with gr.Blocks(title=APP_NAME) as demo:
        gr.Markdown(
            f'# {APP_NAME}\n'
            'Production KPI generation with Groq, Stripe entitlement hooks, SQLite usage tracking, CSV/JSON exports, and Hugging Face Spaces deployment.'
        )
        with gr.Row():
            email = gr.Textbox(label='Account email', placeholder='you@example.com')
            file_in = gr.File(label='Dataset', file_types=['.csv', '.xlsx', '.xls', '.json', '.jsonl', '.parquet'], type='filepath')
        business_context = gr.Textbox(label='Business context / KPI mandate', lines=4, placeholder='Example: B2B SaaS finance/operations executive scorecard...')
        kpi_count = gr.Slider(label='KPI count', minimum=1, maximum=50, value=10, step=1)
        with gr.Row():
            load_btn = gr.Button('Profile dataset')
            gen_btn = gr.Button('Generate KPIs', variant='primary')
            checkout_btn = gr.Button('Create Stripe checkout link')
        status = gr.Textbox(label='Status', interactive=False)
        profile = gr.Textbox(label='Dataset profile', lines=12, interactive=False)
        table = gr.Dataframe(label='Generated KPI catalog', interactive=False, wrap=True)
        with gr.Row():
            json_file = gr.File(label='JSON export')
            csv_file = gr.File(label='CSV export')
        checkout_out = gr.Textbox(label='Checkout', interactive=False)
        state = gr.State([])

        load_btn.click(gradio_load, inputs=[file_in], outputs=[profile, status])
        gen_btn.click(gradio_generate, inputs=[email, file_in, business_context, kpi_count], outputs=[table, status, json_file, csv_file, state])
        checkout_btn.click(gradio_checkout_link, inputs=[email], outputs=[checkout_out])
        gr.Markdown('Set Stripe webhook URL to `/api/stripe/webhook`. Set Space secrets before enabling `REQUIRE_STRIPE=true`.')
    return demo


demo = build_ui()
app = gr.mount_gradio_app(api, demo, path='/')


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=int(os.getenv('PORT', '7860')), log_level=LOG_LEVEL.lower())
