# Challenge 1B: Persona-Driven Document Intelligence

## 🧠 Overview
This system extracts and ranks the most relevant sections from PDF documents based on a persona and their task ("job-to-be-done"). It runs **fully offline** in a Docker container with a local model under 1GB.

## 📂 Directory Structure
challenge-1b/
├── app/ → Source code and model
├── input/ → Input PDFs
├── output/ → Output JSON
├── Dockerfile → Build instructions
├── requirements.txt → Python dependencies


## 🐳 Run Using Docker

### Build the image
```bash
docker build --platform linux/amd64 -t challenge-1b:dev .
```

### Run the container
```bash
docker run --rm ^
 -v "%cd%/input:/app/input" ^
 -v "%cd%/output:/app/output" ^
 --network none ^
 challenge-1b:dev
```
(Use \ instead of ^ on Linux/Mac)

# 📥 Input
Place 3–10 related PDFs inside the input/ folder.

Format includes persona and job-to-be-done.

# 📤 Output
Extracted relevant sections in output/challenge1b_output.json

# ⚙️ Constraints Met
✅ Offline inference (no internet)

✅ Model size < 1GB

✅ CPU-only

✅ Processing time < 60s (for 3–5 PDFs)
