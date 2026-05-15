from fastapi.testclient import TestClient

from app import app


def test_os_health():
    client = TestClient(app)
    res = client.get('/api/health')
    assert res.status_code == 200
    assert res.json()['ok'] is True


def test_registry_contains_kpi():
    client = TestClient(app)
    res = client.get('/api/registry')
    assert res.status_code == 200
    module_ids = [m['id'] for m in res.json()['modules']]
    assert 'membra-kpi' in module_ids


def test_homepage_loads():
    client = TestClient(app)
    res = client.get('/')
    assert res.status_code == 200
    assert 'MEMBRA command center' in res.text
