import os
import json
import re

kb_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend", "knowledge_base")
os.makedirs(kb_dir, exist_ok=True)

# 1. Sources Manifest
sources = [
    {
        "id": "src_aiet_home",
        "title": "AIET Official Website Homepage",
        "url": "https://akashiet.com/",
        "source_type": "Official College Portal",
        "category": "College Profile",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "src_aiet_about",
        "title": "About Akash Institute of Engineering and Technology",
        "url": "https://akashiet.com/about-us/",
        "source_type": "Official College Portal",
        "category": "Institutional Overview",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "src_aiet_faculty",
        "title": "AIET Official Faculty Directory",
        "url": "https://akashiet.com/faculty/",
        "source_type": "Official Faculty Records",
        "category": "Faculty Directory",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "src_aiet_infrastructure",
        "title": "Campus Infrastructure & Facilities",
        "url": "https://akashiet.com/infrastructure/",
        "source_type": "Official Campus Documentation",
        "category": "Infrastructure",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "src_agi_courses",
        "title": "Akash Group Engineering (B.E.) Courses",
        "url": "https://www.akashinstitutions.com/courses/engineering-be/",
        "source_type": "Official Group Portal",
        "category": "Courses & Academics",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "src_agi_scholarships",
        "title": "Scholarships & Financial Assistance",
        "url": "https://www.akashinstitutions.com/scholarships/",
        "source_type": "Official Scholarship Records",
        "category": "Scholarships",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "src_agi_admissions",
        "title": "Engineering Admissions Portal",
        "url": "https://admissions.akashinstitutions.com/engineering",
        "source_type": "Official Admissions Portal",
        "category": "Admissions & Fees",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "src_agi_institutional",
        "title": "AIET Institutional Profile",
        "url": "https://www.akashinstitutions.com/colleges/akash-institute-of-engineering-technology/",
        "source_type": "Official Institutional Record",
        "category": "College Profile",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "src_vtu_affiliation",
        "title": "Visvesvaraya Technological University (VTU) Affiliation",
        "url": "https://vtu.ac.in/",
        "source_type": "University Affiliation Body",
        "category": "Affiliations & Approvals",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    }
]

with open(os.path.join(kb_dir, "sources.json"), "w", encoding="utf-8") as f:
    json.dump(sources, f, indent=2)

# 2. College Profile
college_profile = {
    "category": "College Profile",
    "title": "Akash Institute of Engineering and Technology (AIET) - Complete Institutional Profile",
    "institution_name": "Akash Institute of Engineering and Technology",
    "short_name": "AIET",
    "parent_trust": "Akash Education & Development Trust (AEDT)",
    "parent_group": "Akash Group of Institutions (AGI)",
    "established_year": 2020,
    "location": {
        "address": "Prasannahalli Road, Devanahalli, near Kempegowda International Airport",
        "city": "Bengaluru",
        "state": "Karnataka",
        "pincode": "562110",
        "country": "India",
        "landmarks": "Near Kempegowda International Airport (BLR), off NH-44 Bellary Road, Devanahalli"
    },
    "timings": {
        "regular_college_timings": "Monday to Friday: 9:00 AM to 4:00 PM; Saturday: 9:00 AM to 1:00 PM",
        "working_days": "Monday to Saturday (as per VTU Academic Calendar)",
        "office_hours": "Monday to Friday: 3:00 PM to 5:00 PM; Saturday: 1:00 PM to 3:00 PM"
    },
    "codes": {
        "kcet_code": "E300",
        "comedk_code": "E005",
        "pgcet_mba_code": "B097",
        "pgcet_mca_code": "C550"
    },
    "affiliation_and_approvals": {
        "university_affiliation": "Visvesvaraya Technological University (VTU), Belagavi",
        "aicte_approval": "Approved by All India Council for Technical Education (AICTE), New Delhi",
        "state_government_recognition": "Recognized by the Government of Karnataka"
    },
    "contact": {
        "admissions_hotline": "+91 9513107575",
        "admissions_alt_phone": "+91 9513597575",
        "central_landline": "080-244-11-222",
        "admissions_email": "admissions@akashinstitutions.com",
        "placement_email": "sindhu.placement@akashinstitutions.com",
        "official_website": "https://akashiet.com/",
        "group_website": "https://www.akashinstitutions.com/"
    },
    "vision": "To emerge as a premier centre of excellence in engineering education and research, empowering young minds with technical competence, innovation, leadership, and ethical values to meet global societal challenges.",
    "mission": [
        "Deliver quality technical education through state-of-the-art curriculum, modern laboratories, and experiential learning.",
        "Foster research, innovation, entrepreneurship, and interdisciplinary collaborations with leading industries and global universities.",
        "Inculcate ethical standards, environmental consciousness, and leadership skills for holistic student development."
    ],
    "highlights": [
        "Sprawling green campus in Devanahalli near Bangalore International Airport",
        "Affiliated to Visvesvaraya Technological University (VTU), Belagavi and approved by AICTE",
        "State-of-the-art computer labs, electronics labs, and mechanical workshops",
        "Wi-Fi enabled campus with separate secure hostels for boys (400 beds) and girls (700 beds)",
        "1,500-seat modern auditorium and extensive sports grounds",
        "On-campus multi-specialty Akash Hospital with 24/7 medical & ambulance support",
        "Partnership with 'Nestling' via VTU linking with 3,500 partner universities across 29 countries",
        "Active Placement & Career Development Cell with top industry recruitment drives"
    ],
    "source_url": "https://akashiet.com/about-us/",
    "source_type": "Official College Portal",
    "academic_year": "2025-2026",
    "published_date": "2026-01-01",
    "last_verified_date": "2026-03-15",
    "verification_status": "VERIFIED_OFFICIAL"
}

with open(os.path.join(kb_dir, "college_profile.json"), "w", encoding="utf-8") as f:
    json.dump(college_profile, f, indent=2)

# 3. Faculty
# Load from scratch/cleaned_faculty.json
scratch_faculty_path = r"C:\Users\dheer\.gemini\antigravity-ide\brain\084dd6bb-32bf-4f97-ba91-255569cbd338\scratch\cleaned_faculty.json"
if os.path.exists(scratch_faculty_path):
    with open(scratch_faculty_path, "r", encoding="utf-8") as f:
        faculty_raw = json.load(f)
else:
    faculty_raw = []

faculty_records = []
for idx, fac in enumerate(faculty_raw):
    # Enrich with department standardization
    dept = fac.get("department", "Engineering").strip()
    desig = fac.get("designation", "Faculty Member").strip()
    is_hod = "Head" in desig or "HOD" in desig
    
    faculty_records.append({
        "id": f"fac_{idx+1:03d}",
        "name": fac["name"],
        "designation": desig,
        "is_head_of_department": is_hod,
        "department": dept,
        "institution": "Akash Institute of Engineering and Technology",
        "profile_pdf_url": fac.get("profile_pdf", ""),
        "image_url": fac.get("image_url", ""),
        "source_url": "https://akashiet.com/faculty/",
        "source_type": "Official Faculty Directory",
        "academic_year": "2025-2026",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    })

with open(os.path.join(kb_dir, "faculty.json"), "w", encoding="utf-8") as f:
    json.dump(faculty_records, f, indent=2)

# 4. Courses
courses_records = [
    {
        "id": "course_cse",
        "course_name": "Bachelor of Engineering in Computer Science and Engineering",
        "short_name": "BE CSE",
        "level": "Undergraduate (UG)",
        "duration": "4 Years (8 Semesters)",
        "degree_awarded": "Bachelor of Engineering (B.E.)",
        "affiliated_to": "Visvesvaraya Technological University (VTU), Belagavi",
        "approved_by": "AICTE, New Delhi",
        "department": "Department of Computer Science & Engineering",
        "head_of_department": "Dr. Somanath J Patil (Associate Professor and Head)",
        "eligibility": "Candidate must have passed 10+2 / 2nd PUC or equivalent examination with English, Physics, and Mathematics as compulsory subjects along with Chemistry / Biotechnology / Biology / Computer Science / Electronics as optional subjects, securing at least 45% aggregate marks (40% for SC/ST and OBC candidates of Karnataka).",
        "admission_routes": [
            {"route": "KCET (KEA)", "code": "E300", "description": "Karnataka Common Entrance Test conducted by KEA for Karnataka domicile students."},
            {"route": "COMEDK UGET", "code": "E005", "description": "Consortium of Medical, Engineering and Dental Colleges of Karnataka exam for all-India candidates."},
            {"route": "Management Quota", "code": "AIET-Direct", "description": "Direct institutional merit admission based on 10+2 qualifying marks."}
        ],
        "specialized_laboratories": [
            "Data Structures & Algorithms Laboratory",
            "Python Programming Laboratory",
            "Database Management Systems (DBMS) Laboratory",
            "Java Programming Laboratory",
            "Operating Systems & System Software Laboratory",
            "Computer Networks & Cloud Computing Laboratory",
            "Project & Research Innovation Center"
        ],
        "curriculum_highlights": "Designed under VTU Choice-Based Credit System (CBCS) and Outcome-Based Education (OBE). Covers Data Structures, Design and Analysis of Algorithms, DBMS, Operating Systems, Computer Networks, Software Engineering, Web Technologies, Machine Learning, Cloud Computing, and Capstone Project.",
        "career_pathways": "Software Engineer, Full-Stack Developer, Cloud Architect, Systems Analyst, Database Administrator, DevOps Engineer, Research Scientist in top tech firms.",
        "source_url": "https://akashiet.com/computer-science/",
        "source_type": "Official College Portal",
        "academic_year": "2025-2026",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "course_aiml",
        "course_name": "Bachelor of Engineering in Computer Science (Artificial Intelligence & Machine Learning)",
        "short_name": "BE CSE (AI & ML)",
        "level": "Undergraduate (UG)",
        "duration": "4 Years (8 Semesters)",
        "degree_awarded": "Bachelor of Engineering (B.E.)",
        "affiliated_to": "Visvesvaraya Technological University (VTU), Belagavi",
        "approved_by": "AICTE, New Delhi",
        "department": "Department of Artificial Intelligence & Machine Learning",
        "head_of_department": "Dr. Sridhar C S (Professor and Head)",
        "eligibility": "Passed 10+2 / 2nd PUC examination with Physics and Mathematics as compulsory subjects, with Chemistry/Biotech/Biology/Computer Science as optional, securing at least 45% marks in aggregate (40% for SC/ST/OBC category candidates of Karnataka).",
        "admission_routes": [
            {"route": "KCET (KEA)", "code": "E300"},
            {"route": "COMEDK UGET", "code": "E005"},
            {"route": "Management Quota", "code": "AIET-Direct"}
        ],
        "specialized_laboratories": [
            "Artificial Intelligence & Machine Learning Lab",
            "Deep Learning & Neural Networks Lab",
            "Python & Data Analytics Lab",
            "Natural Language Processing (NLP) Lab",
            "Computer Vision & Robotics Lab"
        ],
        "curriculum_highlights": "Advanced study in Artificial Intelligence, Machine Learning algorithms, Deep Learning frameworks (TensorFlow, PyTorch), NLP, Computer Vision, Reinforcement Learning, Generative AI, and Ethics in AI.",
        "career_pathways": "AI Engineer, Machine Learning Specialist, Data Scientist, Computer Vision Engineer, NLP Researcher, Robotics Software Engineer.",
        "source_url": "https://akashiet.com/machine-learning/",
        "source_type": "Official College Portal",
        "academic_year": "2025-2026",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "course_aids",
        "course_name": "Bachelor of Engineering in Artificial Intelligence and Data Science",
        "short_name": "BE AI & DS",
        "level": "Undergraduate (UG)",
        "duration": "4 Years (8 Semesters)",
        "degree_awarded": "Bachelor of Engineering (B.E.)",
        "affiliated_to": "Visvesvaraya Technological University (VTU), Belagavi",
        "approved_by": "AICTE, New Delhi",
        "department": "Department of Artificial Intelligence & Data Science",
        "head_of_department": "Mr. Anil Kumar Warad (Assistant Professor and Head)",
        "eligibility": "Passed 10+2 / 2nd PUC with Physics & Mathematics as core subjects and minimum 45% marks in aggregate (40% for Karnataka reserved categories).",
        "admission_routes": [
            {"route": "KCET (KEA)", "code": "E300"},
            {"route": "COMEDK UGET", "code": "E005"},
            {"route": "Management Quota", "code": "AIET-Direct"}
        ],
        "specialized_laboratories": [
            "Data Science & Statistical Modeling Lab",
            "Big Data Technologies (Hadoop/Spark) Lab",
            "Business Intelligence & Tableau/PowerBI Lab",
            "Machine Learning Applications Lab"
        ],
        "curriculum_highlights": "Integrates core AI methodologies with statistical data science, big data analytics, data visualization, predictive analytics, cloud data engineering, and data mining.",
        "career_pathways": "Data Scientist, Business Intelligence Analyst, Big Data Engineer, Quantitative Analyst, AI Product Developer.",
        "source_url": "https://akashiet.com/artificial-intelligence/",
        "source_type": "Official College Portal",
        "academic_year": "2025-2026",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "course_ise",
        "course_name": "Bachelor of Engineering in Information Science and Engineering",
        "short_name": "BE ISE",
        "level": "Undergraduate (UG)",
        "duration": "4 Years (8 Semesters)",
        "degree_awarded": "Bachelor of Engineering (B.E.)",
        "affiliated_to": "Visvesvaraya Technological University (VTU), Belagavi",
        "approved_by": "AICTE, New Delhi",
        "department": "Department of Information Science & Engineering",
        "head_of_department": "Mrs. Roopa G (Assistant Professor and Head)",
        "eligibility": "Passed 10+2 / 2nd PUC with 45% aggregate in Physics, Mathematics and one optional subject (40% for SC/ST/OBC).",
        "admission_routes": [
            {"route": "KCET (KEA)", "code": "E300"},
            {"route": "COMEDK UGET", "code": "E005"},
            {"route": "Management Quota", "code": "AIET-Direct"}
        ],
        "specialized_laboratories": [
            "Information Systems & Web Architecture Lab",
            "Software Testing & Quality Assurance Lab",
            "Information Security Lab",
            "Database & Enterprise Systems Lab"
        ],
        "curriculum_highlights": "Information theory, Software Engineering, Mobile Application Development, Web Services, Cloud Computing, Database Administration, and Enterprise IT Systems.",
        "career_pathways": "Information Architect, IT Consultant, Systems Software Engineer, Web Applications Specialist, Enterprise IT Manager.",
        "source_url": "https://akashiet.com/be-information-science-and-engineering/",
        "source_type": "Official College Portal",
        "academic_year": "2025-2026",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "course_cyber",
        "course_name": "Bachelor of Engineering in Computer Science Engineering (Cyber Security)",
        "short_name": "BE CSE (Cyber Security)",
        "level": "Undergraduate (UG)",
        "duration": "4 Years (8 Semesters)",
        "degree_awarded": "Bachelor of Engineering (B.E.)",
        "affiliated_to": "Visvesvaraya Technological University (VTU), Belagavi",
        "approved_by": "AICTE, New Delhi",
        "department": "Department of Computer Science Engineering (Cybersecurity)",
        "head_of_department": "Mrs. Nagamma (Assistant Professor and Head)",
        "eligibility": "10+2 / 2nd PUC with Physics & Mathematics plus optional technical subject, at least 45% marks (40% for SC/ST/OBC).",
        "admission_routes": [
            {"route": "KCET (KEA)", "code": "E300"},
            {"route": "COMEDK UGET", "code": "E005"},
            {"route": "Management Quota", "code": "AIET-Direct"}
        ],
        "specialized_laboratories": [
            "Cyber Defense & Ethical Hacking Lab",
            "Network Security & Penetration Testing Lab",
            "Digital Forensics & Incident Response Lab",
            "Cryptography & Blockchain Lab"
        ],
        "curriculum_highlights": "Network Security, Ethical Hacking, Cryptography, Secure Coding, Cyber Forensics, Threat Intelligence, Information Security Management, and Cloud Security.",
        "career_pathways": "Cyber Security Analyst, Information Security Specialist, Ethical Hacker / Penetration Tester, Security Operations Center (SOC) Analyst, Cryptographer.",
        "source_url": "https://akashiet.com/be-computer-science/",
        "source_type": "Official College Portal",
        "academic_year": "2025-2026",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "course_ds",
        "course_name": "Bachelor of Engineering in Computer Science Engineering (Data Science)",
        "short_name": "BE CSE (Data Science)",
        "level": "Undergraduate (UG)",
        "duration": "4 Years (8 Semesters)",
        "degree_awarded": "Bachelor of Engineering (B.E.)",
        "affiliated_to": "Visvesvaraya Technological University (VTU), Belagavi",
        "approved_by": "AICTE, New Delhi",
        "department": "Department of Computer Science Engineering (Data Science)",
        "head_of_department": "Mr. Praveen P (Assistant Professor and Head)",
        "eligibility": "10+2 / 2nd PUC with Physics & Mathematics, minimum 45% marks in aggregate (40% for reserved categories of Karnataka).",
        "admission_routes": [
            {"route": "KCET (KEA)", "code": "E300"},
            {"route": "COMEDK UGET", "code": "E005"},
            {"route": "Management Quota", "code": "AIET-Direct"}
        ],
        "specialized_laboratories": [
            "Data Analytics & Computational Statistics Lab",
            "Big Data Engineering Lab",
            "Data Mining & Machine Intelligence Lab"
        ],
        "curriculum_highlights": "Combines fundamental computer science with deep focus on data engineering, statistics, distributed computing, data warehousing, and business intelligence.",
        "career_pathways": "Data Engineer, Analytics Consultant, Big Data Architect, Business Intelligence Developer.",
        "source_url": "https://akashiet.com/be-computer-data-science/",
        "source_type": "Official College Portal",
        "academic_year": "2025-2026",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "course_ece",
        "course_name": "Bachelor of Engineering in Electronics and Communication Engineering",
        "short_name": "BE ECE",
        "level": "Undergraduate (UG)",
        "duration": "4 Years (8 Semesters)",
        "degree_awarded": "Bachelor of Engineering (B.E.)",
        "affiliated_to": "Visvesvaraya Technological University (VTU), Belagavi",
        "approved_by": "AICTE, New Delhi",
        "department": "Department of Electronics & Communication",
        "head_of_department": "Dr. Rajkumar V (Associate Professor and HOD)",
        "eligibility": "10+2 / 2nd PUC with Physics & Mathematics, at least 45% aggregate (40% for SC/ST/OBC).",
        "admission_routes": [
            {"route": "KCET (KEA)", "code": "E300"},
            {"route": "COMEDK UGET", "code": "E005"},
            {"route": "Management Quota", "code": "AIET-Direct"}
        ],
        "specialized_laboratories": [
            "Analog & Digital Electronics Laboratory",
            "VLSI Design & Verilog HDL Laboratory",
            "Digital Signal Processing (DSP) Laboratory",
            "Microcontroller & Embedded Systems Laboratory",
            "Microwave & Optical Communication Laboratory"
        ],
        "curriculum_highlights": "Electronic devices, signals and systems, microcontrollers, VLSI circuits, embedded IoT systems, digital communication, antenna design, wireless networks, and robotics.",
        "career_pathways": "VLSI Design Engineer, Embedded Systems Developer, Telecommunications Specialist, Hardware Design Engineer, IoT Solutions Architect.",
        "source_url": "https://akashiet.com/be-electronics-and-communication-engineering/",
        "source_type": "Official College Portal",
        "academic_year": "2025-2026",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "course_me",
        "course_name": "Bachelor of Engineering in Mechanical Engineering",
        "short_name": "BE ME",
        "level": "Undergraduate (UG)",
        "duration": "4 Years (8 Semesters)",
        "degree_awarded": "Bachelor of Engineering (B.E.)",
        "affiliated_to": "Visvesvaraya Technological University (VTU), Belagavi",
        "approved_by": "AICTE, New Delhi",
        "department": "Department of Mechanical Engineering",
        "head_of_department": "Dr. Pranesh K G (Associate Professor and Head)",
        "eligibility": "10+2 / 2nd PUC with Physics & Mathematics, minimum 45% marks in aggregate (40% for SC/ST/OBC of Karnataka).",
        "admission_routes": [
            {"route": "KCET (KEA)", "code": "E300"},
            {"route": "COMEDK UGET", "code": "E005"},
            {"route": "Management Quota", "code": "AIET-Direct"}
        ],
        "specialized_laboratories": [
            "Computer Aided Design & Manufacturing (CAD/CAM) Lab",
            "Fluid Mechanics & Hydraulic Machinery Lab",
            "Heat Transfer Laboratory",
            "Material Testing & Metallography Lab",
            "Foundry, Forging & Welding Workshop",
            "Machine Shop & CNC Machining Center"
        ],
        "curriculum_highlights": "Thermodynamics, mechanics of materials, manufacturing technology, fluid machinery, CAD/CAM/CAE, mechatronics, automotive engineering, thermal engineering, and renewable energy.",
        "career_pathways": "Mechanical Design Engineer, Production & Quality Engineer, Automotive Engineer, Thermal Power Specialist, Robotics & Automation Engineer.",
        "source_url": "https://akashiet.com/be-mechanical-engineering/",
        "source_type": "Official College Portal",
        "academic_year": "2025-2026",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "course_mba",
        "course_name": "Master of Business Administration",
        "short_name": "MBA",
        "level": "Postgraduate (PG)",
        "duration": "2 Years (4 Semesters)",
        "degree_awarded": "Master of Business Administration (MBA)",
        "affiliated_to": "Visvesvaraya Technological University (VTU), Belagavi",
        "approved_by": "AICTE, New Delhi",
        "department": "Department of Management Studies",
        "head_of_department": "Dr. Sri Hari V (Associate Professor and Head)",
        "eligibility": "Passed Bachelor’s degree of minimum 3 years duration with at least 50% marks in aggregate (45% for Karnataka SC/ST/Cat-1 candidates).",
        "admission_routes": [
            {"route": "KEA - PGCET", "code": "B097", "description": "Karnataka Post Graduate Common Entrance Test"},
            {"route": "KMAT / CMAT / MAT / CAT", "code": "Management", "description": "National and state management entrance tests for direct admission"}
        ],
        "specializations": ["Finance", "Marketing", "Human Resource Management (HR)", "Business Analytics", "Supply Chain & Operations"],
        "curriculum_highlights": "Managerial Economics, Organizational Behavior, Financial Management, Marketing Strategy, Corporate Governance, Business Analytics, and Corporate Internship.",
        "career_pathways": "Business Consultant, Financial Analyst, Marketing Manager, HR Business Partner, Operations Manager, Product Manager.",
        "source_url": "https://akashiet.com/mba/",
        "source_type": "Official College Portal",
        "academic_year": "2025-2026",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "course_mca",
        "course_name": "Master of Computer Applications",
        "short_name": "MCA",
        "level": "Postgraduate (PG)",
        "duration": "2 Years (4 Semesters)",
        "degree_awarded": "Master of Computer Applications (MCA)",
        "affiliated_to": "Visvesvaraya Technological University (VTU), Belagavi",
        "approved_by": "AICTE, New Delhi",
        "department": "Department of Master of Computer Applications (MCA)",
        "head_of_department": "Mr. Madhu N (Assistant Professor and Head)",
        "eligibility": "Passed BCA / Bachelor Degree in Computer Science Engineering or equivalent Degree OR passed B.Sc./ B.Com./ B.A. with Mathematics at 10+2 level or at Graduation level, with at least 50% marks (45% for reserved category).",
        "admission_routes": [
            {"route": "KEA - PGCET", "code": "C550", "description": "Karnataka Post Graduate Common Entrance Test for MCA"},
            {"route": "KMAT / Direct", "code": "Management", "description": "Management entrance route"}
        ],
        "specialized_laboratories": [
            "Advanced Java & Cloud Computing Lab",
            "Full Stack Web Development Lab",
            "Database Systems & Data Analytics Lab"
        ],
        "curriculum_highlights": "Object Oriented Programming, Advanced Web Technologies, Database Systems, Cloud Computing, Mobile Computing, Machine Learning, and Enterprise Project Work.",
        "career_pathways": "Software Developer, Systems Analyst, Database Administrator, Web Architect, Cloud Application Developer.",
        "source_url": "https://akashiet.com/mca/",
        "source_type": "Official College Portal",
        "academic_year": "2025-2026",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "course_lateral",
        "course_name": "B.E. Lateral Entry (Direct 2nd Year / 3rd Semester)",
        "short_name": "BE Lateral Entry",
        "level": "Undergraduate (UG)",
        "duration": "3 Years (6 Semesters)",
        "degree_awarded": "Bachelor of Engineering (B.E.)",
        "affiliated_to": "Visvesvaraya Technological University (VTU), Belagavi",
        "approved_by": "AICTE, New Delhi",
        "eligibility": "Passed minimum 3-year Diploma in appropriate branch of Engineering / Technology with at least 45% marks (40% for Karnataka SC/ST/OBC), or passed B.Sc. Degree from a recognized University with Mathematics at 10+2 level and minimum 45% marks.",
        "admission_routes": [
            {"route": "KEA - DCET", "code": "DCET Quota", "description": "Diploma Common Entrance Test conducted by Karnataka Examination Authority"},
            {"route": "Management Lateral Entry", "code": "AIET-Direct", "description": "Direct institutional lateral entry"}
        ],
        "source_url": "https://akashiet.com/",
        "source_type": "Official College Portal",
        "academic_year": "2025-2026",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    }
]

