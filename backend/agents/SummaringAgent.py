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
def summarize_chunk(chunk, llm, userPrompt=None):
    try:
        chunk_text = json.dumps(chunk, indent=2)

        prompt = f"""
        You are an AI assistant helping to summarize part of a dataset. 
        Your summary will be used by another AI agent for deeper analysis.

        User request: {userPrompt if userPrompt else "General summary"}

        Here is one chunk of the dataset:
        {chunk_text}

        Task:
        1. Identify and explain the **main patterns, trends, or anomalies** in this chunk.  
        2. Provide important **numerical ranges, averages, or extreme values** if they are relevant.  
        3. Keep the explanation in **clear, beginner-friendly language** so it is easy to understand.  
        4. Format the output in a **consistent, structured style**:

        Summary:
        - Key trends:
        - Notable anomalies/outliers:
        - Important numeric insights:
        - Other observations:

        Do not provide a final conclusion. Keep it short, factual, and clear.
        """

        response = llm.invoke(prompt)
        return extract_llm_text(response)

    except Exception as e:
        print(f"⚠️ Chunk summarization error: {e}")
        return ""


# === Visualization suggestions based on summary ===
def get_visualizations_from_summary(summary_text, user_request):
    print(summary_text)
    llm = llm_model(55,0.2)

    viz_prompt = f"""
    You are a data visualization assistant. The dataset contains the following attributes:
    - time
    - latitude
    - longitude
    - depth
    - temperature
    - salinity
    - Any aggregated columns like avg_salinity or max_temperature should be treated as their base column name (e.g., salinity, temperature).

    Based on the following textual summary of the data, suggest visualizations to help a user understand the data clearly. 

    Rules:
    1. Only use these visualization types: {ALLOWED_VISUALIZATIONS}.
    2. Avoid illogical visualizations. For example:
       - Do not plot latitude vs longitude as a scatter unless it's explicitly for mapping.
       - Do not plot unrelated numeric comparisons without context.
    3. Prioritize Line Charts when the x-axis can be time.
    4. Each visualization should use columns that make logical sense:
       - Use time on the x-axis for trends over time.
       - Use numeric columns (temperature, salinity, depth) for y-axis values.
    5. Return **only valid JSON**, with each object containing:
       - type: visualization type (from allowed list)
       - columns: list of columns to use (choose from the attributes above)

    Even if the dataset is small or uniform, suggest at least 1–2 visualizations using columns from the summary.
        
    User request:
    {user_request}
    
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
            {"type": "Bar Chart", "columns": ["time", "temperature"],
             "purpose": "Show distribution of temperature over time"},
            {"type": "Scatter Plot", "columns": ["latitude", "salinity"],
             "purpose": "Visualize relationship between latitude and salinity"}
        ]
    return visualizations_info


# === Main summary + visualization generator ===
def summarizeTable(userPrompt, csv_file=None):
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
            futures = {
                executor.submit(summarize_chunk, chunk, llm, userPrompt): idx
                for idx, chunk in enumerate(chunks)
            }
            for future in tqdm(as_completed(futures), total=len(futures), desc="Summarizing Chunks"):
                summary = future.result()
                all_summaries.append(summary)

        # Create final combined prompt with user input
        combined_prompt = f"""
        You are an AI assistant helping a beginner understand data from a CSV file.

        User request: {userPrompt}

        Here are simplified summaries of different chunks of the dataset:
        {"\n---\n".join(all_summaries)}

        Task:
        1. Read the user’s request and the chunk summaries.
        2. Create a **single, clear, and beginner-friendly explanation** of the data.
        3. Use **simple words and short sentences** (avoid technical jargon).
        4. Point out important **trends, patterns, or unusual values**.
        5. If numbers are important, give **context in plain English** 
           (e.g., instead of "mean temperature = 20", say "on average, the temperature stays around 20°C").
        6. Do not repeat information; merge related insights into a smooth explanation.
        7. Write it like you are **teaching a student who is new to data analysis**.
        """

        final_response = llm_model(55).invoke(combined_prompt)
        final_summary = extract_llm_text(final_response)

        # Get visualizations
        visualizations_info = get_visualizations_from_summary(final_summary, userPrompt)

        print("visualizations_info: ", visualizations_info)
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
