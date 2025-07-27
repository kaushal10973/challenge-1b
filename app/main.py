import os
import json
from datetime import datetime
from utils import (
    load_persona_job,
    load_and_chunk_pdfs,
    compute_similarity_ranking,
    generate_output_json
)

INPUT_DOCS_PATH = "./docs"
OUTPUT_PATH = "./output"
PERSONA_FILE = "./app/persona.json"

def main():
    # Load persona and job
    persona, job = load_persona_job(PERSONA_FILE)
    print(f"🔍 Persona: {persona}")
    print(f"🛠️ Job: {job}")

    # Load and chunk PDFs
    chunks = load_and_chunk_pdfs(INPUT_DOCS_PATH)

    # Compute similarity scores
    ranked_sections = compute_similarity_ranking(chunks, persona, job)

    # Generate JSON output
    timestamp = datetime.now().isoformat()
    output_data = generate_output_json(
        ranked_sections, persona, job, timestamp
    )

    # Save to output/
    output_file = os.path.join(OUTPUT_PATH, "challenge1b_output.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Output saved to {output_file}")

if __name__ == "__main__":
    main()
