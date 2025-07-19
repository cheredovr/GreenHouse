import logging
from typing import Dict, Any, List, TypedDict
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit

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
        self.db_agent = create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            agent_type="zero-shot-react-description",  # Измените на "zero-shot-react-description" если ошибка останется
            verbose=True
        )
        
    def _extract_dish_ids(self, result: Dict[str, Any]) -> List[str]:
        """Извлекает ID блюд из результата SQL-запроса"""
        try:
            if isinstance(result, dict) and 'output' in result:
                output = result['output']
            else:
                output = str(result)
            
            # Улучшенное регулярное выражение
            import re
            ids = re.findall(r'(?:dish_?id|id)[\s:=]+[\'"]?(\d+)[\'"]?', output, re.IGNORECASE)
            return list(set(ids))
            
        except Exception as e:
            logging.error(f"Error extracting dish IDs: {e}")
            return []

    def process(self, state: AgentState) -> List[str]:
        """Основной метод обработки запроса"""
        try:
            query = {
                "input": f"""
                Пользователь запросил: '{state['message']}'
                Метаданные: {state.get('metadata', {})}
                
                Сформируй правильный SQL-запрос для поиска ID блюд.
                Запрос должен:
                - Точно соответствовать структуре базы данных
                - Учитывать все критерии пользователя
                - Возвращать только столбец с ID (dish_id или аналогичный)
                """
            }
            
            result = self.db_agent.invoke(query)
            return self._extract_dish_ids(result)
            
        except Exception as e:
            logging.error(f"Error processing request: {e}")
            return []