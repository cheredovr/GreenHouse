import logging
import ast
from typing import Dict, Any, List, TypedDict
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import text

class Metadata(TypedDict):
    tags: List[str]

class AgentState(TypedDict):
    user_id: str
    message: str
    metadata: Dict[str, Any]

class RecommendationAgent:
    def __init__(self, llm: ChatOpenAI, db: SQLDatabase):
        self.llm = llm
        self.db = db
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        
        # Явные инструкции по формату вывода
        self.format_instructions = """
        Ты должен вернуть строго в следующем формате:

        SQL QUERY:
        ```sql
        SELECT dish_id FROM таблица WHERE условия;
        ```

        Дополнительные требования:
        1. Запрос должен возвращать только столбец dish_id
        2. Не добавляй никаких пояснений после запроса
        """
        self.db_agent = create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            agent_type="openai-tools",
            verbose=True,
            format_instructions=self.format_instructions
        )

    def _extract_and_execute_sql(self, agent_output: str) -> List[str]:
        """Извлекает SQL из ответа агента и выполняет его"""
        try:
            import re
            sql_match = re.search(r'```sql\n(.*?)\n```', agent_output, re.DOTALL)
            if not sql_match:
                logging.error("SQL query not found in expected format")
                return []
            sql_query = sql_match.group(1).strip()
            logging.info(f"Executing SQL: {sql_query}")
            result = self.db.run(sql_query)
            logging.info(f"Result: {result}")
            result = ast.literal_eval(result)
            return  [str(item[0]) for item in result]
        except Exception as e:
            logging.error(f"SQL extraction/execution error: {e}")
            return []

    def process(self, state: Dict[str, Any]) -> List[str]:
        """Обработка запроса"""
        try:
            prompt = f"""
            {self.format_instructions}
            
            Запрос пользователя: {state['message']}
            Метаданные: {state.get('metadata', {})}
            
            Сгенерируй SQL-запрос для поиска ID блюд, соответствующих запросу. 

            Действуй по шагам:
            1. Проанализируй структуру базы данных
            2. Получи из базы данных все теги и выбери подходящие под запрос пользователя.
            3. Получи из базы данных все ингредиенты и выбери подходящие под запрос пользователя.
            4. Сформируй правильный SQL-запрос. Обязательно учти, чтобы теги(tags) из метаданных были в блюдах полученных через этот запрос.
            5. Верни ТОЛЬКО SQL-запрос без пояснений
            """
            
            response = self.db_agent.invoke({"input": prompt})
            output = response['output'] if isinstance(response, dict) else str(response)
            
            return self._extract_and_execute_sql(output)
            
        except Exception as e:
            logging.error(f"Processing error: {e}")
            return []