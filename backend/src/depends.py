import sqlite3
import os
import dotenv
from contextlib import contextmanager
from langchain_openai import ChatOpenAI, OpenAI
from langchain_community.utilities.sql_database import SQLDatabase
from dotenv import load_dotenv
from src.agent import RecommendationAgent

load_dotenv()

LLM_MODEL = os.getenv("LLM_MODEL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DB_FILENAME = "resources/greenhouse.db"
INITSQL_FILE = "resources/init.sql"

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DB_FILENAME)
    conn.row_factory = sqlite3.Row  # Для доступа к полям по имени
    try:
        yield conn
    finally:
        conn.close()


def get_db() -> SQLDatabase:
    return SQLDatabase.from_uri(f"sqlite:///{DB_FILENAME}")

def get_llm():
    return ChatOpenAI(model=LLM_MODEL, api_key=OPENAI_API_KEY, base_url='https://api.openai.com/v1')

def get_recommendation_agent():
    return RecommendationAgent(get_llm(), get_db())