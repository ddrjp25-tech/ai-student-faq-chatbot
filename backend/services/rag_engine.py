import re
import json
from typing import List, Dict, Any, Optional, Tuple
import httpx
from backend.config import settings
from backend.services.vector_store import VectorStoreService
from backend.models.schemas import ChatResponse, SourceCitation, ChatMessage

SYSTEM_PROMPT = """You are the official AIET Voice Assistant for Akash Institute of Engineering and Technology (AIET), located in Devanahalli, Bengaluru, Karnataka, India.
Your mission is to provide accurate, verified, helpful, and professional answers to students, parents, faculty, and prospective applicants.

CORE PRINCIPLES AND RULES:
1. GROUNDING: Answer questions ONLY using the retrieved context provided below. Never make up or hallucinate information.
2. TIMINGS: 
   - College timing is from 9:00 AM to 4:00 PM from Monday to Friday, and 9:00 AM to 1:00 PM on Saturday.
   - Office timing is from 3:00 PM to 5:00 PM from Monday to Friday, and 1:00 PM to 3:00 PM on Saturday.
3. CODES: KCET Code is E300, COMEDK Code is E005, PGCET MBA Code is B097, PGCET MCA Code is C550.
4. LOCATION: Prasannahalli Road, Devanahalli, near Kempegowda International Airport, Bengaluru, Karnataka – 562110.
5. CAMPUS FLOOR LOCATIONS:
   - Library is located on the first floor.
   - Computer labs are on the first floor.
   - Chemistry lab is on the ground floor.
   - Physics lab is on the fourth floor.
   - Principal's office is on the ground floor.
   - Books and stationery store is on the ground floor.
6. COLLEGE RULES & DRESS CODE:
   - Wear full uniform with shoes.
   - Should maintain professional attire.
   - Hair and beard should be properly trimmed.
   - Cargos, jeans, tshirt, chappals, crocs are not allowed inside campus.
   - Should wear ID card.
   - Without following these rules you might not be permitted inside the campus premises.
   - Minimum 85% attendance is compulsory in classes and labs.
7. AFFILIATION: Affiliated to Visvesvaraya Technological University (VTU), Belagavi, and approved by AICTE, New Delhi.
8. FEES: If asked about management fees or unverified specific branch fees, you MUST state: "I couldn't verify the latest official fee for this category. Please contact the AIET admissions office for confirmation."
   Provide the official admissions contacts: Phone: +91 9513107575 / +91 9513597575, Email: admissions@akashinstitutions.com.
9. FACULTY: For faculty questions, state the exact name, designation, and department as verified from official AIET records.
10. SCHOLARSHIPS: Clearly distinguish government scholarships (SSP, NSP, AICTE Pragati/Saksham) from college-specific assistance (AET). Never guarantee that any student will receive a scholarship.
11. TONE: Professional, friendly, encouraging, and natural for both voice speech and readable text.
12. UNVERIFIED: If the retrieved documents do not contain the answer, say: "I'm sorry, I couldn't verify that information in the available official AIET documents. Please check the official website (https://akashiet.com/) or contact the college admissions office."
"""

