import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env file
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Set GEMINI_API_KEY in your .env file")

model_switch = {
    5: "gemma-3n-e2b-it",
    10: "gemma-3n-e4b-it",
    15: "gemma-3-1b-it",
    20: "gemma-3-4b-it",
    25: "gemma-3-12b-it",
    30: "gemma-3-27b-it",
    35: "gemini-1.5-flash",
    40: "gemini-2.0-flash-lite",
    45: "gemini-2.0-flash",
    50: "gemini-2.5-flash-lite",
    55: "gemini-2.5-flash",
    60: "gemini-2.5-pro"
}


def llm_model(model_number: int, temp: float = 0.5):
    """
    Returns a ChatGoogleGenerativeAI instance for the requested model_number.
    Falls back to the lowest-power model if rate limits or API quota errors occur.
    """

    # Validate model number
    if model_number in model_switch:
        model_name = model_switch[model_number]
    else:
        print(f"Warning: Invalid model number {model_number}. Defaulting to {model_switch[30]}.")
        model_name = model_switch[30]

    # Try creating the model; fall back if API error / rate limit
    try:
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=API_KEY,
            temperature=temp
        )

        return llm

    except Exception as e:  # could replace with specific rate limit exception
        print(
            f"Warning: Model {model_name} unavailable or rate limit exceeded. Falling back to lowest model. Error: {e}")
        fallback_model = model_switch[30]
        return ChatGoogleGenerativeAI(
            model=fallback_model,
            google_api_key=API_KEY,
            temperature=temp
        )
