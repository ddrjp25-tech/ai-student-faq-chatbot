# Akash Institute of Engineering & Technology (AIET) - AI Voice Assistant & College Chatbot

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.13+-3776AB.svg?logo=python)](https://python.org)
[![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-blue.svg)](https://www.trychroma.com/)
[![License](https://img.shields.io/badge/Academic-VTU%20Mini%20Project-orange.svg)]()

A complete, modern, responsive, voice-first AI College Assistant and FAQ system built for **Akash Institute of Engineering and Technology (AIET)**, Devanahalli, Bengaluru, Karnataka, India.

Students, parents, faculty, and prospective applicants can speak naturally or type questions to obtain accurate, verified, source-grounded answers about courses, departments, faculty directory, fee policies, scholarships, campus facilities, college timings, and admissions.

---

## 🏛️ Official Institutional Profile & Key Facts

| Property | Official Verified Detail |
| :--- | :--- |
| **Institution Name** | **Akash Institute of Engineering and Technology** |
| **Abbreviation** | **AIET** |
| **Parent Trust** | Akash Education & Development Trust (AEDT) / Akash Group of Institutions (AGI) |
| **Established** | 2020 |
| **Location & Address** | Prasannahalli Road, Devanahalli, near Kempegowda International Airport, Bengaluru, Karnataka – 562110 |
| **Regular College Timings** | **9:00 AM to 4:00 PM** (Monday to Saturday as per VTU calendar) |
| **Office Hours** | 9:00 AM to 5:00 PM |
| **Academic Affiliation** | **Visvesvaraya Technological University (VTU)**, Belagavi |
| **Approvals** | **AICTE**, New Delhi; Recognized by Government of Karnataka |
| **KCET College Code** | **E300** (KEA Karnataka Engineering Quota) |
| **COMEDK College Code** | **E005** (All-India Engineering Merit Quota) |
| **KEA-PGCET MBA Code** | **B097** |
| **KEA-PGCET MCA Code** | **C550** |
| **Admissions Hotline** | **+91 9513107575** / **+91 9513597575** / **080-244-11-222** |
| **Admissions Email** | `admissions@akashinstitutions.com` |
| **Official Portals** | [https://akashiet.com/](https://akashiet.com/) & [https://admissions.akashinstitutions.com/engineering](https://admissions.akashinstitutions.com/engineering) |

---

## 🚀 Key Features

1. **Real Voice Interaction**:
   - Spoken question input using browser Web Speech API (`SpeechRecognition`).
   - Natural spoken responses via browser Speech Synthesis (`SpeechSynthesisUtterance`).
   - Interrupt/Stop audio controls, voice mute/unmute toggle, and replay button for any response.
   - Live visual transcript waveform showing speech recognition progress in real time.

2. **RAG (Retrieval-Augmented Generation) Architecture**:
   - Zero hallucination: Answers strictly grounded in verified official college records.
   - Embedded high-speed vector database with **ChromaDB** and local **ONNX all-MiniLM-L6-v2** embeddings (79 MB cached model runs 100% locally and offline without external dependencies).
   - **Hybrid Search**: Combines dense semantic vector retrieval with BM25/keyword lexical boost for exact code matching (e.g., `E300`, `E005`, `B097`, `C550`, `9:00 AM`).

3. **Multi-Turn Context & Follow-Ups**:
   - Context-aware conversation tracking (e.g. asking "Tell me about AI & DS" followed by "Who is the HOD?" correctly identifies Mr. Anil Kumar Warad).
   - Dynamic contextual suggestion chips after each turn.

4. **Answer Accuracy & Strict Safety Rules**:
   - Management quota fees and unconfirmed specific amounts are never fabricated: the assistant states *"I couldn't verify the latest official fee for this category. Please contact the AIET admissions office for confirmation"* and provides verified admissions desk contacts.
   - Never promises guaranteed employment, placement salaries, or guaranteed scholarship awards.
   - Shows official clickable source chips with last-verified dates.

5. **Searchable Data Explorers**:
   - **Courses & Departments**: 8 B.E. programmes (CSE, ISE, AI&ML, AI&DS, Cyber Security, Data Science, ECE, Mechanical), MBA, MCA, and Lateral Entry.
   - **Faculty Directory**: 46 publicly listed faculty members with designations, HOD markers, and official CV/Profile PDF downloads.
   - **Fees & Expenses Policy**: Transparent guidance for KCET, COMEDK, Management, Hostels, and Transport.
   - **Scholarships**: SSP Karnataka, NSP Central, AICTE Pragati for Girls (₹50,000/yr), AICTE Saksham for specially-abled, and Akash Entrance Test (AET) Institutional Awards.
   - **Campus Infrastructure**: On-campus multi-specialty Akash Hospital, 1,500-seat central auditorium, Wi-Fi hostels (400 boys, 700 girls), and sports facilities.

6. **Knowledge Base Administration**:
   - Protected with `ADMIN_API_KEY` authentication.
   - Inspect indexed documents, preview uploaded PDFs/text before indexing, add custom updates, delete outdated documents, and rebuild the vector database with one click.

---

## 📐 System Architecture

```mermaid
graph TD
    User([Student / Parent / Faculty]) <-->|Voice Input & Spoken Audio| Browser[Browser Web Speech API & UI]
    
    subgraph Frontend [Vanilla Modern Web UI]
        Browser -->|HTTP POST /api/chat| ChatHandler[Chat & Voice Controller]
        Browser -->|HTTP GET /api/*| DataExplorers[Courses, Faculty, Fees, Admin]
    end

    subgraph Backend [FastAPI Application]
        ChatHandler --> RAGEngine[RAG Engine]
        RAGEngine --> HybridRetriever[Hybrid Search Engine]
        
        subgraph VectorStore [ChromaDB Local Vector Engine]
            HybridRetriever <--> ChromaDB[(ChromaDB Persistent Store<br/>all-MiniLM-L6-v2)]
        end
        
        subgraph KnowledgeBase [Structured Verified JSON Records]
            ChromaDB -.->|Indexed from| KBFiles[9 JSON Files: Profile, Courses,<br/>Faculty, Fees, Scholarships, Infra]
        end

        RAGEngine --> LLMOrSynthesizer{LLM Key Available?}
        LLMOrSynthesizer -->|Yes| LLMService[OpenAI/Groq Compatible API]
        LLMOrSynthesizer -->|No (Default Offline)| GroundedSynthesizer[Deterministic Grounded Synthesizer]
    end

    GroundedSynthesizer --> ChatResponse[Grounded Answer + Citations + Disclaimers]
    LLMService --> ChatResponse
    ChatResponse --> Browser
```

---

## 📁 Project Structure

```
aiet-voice-assistant/
├── backend/
│   ├── main.py                     # FastAPI application entry point
│   ├── config.py                   # Settings, paths, and environment config
│   ├── requirements.txt            # Python dependencies
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py              # Pydantic data schemas
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── chat.py                 # POST /api/chat
│   │   ├── courses.py              # GET /api/courses
│   │   ├── faculty.py              # GET /api/faculty
│   │   ├── fees.py                 # GET /api/fees
│   │   ├── scholarships.py         # GET /api/scholarships
│   │   ├── infrastructure.py       # GET /api/infrastructure
│   │   ├── sources.py              # GET /api/sources
│   │   └── admin.py                # Admin endpoints (protected)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── rag_engine.py           # Core RAG QA pipeline
│   │   ├── vector_store.py         # ChromaDB client & hybrid search
│   │   └── knowledge_manager.py    # Admin document indexing & preview
│   └── knowledge_base/             # 9 Verified Official JSON Datasets
│       ├── college_profile.json
│       ├── courses.json
│       ├── faculty.json
│       ├── fees.json
│       ├── scholarships.json
│       ├── infrastructure.json
│       ├── admissions.json
│       ├── academic_information.json
│       └── sources.json
├── frontend/
│   ├── index.html                  # Semantic, accessible HTML5 layout
│   ├── css/
│   │   └── style.css               # Modern academic dark theme design system
│   ├── js/
│   │   ├── voice.js                # Web Speech STT & TTS controller
│   │   └── app.js                  # Frontend state & dynamic UI rendering
│   └── assets/
│       └── logo.svg                # Authentic AIET vector logo
├── scripts/
│   ├── build_knowledge_base.py     # Script to generate JSON knowledge base
│   └── verify_all_endpoints.py     # Full regression verification script
├── tests/
│   ├── test_rag.py                 # 15 comprehensive RAG unit tests
│   └── test_api.py                 # 9 API integration tests
├── .env.example                    # Environment variable template
├── .gitignore                      # Git exclusion rules
├── run.py                          # Single-command server launcher
└── README.md                       # Documentation
```

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.10+ (tested on Python 3.13)
- Google Chrome, Microsoft Edge, or Safari (for full Web Speech API voice support)

### 1. Clone or Open the Workspace
```bash
cd "c:\Users\dheer\OneDrive\Desktop\VA Chatbot1"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
> **Note:** An LLM API key is **completely optional**. The system includes an intelligent grounded offline synthesizer that works 100% locally with zero external API dependencies!

---

## 🌐 Deploying to Public Cloud (Render / Railway)

### Deploying on Render (Web Service):
1. Create a **New Web Service** connected to your repository.
2. Configure settings:
   - **Root Directory:** *(leave blank / default)*
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python run.py` *(or `uvicorn main:app --host 0.0.0.0 --port $PORT`)*
3. Render automatically sets the `$PORT` environment variable (e.g. 10000), which the application automatically detects and binds to.


---

## ▶️ Running the Application

Launch the server with the single command:
```bash
python run.py
```

Open your browser and navigate to:
- **Application Interface:** [http://localhost:8000](http://localhost:8000)
- **Interactive Swagger API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Alternative ReDoc Docs:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧪 Testing & Verification

Run the automated test suite:
```bash
# Run RAG Engine Unit Tests (15 tests)
python -m pytest tests/test_rag.py

# Run API Integration Tests (9 tests)
python -m pytest tests/test_api.py

# Run Full Test Suite (24 tests)
python -m pytest

# Run Full End-to-End Endpoint & QA Verification
python scripts/verify_all_endpoints.py
```

### Test Coverage Highlights
- ✅ **College & Office Timings**: Verifies regular timings (Mon-Fri: 9 AM - 4 PM, Sat: 9 AM - 1 PM) and office timings (Mon-Fri: 3 PM - 5 PM, Sat: 1 PM - 3 PM).
- ✅ **Campus Floor Directory**: Verifies Library (1st floor), Computer labs (1st floor), Chemistry lab (Ground floor), Physics lab (4th floor), Principal office (Ground floor), and Books & Stationery store (Ground floor).
- ✅ **College Rules & Dress Code**: Verifies full uniform with shoes, professional attire, neatly trimmed hair and beard, prohibitions on cargos/jeans/t-shirts/chappals/crocs, mandatory ID card, and campus admittance requirements.
- ✅ **Codes**: Verifies KCET `E300`, COMEDK `E005`, PGCET `B097` & `C550`.
- ✅ **HOD Queries**: Correctly identifies Dr. Somanath J Patil (CSE) and Mr. Anil Kumar Warad (AI & DS).
- ✅ **Fee Safety**: Verifies that unconfirmed management fees state *"I couldn't verify the latest official fee for this category..."* and provide admissions contacts.
- ✅ **Hostel**: Verifies Wi-Fi hostel accommodation (400 boys, 700 girls).
- ✅ **Scholarships**: Verifies AICTE Pragati, Saksham, SSP Karnataka, and AET.
- ✅ **Multi-turn Context**: Validates pronoun resolution and conversational flow.
- ✅ **Admin Authentication**: Validates 401 Unauthorized for invalid keys.

---

## 🔐 Administrative Workflow

1. Navigate to the **Knowledge Admin** tab on [http://localhost:8000](http://localhost:8000).
2. Enter the Admin Secret Key (default: `aiet_admin_secret_2026`).
3. You can:
   - View all 102 indexed vector document chunks.
   - Delete outdated or incorrect documents.
   - Paste or upload official circulars to index directly into ChromaDB.
   - Click **Rebuild Full Vector Database** to re-index baseline official JSON files.

---

## 🎓 Academic Project Information

- **Degree**: Bachelor of Engineering (B.E.)
- **Affiliated University**: Visvesvaraya Technological University (VTU), Belagavi
- **College**: Akash Institute of Engineering and Technology (AIET), Devanahalli, Bengaluru
- **Subject**: Computer Science Engineering / Artificial Intelligence & Data Science Mini Project
- **Designed for**: 4-member student project team demonstration