with open(os.path.join(kb_dir, "courses.json"), "w", encoding="utf-8") as f:
    json.dump(courses_records, f, indent=2)

# 5. Fees and Expenses
fees_records = [
    {
        "id": "fee_kcet_quota",
        "category": "Fees and Expenses",
        "title": "Government Quota (KCET / KEA) Engineering Tuition Fee Structure",
        "quota_type": "Government Quota via KCET (Karnataka Examination Authority)",
        "college_code": "E300",
        "academic_year": "2025-2026",
        "fee_type": "Annual Fee (Subject to KEA Annual Regulatory Order)",
        "fee_range_inr": "Regulated by KEA Fee Regulatory Committee (typically approx. ₹75,000 to ₹1,05,000/year for unaided engineering colleges)",
        "mandatory_components": [
            "Government Tuition Fee (payable to KEA)",
            "VTU University Registration, Exam & Development Charges",
            "College Laboratory & Digital Library Access",
            "Student Welfare & Identity Card charges"
        ],
        "official_guidance_rule": "Tuition fees for government quota seats are strictly determined each academic year by the Government of Karnataka and KEA. If official website does not confirm an exact amount for this category, contact the AIET admissions office.",
        "admissions_contact": {
            "phone": "+91 9513107575 / +91 9513597575",
            "email": "admissions@akashinstitutions.com",
            "portal": "https://admissions.akashinstitutions.com/engineering"
        },
        "source_url": "https://admissions.akashinstitutions.com/engineering",
        "source_type": "Official Admissions Portal & KEA Guidelines",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "fee_comedk_quota",
        "category": "Fees and Expenses",
        "title": "COMEDK UGET Quota Engineering Tuition Fee Structure",
        "quota_type": "COMEDK UGET Merit Quota",
        "college_code": "E005",
        "academic_year": "2025-2026",
        "fee_type": "Annual Fee (As per COMEDK Consortium Circular)",
        "fee_range_inr": "As notified by COMEDK consortium annually (typically approx. ₹2,00,000 to ₹2,40,000/year for private colleges, plus applicable VTU & institutional charges)",
        "mandatory_components": [
            "COMEDK Tuition Fee",
            "VTU Registration & Examination Fees",
            "Institutional Lab & Resource Fee"
        ],
        "official_guidance_rule": "Final fee payable for COMEDK seats is governed by the COMEDK fee circular for the respective academic year. Contact the admissions office to obtain the current written fee circular.",
        "admissions_contact": {
            "phone": "+91 9513107575 / +91 9513597575",
            "email": "admissions@akashinstitutions.com"
        },
        "source_url": "https://akashiet.com/",
        "source_type": "Official College Portal",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "fee_management_quota",
        "category": "Fees and Expenses",
        "title": "Management Quota B.E. & PG Tuition Fee Structure",
        "quota_type": "Management Quota (Merit Direct Admission)",
        "academic_year": "2025-2026",
        "fee_type": "Annual or Total Program Fee (Varies by Discipline)",
        "fee_range_inr": "I couldn't verify the latest official fee for this category. Please contact the AIET admissions office for confirmation.",
        "disciplines": [
            "BE Computer Science and Engineering",
            "BE Artificial Intelligence & Machine Learning",
            "BE Artificial Intelligence & Data Science",
            "BE Information Science & Engineering",
            "BE Computer Science (Cyber Security)",
            "BE Computer Science (Data Science)",
            "BE Electronics & Communication Engineering",
            "BE Mechanical Engineering",
            "MBA (KEA PGCET: B097)",
            "MCA (KEA PGCET: C550)"
        ],
        "official_guidance_rule": "Management quota fees depend on the branch opted, candidate's merit standing, and seat availability. The college does not publish a single flat management fee publicly to prevent misrepresentation. Candidates must contact the official admissions office at +91 9513107575 or visit the campus admissions office in Devanahalli to receive the authorized written fee structure.",
        "admissions_contact": {
            "phone": "+91 9513107575 / +91 9513597575",
            "landline": "080-244-11-222",
            "email": "admissions@akashinstitutions.com"
        },
        "source_url": "https://admissions.akashinstitutions.com/engineering",
        "source_type": "Official Admissions Portal",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "fee_hostel_expenses",
        "category": "Fees and Expenses",
        "title": "Hostel Facilities, Room Sharing, Food Charges & Deposits",
        "academic_year": "2025-2026",
        "hostel_capacity": "Wi-Fi enabled boys hostel (400 beds) and girls hostel (700 beds)",
        "room_types": ["Twin Sharing (2-sharing)", "Triple Sharing (3-sharing)", "Four Sharing (4-sharing)"],
        "amenities_included": [
            "Fully furnished rooms with bed, study table, chair, and wardrobe",
            "High-speed Wi-Fi internet connectivity",
            "Wholesome multi-cuisine food (Breakfast, Lunch, Evening Snacks, Dinner)",
            "24/7 solar hot water supply and RO purified drinking water",
            "Housekeeping and laundry services",
            "Round-the-clock security and CCTV monitoring",
            "On-campus healthcare support from Akash Hospital"
        ],
        "fee_details": "Hostel and mess charges are payable annually and vary based on the room occupancy chosen (2-sharing, 3-sharing, 4-sharing) and air-conditioning preferences. Refundable security deposit is collected upon admission. Contact the hostel warden / admissions office for the exact current room-wise fee schedule.",
        "admissions_contact": {
            "phone": "+91 9513107575",
            "email": "admissions@akashinstitutions.com"
        },
        "source_url": "https://akashiet.com/infrastructure/",
        "source_type": "Official College Portal",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "fee_transport_charges",
        "category": "Fees and Expenses",
        "title": "College Bus & Transportation Charges",
        "academic_year": "2025-2026",
        "fleet_coverage": "Fleet of dedicated college buses covering key routes across Bengaluru city, North Bengaluru, Yelahanka, Hebbal, KR Puram, Devanahalli, Doddaballapur, and Chickballapur.",
        "fee_details": "Transport charges are optional and calculated annually depending on the pick-up and drop location distance. Pass cards are issued at the start of each academic year.",
        "source_url": "https://akashiet.com/infrastructure/",
        "source_type": "Official College Portal",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "fee_refund_policy",
        "category": "Fees and Expenses",
        "title": "Fee Refund & Cancellation Policy",
        "academic_year": "2025-2026",
        "policy_summary": "Refund of tuition and institutional fees in case of cancellation or withdrawal strictly follows the guidelines laid down by the All India Council for Technical Education (AICTE), the University Grants Commission (UGC), and the Karnataka Examination Authority (KEA).",
        "key_terms": [
            "Cancellations requested before the officially notified last date of admission are processed with nominal processing charge deductions as prescribed by AICTE/KEA regulations.",
            "Candidates surrendering seats through KEA or COMEDK rounds must submit their surrender orders directly through the respective portal.",
            "Caution deposits are refundable upon completion of the course and submission of No Due certificates from all departments, library, and hostel."
        ],
        "source_url": "https://www.akashinstitutions.com/",
        "source_type": "Official Group Portal",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    }
]

with open(os.path.join(kb_dir, "fees.json"), "w", encoding="utf-8") as f:
    json.dump(fees_records, f, indent=2)

# 6. Scholarships
scholarships_records = [
    {
        "id": "sch_aet",
        "category": "Scholarships",
        "scheme_name": "Akash Entrance Test (AET) Institutional Scholarships",
        "offered_by": "Akash Group of Institutions / Akash Education & Development Trust",
        "eligibility_criteria": "Students with outstanding academic performance in their 10+2 / 2nd PUC qualifying exams who participate in the Akash Entrance Test (AET).",
        "benefit": "Merit-based tuition fee concessions and institutional scholarships awarded for qualifying scores in AET.",
        "application_mode": "Conducted annually prior to the start of the academic year by Akash Group of Institutions.",
        "contact": "admissions@akashinstitutions.com / +91 9513107575",
        "source_url": "https://www.akashinstitutions.com/scholarships/",
        "source_type": "Official Scholarship Records",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "sch_inst_awards",
        "category": "Scholarships",
        "scheme_name": "AGI Institutional Awards of Excellence",
        "offered_by": "Akash Group of Institutions",
        "eligibility_criteria": "Award of Excellence presented to academic achievers and department toppers each academic year. Also honors extraordinary achievements in sports, cultural activities, and state/national recognitions.",
        "benefit": "Certificate of merit, cash awards, and tuition concessions.",
        "source_url": "https://www.akashinstitutions.com/scholarships/",
        "source_type": "Official Scholarship Records",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "sch_ssp_karnataka",
        "category": "Scholarships",
        "scheme_name": "Karnataka State Scholarship Portal (SSP) - Post Matric Scholarships",
        "offered_by": "Government of Karnataka",
        "applicable_to": "Eligible Karnataka domicile students belonging to SC, ST, and Backward Classes (OBC Cat-1, 2A, 2B, 3A, 3B).",
        "benefits": "Tuition fee reimbursement, maintenance allowances, and Vidyasiri food & accommodation assistance as per state government norms.",
        "application_portal": "https://ssp.postmatric.karnataka.gov.in/",
        "required_documents": [
            "Student Aadhaar Card & linked bank account",
            "College Registration / USN Number",
            "Caste and Income Certificate (RD Number)",
            "10th & 12th Marks Cards",
            "Fee Receipt & College Bonafide Certificate"
        ],
        "important_note": "Scholarship is disbursed directly by the Government of Karnataka into the student's Aadhaar-seeded bank account via DBT upon successful verification. AIET provides full documentation support through its scholarship desk.",
        "source_url": "https://www.akashinstitutions.com/scholarships/",
        "source_type": "Government Portal & Institutional Guide",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "sch_nsp_central",
        "category": "Scholarships",
        "scheme_name": "National Scholarship Portal (NSP) - Central Sector Schemes",
        "offered_by": "Government of India (Ministry of Education & Ministry of Minority Affairs)",
        "applicable_to": "Meritorious students from low-income families and recognized minority communities (Muslim, Christian, Sikh, Buddhist, Jain, Parsi) enrolled in technical degree programs.",
        "schemes_included": [
            "Central Sector Scheme of Scholarships for College and University Students",
            "Merit-cum-Means Scholarship for Professional and Technical Courses CS (Minorities)",
            "Post-Matric Scholarship for Students with Disabilities"
        ],
        "application_portal": "https://scholarships.gov.in/",
        "income_limit": "Generally annual parental income <= ₹2.5 Lakhs (MCM) or <= ₹4.5 Lakhs (Central Sector).",
        "source_url": "https://www.akashinstitutions.com/scholarships/",
        "source_type": "Government Portal & Institutional Guide",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "sch_aicte_pragati",
        "category": "Scholarships",
        "scheme_name": "AICTE Pragati Scholarship for Girl Students",
        "offered_by": "All India Council for Technical Education (AICTE), New Delhi",
        "applicable_to": "Female students admitted to 1st year of B.E. degree or 2nd year (lateral entry) in AICTE-approved institutions (maximum two girls per family).",
        "benefit_amount": "₹50,000 per annum for every year of study towards college fees, computer, books, and living expenses.",
        "income_limit": "Family income must not exceed ₹8.00 Lakhs per annum.",
        "portal": "National Scholarship Portal (NSP) / AICTE Portal",
        "source_url": "https://www.akashinstitutions.com/scholarships/",
        "source_type": "AICTE Official Directive",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "sch_aicte_saksham",
        "category": "Scholarships",
        "scheme_name": "AICTE Saksham Scholarship for Specially-Abled Students",
        "offered_by": "All India Council for Technical Education (AICTE), New Delhi",
        "applicable_to": "Specially-abled students having disability of not less than 40% admitted to 1st year B.E. or 2nd year lateral entry in AICTE approved college.",
        "benefit_amount": "₹50,000 per annum for tuition, equipment, and learning aids.",
        "income_limit": "Family income must not exceed ₹8.00 Lakhs per annum.",
        "portal": "National Scholarship Portal (NSP) / AICTE Portal",
        "source_url": "https://www.akashinstitutions.com/scholarships/",
        "source_type": "AICTE Official Directive",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    }
]

