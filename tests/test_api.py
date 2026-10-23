import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.config import settings

client = TestClient(app)

def test_api_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "Akash" in data["college"]
    assert data["total_chunks_indexed"] > 0

def test_api_chat():
    payload = {
        "question": "What are the college timings and location of AIET?",
        "session_id": "test_session_1"
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "9:00 AM" in data["answer"] or "9 AM" in data["answer"]
    assert len(data["sources"]) > 0

def test_api_courses():
    response = client.get("/api/courses")
    assert response.status_code == 200
    courses = response.json()
    assert len(courses) >= 8
    # verify BE CSE is present
    cse = next((c for c in courses if "Computer Science and Engineering" in c["course_name"]), None)
    assert cse is not None

def test_api_faculty():
    response = client.get("/api/faculty")
    assert response.status_code == 200
    faculty = response.json()
    assert len(faculty) >= 40
    # verify HOD filter
    hod_res = client.get("/api/faculty?hod_only=true")
    assert hod_res.status_code == 200
    hods = hod_res.json()
    assert len(hods) >= 8

def test_api_fees():
    response = client.get("/api/fees")
    assert response.status_code == 200
    fees = response.json()
    assert len(fees) > 0

def test_api_scholarships():
    response = client.get("/api/scholarships")
    assert response.status_code == 200
    sch = response.json()
    assert len(sch) >= 6

def test_api_infrastructure():
    response = client.get("/api/infrastructure")
    assert response.status_code == 200
    infra = response.json()
    assert len(infra) >= 8

def test_api_sources():
    response = client.get("/api/sources")
    assert response.status_code == 200
    sources = response.json()
    assert len(sources) >= 8

def test_admin_authentication():
    # Attempt without admin key -> 401
    res_unauth = client.get("/api/admin/documents")
    assert res_unauth.status_code == 401

    # Attempt with valid admin key -> 200
    headers = {"x-admin-key": settings.ADMIN_API_KEY}
    res_auth = client.get("/api/admin/documents", headers=headers)
    assert res_auth.status_code == 200
    data = res_auth.json()
    assert "documents" in data
    assert data["total_count"] > 0
