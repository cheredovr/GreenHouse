import sqlite3
import logging
from src.depends import DB_FILENAME, INITSQL_FILE

def init_db():
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()

    with open(INITSQL_FILE, 'r') as sql_file:
        sql_script = sql_file.read()
    
    cursor.executescript(sql_script)
    
    conn.commit()
    conn.close()
    logging.info(f"База данных успешно создана: {DB_FILENAME}")