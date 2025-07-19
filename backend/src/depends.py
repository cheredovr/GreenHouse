import sqlite3
import os

from contextlib import contextmanager
from langchain_openai import ChatOpenAI

LLM_TOKEN = os.getenv("API_KEY")
DB_FILENAME = "resources/greenhouse.db"
INITSQL_FILE = "resources/init.sql"
#db = SQLDatabase.from_uri("greenhouse.db")


#llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, token=LLM_TOKEN)


@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DB_FILENAME)
    conn.row_factory = sqlite3.Row  # Для доступа к полям по имени
    try:
        yield conn
    finally:
        conn.close()
