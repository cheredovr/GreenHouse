from fastapi import APIRouter

from src.depends import get_db, get_db_connection

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



from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import sqlite3
from datetime import datetime


dishes = APIRouter(prefix="/dishes")

# Модели запроса
class DishCreate(BaseModel):
    name: str
    price: float
    ingredients: List[str]
    tags: List[str]

@dishes.post("/", status_code=201)
async def create_dish(dish: DishCreate):
    try:
        with get_db_connection() as db:
            cursor = db.cursor()
            cursor.execute("BEGIN TRANSACTION")
            
            # 1. Добавляем блюдо
            cursor.execute(
                "INSERT INTO dishes (name, price) VALUES (?, ?)",
                (dish.name, dish.price)
            )
            dish_id = cursor.lastrowid
            
            # 2. Обрабатываем ингредиенты
            for ingredient_name in dish.ingredients:
                # Добавляем ингредиент если его нет
                cursor.execute(
                    "INSERT OR IGNORE INTO ingredients (name) VALUES (?)",
                    (ingredient_name.lower(),)
                )
                
                # Получаем ID ингредиента
                ingredient_row = cursor.execute(
                    "SELECT id FROM ingredients WHERE name = ?",
                    (ingredient_name.lower(),)
                ).fetchone()
                
                if not ingredient_row:
                    db.rollback()
                    raise HTTPException(status_code=400, detail=f"Ingredient {ingredient_name} not found after insert")
                
                ingredient_id = ingredient_row['id']
                
                # Связываем с блюдом
                cursor.execute(
                    "INSERT INTO dish_ingredients (dish_id, ingredient_id) VALUES (?, ?)",
                    (dish_id, ingredient_id)
                )
            
            # 3. Обрабатываем теги
            for tag_name in dish.tags:
                # Добавляем тег если его нет
                cursor.execute(
                    "INSERT OR IGNORE INTO tags (name) VALUES (?)",
                    (tag_name.lower(),)
                )
                
                # Получаем ID тега
                tag_row = cursor.execute(
                    "SELECT id FROM tags WHERE name = ?",
                    (tag_name.lower(),)
                ).fetchone()
                
                if not tag_row:
                    db.rollback()
                    raise HTTPException(status_code=400, detail=f"Tag {tag_name} not found after insert")
                
                tag_id = tag_row['id']
                
                # Связываем с блюдом
                cursor.execute(
                    "INSERT INTO dish_tags (dish_id, tag_id) VALUES (?, ?)",
                    (dish_id, tag_id)
                )
            
            db.commit()
            return {"status": "success", "dish_id": dish_id}
    
    except sqlite3.Error as e:
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))