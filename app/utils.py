import os
import pdfplumber
import json
from tqdm import tqdm
from sentence_transformers import SentenceTransformer, util

# Load sentence transformer model
model = SentenceTransformer("app/local_model")

def load_persona_job(persona_path):
    with open(persona_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["persona"], data["job_to_be_done"]

def load_and_chunk_pdfs(folder):
    chunks = []
    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            path = os.path.join(folder, file)
            with pdfplumber.open(path) as pdf:
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        text = text.strip()
                        if len(text) > 100:
                            chunks.append({
                                "document": file,
                                "page": i + 1,
                                "text": text
                            })
    return chunks

def compute_similarity_ranking(chunks, persona, job):
    query = f"{persona}. Task: {job}"
    query_emb = model.encode(query, convert_to_tensor=True)

    results = []
    for chunk in tqdm(chunks, desc="Scoring"):
        chunk_emb = model.encode(chunk["text"], convert_to_tensor=True)
        score = util.cos_sim(query_emb, chunk_emb).item()
        results.append({**chunk, "score": score})

    # Sort by score
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:10]  # top 10 sections

def generate_output_json(ranked_chunks, persona, job, timestamp):
    metadata = {
        "input_documents": list({chunk["document"] for chunk in ranked_chunks}),
        "persona": persona,
        "job_to_be_done": job,
        "processing_timestamp": timestamp
    }

    extracted_sections = []
    subsection_analysis = []

    for i, chunk in enumerate(ranked_chunks, start=1):
        extracted_sections.append({
            "document": chunk["document"],
            "page_number": chunk["page"],
            "section_title": chunk["text"][:80].replace("\n", " ") + "...",
            "importance_rank": i
        })

        subsection_analysis.append({
            "document": chunk["document"],
            "page_number": chunk["page"],
            "refined_text": chunk["text"][:500] + "...",
            "importance_rank": i
        })

    return {
        "metadata": metadata,
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }
