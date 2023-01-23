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
    delete_tables, get_menu_item,
    get_submenu_item, get_dish_item
)
from app.db_models import Menu, Submenu, Dish


app = FastAPI()


def get_session():
    session = Sessions()
    try:
        yield session
    finally:
        session.close()


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


@app.post("/api/v1/menus",
          response_model=ResponseMenuModel,
          status_code=status.HTTP_201_CREATED)
def add_menu(menu: MenuModel, db: Session = Depends(get_session)):
    menu = Menu(**menu.dict())
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu


@app.get("/api/v1/menus/{menu_id}",
         response_model=ResponseMenuModel,
         status_code=status.HTTP_200_OK)
def get_menu(menu_id: int, db: Session = Depends(get_session)):
    menu_t = get_menu_item(menu_id, db)
    if is_found(menu_t, "menu"):
        return add_counts_to_menu(menu_t)


@app.get("/api/v1/menus",
         response_model=List[ResponseMenuModel],
         status_code=status.HTTP_200_OK)
def get_menus(db: Session = Depends(get_session)):
    menus = db.query(Menu, func.count(distinct(Submenu.id)), func.count(Dish.id)
                     ).join(Submenu, Menu.id == Submenu.menu_id, isouter=True
                            ).join(Dish, Submenu.id == Dish.submenu_id, isouter=True
                                   ).group_by(Menu.id).all()
    if is_found(menus, "menu"):
        menus_with_counts = []
        for e in menus:
            menus_with_counts.append(add_counts_to_menu(e))
        return menus_with_counts


@app.patch("/api/v1/menus/{menu_id}",
           response_model=ResponseMenuModel,
           status_code=status.HTTP_200_OK)
def update_menu(menu_id: int, menu: UpdateMenuModel,
                db: Session = Depends(get_session)):
    menu_t = get_menu_item(menu_id, db)
    if is_found(menu_t, "menu"):
        menu_ = menu_t[0]
        menu_.title = menu.title if menu.title else menu_.title
        menu_.description = menu.description if menu.description else menu_.description
        db.add(menu_)
        db.commit()
        db.refresh(menu_)
        return menu_


@app.delete("/api/v1/menus/{menu_id}",
            status_code=status.HTTP_200_OK)
def delete_menu(menu_id: int, db: Session = Depends(get_session)):
    menu_t = get_menu_item(menu_id, db)
    if is_found(menu_t, "menu"):
        menu = menu_t[0]
        db.delete(menu)
        db.commit()
        return {"status": True, "message": "The menu has been deleted"}


@app.post("/api/v1/menus/{menu_id}/submenus",
          response_model=ResponseSubmenuModel,
          status_code=status.HTTP_201_CREATED)
def add_submenu(menu_id: int, submenu: SubmenuModel, db: Session = Depends(get_session)):
    menu_t = get_menu_item(menu_id, db)
    if is_found(menu_t, "menu"):
        menu = menu_t[0]
        submenu = Submenu(**submenu.dict())
        menu.submenu.append(submenu)
        db.commit()
        db.refresh(submenu)
        return submenu


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}",
         response_model=ResponseSubmenuModel,
         status_code=status.HTTP_200_OK)
def get_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_session)):
    submenu_t = get_submenu_item(menu_id, submenu_id, db)
    if is_found(submenu_t, "submenu"):
        return add_counts_to_submenu(submenu_t)


@app.get("/api/v1/menus/{menu_id}/submenus",
         response_model=List[ResponseSubmenuModel],
         status_code=status.HTTP_200_OK)
def get_submenus(menu_id: int, db: Session = Depends(get_session)):
    submenus = db.query(Submenu, func.count(Dish.id)
                        ).join(Dish, Dish.submenu_id == Submenu.id, isouter=True
                               ).filter(Submenu.menu_id == menu_id
                                        ).group_by(Submenu.id).all()
    if is_found(submenus, "submenu"):
        submenus_with_counts = []
        for e in submenus:
            submenus_with_counts.append(add_counts_to_submenu(e))
        return submenus_with_counts


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}",
           response_model=ResponseSubmenuModel,
           status_code=status.HTTP_200_OK)