class RAGEngine:
    def __init__(self):
        self.vector_store = VectorStoreService.get_instance()

    async def answer_question(
        self,
        question: str,
        history: Optional[List[ChatMessage]] = None,
        session_id: str = "default_session",
        language: str = "en"
    ) -> ChatResponse:
        question_clean = question.strip()
        if not question_clean:
            return ChatResponse(
                answer="Hello! I didn't catch that question. You can ask me about AIET courses, faculty, fees, college timings, scholarships, admissions, and campus facilities.",
                confidence=1.0,
                sources=[],
                needs_confirmation=False,
                suggested_followups=[
                    "What courses does AIET offer?",
                    "What are the college timings?",
                    "Where is AIET located?"
                ]
            )

        # 1. Hybrid Retrieval from ChromaDB
        # Expand query if follow-up context is detected
        search_query = self._expand_query_with_history(question_clean, history)
        retrieved_chunks = self.vector_store.hybrid_search(search_query, top_k=5)

        # 2. Extract sources
        sources: List[SourceCitation] = []
        seen_urls = set()
        for chunk in retrieved_chunks:
            meta = chunk["metadata"]
            url = meta.get("source_url", "https://akashiet.com/")
            if url not in seen_urls:
                seen_urls.add(url)
                sources.append(SourceCitation(
                    title=meta.get("title", "AIET Official Document"),
                    url=url,
                    category=meta.get("category", "General"),
                    last_verified_date=meta.get("last_verified_date", "2026-03-15"),
                    verification_status="VERIFIED_OFFICIAL"
                ))

        # Check retrieval quality
        avg_score = sum(c["score"] for c in retrieved_chunks) / max(len(retrieved_chunks), 1) if retrieved_chunks else 0.0
        confidence = min(round(avg_score, 2), 0.99)
        if confidence < 0.25:
            # Low confidence fallback
            return ChatResponse(
                answer="I'm sorry, I couldn't verify that specific information in the available official AIET documents. Please check the official college portal at https://akashiet.com/ or contact the AIET admissions desk at +91 9513107575 / admissions@akashinstitutions.com.",
                confidence=confidence,
                sources=[],
                needs_confirmation=True,
                confirmation_note="Information not found in official indexed documents.",
                suggested_followups=[
                    "What courses does AIET offer?",
                    "What are the college timings?",
                    "How can I contact admissions?"
                ]
            )

        # 3. Determine if LLM API is available
        llm_key = settings.LLM_API_KEY
        needs_confirmation = self._check_needs_confirmation(question_clean, retrieved_chunks)

        if llm_key and len(llm_key) > 5 and not llm_key.startswith("your_"):
            try:
                answer = await self._generate_with_llm(question_clean, retrieved_chunks, history)
                intent, followups = self._generate_followups_and_intent(question_clean, retrieved_chunks)
                return ChatResponse(
                    answer=answer,
                    sources=sources,
                    confidence=confidence,
                    needs_confirmation=needs_confirmation,
                    confirmation_note="Please confirm final fee structure and admission requirements with the AIET admissions office." if needs_confirmation else None,
                    language=language,
                    intent=intent,
                    suggested_followups=followups
                )
            except Exception as e:
                print(f"LLM generation failed, falling back to offline grounded synthesizer: {e}")

        # 4. Fallback / Offline Grounded Synthesizer
        answer = self._generate_grounded_fallback(question_clean, retrieved_chunks, history)
        intent, followups = self._generate_followups_and_intent(question_clean, retrieved_chunks)

        return ChatResponse(
            answer=answer,
            sources=sources,
            confidence=confidence,
            needs_confirmation=needs_confirmation,
            confirmation_note="Fees and admission policies are subject to annual regulatory updates. Contact admissions for official verification." if needs_confirmation else None,
            language=language,
            intent=intent,
            suggested_followups=followups
        )

    def _expand_query_with_history(self, question: str, history: Optional[List[ChatMessage]]) -> str:
        """Expands pronoun/follow-up queries using recent context."""
        if not history or len(history) < 2:
            return question
        
        # Check if question is a short follow-up
        lower = question.lower()
        if any(term in lower for term in ["hod", "head", "eligibility", "fees", "fee", "timing", "where", "how many", "who is", "what about"]):
            # Get last user question
            last_user_msg = next((m.content for m in reversed(history) if m.role == "user"), "")
            if last_user_msg and last_user_msg.lower() != lower:
                return f"{last_user_msg} {question}"
        return question

    def _check_needs_confirmation(self, question: str, chunks: List[Dict[str, Any]]) -> bool:
        lower = question.lower()
        if any(w in lower for w in ["fee", "fees", "cost", "tuition", "hostel fee", "management quota", "deadline", "last date", "refund"]):
            return True
        return False

    async def _generate_with_llm(self, question: str, chunks: List[Dict[str, Any]], history: Optional[List[ChatMessage]]) -> str:
        """Calls external OpenAI-compatible API with strict grounding context."""
        context_text = "\n\n".join([f"Document [{c['id']}] - {c['metadata'].get('title')}:\n{c['content']}" for c in chunks])
        
        messages = [
            {"role": "system", "content": f"{SYSTEM_PROMPT}\n\nCURRENT VERIFIED AIET CONTEXT:\n{context_text}"}
        ]
        
        # Add recent conversation turns
        if history:
            for msg in history[-4:]:
                messages.append({"role": msg.role, "content": msg.content})
                
        messages.append({"role": "user", "content": question})

        headers = {
            "Authorization": f"Bearer {settings.LLM_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": settings.LLM_MODEL,
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": 600
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                f"{settings.LLM_BASE_URL.rstrip('/')}/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()

    def _generate_grounded_fallback(self, question: str, chunks: List[Dict[str, Any]], history: Optional[List[ChatMessage]]) -> str:
        """
        High-precision deterministic grounded synthesizer.
        Extracts verified answers directly from the top matching official chunks.
        """
        q = question.lower()
        top_chunk = chunks[0]
        top_content = top_chunk["content"]
        top_title = top_chunk["metadata"].get("title", "")

        # 1. College Rules & Code of Conduct
        if any(w in q for w in ["rule", "rules", "dress code", "uniform", "attire", "beard", "hair", "shoes", "crocs", "chappals", "cargos", "jeans", "tshirt", "t-shirt", "id card", "permitted", "campus premises"]):
            return (
                "Official AIET College Rules & Code of Conduct:\n\n"
                "• Wear full uniform with shoes\n"
                "• Should maintain professional attire\n"
                "• Hair and beard should be properly trimmed\n"
                "• Cargos, jeans, tshirt, chappals, crocs are not allowed inside campus\n"
                "• Should wear ID card\n"
                "• Without following these rules you might not be permitted inside the campus premises\n"
                "• Minimum 85% attendance is compulsory across all classes and laboratories."
            )

        # 2. Specific Campus Floor Locations
        if "library" in q and any(w in q for w in ["where", "floor", "locate", "which"]):
            return "Our library is located on the first floor."
        if ("computer lab" in q or "computer laboratory" in q or "computer labs" in q) and any(w in q for w in ["where", "floor", "locate", "which"]):
            return "Computer labs are located on the first floor."
        if "chemistry" in q and any(w in q for w in ["where", "floor", "locate", "which", "lab"]):
            return "The chemistry lab is located on the ground floor."
        if "physics" in q and any(w in q for w in ["where", "floor", "locate", "which", "lab"]):
            return "The physics lab is located on the fourth floor."
        if "principal" in q and any(w in q for w in ["office", "where", "floor", "locate", "which"]):
            return "The Principal's office is located on the ground floor."
        if any(w in q for w in ["books", "stationary", "stationery"]) and any(w in q for w in ["where", "floor", "locate", "store", "shop"]):
            return "The books and stationery store is located on the ground floor."
        if any(w in q for w in ["floor", "floors", "directory", "navigation"]) and any(w in q for w in ["campus", "building", "where", "list", "layout"]):
            return (
                "AIET Campus Floor Directory:\n\n"
                "• Ground Floor: Principal's Office, College Administrative Office, Books and Stationery store, Chemistry Lab\n"
                "• First Floor: Central Library, Computer Labs\n"
                "• Fourth Floor: Physics Lab"
            )

        # 3. College Timings & Office Hours
        if any(w in q for w in ["timing", "timings", "time", "hours", "schedule", "open", "close"]):
            if "office" in q:
                return (
                    "AIET Administrative Office Timing:\n"
                    "• Monday to Friday: 3:00 PM to 5:00 PM (3 PM to 5 PM)\n"
                    "• Saturday: 1:00 PM to 3:00 PM (1 PM to 3 PM)\n"
                    "The administrative office is located on the ground floor."
                )
            return (
                "The college timing and office hours for Akash Institute of Engineering and Technology (AIET) are:\n\n"
                "• College Timing: 9:00 AM to 4:00 PM from Monday to Friday, and 9:00 AM to 1:00 PM on Saturday\n"
                "• Office Timing: 3:00 PM to 5:00 PM from Monday to Friday, and 1:00 PM to 3:00 PM on Saturday"
            )

        # 2. Codes (KCET / COMEDK / PGCET)
        if any(w in q for w in ["kcet", "comedk", "code", "pgcet", "e300", "e005"]):
            return (
                "Here are the official institutional entrance exam codes for Akash Institute of Engineering and Technology (AIET):\n\n"
                "• KCET Code (KEA Engineering): E300\n"
                "• COMEDK Code (UGET Engineering): E005\n"
                "• KEA-PGCET MBA Code: B097\n"
                "• KEA-PGCET MCA Code: C550\n\n"
                "These codes can be used directly during option entry and counselling rounds."
            )

        # 3. Location / Address
        if any(w in q for w in ["where", "location", "address", "locate", "devanahalli", "how to reach", "campus address"]):
            return (
                "Akash Institute of Engineering and Technology (AIET) is located at:\n"
                "Prasannahalli Road, Devanahalli, near Kempegowda International Airport, Bengaluru, Karnataka – 562110, India.\n\n"
                "The campus is situated just off NH-44 (Bellary Road), approximately 10 to 15 minutes from Bengaluru Kempegowda International Airport (BLR), "
                "and is well-connected by college buses, BMTC buses, and the Devanahalli railway terminal."
            )

        # 4. Affiliation and Approvals
        if any(w in q for w in ["affiliation", "affiliated", "vtu", "aicte", "approval", "approved", "recognised", "recognized"]):
            return (
                "Akash Institute of Engineering and Technology (AIET) is affiliated with Visvesvaraya Technological University (VTU), Belagavi, "
                "approved by the All India Council for Technical Education (AICTE), New Delhi, and recognized by the Government of Karnataka. "
                "It is managed by the Akash Education & Development Trust (AEDT) under the Akash Group of Institutions."
            )

        # 5. Courses Offered
        if any(w in q for w in ["what courses", "courses offer", "branches", "programs", "departments", "which engineering", "b.e courses"]):
            return (
                "Akash Institute of Engineering and Technology (AIET) offers 8 Undergraduate B.E. programmes and 2 Postgraduate programmes, all affiliated to VTU Belagavi and approved by AICTE:\n\n"
                "Undergraduate (B.E. - 4 Years):\n"
                "1. BE Computer Science and Engineering (CSE)\n"
                "2. BE Information Science and Engineering (ISE)\n"
                "3. BE Computer Science (Artificial Intelligence & Machine Learning)\n"
                "4. BE Artificial Intelligence and Data Science (AI & DS)\n"
                "5. BE Computer Science Engineering (Cyber Security)\n"
                "6. BE Computer Science Engineering (Data Science)\n"
                "7. BE Electronics and Communication Engineering (ECE)\n"
                "8. BE Mechanical Engineering (ME)\n\n"
                "Postgraduate (2 Years):\n"
                "1. Master of Business Administration (MBA - PGCET Code: B097)\n"
                "2. Master of Computer Applications (MCA - PGCET Code: C550)\n\n"
                "Lateral entry admission directly into the 3rd semester is also offered for eligible Diploma and B.Sc. graduates."
            )

        # 6. Fees & Expenses
        if any(w in q for w in ["fee", "fees", "tuition", "cost", "charge", "expenses", "hostel fee", "bus fee"]):
            # Specific branch fee or management fee
            return (
                "Regarding fees at Akash Institute of Engineering and Technology (AIET):\n\n"
                "• Government Quota (KCET Code: E300): Fees are regulated annually by the Karnataka Examination Authority (KEA) Fee Regulatory Committee (typically approx. ₹75,000 - ₹1,05,000/year for unaided private institutions, plus VTU fees).\n"
                "• COMEDK Quota (Code: E005): As per the official COMEDK consortium fee circular for the academic year.\n"
                "• Management Quota: I couldn't verify the latest official fee for this category. Please contact the AIET admissions office for confirmation.\n\n"
                "To receive the exact verified fee structure, brochure, and payment schedule, please contact:\n"
                "• Admissions Helpline: +91 9513107575 / +91 9513597575\n"
                "• Landline: 080-244-11-222\n"
                "• Email: admissions@akashinstitutions.com\n"
                "• Official Portal: https://admissions.akashinstitutions.com/engineering"
            )

        # 7. Faculty / HOD questions
        if any(w in q for w in ["hod", "head of department", "who is the hod", "faculty", "professor", "teacher", "who teaches"]):
            # Find the best matching faculty chunk for the requested department
            target_chunk = None
            if ("computer science and engineering" in q or "cse" in q) and "data" not in q and "cyber" not in q:
                target_chunk = next((c for c in chunks if "fac_dept_computer_science___engineering" in c["id"] or ("computer science & engineering" in c["content"].lower() and "data" not in c["content"].lower() and "cyber" not in c["content"].lower())), None)
            elif "data science" in q and ("ai" in q or "artificial" in q):
                target_chunk = next((c for c in chunks if "artificial_intelligence___data_science" in c["id"] or "ai & ds" in c["content"].lower()), None)
            elif "machine learning" in q or "aiml" in q or "ai & ml" in q:
                target_chunk = next((c for c in chunks if "artificial_intelligence___machine_learning" in c["id"]), None)
            elif "cyber" in q:
                target_chunk = next((c for c in chunks if "cybersecurity" in c["id"] or "cyber" in c["content"].lower()), None)
            elif "data science" in q:
                target_chunk = next((c for c in chunks if "datascience" in c["id"]), None)
            elif "information science" in q or "ise" in q:
                target_chunk = next((c for c in chunks if "information_science" in c["id"] or "ise" in c["content"].lower()), None)
            elif "electronics" in q or "ece" in q:
                target_chunk = next((c for c in chunks if "electronics" in c["id"]), None)
            elif "mechanical" in q:
                target_chunk = next((c for c in chunks if "mechanical" in c["id"]), None)
            elif "mba" in q or "management" in q:
                target_chunk = next((c for c in chunks if "management" in c["id"]), None)
            elif "mca" in q:
                target_chunk = next((c for c in chunks if "mca" in c["id"]), None)
            elif any(sub in q for sub in ["math", "physics", "chemistry", "basic science"]):
                target_chunk = next((c for c in chunks if "basic_science" in c["id"]), None)

            if not target_chunk:
                target_chunk = next((c for c in chunks if "faculty" in c["metadata"].get("category", "").lower() or "faculty" in c["content"].lower()), chunks[0])

            return (
                f"Based on the official AIET Faculty Directory:\n\n{target_chunk['content']}\n\n"
                f"For verified profile documents and curriculum vitae, visit the official AIET faculty directory at https://akashiet.com/faculty/."
            )

        # 8. Scholarships
        if any(w in q for w in ["scholarship", "scholarships", "financial aid", "concession", "ssp", "nsp", "pragati", "saksham", "aet"]):
            return (
                "Akash Institute of Engineering and Technology (AIET) supports multiple scholarship opportunities:\n\n"
                "1. Akash Entrance Test (AET): Institutional merit-based scholarships awarded by Akash Group of Institutions for outstanding scores in qualifying exams.\n"
                "2. AGI Awards of Excellence: Honors department toppers, academic achievers, and sports/cultural talents.\n"
                "3. Karnataka State Scholarship Portal (SSP): Post-Matric fee concessions, maintenance, and Vidyasiri assistance for eligible Karnataka SC, ST, and OBC students.\n"
                "4. National Scholarship Portal (NSP): Central Sector Schemes for meritorious students and Minority communities (Muslim, Christian, Jain, Sikh, Buddhist, Parsi).\n"
                "5. AICTE Pragati Scholarship: ₹50,000 per annum for eligible girl students admitted to technical degree courses.\n"
                "6. AICTE Saksham Scholarship: ₹50,000 per annum for specially-abled students with >=40% disability.\n\n"
                "Note: Government scholarships are disbursed through official portals (SSP/NSP) via Direct Benefit Transfer (DBT). Contact admissions@akashinstitutions.com for documentation support."
            )

        # 9. Hostel and Campus Facilities
        if any(w in q for w in ["hostel", "accommodation", "stay", "mess", "food", "cafeteria", "canteen", "library", "auditorium", "hospital", "gym", "sports", "bus", "transport"]):
            for c in chunks:
                if "infrastructure" in c["metadata"].get("category", "").lower() or any(term in c["content"].lower() for term in ["hostel", "library", "auditorium", "hospital"]):
                    return (
                        f"Campus Infrastructure & Facilities at AIET:\n\n{c['content']}\n\n"
                        "Highlights include Wi-Fi enabled hostels (400 boys, 700 girls), 1,500-seat central auditorium, "
                        "on-campus 24/7 Akash Hospital with emergency care, Central Library with VTU e-resources, and sports grounds."
                    )

        # 10. Default synthesization from top chunks
        summary_sentences = []
        for c in chunks[:3]:
            # Take first 2 meaningful sentences
            sentences = re.split(r'(?<=[.!?])\s+', c["content"])
            for s in sentences[:2]:
                s_strip = s.strip()
                if s_strip and len(s_strip) > 20 and s_strip not in summary_sentences:
                    summary_sentences.append(s_strip)

        extracted_text = " ".join(summary_sentences[:4])
        return (
            f"Here is the verified information from official AIET records:\n\n{extracted_text}\n\n"
            f"For further details or official brochures, please check https://akashiet.com/ or reach out to the admissions office at +91 9513107575 / admissions@akashinstitutions.com."
        )

    def _generate_followups_and_intent(self, question: str, chunks: List[Dict[str, Any]]) -> Tuple[str, List[str]]:
        """Determines query intent and offers intuitive suggested follow-up questions."""
        q = question.lower()
        if any(w in q for w in ["rule", "rules", "uniform", "dress code", "id card", "attire"]):
            return "RULES", [
                "What are the college timings?",
                "Where is the library located?",
                "What are the office timings?",
                "What courses are offered at AIET?"
            ]
        elif any(w in q for w in ["floor", "where is", "chemistry lab", "physics lab", "principal office", "stationary", "stationery"]):
            return "CAMPUS_DIRECTORY", [
                "Where is the library located?",
                "Where are the computer labs?",
                "What are the college timings?",
                "What are the college rules?"
            ]
        elif any(w in q for w in ["timing", "hour", "schedule"]):
            return "TIMINGS", [
                "What are the office timings?",
                "Where is the AIET campus located?",
                "What courses are offered at AIET?",
                "What are the college rules?"
            ]
        elif any(w in q for w in ["course", "branch", "engineering", "b.e", "mba", "mca"]):
            return "COURSES", [
                "What is the eligibility for Computer Science Engineering?",
                "What are the KCET and COMEDK codes for AIET?",
                "Who is the HOD of AI and Data Science?",
                "Does AIET offer hostel facilities?"
            ]
        elif any(w in q for w in ["fee", "fees", "cost", "tuition"]):
            return "FEES", [
                "What scholarships can I apply for?",
                "What is the KCET code for AIET?",
                "How do I contact the admissions office?",
                "What are the hostel charges?"
            ]
        elif any(w in q for w in ["hod", "faculty", "professor", "teacher"]):
            return "FACULTY", [
                "Who is the HOD of Computer Science?",
                "Who is the HOD of AI and Data Science?",
                "What courses does AIET offer?",
                "What are the college timings?"
            ]
        elif any(w in q for w in ["scholarship", "ssp", "nsp", "pragati"]):
            return "SCHOLARSHIPS", [
                "How do I apply for the AICTE Pragati scholarship?",
                "What is the Akash Entrance Test (AET)?",
                "What are the admission requirements for B.E.?"
            ]
        elif any(w in q for w in ["hostel", "facility", "infrastructure", "library", "hospital", "sports"]):
            return "INFRASTRUCTURE", [
                "Does AIET have an on-campus hospital?",
                "What are the college bus transportation routes?",
                "What is the capacity of the student hostels?"
            ]
        elif any(w in q for w in ["code", "kcet", "comedk", "pgcet"]):
            return "CODES", [
                "What is the admission procedure for KCET students?",
                "What courses does AIET offer?",
                "What are the college timings?"
            ]
        else:
            return "GENERAL", [
                "What courses does AIET offer?",
                "What are the college timings?",
                "Who is the HOD of AI and Data Science?",
                "Does AIET have hostel facilities?"
            ]
