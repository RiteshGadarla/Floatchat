import os
import json
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from LLM.llmHelper import llm_model

# === Global config ===
CHUNK_SIZE = 30000  # Max characters per chunk
NUM_WORKERS = 2     # Set number of parallel workers


def summarize_chunk(chunk, llm):
    """Summarize a single chunk using LLM."""
    try:
        chunk_text = json.dumps(chunk)
        prompt = f"Summarize this data chunk:\n{chunk_text}"
        response = llm.invoke(prompt)
        return response.content["parts"][0]["text"] if "parts" in response.content else response.content

    except Exception as e:
        print(f"⚠️ Chunk summarization error: {e}")
        return ""


def summarizeTable(csv_file=None):
    """
    Generate a summary from a CSV file using LLM in parallel for chunks.

    Args:
        csv_file (str, optional): Path to CSV. Defaults to 'query_result.csv' in project root.

    Returns:
        str: Final summary
    """
    try:
        # Default CSV path = project root
        if csv_file is None:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            csv_file = os.path.join(project_root, "dataExtracted.csv")

        if not os.path.exists(csv_file):
            print(f"⚠️ CSV file not found: {csv_file}")
            return None

        # Load CSV
        df = pd.read_csv(csv_file)
        data_as_list = df.to_dict(orient='records')

        if not data_as_list:
            print("⚠️ No data to summarize.")
            return None

        # === Split data into chunks ===
        chunks, current_chunk, current_size = [], [], 0
        for row in data_as_list:
            row_text = json.dumps(row)
            row_size = len(row_text)
            if current_size + row_size <= CHUNK_SIZE:
                current_chunk.append(row)
                current_size += row_size
            else:
                chunks.append(current_chunk)
                current_chunk = [row]
                current_size = row_size
        if current_chunk:
            chunks.append(current_chunk)

        print(f"🔹 Total chunks to summarize: {len(chunks)}")

        # === Initialize LLM ===
        llm = llm_model(50)

        # === Multithreaded chunk summarization ===
        all_summaries = []
        with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
            futures = {executor.submit(summarize_chunk, chunk, llm): idx for idx, chunk in enumerate(chunks)}

            for future in tqdm(as_completed(futures), total=len(futures), desc="Summarizing Chunks"):
                idx = futures[future]
                summary = future.result()
                all_summaries.append(summary)

        # === Combine summaries for final summary ===
        combined_prompt = "Based on the following chunk summaries, generate a final concise summary:\n" + "\n---\n".join(all_summaries)
        final_response = llm_model(55).invoke(combined_prompt)
        final_summary = final_response.content["parts"][0]["text"] if "parts" in final_response.content else final_response.content

        print("🎉 Final summary generated successfully.")
        return final_summary

    except Exception as e:
        print("Summary generation error:", e)
        return "Error generating summary."


if __name__ == "__main__":
    summary = summarizeTable()
    print("\n=== Final Summary ===")
    print(summary)