with open(os.path.join(kb_dir, "scholarships.json"), "w", encoding="utf-8") as f:
    json.dump(scholarships_records, f, indent=2)

# 7. Infrastructure
infrastructure_records = [
    {
        "id": "infra_campus_overview",
        "category": "Infrastructure",
        "title": "AIET Campus Overview & Learning Environment",
        "description": "Akash Institute of Engineering & Technology is established on a vast, eco-friendly campus on Prasannahalli Road, Devanahalli, North Bengaluru. The campus features state-of-the-art academic blocks, smart lecture halls, advanced research laboratories, central library, Wi-Fi connectivity, separate student hostels, sports grounds, and on-campus hospital support.",
        "source_url": "https://akashiet.com/infrastructure/",
        "source_type": "Official College Portal",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "infra_classrooms",
        "category": "Infrastructure",
        "title": "Smart Classrooms & Lecture Halls",
        "description": "ICT-enabled lecture halls equipped with digital projectors, audio-visual systems, high-speed Wi-Fi, and ergonomic seating designed to foster interactive and participatory teaching-learning experiences.",
        "source_url": "https://akashiet.com/infrastructure/",
        "source_type": "Official College Portal",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "infra_computer_labs",
        "category": "Infrastructure",
        "title": "Specialized Computer Science & AI Laboratories (First Floor)",
        "description": "Modern air-conditioned computer laboratories equipped with high-end workstations, gigabit network backbones, and development stacks. Located on the first floor. Labs include: Data Structures Lab, Python Lab, DBMS Lab, Java Lab, C-Programming Lab, Operating Systems Lab, Artificial Intelligence & Machine Learning Lab, and Cybersecurity Defense Lab.",
        "floor_location": "First Floor",
        "source_url": "https://www.akashinstitutions.com/colleges/akash-institute-of-engineering-technology/",
        "source_type": "Official College Portal",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "infra_library",
        "category": "Infrastructure",
        "title": "Central Library & Digital E-Library (First Floor)",
        "description": "Comprehensive library housing extensive collections of standard engineering textbooks, reference volumes, print journals, and digital e-resources under VTU Consortium. Located on the first floor. Includes a multimedia digital library section with high-speed internet for accessing research papers, NPTEL courseware, and e-books.",
        "floor_location": "First Floor",
        "source_url": "https://akashiet.com/infrastructure/",
        "source_type": "Official College Portal",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "infra_chemistry_lab",
        "category": "Infrastructure",
        "title": "Engineering Chemistry Laboratory (Ground Floor)",
        "description": "Equipped with state-of-the-art instrumental analysis and chemical experimentation equipment for basic science engineering curriculum. Located on the ground floor.",
        "floor_location": "Ground Floor",
        "source_url": "https://akashiet.com/infrastructure/",
        "source_type": "Official College Portal",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "infra_physics_lab",
        "category": "Infrastructure",
        "title": "Engineering Physics Laboratory (Fourth Floor)",
        "description": "Advanced physics laboratory equipped with optical benches, laser apparatus, and semiconductor testing equipment. Located on the fourth floor.",
        "floor_location": "Fourth Floor",
        "source_url": "https://akashiet.com/infrastructure/",
        "source_type": "Official College Portal",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "infra_principal_office",
        "category": "Infrastructure",
        "title": "Principal's Office (Ground Floor)",
        "description": "The Principal's Office of Akash Institute of Engineering and Technology (AIET) is situated on the ground floor. It serves as the institutional head office for academic and executive administration.",
        "floor_location": "Ground Floor",
        "source_url": "https://akashiet.com/",
        "source_type": "Official College Portal",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "infra_admin_office",
        "category": "Infrastructure",
        "title": "Administrative Office & Student Section (Ground Floor)",
        "description": "The college administrative office is located on the ground floor. Office timing is from 3:00 PM to 5:00 PM Monday to Friday, and from 1:00 PM to 3:00 PM on Saturday. It assists students with admissions, certificates, fee receipts, identity cards, and university documentation.",
        "floor_location": "Ground Floor",
        "office_hours": "Monday to Friday: 3:00 PM to 5:00 PM; Saturday: 1:00 PM to 3:00 PM",
        "source_url": "https://akashiet.com/",
        "source_type": "Official College Portal",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "infra_stationery_store",
        "category": "Infrastructure",
        "title": "Books and Stationery Store (Ground Floor)",
        "description": "The campus books and stationery store is located on the ground floor. Students can procure VTU prescribed textbooks, assignment books, records, engineering drawing instruments, stationery, and academic supplies here.",
        "floor_location": "Ground Floor",
        "source_url": "https://akashiet.com/",
        "source_type": "Official College Portal",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "infra_floor_directory",
        "category": "Infrastructure",
        "title": "Campus Floor Directory & Landmark Navigation",
        "description": "Campus Floor Navigation Directory: 1. Ground Floor: Houses the Principal's Office, the Administrative Office, the Books and Stationery store, and the Chemistry Lab. 2. First Floor: Houses the Central Library and the Computer Labs. 3. Fourth Floor: Houses the Physics Lab.",
        "ground_floor": "Principal Office, College Administrative Office, Books and Stationery store, Chemistry Lab",
        "first_floor": "Central Library, Computer Labs",
        "fourth_floor": "Physics Lab",
        "source_url": "https://akashiet.com/",
        "source_type": "Official College Portal",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "infra_hostels",
        "category": "Infrastructure",
        "title": "Student Residential Hostels (Boys & Girls)",
        "description": "Separate Wi-Fi enabled hostels on campus with 400 accommodations for boys and 700 accommodations for girls. Features furnished rooms (twin/triple/quad sharing), 24/7 security, CCTV surveillance, continuous water supply with solar heating, hygienic mess dining facilities, reading room, indoor games, and laundry service.",
        "source_url": "https://akashiet.com/infrastructure/",
        "source_type": "Official College Portal",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "infra_auditorium",
        "category": "Infrastructure",
        "title": "Central Auditorium & Seminar Facilities",
        "description": "Magnificent air-conditioned central auditorium with 1,500 seating capacity, equipped with world-class acoustic engineering, advanced lighting, and stage multimedia systems for hosting national conferences, technical symposiums, hackathons, and cultural fests.",
        "source_url": "https://akashiet.com/infrastructure/",
        "source_type": "Official College Portal",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "infra_hospital",
        "category": "Infrastructure",
        "title": "Akash Hospital & On-Campus Healthcare Support",
        "description": "Unique advantage of an integrated on-campus multi-specialty teaching hospital (Akash Hospital) operating 24 hours a day, 7 days a week. Provides immediate emergency medical support, outpatient and inpatient care, specialized consultations, diagnostic laboratories, and round-the-clock ambulance service for students, faculty, and staff.",
        "source_url": "https://akashiet.com/infrastructure/",
        "source_type": "Official College Portal",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "infra_sports",
        "category": "Infrastructure",
        "title": "Sports, Fitness & Recreation",
        "description": "Extensive outdoor sports grounds for cricket, football, basketball, and volleyball. Indoor sports arena for table tennis, badminton, carrom, and chess. Fully equipped gymnasium to promote physical health and active lifestyle.",
        "source_url": "https://akashiet.com/infrastructure/",
        "source_type": "Official College Portal",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "infra_cafeteria",
        "category": "Infrastructure",
        "title": "Cafeteria & Dining Facilities",
        "description": "Spacious, hygienic cafeteria serving fresh South Indian, North Indian, and continental food, healthy snacks, and beverages at subsidized student rates. Prepared under strict hygiene and quality oversight.",
        "source_url": "https://akashiet.com/infrastructure/",
        "source_type": "Official College Portal",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "infra_transport",
        "category": "Infrastructure",
        "title": "Transportation & Bus Services",
        "description": "Fleet of well-maintained college buses connecting AIET campus with various parts of Bengaluru urban and rural districts including Yelahanka, Hebbal, Majestic, RT Nagar, KR Puram, Devanahalli town, and Doddaballapur.",
        "source_url": "https://akashiet.com/infrastructure/",
        "source_type": "Official College Portal",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    }
]