def update_submenu(menu_id: int, submenu_id: int,
                   submenu: UpdateSubmenuModel,
                   db: Session = Depends(get_session)):
    submenu_t = get_submenu_item(menu_id, submenu_id, db)
    if is_found(submenu_t, "submenu"):
        submenu_ = submenu_t[0]
        submenu_.title = submenu.title if submenu.title else submenu_.title
        submenu_.description = submenu.description if submenu.description else submenu_.description
        db.add(submenu_)
        db.commit()
        db.refresh(submenu_)
        return submenu_


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}",
            status_code=status.HTTP_200_OK)
def delete_submenu(menu_id: int, submenu_id: int,
                   db: Session = Depends(get_session)):
    submenu_t = get_submenu_item(menu_id, submenu_id, db)
    if is_found(submenu_t, "submenu"):
        submenu = submenu_t[0]
        db.delete(submenu)
        db.commit()
        return {"status": True, "message": "The submenu has been deleted"}


@app.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
          response_model=ResponseDishModel,
          status_code=status.HTTP_201_CREATED)
def add_dish(menu_id: int, submenu_id: int,
             dish: DishModel, db: Session = Depends(get_session)):
    submenu_t = get_submenu_item(menu_id, submenu_id, db)
    if is_found(submenu_t, "submenu"):
        submenu = submenu_t[0]
        dish = Dish(**dish.dict(), submenu_id=submenu_id)
        submenu.dish.append(dish)
        db.commit()
        db.refresh(dish)
        return dish


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
         response_model=ResponseDishModel,
         status_code=status.HTTP_200_OK)
def get_dish(menu_id: int, submenu_id: int,
             dish_id: int, db: Session = Depends(get_session)):
    dish = get_dish_item(menu_id, submenu_id, dish_id, db)
    if is_found(dish, "dish"):
        return dish


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
         response_model=List[ResponseDishModel],
         status_code=status.HTTP_200_OK)
def get_dishes(menu_id: int, submenu_id: int,
               db: Session = Depends(get_session)):
    dishes = db.query(Dish).join(Submenu, Submenu.id == Dish.submenu_id
                                 ).filter(Submenu.id == submenu_id,
                                          Submenu.menu_id == menu_id).all()
    if is_found(dishes, "dish"):
        return dishes


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
           response_model=ResponseDishModel,
           status_code=status.HTTP_200_OK)
def update_dish(menu_id: int, submenu_id: int, dish_id: int,
                dish: UpdateDishModel, db: Session = Depends(get_session)):
    dish_ = get_dish_item(menu_id, submenu_id, dish_id, db)
    if is_found(dish, "dish"):
        dish_.title = dish.title if dish.title else dish_.title
        dish_.description = dish.description if dish.description else dish_.description
        dish_.price = dish.price if dish.price else dish_.price
        db.add(dish_)
        db.commit()
        db.refresh(dish_)
        return dish_


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
            status_code=status.HTTP_200_OK)
def delete_dish(menu_id: int, submenu_id: int,
                dish_id: int, db: Session = Depends(get_session)):
    dish = get_dish_item(menu_id, submenu_id, dish_id, db)
    if is_found(dish, "dish"):
        db.delete(dish)
        db.commit()
        return {"status": True, "message": "The dish has been deleted"}


def is_found(item, name):
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{name} not found")
    else:
        return True


def add_counts_to_menu(menu_t: tuple):
    menu = menu_t[0]
    menu.submenus_count = menu_t[1]
    menu.dishes_count = menu_t[2]
    return menu


def add_counts_to_submenu(submenu_t: tuple):
    submenu = submenu_t[0]
    submenu.dishes_count = submenu_t[1]
    return submenu


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0")
