import os
from pathlib import Path
from dotenv import load_dotenv
import psycopg2

# Load environment variables from .env (assumes .env is in parent folder)
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")


def run_query(query: str, return_columns: bool = False):
    """
    Execute a SQL query on PostgreSQL and return results.

    Args:
        query (str): SQL query string
        return_columns (bool): If True, also return column names

    Returns:
        list of tuples (rows), or (rows, columns) if return_columns=True
    """
    try:
        # Connect using environment variables
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

        cur = conn.cursor()
        cur.execute(query)

        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description] if return_columns else None

        cur.close()
        conn.close()

        if return_columns:
            return rows, columns
        return rows

    except Exception as e:
        return f"PostgreSQL Error: {e}"


if __name__ == "__main__":
    test_query = "SELECT version();"
    result, columns = run_query(test_query, return_columns=True)

    if isinstance(result, str) and result.startswith("PostgreSQL Error"):
        print("Connection failed:", result)
    else:
        print("Connection successful!")
        print("Columns:", columns)
        print("PostgreSQL version:", result[0][0])
