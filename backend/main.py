
import os.path
from fastapi import FastAPI

from log import setup_logging
from src.depends import DB_FILENAME
from src.api import user, recommendation, dishes
from src.db import init_db

app = FastAPI(
    title="GreenHouse API",
    version="0.1.0"
)

@app.on_event("startup")
def on_startup():
    setup_logging()
    if not os.path.exists(DB_FILENAME):
        init_db()

app.include_router(user)
app.include_router(recommendation)
app.include_router(dishes)