# Resume Analyzer - System Architecture & Progress Notes

## 🏗️ System Overview
The system is an AI-first HR platform that acts as a hybrid **Resume Understanding Engine, ATS Scoring System, and Semantic Job Matching System**. It processes candidate resumes, extracts structured data using AI embeddings, calculates ATS scores, and semantically matches candidates to jobs while providing a skill gap analysis.

---

## 📂 Codebase Walkthrough (In Sequential Data Flow Order)

This section outlines every file in the exact sequence that data flows through the system, from database definitions up to the final job match.

### 1. Database Foundation
Before anything runs, the database schema defines how data is stored.
* **`app/models/resume_model.py`**
  * **What's inside:** The PostgreSQL SQLAlchemy schema for candidate resumes. It defines fields for the uploaded file name, the raw text extracted from it, a JSONB column (`parsed_json`) to store structured extracted skills, and a float for the ATS score.
* **`app/models/job_model.py`**
  * **What's inside:** The schema for Jobs. It stores job titles, required skills, and importantly, the pre-computed embedding vector (`job.embedding`) used for semantic matching.

### 2. The Entry Point
* **`app/api/routes/resume_routes.py`**
  * **What's inside:** The FastAPI endpoint (`/upload-resume`). This is the orchestrator. It receives a file upload, checks the extension (PDF, DOCX, TXT), saves it locally to `app/uploads`, and then sequentially calls the parsers, the cleaner, the skill extractor, and finally saves everything to the PostgreSQL database.

### 3. Text Extraction Pipeline
Once the route receives the file, it passes it to the parsers.
* **`app/services/parser/pdf_parser.py`**
  * **What's inside:** Uses PyPDF (or similar) to extract raw string text from PDF resumes.
* **`app/services/parser/docx_parser.py`**
  * **What's inside:** Extracts raw string text from Word documents.
* **`app/services/parser/txt_parser.py`**
  * **What's inside:** Reads standard plain text files.
* **`app/services/parser/cleaner.py`**
  * **What's inside:** Takes the raw, messy text from the parsers and normalizes it. It strips out bad whitespace, weird Unicode characters, and standardizes the format so the AI models don't get confused.

### 4. AI Skill Extraction & NLP Layer
After the text is clean, the system extracts what the candidate actually knows.
* **`app/services/nlp/skill_embeddings.py`**
  * **What's inside:** Contains predefined lists of `TECHNICAL_SKILLS` and `SOFT_SKILLS`, and a function `build_skill_embeddings()` that loads precomputed vector embeddings for each of these skills.
* **`app/services/embeddings/embedding_model.py`**
  * **What's inside:** Contains the `get_embedding(text)` function, which turns any piece of text (like the resume) into a mathematical vector representation.
* **`app/services/embeddings/similarity.py`**
  * **What's inside:** Contains the mathematical `cosine_similarity(vec1, vec2)` function used to see how closely two vectors match.
* **`app/services/nlp/embedding_skill_extractor.py`**
  * **What's inside:** The core semantic skill engine. It has been updated to use a **Hybrid Approach**: first, it uses exact string matching to instantly find explicit skills (preventing similarity dilution on massive texts), and then chunks the remaining text into 50-word blocks to calculate semantic cosine similarity against predefined skill vectors. It strictly returns a dictionary with `"technical_skills"`, `"soft_skills"`, and `"all_skills"`.

### 5. ATS Scoring Engine
* **`app/services/ats/ats_calculator.py`**
  * **What's inside:** Analyzes the resume's formatting, length, and keyword density to give it a standard ATS (Applicant Tracking System) score out of 100. *Note:* The base `structure_score` from this module is now actively hooked into `resume_routes.py` and calculated upon upload so the database accurately reflects the resume's quality.

---

## 🛠️ Recent System Bug Fixes (May 2026)
* **Empty `parsed_json` Fix:** The system previously failed to extract skills from very long resumes because comparing a massive document embedding to a single-word skill embedding diluted the similarity score below the `0.45` threshold. This was solved by implementing the Hybrid Approach (exact string match + chunked embeddings).
* **`ats_score` Defaulting to 0 Fix:** The `ats_score` field in the database was defaulting to `0` because the ATS calculator wasn't being called during the upload sequence. `resume_routes.py` was updated to calculate a base `structure_score` and save it to the database immediately upon file upload.

### 6. Job Matching & Recommendation Engine
Once the resume is fully parsed, scored, and saved, the system attempts to find the candidate a job.
* **`app/services/matching/gap_analysis.py`**
  * **What's inside:** Contains the `skill_gap_analyzer()`. It does a set comparison between the candidate's extracted skills and the job's required skills. It figures out what is missing, what matches, and uses a rule-based engine to generate study recommendations (e.g., "Learn cloud fundamentals" if AWS is missing).
* **`app/services/matching/job_matcher.py`**
  * **What's inside:** The grand finale. It loads all jobs from the database, grabs their embeddings, and compares them semantically against the candidate's resume embedding. It calculates a `match_score`, runs the `gap_analysis` for each job, sorts the best matches, and returns the top `K` results.

### 7. Application Initialization
* **`app/main.py`**
  * **What's inside:** The root FastAPI application. It wires all the individual routers (like `resume_routes.py`, `job_routes.py`, etc.) together so the server can run.

---

## 🚀 Future Improvements & Minor Notes
*These are not blockers, but important architectural reminders for future iterations:*

1. **Job Embeddings Ingestion:** `job_matcher.py` assumes `job.embedding` is already populated in the database. A script or API endpoint must be created to precompute and save these embeddings whenever a new Job is inserted.
2. **Stable Skill Extraction Output:** `gap_analysis.py` and `job_matcher.py` tightly couple with the skill extractor via the `"all_skills"` dictionary key. Any future updates to the skill extractor (like moving to an LLM API) must maintain this exact data schema (`{"all_skills": ["List", "of", "strings"]}`) to prevent system crashes.
3. **Vector Database Integration:** As the job pool scales, iterating over every single job and calculating cosine similarity in Python (`job_matcher.py`) will become slow. Integrating a dedicated vector database (like ChromaDB or pgvector) for the job embeddings is highly recommended for production scale.
