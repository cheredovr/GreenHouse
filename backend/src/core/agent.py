# from langgraph.graph import Graph
# from langchain_community.utilities import SQLDatabase
# from langchain_openai import ChatOpenAI
# from langchain.chains import create_sql_query_chain
# from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
# from langchain_core.messages import HumanMessage, AIMessage
# from typing import Dict, Any, List, Optional, TypedDict


# class AgentState(TypedDict):
#     user_id: str
#     message: str
#     tags: list[str]
#     metadata: dict

# # Инструмент для NL-to-SQL
# query_chain = create_sql_query_chain(llm, db)
# execute_tool = QuerySQLDataBaseTool(db=db)

# def parse_input(state: Dict[str, Any]):
#     """Анализ ввода пользователя и определение intent"""
#     user_input = state["user_input"]
#     messages = state.get("messages", [])
    
#     # Определяем, нужно ли уточнение
#     needs_clarification = len(messages) > 0 and "уточните" in messages[-1].content.lower()
    
#     return {
#         "intent": "find_dishes" if not needs_clarification else "clarify",
#         "user_input": user_input
#     }

# def query_database(state: Dict[str, Any]):
#     """Запрос к базе данных через NL-to-SQL"""
#     question = state["user_input"]
#     try:
#         sql = query_chain.invoke({"question": question})
#         dishes = execute_tool.run(sql)
#         return {
#             "dishes": dishes,
#             "sql_query": sql,
#             "status": "success"
#         }
#     except Exception as e:
#         return {
#             "dishes": [],
#             "error": str(e),
#             "status": "fail"
#         }

# def clarify_question(state: Dict[str, Any]):
#     """Генерация уточняющего вопроса"""
#     last_msg = state["messages"][-1].content if state.get("messages") else ""
#     prompt = f"""
#     Пользователь спросил: '{last_msg}'
#     Нужно уточнить его запрос. Задай ОДИН вопрос.
#     Примеры:
#     - "Вы имеете в виду веганские или обычные блюда?"
#     - "Вам важно, чтобы блюдо было низкокалорийным?"
#     """
#     response = llm.invoke(prompt)
#     return {"response": response.content}

# def generate_recommendation(state: Dict[str, Any]):
#     """Генерация финального ответа с рекомендациями"""
#     dishes = state.get("dishes", [])
    
#     if not dishes:
#         return {"response": "К сожалению, ничего не найдено. Попробуйте изменить запрос."}
    
#     prompt = f"""
#     Сгенерируй рекомендацию на основе блюд:
#     {dishes}
    
#     Формат:
#     «Рекомендую: [Название]. [Описание]. [Цена: X ₽]. 
#     [Дополнение: "Это веганское/низкокалорийное и т.д."]»
#     """
#     response = llm.invoke(prompt)
#     return {"response": response.content}

# # ==================== 4. Сборка графа ====================
# workflow = Graph()

# workflow.add_node("parse_input", parse_input)
# workflow.add_node("query_db", query_database)
# workflow.add_node("clarify", clarify_question)
# workflow.add_node("generate_response", generate_recommendation)

# # Условия переходов
# def router(state: Dict[str, Any]):
#     if state.get("intent") == "clarify":
#         return "clarify"
#     elif state.get("status", "") == "fail":
#         return "clarify"
#     else:
#         return "generate_response"

# workflow.add_conditional_edges(
#     "parse_input",
#     router,
#     {
#         "clarify": "clarify",
#         "generate_response": "generate_response",
#         "query_db": "query_db"
#     }
# )

# workflow.add_edge("query_db", "generate_response")
# workflow.add_edge("clarify", "parse_input")  # Возврат к началу после уточнения

# # ==================== 5. Запуск агента ====================
# app = workflow.compile()

# def run_agent(user_input: str, messages: List = None):
#     """Интерфейс для взаимодействия с агентом"""
#     state = {
#         "user_input": user_input,
#         "messages": messages or []
#     }
    
#     output = None
#     for step in app.stream(state):
#         for node, value in step.items():
#             if node == "response":
#                 output = value["response"]
    
#     return output or "Ошибка обработки запроса"

# # ==================== 6. Примеры использования ====================
# if __name__ == "__main__":
#     # Тест 1: Простой запрос
#     print(run_agent("Посоветуй веганский завтрак"))
    
#     # Тест 2: Запрос с уточнением
#     print(run_agent("Что-то вкусное"))  # Агент спросит уточнения
    
#     # Тест 3: Ошибка в запросе
#     print(run_agent("Блюда с неизвестным ингредиентом"))