import pytest
import asyncio
from backend.services.rag_engine import RAGEngine
from backend.models.schemas import ChatMessage

@pytest.fixture(scope="module")
def rag_engine():
    return RAGEngine()

def test_college_timings(rag_engine):
    res = asyncio.run(rag_engine.answer_question("What are the college timings?"))
    assert "9:00 AM" in res.answer or "9 AM" in res.answer
    assert "4:00 PM" in res.answer or "4 PM" in res.answer
    assert len(res.sources) > 0

def test_kcet_and_comedk_codes(rag_engine):
    res = asyncio.run(rag_engine.answer_question("What are the KCET and COMEDK codes for AIET?"))
    assert "E300" in res.answer
    assert "E005" in res.answer

def test_courses_offered(rag_engine):
    res = asyncio.run(rag_engine.answer_question("What courses does AIET offer?"))
    assert "Computer Science" in res.answer
    assert "Artificial Intelligence" in res.answer
    assert "Mechanical" in res.answer
    assert "MBA" in res.answer

def test_hod_ai_and_data_science(rag_engine):
    res = asyncio.run(rag_engine.answer_question("Who is the HOD of AI and Data Science?"))
    assert "Anil Kumar Warad" in res.answer

def test_hod_cse(rag_engine):
    res = asyncio.run(rag_engine.answer_question("Who is the HOD of Computer Science and Engineering?"))
    assert "Somanath" in res.answer

def test_fee_guidance_rule(rag_engine):
    res = asyncio.run(rag_engine.answer_question("What is the management fee for Computer Science?"))
    assert "couldn't verify" in res.answer.lower() or "admissions office" in res.answer.lower()
    assert res.needs_confirmation is True
    assert "9513107575" in res.answer or "admissions@akashinstitutions.com" in res.answer

def test_hostel_facilities(rag_engine):
    res = asyncio.run(rag_engine.answer_question("Does AIET have hostel facilities?"))
    assert "hostel" in res.answer.lower()
    assert "400" in res.answer or "700" in res.answer

def test_scholarships(rag_engine):
    res = asyncio.run(rag_engine.answer_question("What scholarships can students apply for?"))
    assert "pragati" in res.answer.lower() or "ssp" in res.answer.lower() or "aet" in res.answer.lower()

def test_location(rag_engine):
    res = asyncio.run(rag_engine.answer_question("Where is AIET located?"))
    assert "devanahalli" in res.answer.lower()
    assert "bengaluru" in res.answer.lower() or "bangalore" in res.answer.lower()

def test_followup_question(rag_engine):
    # Turn 1: user asks about AI and Data Science course
    turn1 = asyncio.run(rag_engine.answer_question("Tell me about BE Artificial Intelligence and Data Science"))
    # Turn 2: user asks follow-up "Who is the HOD?"
    history = [
        ChatMessage(role="user", content="Tell me about BE Artificial Intelligence and Data Science"),
        ChatMessage(role="assistant", content=turn1.answer)
    ]
    turn2 = asyncio.run(rag_engine.answer_question("Who is the HOD?", history=history))
    assert "Anil Kumar Warad" in turn2.answer

def test_library_and_computer_labs_location(rag_engine):
    res_lib = asyncio.run(rag_engine.answer_question("Where is the library located?"))
    assert "first floor" in res_lib.answer.lower()
    
    res_comp = asyncio.run(rag_engine.answer_question("Where are the computer labs located?"))
    assert "first floor" in res_comp.answer.lower()

def test_chemistry_and_physics_labs_location(rag_engine):
    res_chem = asyncio.run(rag_engine.answer_question("Where is the chemistry lab located?"))
    assert "ground floor" in res_chem.answer.lower()

    res_phys = asyncio.run(rag_engine.answer_question("Where is the physics lab located?"))
    assert "fourth floor" in res_phys.answer.lower()

def test_principal_office_and_stationery_location(rag_engine):
    res_prin = asyncio.run(rag_engine.answer_question("Where is the principal office?"))
    assert "ground floor" in res_prin.answer.lower()

    res_stat = asyncio.run(rag_engine.answer_question("Where is the books and stationary store?"))
    assert "ground floor" in res_stat.answer.lower()

def test_office_and_college_timings(rag_engine):
    res_col = asyncio.run(rag_engine.answer_question("What are the college timings?"))
    assert "9:00 am to 4:00 pm" in res_col.answer.lower() or "9 am to 4 pm" in res_col.answer.lower()
    assert "9:00 am to 1:00 pm" in res_col.answer.lower() or "9 am to 1 pm" in res_col.answer.lower()
    assert "saturday" in res_col.answer.lower()

    res_off = asyncio.run(rag_engine.answer_question("What is the office timing?"))
    assert "3:00 pm to 5:00 pm" in res_off.answer.lower() or "3 pm to 5 pm" in res_off.answer.lower()
    assert "1:00 pm to 3:00 pm" in res_off.answer.lower() or "1 pm to 3 pm" in res_off.answer.lower()

def test_college_rules(rag_engine):
    res_rules = asyncio.run(rag_engine.answer_question("What are the college rules?"))
    ans = res_rules.answer.lower()
    assert "uniform" in ans
    assert "shoes" in ans
    assert "professional attire" in ans
    assert "hair" in ans and "beard" in ans and "trimmed" in ans
    assert "cargos" in ans or "jeans" in ans or "crocs" in ans
    assert "id card" in ans
    assert "permitted" in ans or "campus premises" in ans