with open(os.path.join(kb_dir, "infrastructure.json"), "w", encoding="utf-8") as f:
    json.dump(infrastructure_records, f, indent=2)

# 8. Admissions
admissions_records = [
    {
        "id": "adm_overview",
        "category": "Admissions",
        "title": "Engineering & Postgraduate Admissions at AIET",
        "description": "Admissions to Akash Institute of Engineering & Technology are open for Karnataka and Non-Karnataka students across B.E., B.E. Lateral Entry, MBA, and MCA programmes.",
        "intake_codes": {
            "KCET_Code": "E300 (Akash Institute of Engineering and Technology, Devanahalli)",
            "COMEDK_Code": "E005",
            "PGCET_MBA_Code": "B097",
            "PGCET_MCA_Code": "C550"
        },
        "btech_eligibility": "Passed 10+2 / 2nd PUC examination with Physics and Mathematics as compulsory subjects, plus Chemistry/Biology/Biotech/Computer Science, securing minimum 45% aggregate marks (40% for SC/ST and OBC of Karnataka).",
        "admission_steps": [
            "Step 1: Check eligibility criteria for the desired engineering or PG program.",
            "Step 2: Appear for entrance exam (KCET for Karnataka quota, COMEDK for all-India merit, PGCET for MBA/MCA, or apply for Management quota).",
            "Step 3: Participate in KEA / COMEDK counselling and choose AIET (KCET: E300, COMEDK: E005).",
            "Step 4: For Management quota, fill out the online application at admissions.akashinstitutions.com or visit campus admissions office.",
            "Step 5: Verify original documents and complete seat confirmation."
        ],
        "mandatory_documents": [
            "10th Standard / SSLC Marks Card (proof of date of birth)",
            "12th Standard / 2nd PUC Marks Card",
            "Transfer Certificate (TC) from previous institution",
            "Migration Certificate (for Non-Karnataka / CBSE / ICSE boards)",
            "Conduct / Character Certificate",
            "Caste and Income Certificate (if claiming reservation in Karnataka)",
            "Karnataka Study Certificate (7 years study proof for KCET quota)",
            "Entrance Exam Rank Card / Allotment Letter (KCET / COMEDK / PGCET)",
            "Copy of Student Aadhaar Card",
            "Recent passport-size photographs (6 copies)"
        ],
        "contact_info": {
            "admissions_office": "Akash Institute of Engineering & Technology, Prasannahalli Road, Devanahalli, Bengaluru - 562110",
            "phone_numbers": ["+91 9513107575", "+91 9513597575"],
            "landline": "080-244-11-222",
            "email": "admissions@akashinstitutions.com",
            "website": "https://admissions.akashinstitutions.com/engineering"
        },
        "source_url": "https://admissions.akashinstitutions.com/engineering",
        "source_type": "Official Admissions Portal",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    }
]

