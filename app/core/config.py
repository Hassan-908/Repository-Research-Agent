import os

from dotenv import load_dotenv


load_dotenv()

GROQ_API_KEY: str = os.getenv("GROQ_API_KEY") or ""
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

GROQ_MODEL = "openai/gpt-oss-20b"

GITHUB_API_URL = "https://api.github.com"
GITHUB_API_VERSION = "2026-03-10"


if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set.")