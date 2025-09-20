import os
import json
import re
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from LLM.llmHelper import llm_model

# === Global config ===
CHUNK_SIZE = 30000  # Max characters per chunk
NUM_WORKERS = 2
ALLOWED_VISUALIZATIONS = [
    "Bar Chart", "Line Chart", "Histogram", "Scatter Plot",
    "Pie Chart", "Box Plot", "Area Chart", "Heatmap"
]

# === Robust JSON extractor ===
def safe_json_load(text):
    """Extract JSON from LLM response robustly."""
    try:
        match = re.search(r'(\[.*\]|\{.*\})', text, re.DOTALL)
        if match:
            json_text = re.sub(r',(\s*[}\]])', r'\1', match.group(1))
            return json.loads(json_text)
    except Exception as e:
        print("⚠️ JSON parsing failed:", e)
    return []

# === Helper to safely extract LLM text ===
def extract_llm_text(response):
    """Safely extract text from LLM response."""
    if isinstance(response.content, dict):
        if "parts" in response.content and isinstance(response.content["parts"], list):
            return response.content["parts"][0].get("text", "")
    elif isinstance(response.content, str):
        return response.content
    return ""

# === Chunk summarization ===
def summarize_chunk(chunk, llm):
    try:
        chunk_text = json.dumps(chunk)
        prompt = f"Summarize this data chunk:\n{chunk_text}"
        response = llm.invoke(prompt)
        return extract_llm_text(response)
    except Exception as e:
        print(f"⚠️ Chunk summarization error: {e}")
        return ""

# === Visualization suggestions based on summary ===
def get_visualizations_from_summary(summary_text):
    print(summary_text)
    llm = llm_model(55)
    viz_prompt = f"""
You are a data visualization assistant. The dataset contains the following attributes:
- if you get any get aggreagate columns, take it as avg_columnname like avg_salinity or max_temperature or any other column name  then just take the column name as it is
- time
- latitude
- longitude
- depth
- temperature
- salinity

Based on the following textual summary of the data, suggest visualizations to help a user understand the data clearly. 
Only use these visualization types: {ALLOWED_VISUALIZATIONS}. 
For each suggested visualization, return **only valid JSON**, with the following fields:
- type: visualization type (from allowed list)
- columns: list of columns to use (choose from the attributes above)
Even if the dataset is small or uniform, suggest at least 1-2 visualizations using columns from the summary.
Do **not** add any text outside the JSON.

Textual Summary:
{summary_text}
"""
    try:
        response = llm.invoke(viz_prompt)
        text = extract_llm_text(response)
        visualizations_info = safe_json_load(text)
        print("testing: ", visualizations_info)
    except Exception as e:
        print("⚠️ Visualization generation error:", e)
        visualizations_info = []

    # Fallback
    if not visualizations_info:
        visualizations_info = [
            {"type": "Bar Chart", "columns": ["time", "temperature"], "purpose": "Show distribution of temperature over time"},
            {"type": "Scatter Plot", "columns": ["latitude", "salinity"], "purpose": "Visualize relationship between latitude and salinity"}
        ]
    return visualizations_info

# === Main summary + visualization generator ===
def summarizeTable(csv_file=None):
    try:
        if csv_file is None:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            csv_file = os.path.join(project_root, "dataExtracted.csv")

        if not os.path.exists(csv_file):
            print(f"⚠️ CSV file not found: {csv_file}")
            return None, []

        df = pd.read_csv(csv_file)
        data_as_list = df.to_dict(orient='records')

        if not data_as_list:
            print("⚠️ No data to summarize.")
            return None, []

        # Split data into chunks
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

        # Summarize chunks in parallel
        llm = llm_model(50)
        all_summaries = []
        with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
            futures = {executor.submit(summarize_chunk, chunk, llm): idx for idx, chunk in enumerate(chunks)}
            for future in tqdm(as_completed(futures), total=len(futures), desc="Summarizing Chunks"):
                summary = future.result()
                all_summaries.append(summary)

        # Final summary
        combined_prompt = "Based on the following chunk summaries, generate a concise textual summary of the data:\n" + "\n---\n".join(all_summaries)
        final_response = llm_model(55).invoke(combined_prompt)
        final_summary = extract_llm_text(final_response)

        # Get visualizations
        visualizations_info = get_visualizations_from_summary(final_summary)

        print("visualizations_info: ",visualizations_info)
        print("🎉 Final summary and visualizations generated successfully.")
        return final_summary, visualizations_info

    except Exception as e:
        print("Summary generation error:", e)
        return "Error generating summary.", []

# === Main entry point ===
if __name__ == "__main__":
    summary, visualizations = summarizeTable()
    print("\n=== Final Summary ===")
    print(summary)
    print("\n=== Visualization Recommendations ===")
    print(json.dumps(visualizations, indent=2))
