
from fastapi import FastAPI
from src.api import user, recommendation

app = FastAPI(
    title="GreenHouse API",
    version="0.1.0"
)

app.include_router(user)
app.include_router(recommendation)