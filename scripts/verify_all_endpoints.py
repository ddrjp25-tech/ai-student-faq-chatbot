import urllib.request
import json

base_url = "http://localhost:8000"

endpoints = [
    ("/", 200, "Frontend Home HTML"),
    ("/static/css/style.css", 200, "Frontend Stylesheet"),
    ("/static/js/app.js", 200, "Frontend Application Logic"),
    ("/static/js/voice.js", 200, "Frontend Voice Controller"),
    ("/static/assets/logo.svg", 200, "Official College Logo"),
    ("/api/health", 200, "System Health"),
    ("/api/courses", 200, "Courses List"),
    ("/api/faculty", 200, "Faculty Directory"),
    ("/api/fees", 200, "Fee Guidelines"),
    ("/api/scholarships", 200, "Scholarship Schemes"),
    ("/api/infrastructure", 200, "Infrastructure"),
    ("/api/sources", 200, "Approved Sources")
]

print("=== VERIFYING ALL AIET APPLICATION ENDPOINTS ===")
all_passed = True

for path, expected_status, label in endpoints:
    url = f"{base_url}{path}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            status = resp.status
            data = resp.read()
            passed = (status == expected_status)
            print(f"[{'PASS' if passed else 'FAIL'}] {status} - {label} ({url}) - Size: {len(data)} bytes")
            if not passed:
                all_passed = False
    except Exception as e:
        print(f"[FAIL] Error requesting {url}: {e}")
        all_passed = False

# Test POST /api/chat with questions
chat_questions = [
    "What are the college timings?",
    "What courses does AIET offer?",
    "Who is the HOD of AI and Data Science?",
    "What are the KCET and COMEDK codes?",
    "What is the management fee for Computer Science?",
    "Does AIET have hostel facilities?"
]

print("\n=== VERIFYING AI VOICE QA RESPONSES ===")
for q in chat_questions:
    try:
        req = urllib.request.Request(
            f"{base_url}/api/chat",
            data=json.dumps({"question": q}).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req) as resp:
            res_data = json.loads(resp.read().decode())
            print(f"\nQ: {q}")
            print(f"A: {res_data['answer'][:160]}...")
            print(f"   Sources: {len(res_data['sources'])}, Confidence: {res_data['confidence']}, Needs Confirmation: {res_data['needs_confirmation']}")
    except Exception as e:
        print(f"[FAIL] Chat question failed: {q} - Error: {e}")
        all_passed = False

print("\n" + "="*50)
if all_passed:
    print("ALL ENDPOINTS AND CHAT FLOWS VERIFIED SUCCESSFULLY!")
else:
    print("SOME CHECKS FAILED.")
