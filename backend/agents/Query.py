import os
import pandas as pd
from database.postgres import run_query
from LLM.llmHelper import llm_model
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env (assumes .env is in parent folder)
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

tableName = os.getenv("TABLE_NAME")

def SQLagent(request):
    """
    Generate a SQL query using Gemini models and execute it on PostgreSQL.
    Save results as a CSV file in the project root with correct column names.
    """
    try:
        # Step 1: Get LLM model
        llm = llm_model(50)


        prompt = f"""
        You are an AI that writes SQL queries for a PostgreSQL table called "{tableName}".
        Columns: time, latitude, longitude, depth, temperature, salinity.

        Instructions:
        1. Always include the "time" column in the SELECT query, even if the user does not request it.
        2. If the user does not mention depth, assume depth = 10 and add it as a filter in the WHERE clause.
        3. Ensure the query is syntactically correct PostgreSQL.
        4. Correct any user spelling mistakes in column names (e.g., "temprature" → "temperature").
        5. Return only the SQL query without any explanation or formatting.
        6. While using aggregation operations name the columns as "avg_columnname" like avg_salinity ot avg_temperature or any other like max_salinity or min_columnname 
    
        

        User request: {request}
        """

        # Step 3: Generate SQL query
        response = llm.invoke(prompt)
        sql_query = response.content.strip()
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

        print("Generated SQL Query:\n", sql_query)

        # Step 4: Execute SQL query (with column names)
        result, columns = run_query(sql_query, return_columns=True)

        # Step 5: Save result as CSV in project root
        if result:
            # Project root = one level up from agents/
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            output_path = os.path.join(project_root, "dataExtracted.csv")

            # Delete existing file if present
            if os.path.exists(output_path):
                os.remove(output_path)
                print("🗑️ Old query_result.csv deleted.")

            df = pd.DataFrame(result, columns=columns)

            try:
                df["time"] = pd.to_datetime(df["time"])
                df = df.sort_values("time")
            except Exception:
                print("⚠️ Could not convert 'time' column to datetime.")

            # Save new file
            df.to_csv(output_path, index=False)
            print(f"✅ Results saved to: {output_path}")
        else:
            print("⚠️ No results to save.")

        return {
            "sql_query": sql_query,
            "result": result,
        }

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    # Example user request
    test_request = "get me all salinity from year 2014 in arabic sea"
    SQLagent(test_request)
