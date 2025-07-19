from fastapi import APIRouter

user = APIRouter(prefix="/user")

@user.post("")
def create_user(user_id: str):
    pass


@user.post("/order")
def create_order(user_id: str):
    pass


recommendation = APIRouter(prefix="/recommendation")


@recommendation.get("/")
def reccomend(user_id: str, prompt: str):
    pass

