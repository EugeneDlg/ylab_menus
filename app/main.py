from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
import uvicorn
import sys

from app.models import (
    MenuModel, SubmenuModel, DishModel,
    ResponseMenuModel, ResponseSubmenuModel, ResponseDishModel,
    UpdateMenuModel, UpdateSubmenuModel, UpdateDishModel
)
from app.db_utils import (
    Sessions, create_tables, clean_tables,
    delete_tables
)
from app.db_models import Menu, Submenu, Dish
from app.router import router


app = FastAPI()


app.include_router(router=router, prefix='/api/v1')





# @app.on_event("startup")
# def startup():
#     return create_tables()


@app.on_event("shutdown")
def on_shutdown():
    # return delete_tables()
    clean_tables()


@app.get("/")
def homepage():
    return JSONResponse({'message': 'This is a restaurant menu system'})




if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0")