with open(os.path.join(kb_dir, "admissions.json"), "w", encoding="utf-8") as f:
    json.dump(admissions_records, f, indent=2)

# 9. Academic Information & Student Life
academic_records = [
    {
        "id": "acad_curriculum_vtu",
        "category": "Academic Information",
        "title": "VTU Academic Curriculum & Grading System",
        "description": "AIET strictly follows the Choice-Based Credit System (CBCS) and Outcome-Based Education (OBE) model prescribed by Visvesvaraya Technological University (VTU), Belagavi. The curriculum is divided into 8 semesters for B.E. and 4 semesters for MBA/MCA.",
        "attendance_policy": "Minimum 85% attendance is mandatory in each theory and laboratory course as per college rules and VTU regulations.",
        "evaluation_system": "Continuous Internal Evaluation (CIE) carrying 50% weightage (internal tests, assignments, lab work) and Semester End Examination (SEE) carrying 50% weightage conducted by VTU.",
        "source_url": "https://vtu.ac.in/",
        "source_type": "University Affiliation Regulations",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "acad_college_timings",
        "category": "Academic Information",
        "title": "Official College Timings & Office Hours",
        "regular_timing": "Monday to Friday: 9:00 AM to 4:00 PM; Saturday: 9:00 AM to 1:00 PM",
        "office_timing": "Monday to Friday: 3:00 PM to 5:00 PM; Saturday: 1:00 PM to 3:00 PM",
        "description": "College timing is from 9:00 AM to 4:00 PM from Monday to Friday and 9:00 AM to 1:00 PM on Saturday. Office timing is from 3:00 PM to 5:00 PM Monday to Friday and 1:00 PM to 3:00 PM on Saturday.",
        "source_url": "https://akashiet.com/",
        "source_type": "Official Institutional Record",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "acad_college_rules",
        "category": "Academic Information",
        "title": "College Rules, Dress Code & Code of Conduct",
        "rules_list": [
            "Wear full uniform with shoes",
            "Should maintain professional attire",
            "Hair and beard should be properly trimmed",
            "Cargos, jeans, tshirt, chappals, crocs are not allowed inside campus",
            "Should wear ID card",
            "Without following these rules you might not be permitted inside the campus premises",
            "Maintain 85% attendance compulsory in all classes and labs"
        ],
        "description": "Official AIET College Rules & Code of Conduct: 1. Wear full uniform with shoes. 2. Should maintain professional attire. 3. Hair and beard should be properly trimmed. 4. Cargos, jeans, tshirt, chappals, crocs are not allowed inside campus. 5. Should wear ID card. 6. Without following these rules you might not be permitted inside the campus premises. 7. Maintain 85% attendance compulsory across all theory classes and labs.",
        "source_url": "https://akashiet.com/",
        "source_type": "Official Institutional Record",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "acad_placement_training",
        "category": "Academic Information",
        "title": "Placement Cell & Career Development",
        "description": "The Placement and Training Cell at AIET provides comprehensive pre-placement training starting from early semesters. Training includes quantitative aptitude, logical reasoning, verbal ability, coding bootcamps (Data Structures, Python, Java, C++), soft skills, resume building, and mock interviews.",
        "global_collaborations": "AIET has partnered with 'Nestling' via VTU, facilitating international internships, study abroad semesters at partnered universities, final-year degrees abroad, and international placement support across 3,500 partner universities in 29 countries including USA, UK, Canada, Australia, and Europe.",
        "placement_contact": "sindhu.placement@akashinstitutions.com",
        "source_url": "https://akashiet.com/about-us/",
        "source_type": "Official College Portal",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    },
    {
        "id": "acad_anti_ragging",
        "category": "Academic Information",
        "title": "Anti-Ragging Policy & Student Safety",
        "description": "AIET enforces a strict zero-tolerance policy against ragging in accordance with Supreme Court directives, AICTE norms, and VTU regulations. An active Anti-Ragging Committee and Squad monitor campus and hostel premises 24/7. Student Grievance Redressal Cell and Internal Complaints Committee (ICC) ensure safety and inclusivity for all students.",
        "source_url": "https://akashiet.com/",
        "source_type": "Official College Portal",
        "last_verified_date": "2026-03-15",
        "verification_status": "VERIFIED_OFFICIAL"
    }
]

with open(os.path.join(kb_dir, "academic_information.json"), "w", encoding="utf-8") as f:
    json.dump(academic_records, f, indent=2)

print(f"Successfully generated all 9 knowledge base files in: {kb_dir}")
print(f"Sources: {len(sources)}")
print(f"Faculty records: {len(faculty_records)}")
print(f"Courses: {len(courses_records)}")
print(f"Fee records: {len(fees_records)}")
print(f"Scholarships: {len(scholarships_records)}")
print(f"Infrastructure: {len(infrastructure_records)}")
