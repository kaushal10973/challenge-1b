## Challenge 1B: Approach Explanation

### 📌 Problem
Given a collection of documents, a user persona, and a task to perform ("job-to-be-done"), we need to extract the most relevant document sections and rank them by importance.

### 🧠 Approach

1. **Text Extraction:**
   - We use `pdfplumber` to extract text, titles, and sections from PDFs.
   - Pages are segmented and assigned basic metadata (document name, page number).

2. **Embedding-Based Relevance Scoring:**
   - We load a lightweight local embedding model (`all-MiniLM-L6-v2`, ~90MB).
   - The persona + task is embedded as a combined query.
   - Each page/section is embedded and compared using cosine similarity.

3. **Section Ranking:**
   - Top-N sections are selected based on similarity.
   - These are assigned `importance_rank` values.
   - Each section's refined text and metadata is returned.

4. **Offline Execution:**
   - The model and dependencies are packaged inside a Docker image.
   - No downloads or internet access required.

### ⚙️ Technologies
- Python 3.11
- `sentence-transformers`, `pdfplumber`, `numpy`
- Docker (with CPU-only constraint)
- JSON for structured output

### ✅ Constraints Handled
- Model size is < 1GB
- Inference completes within 60s for 3–5 PDFs
- No internet access during runtime