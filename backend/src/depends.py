from langchain_openai import ChatOpenAI
import os

LLM_TOKEN = os.getenv("API_KEY")


llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)