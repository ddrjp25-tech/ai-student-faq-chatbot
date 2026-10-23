import os
import json
import re
import math
from typing import List, Dict, Any, Tuple
from pathlib import Path
import chromadb
from chromadb.config import Settings as ChromaSettings
from backend.config import settings

class VectorStoreService:
    _instance = None
    
    def __init__(self):
        self.persist_dir = str(settings.CHROMA_PERSIST_DIR)
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        self.collection_name = "aiet_knowledge_base"
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "Akash Institute of Engineering and Technology Knowledge Base"}
        )
        self.documents_metadata: Dict[str, Dict[str, Any]] = {}
        # Ensure knowledge base is indexed if empty
        if self.collection.count() == 0:
            self.index_all_knowledge_base()
        else:
            self._load_doc_cache()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = VectorStoreService()
        return cls._instance

    def _load_doc_cache(self):
        # Cache existing metadata
        try:
            results = self.collection.get()
            if results and "metadatas" in results:
                for idx, m in enumerate(results["metadatas"]):
                    doc_id = results["ids"][idx]
                    self.documents_metadata[doc_id] = m
        except Exception as e:
            print(f"Notice loading doc cache: {e}")

    def index_all_knowledge_base(self):
        """Indexes all structured JSON files in the knowledge_base directory into ChromaDB."""
        print("Indexing AIET knowledge base into ChromaDB...")
        kb_path = settings.KB_DIR
        chunks = []
        
        # 1. College Profile
        prof_file = kb_path / "college_profile.json"
        if prof_file.exists():
            with open(prof_file, "r", encoding="utf-8") as f:
                prof = json.load(f)
            # Main profile chunk
            chunks.append({
                "id": "prof_main",
                "title": "AIET Institutional Profile and Overview",
                "category": "College Profile",
                "content": f"Akash Institute of Engineering and Technology (AIET) is a premier engineering college established in 2020 by the Akash Education & Development Trust (AEDT) under the Akash Group of Institutions (AGI). Located on Prasannahalli Road, Devanahalli, near Kempegowda International Airport, Bengaluru, Karnataka - 562110. Regular college timings are 9:00 AM to 4:00 PM. Affiliated to Visvesvaraya Technological University (VTU), Belagavi, approved by AICTE, New Delhi, and recognized by Government of Karnataka. Official website: https://akashiet.com/. Admissions Contact: +91 9513107575, +91 9513597575, Landline 080-244-11-222, Email: admissions@akashinstitutions.com.",
                "source_url": "https://akashiet.com/about-us/",
                "source_type": "Official College Portal",
                "academic_year": "2025-2026",
                "last_verified_date": "2026-03-15",
                "keywords": ["aiet", "akash institute of engineering and technology", "location", "address", "devanahalli", "bengaluru", "airport", "overview", "established", "trust"]
            })
            # Codes & Entrance chunk
            chunks.append({
                "id": "prof_codes",
                "title": "AIET College Codes for KCET, COMEDK, PGCET",
                "category": "Admissions & Codes",
                "content": f"Official Institutional Codes for Akash Institute of Engineering & Technology (AIET), Devanahalli, Bengaluru: KCET CODE: E300 (Karnataka Common Entrance Test for B.E. government quota). COMEDK CODE: E005 (Consortium of Medical, Engineering and Dental Colleges of Karnataka for all-India B.E. admissions). KEA-PGCET MBA CODE: B097 (Post Graduate Common Entrance Test for MBA). KEA-PGCET MCA CODE: C550 (Post Graduate Common Entrance Test for MCA).",
                "source_url": "https://akashiet.com/",
                "source_type": "Official College Portal",
                "academic_year": "2025-2026",
                "last_verified_date": "2026-03-15",
                "keywords": ["kcet code", "comedk code", "pgcet code", "e300", "e005", "b097", "c550", "code"]
            })
            # Timings chunk
            chunks.append({
                "id": "prof_timings",
                "title": "AIET Regular College Timings & Office Hours",
                "category": "Academic Timings",
                "content": f"The regular college timing for Akash Institute of Engineering and Technology (AIET) is from 9:00 AM to 4:00 PM from Monday to Friday, and from 9:00 AM to 1:00 PM on Saturday. The college administrative office timing is from 3:00 PM to 5:00 PM from Monday to Friday, and from 1:00 PM to 3:00 PM on Saturday.",
                "source_url": "https://akashiet.com/",
                "source_type": "Official Institutional Record",
                "academic_year": "2025-2026",
                "last_verified_date": "2026-03-15",
                "keywords": ["timings", "college timings", "timing", "hours", "schedule", "working hours", "9:00 AM", "4:00 PM", "saturday timings", "9 am to 1 pm", "9 am to 4 pm", "monday to friday", "office timing", "3 pm to 5 pm", "1 pm to 3 pm"]
            })
            # Office Hours chunk
            chunks.append({
                "id": "prof_office_timings",
                "title": "AIET Administrative Office Timings and Location",
                "category": "Administrative Office",
                "content": f"AIET College Office timings: Monday to Friday from 3:00 PM to 5:00 PM, and Saturday from 1:00 PM to 3:00 PM. The administrative office is located on the ground floor. Students can visit the office during these operational hours for admissions, documents, fee certificates, and inquiries.",
                "source_url": "https://akashiet.com/",
                "source_type": "Official Institutional Record",
                "academic_year": "2025-2026",
                "last_verified_date": "2026-03-15",
                "keywords": ["office timing", "office timings", "office hours", "when does office open", "administrative office", "office on ground floor", "3 pm to 5 pm", "1 pm to 3 pm", "ground floor"]
            })
            # Campus Floor Directory chunk
            chunks.append({
                "id": "prof_floor_directory",
                "title": "AIET Campus Floor Directory & Landmark Navigation",
                "category": "Campus Navigation",
                "content": f"AIET Campus Floor Navigation Directory: 1. Ground Floor: Houses the Principal's Office, the Administrative Office (college office), the Books and Stationery store, and the Chemistry Lab. 2. First Floor: Houses the Central Library and the specialized Computer Labs. 3. Fourth Floor: Houses the Physics Lab.",
                "source_url": "https://akashiet.com/",
                "source_type": "Official Institutional Record",
                "academic_year": "2025-2026",
                "last_verified_date": "2026-03-15",
                "keywords": ["library floor", "where is library", "library located", "first floor", "computer labs floor", "computer labs located", "chemistry lab", "chemistry lab on ground floor", "physics lab", "physics lab on fourth floor", "fourth floor", "4th floor", "principal office floor", "ground floor", "books and stationary", "office floor", "where is office", "where is principal office", "floor directory", "campus directory"]
            })
            # College Rules & Dress Code chunk
            chunks.append({
                "id": "prof_college_rules",
                "title": "AIET College Rules, Grooming & Dress Code",
                "category": "Student Code of Conduct",
                "content": f"Official AIET College Rules & Code of Conduct: 1. Wear full uniform with shoes. 2. Should maintain professional attire. 3. Hair and beard should be properly trimmed. 4. Cargos, jeans, tshirt, chappals, crocs are not allowed inside campus. 5. Should wear ID card. 6. Without following these rules you might not be permitted inside the campus premises. 7. Maintain 85% attendance compulsory in all classes and labs.",
                "source_url": "https://akashiet.com/",
                "source_type": "Official Institutional Record",
                "academic_year": "2025-2026",
                "last_verified_date": "2026-03-15",
                "keywords": ["rules", "college rules", "dress code", "uniform", "shoes", "professional attire", "hair", "beard", "trimmed", "hair and beard properly trimmed", "cargos", "jeans", "tshirt", "chappals", "crocs", "not allowed inside campus", "id card", "wear id card", "permitted inside campus", "campus premises", "85% attendance", "code of conduct"]
            })
            # Vision and Mission
            chunks.append({
                "id": "prof_vision_mission",
                "title": "AIET Vision, Mission, and Institutional Purpose",
                "category": "College Profile",
                "content": f"Vision of AIET: To emerge as a premier centre of excellence in engineering education and research, empowering young minds with technical competence, innovation, leadership, and ethical values to meet global societal challenges. Mission of AIET: Deliver quality technical education through state-of-the-art curriculum, modern laboratories, and experiential learning; Foster research, innovation, entrepreneurship, and interdisciplinary collaborations with leading industries and global universities; Inculcate ethical standards, environmental consciousness, and leadership skills for holistic student development.",
                "source_url": "https://akashiet.com/about-us/",
                "source_type": "Official College Portal",
                "academic_year": "2025-2026",
                "last_verified_date": "2026-03-15",
                "keywords": ["vision", "mission", "purpose", "values", "goals"]
            })

        # 2. Courses
        courses_file = kb_path / "courses.json"
        if courses_file.exists():
            with open(courses_file, "r", encoding="utf-8") as f:
                courses = json.load(f)
            # Courses summary chunk
            course_names = [c["course_name"] for c in courses]
            chunks.append({
                "id": "courses_summary",
                "title": "Engineering and Postgraduate Programmes Offered at AIET",
                "category": "Courses and Departments",
                "content": f"Akash Institute of Engineering and Technology offers Undergraduate (UG) and Postgraduate (PG) programmes affiliated to VTU Belagavi and approved by AICTE. UG B.E. Programmes (4 Years): 1. BE Computer Science and Engineering (CSE), 2. BE Information Science and Engineering (ISE), 3. BE Computer Science (Artificial Intelligence & Machine Learning), 4. BE Artificial Intelligence and Data Science (AI & DS), 5. BE Computer Science Engineering (Cyber Security), 6. BE Computer Science Engineering (Data Science), 7. BE Electronics and Communication Engineering (ECE), 8. BE Mechanical Engineering (ME). PG Programmes (2 Years): 1. Master of Business Administration (MBA, PGCET Code: B097), 2. Master of Computer Applications (MCA, PGCET Code: C550). Lateral Entry (3 Years): Direct admission to 3rd semester for Diploma/B.Sc. holders.",
                "source_url": "https://akashiet.com/",
                "source_type": "Official College Portal",
                "academic_year": "2025-2026",
                "last_verified_date": "2026-03-15",
                "keywords": ["courses", "branches", "departments", "programs", "degrees", "b.e", "mba", "mca", "ug", "pg", "what courses"]
            })
            # Individual Course Chunks
            for c in courses:
                cid = c["id"]
                labs_str = ", ".join(c.get("specialized_laboratories", [])) if c.get("specialized_laboratories") else "Departmental laboratories"
                routes_str = ", ".join([f"{r.get('route')} ({r.get('code', '')})" for r in c.get("admission_routes", [])])
                content_text = f"Course Name: {c['course_name']} ({c['short_name']}). Department: {c.get('department')}. Head of Department: {c.get('head_of_department', 'Not published')}. Level: {c['level']}. Duration: {c['duration']}. Affiliated to VTU Belagavi, approved by AICTE. Eligibility: {c['eligibility']}. Admission Routes: {routes_str}. Laboratories: {labs_str}. Curriculum Highlights: {c.get('curriculum_highlights', '')}. Career Pathways: {c.get('career_pathways', '')}."
                chunks.append({
                    "id": f"course_{cid}",
                    "title": f"Course Profile: {c['course_name']}",
                    "category": "Courses and Departments",
                    "content": content_text,
                    "source_url": c.get("source_url", "https://akashiet.com/"),
                    "source_type": "Official College Portal",
                    "academic_year": "2025-2026",
                    "last_verified_date": "2026-03-15",
                    "keywords": [c["short_name"].lower(), c["course_name"].lower(), "eligibility", "duration", "curriculum", "labs"]
                })

        # 3. Faculty
        fac_file = kb_path / "faculty.json"
        if fac_file.exists():
            with open(fac_file, "r", encoding="utf-8") as f:
                faculty = json.load(f)
            
            # Faculty by department aggregation chunks
            depts = {}
            for fac in faculty:
                d = fac["department"]
                depts.setdefault(d, []).append(fac)
            
            for d, fac_list in depts.items():
                hod = next((f for f in fac_list if f.get("is_head_of_department")), None)
                hod_str = f"Head of Department (HOD): {hod['name']} ({hod['designation']}). " if hod else ""
                members_str = "; ".join([f"{f['name']} ({f['designation']})" for f in fac_list])
                chunks.append({
                    "id": f"fac_dept_{re.sub(r'[^a-zA-Z0-9]', '_', d).lower()}",
                    "title": f"Faculty Members in {d}",
                    "category": "Faculty Directory",
                    "content": f"Department: {d} at Akash Institute of Engineering and Technology (AIET). {hod_str}Publicly listed faculty members ({len(fac_list)} members): {members_str}. All faculty profiles are verifiable via the official AIET faculty directory at https://akashiet.com/faculty/.",
                    "source_url": "https://akashiet.com/faculty/",
                    "source_type": "Official Faculty Records",
                    "academic_year": "2025-2026",
                    "last_verified_date": "2026-03-15",
                    "keywords": ["faculty", "teachers", "professors", d.lower(), "hod", "head of department"]
                })
            
            # Individual HOD & Faculty member chunks for exact name queries
            for fac in faculty:
                fid = fac["id"]
                pdf_info = f"Official Profile Document: {fac['profile_pdf_url']}. " if fac.get("profile_pdf_url") else ""
                chunks.append({
                    "id": f"fac_indiv_{fid}",
                    "title": f"Faculty Profile: {fac['name']} ({fac['department']})",
                    "category": "Faculty Directory",
                    "content": f"Faculty Name: {fac['name']}. Designation: {fac['designation']}. Department: {fac['department']}. Institution: Akash Institute of Engineering and Technology (AIET), Devanahalli. Head of Department status: {'Yes (HOD)' if fac.get('is_head_of_department') else 'Faculty Member'}. {pdf_info}Source: AIET Official Faculty Directory (https://akashiet.com/faculty/).",
                    "source_url": fac.get("source_url", "https://akashiet.com/faculty/"),
                    "source_type": "Official Faculty Directory",
                    "academic_year": "2025-2026",
                    "last_verified_date": "2026-03-15",
                    "keywords": [fac["name"].lower(), fac["department"].lower(), fac["designation"].lower(), "hod", "professor"]
                })

        # 4. Fees
        fees_file = kb_path / "fees.json"
        if fees_file.exists():
            with open(fees_file, "r", encoding="utf-8") as f:
                fees = json.load(f)
            for fee in fees:
                fid = fee["id"]
                fee_amount = fee.get('fee_range_inr') or fee.get('fee_details', 'Contact Admissions')
                guidance = fee.get('official_guidance_rule') or fee.get('policy_summary', '')
                content_text = f"Title: {fee['title']}. Category: Fees and Expenses. Quota: {fee.get('quota_type', 'Institutional')}. Academic Year: {fee.get('academic_year', '2025-2026')}. Fee Details: {fee_amount}. Official Policy: {guidance}. Mandatory components: {', '.join(fee.get('mandatory_components', [])) if fee.get('mandatory_components') else 'Tuition & University fees'}. Contact: Admissions Office at +91 9513107575 / +91 9513597575 or admissions@akashinstitutions.com."
                chunks.append({
                    "id": f"fee_{fid}",
                    "title": fee["title"],
                    "category": "Fees and Expenses",
                    "content": content_text,
                    "source_url": fee.get("source_url", "https://admissions.akashinstitutions.com/engineering"),
                    "source_type": fee.get("source_type", "Official Admissions Portal"),
                    "academic_year": fee.get("academic_year", "2025-2026"),
                    "last_verified_date": fee.get("last_verified_date", "2026-03-15"),
                    "keywords": ["fee", "fees", "tuition", "cost", "kcet fee", "comedk fee", "management fee", "hostel fee", "expenses"]
                })

        # 5. Scholarships
        sch_file = kb_path / "scholarships.json"
        if sch_file.exists():
            with open(sch_file, "r", encoding="utf-8") as f:
                scholarships = json.load(f)
            # Scholarships summary
            sch_names = [s["scheme_name"] for s in scholarships]
            chunks.append({
                "id": "sch_summary",
                "title": "Scholarships and Financial Assistance Overview at AIET",
                "category": "Scholarships",
                "content": f"Akash Group of Institutions and AIET offer and support multiple scholarship schemes: 1. Akash Entrance Test (AET) Institutional Scholarships based on qualifying marks; 2. AGI Institutional Awards of Excellence for academic achievers and department toppers; 3. Karnataka State Scholarship Portal (SSP) Post-Matric scholarships for SC/ST and OBC students (Vidyasiri, Fee Concession); 4. National Scholarship Portal (NSP) Central Sector and Minority schemes; 5. AICTE Pragati Scholarship for Girl Students (₹50,000/year); 6. AICTE Saksham Scholarship for Specially-Abled Students (₹50,000/year); 7. Defense and sports recognitions. Contact admissions@akashinstitutions.com or visit https://www.akashinstitutions.com/scholarships/.",
                "source_url": "https://www.akashinstitutions.com/scholarships/",
                "source_type": "Official Scholarship Records",
                "academic_year": "2025-2026",
                "last_verified_date": "2026-03-15",
                "keywords": ["scholarships", "scholarship", "financial aid", "fee concession", "pragati", "saksham", "ssp", "nsp", "aet"]
            })
            for s in scholarships:
                sid = s["id"]
                content_text = f"Scheme Name: {s['scheme_name']}. Offered by: {s.get('offered_by', 'Government/College')}. Applicable to: {s.get('applicable_to') or s.get('eligibility_criteria', '')}. Benefit: {s.get('benefit') or s.get('benefit_amount', '')}. Application Portal: {s.get('portal') or s.get('application_portal', 'College office')}. Verified Source: {s.get('source_url')}."
                chunks.append({
                    "id": f"sch_indiv_{sid}",
                    "title": s["scheme_name"],
                    "category": "Scholarships",
                    "content": content_text,
                    "source_url": s.get("source_url", "https://www.akashinstitutions.com/scholarships/"),
                    "source_type": "Official Scholarship Records",
                    "academic_year": "2025-2026",
                    "last_verified_date": "2026-03-15",
                    "keywords": [s["scheme_name"].lower(), "scholarship", "eligibility", "benefit"]
                })

        # 6. Infrastructure
        infra_file = kb_path / "infrastructure.json"
        if infra_file.exists():
            with open(infra_file, "r", encoding="utf-8") as f:
                infra = json.load(f)
            # Infrastructure summary
            chunks.append({
                "id": "infra_summary",
                "title": "AIET Campus Facilities and Infrastructure Overview",
                "category": "Infrastructure",
                "content": f"Campus Infrastructure at Akash Institute of Engineering & Technology (AIET), Devanahalli: Modern Wi-Fi enabled academic blocks, high-tech computer science and engineering laboratories, Central Library & Digital E-library with VTU e-resources, 1,500-seat central air-conditioned auditorium, Wi-Fi enabled boys hostel (400 beds) and girls hostel (700 beds) with hygienic dining mess, on-campus 24/7 Akash multi-specialty Hospital with emergency care and ambulance, sports grounds for cricket, football, basketball and indoor fitness gymnasium, spacious hygienic cafeteria, and college bus transportation across Bengaluru.",
                "source_url": "https://akashiet.com/infrastructure/",
                "source_type": "Official College Portal",
                "academic_year": "2025-2026",
                "last_verified_date": "2026-03-15",
                "keywords": ["infrastructure", "facilities", "campus", "hostel", "library", "auditorium", "hospital", "sports", "cafeteria", "transport"]
            })
            for item in infra:
                iid = item["id"]
                floor_str = f" Floor location: {item['floor_location']}." if "floor_location" in item else ""
                office_str = f" Office timings: {item['office_hours']}." if "office_hours" in item else ""
                kw = [item["title"].lower(), "facility", "infrastructure"]
                if "floor_location" in item:
                    kw.extend([item["floor_location"].lower(), "floor", "where is", "location"])
                if "office_hours" in item:
                    kw.extend(["office timing", "office hours", "timings"])
                chunks.append({
                    "id": f"infra_indiv_{iid}",
                    "title": item["title"],
                    "category": "Infrastructure",
                    "content": f"{item['title']}: {item['description']}.{floor_str}{office_str} Verified source: {item.get('source_url')}.",
                    "source_url": item.get("source_url", "https://akashiet.com/infrastructure/"),
                    "source_type": "Official College Portal",
                    "academic_year": "2025-2026",
                    "last_verified_date": "2026-03-15",
                    "keywords": kw
                })

        # 7. Admissions
        adm_file = kb_path / "admissions.json"
        if adm_file.exists():
            with open(adm_file, "r", encoding="utf-8") as f:
                admissions = json.load(f)
            for adm in admissions:
                aid = adm["id"]
                steps_str = " ".join(adm.get("admission_steps", []))
                docs_str = ", ".join(adm.get("mandatory_documents", []))
                content_text = f"Title: {adm['title']}. Eligibility: {adm.get('btech_eligibility')}. Admission Codes: KCET Code E300, COMEDK Code E005, PGCET MBA Code B097, PGCET MCA Code C550. Admission Procedure: {steps_str}. Required Documents: {docs_str}. Admissions Office Contact: Phone +91 9513107575 / +91 9513597575, Landline 080-244-11-222, Email admissions@akashinstitutions.com, Address: Prasannahalli Road, Devanahalli, Bengaluru - 562110."
                chunks.append({
                    "id": f"adm_indiv_{aid}",
                    "title": adm["title"],
                    "category": "Admissions",
                    "content": content_text,
                    "source_url": adm.get("source_url", "https://admissions.akashinstitutions.com/engineering"),
                    "source_type": "Official Admissions Portal",
                    "academic_year": "2025-2026",
                    "last_verified_date": "2026-03-15",
                    "keywords": ["admission", "admissions", "apply", "eligibility", "documents required", "procedure", "contact", "phone"]
                })

        # 8. Academic Info & Life
        acad_file = kb_path / "academic_information.json"
        if acad_file.exists():
            with open(acad_file, "r", encoding="utf-8") as f:
                acads = json.load(f)
            for ac in acads:
                acid = ac["id"]
                rules_str = " Rules: " + " ".join(ac.get("rules_list", [])) if "rules_list" in ac else ""
                reg_time_str = f" Regular Timings: {ac.get('regular_timing')}." if "regular_timing" in ac else ""
                off_time_str = f" Office Timings: {ac.get('office_timing')}." if "office_timing" in ac else ""
                content_text = f"Title: {ac['title']}. Category: Academic Information. Description: {ac.get('description', '')}. Attendance: {ac.get('attendance_policy', '')}. Evaluation: {ac.get('evaluation_system', '')}.{reg_time_str}{off_time_str}{rules_str} International Partnership: {ac.get('global_collaborations', '')}."
                kw = [ac["title"].lower(), "academic", "vtu", "attendance", "placement", "internship", "ragging", "nestling"]
                if "rules_list" in ac:
                    kw.extend(["rules", "college rules", "dress code", "uniform", "shoes", "hair", "beard", "formals", "color dress", "85% attendance"])
                if "office_timing" in ac:
                    kw.extend(["office timing", "office hours", "timings", "saturday timings", "working hours"])
                chunks.append({
                    "id": f"acad_indiv_{acid}",
                    "title": ac["title"],
                    "category": "Academic Information",
                    "content": content_text,
                    "source_url": ac.get("source_url", "https://akashiet.com/"),
                    "source_type": "Official College Portal",
                    "academic_year": "2025-2026",
                    "last_verified_date": "2026-03-15",
                    "keywords": kw
                })

        # Batch insert into ChromaDB
        ids = [c["id"] for c in chunks]
        documents = [c["content"] for c in chunks]
        metadatas = [{
            "title": c["title"],
            "category": c["category"],
            "source_url": c["source_url"],
            "source_type": c.get("source_type", "Official Record"),
            "academic_year": c.get("academic_year", "2025-2026"),
            "last_verified_date": c.get("last_verified_date", "2026-03-15"),
            "keywords": " ".join(c.get("keywords", []))
        } for c in chunks]

        # Reset existing collection or upsert
        try:
            self.collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
            print(f"Successfully indexed {len(chunks)} chunks into ChromaDB collection '{self.collection_name}'!")
        except Exception as e:
            print(f"Error during ChromaDB upsert: {e}")

        # Update local metadata cache
        for idx, i in enumerate(ids):
            self.documents_metadata[i] = metadatas[idx]

    def hybrid_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Executes a hybrid search combining dense semantic vector search
        with BM25/keyword lexical matching for maximum precision.
        """
        query_clean = query.strip().lower()
        query_tokens = set(re.findall(r"\w+", query_clean))
        
        # 1. Semantic search with ChromaDB
        chroma_k = min(max(top_k * 3, 10), self.collection.count() or 1)
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=chroma_k
            )
        except Exception as e:
            print(f"ChromaDB query error: {e}")
            results = {"ids": [[]], "documents": [[]], "metadatas": [[]], "distances": [[]]}

        # Combine results
        candidate_scores = {}
        candidate_data = {}

        if results and results["ids"] and results["ids"][0]:
            found_ids = results["ids"][0]
            found_docs = results["documents"][0]
            found_metas = results["metadatas"][0]
            found_dists = results["distances"][0] if "distances" in results and results["distances"] else [0.5]*len(found_ids)

            for idx, doc_id in enumerate(found_ids):
                # distance to similarity score
                dist = found_dists[idx]
                sim_score = 1.0 / (1.0 + max(0.0, float(dist)))
                
                doc_text = found_docs[idx]
                meta = found_metas[idx]
                
                # 2. Lexical / Keyword match scoring
                lexical_score = 0.0
                text_lower = doc_text.lower()
                title_lower = meta.get("title", "").lower()
                kw_str = meta.get("keywords", "").lower()

                # Exact phrase matches get major boost
                if query_clean in text_lower or query_clean in title_lower:
                    lexical_score += 1.5

                # Exact code matches (E300, E005, B097, C550, 9:00 AM)
                for code in ["e300", "e005", "b097", "c550", "9:00 am", "9 am to 4 pm", "devanahalli", "hod", "head of department"]:
                    if code in query_clean and (code in text_lower or code in kw_str):
                        lexical_score += 2.0

                # Token overlap
                matched_tokens = sum(1 for token in query_tokens if token in text_lower or token in title_lower or token in kw_str)
                lexical_score += (matched_tokens / max(len(query_tokens), 1)) * 1.0

                total_score = (0.55 * sim_score) + (0.45 * min(lexical_score, 3.0) / 3.0)
                
                candidate_scores[doc_id] = total_score
                candidate_data[doc_id] = {
                    "id": doc_id,
                    "content": doc_text,
                    "metadata": meta,
                    "score": total_score,
                    "semantic_sim": sim_score
                }

        # Sort by total score descending
        ranked = sorted(candidate_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        output = [candidate_data[doc_id] for doc_id, _ in ranked]
        return output

    def add_custom_document(self, doc_id: str, title: str, category: str, content: str, source_url: str, academic_year: str = "2025-2026"):
        """Adds or updates an administrative document in ChromaDB."""
        meta = {
            "title": title,
            "category": category,
            "source_url": source_url,
            "source_type": "Admin Upload",
            "academic_year": academic_year,
            "last_verified_date": "2026-03-15",
            "keywords": f"{title.lower()} {category.lower()}"
        }
        self.collection.upsert(
            ids=[doc_id],
            documents=[content],
            metadatas=[meta]
        )
        self.documents_metadata[doc_id] = meta
        return {"status": "success", "id": doc_id}

    def delete_document(self, doc_id: str):
        """Removes a document from the vector store."""
        try:
            self.collection.delete(ids=[doc_id])
            if doc_id in self.documents_metadata:
                del self.documents_metadata[doc_id]
            return True
        except Exception as e:
            print(f"Error deleting doc {doc_id}: {e}")
            return False

    def list_indexed_documents(self) -> List[Dict[str, Any]]:
        """Returns overview of all indexed knowledge items."""
        docs = []
        try:
            results = self.collection.get()
            if results and results["ids"]:
                for idx, doc_id in enumerate(results["ids"]):
                    meta = results["metadatas"][idx]
                    docs.append({
                        "id": doc_id,
                        "title": meta.get("title", doc_id),
                        "category": meta.get("category", "General"),
                        "source_url": meta.get("source_url", ""),
                        "last_verified_date": meta.get("last_verified_date", ""),
                        "academic_year": meta.get("academic_year", "2025-2026")
                    })
        except Exception as e:
            print(f"Error listing documents: {e}")
        return docs
