from typing import List
from sqlalchemy import create_engine, func, distinct
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from app.config import DB_CONN_STRING
from app.db_models import Menu, Submenu, Dish
from app.db_models import Base

engine = create_engine(DB_CONN_STRING, echo=True)
Sessions = sessionmaker(bind=engine, autocommit=False, autoflush=False)
engine = create_engine(DB_CONN_STRING, echo=True)
Sessions = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Database:
    def __init__(self, session):
        self.session = session

    def add_menu(self, menu: dict) -> Menu:
        menu = Menu(**menu)
        self.session.add(menu)
        self.session.commit()
        self.session.refresh(menu)
        return menu

    def get_menu(self, menu_id: int) -> Menu:
        session = self.session
        menu = session.query(
            Menu, func.count(distinct(Submenu.id)), func.count(Dish.id),
        )\
            .join(Submenu, Menu.id == Submenu.menu_id, isouter=True)\
            .join(Dish, Submenu.id == Dish.submenu_id, isouter=True)\
            .filter(Menu.id == menu_id).group_by(Menu.id).first()

        return menu

    def get_menu_list(self) -> List[Menu]:
        session = self.session
        menus = session.query(
            Menu, func.count(distinct(Submenu.id)), func.count(Dish.id),
        ).join(
            Submenu, Menu.id == Submenu.menu_id, isouter=True,
        ).join(
            Dish, Submenu.id == Dish.submenu_id, isouter=True,
        ).group_by(Menu.id).all()
        return menus

    def update_menu(self, menu_id: int, menu: dict) -> Menu:
        session = self.session
        menu_t = self.get_menu(menu_id)
        if menu_t is not None:
            menu_ = menu_t[0]
            menu_.title = menu["title"] if menu["title"] \
                else menu_.title
            menu_.description = menu["description"] if menu["description"] \
                else menu_.description
            session.add(menu_)
            session.commit()
            session.refresh(menu_)
            return menu_

    def delete_menu(self, menu_id: int):
        session = self.session
        menu_t = self.get_menu(menu_id)
        if menu_t is not None:
            menu = menu_t[0]
            session.delete(menu)
            session.commit()
            return True

    def add_submenu(self, menu_id: int, submenu: dict):
        session = self.session
        menu_t = self.get_menu(menu_id)
        if menu_t is not None:
            menu = menu_t[0]
            submenu = Submenu(**submenu)
            menu.submenu.append(submenu)
            session.commit()
            session.refresh(submenu)
            return submenu

    def get_submenu(self, menu_id: int, submenu_id: int):
        submenu = self.session.query(
            Submenu, func.count(Dish.id),
        ).join(
            Dish, Dish.submenu_id == Submenu.id, isouter=True,
        ).filter(
            Submenu.menu_id == menu_id, Submenu.id == submenu_id,
        ).group_by(Submenu.id).first()
        return submenu

    def get_submenu_list(self, menu_id: int):
        session = self.session
        submenu_list = session.query(
            Submenu, func.count(Dish.id),
        ).join(
            Dish, Dish.submenu_id == Submenu.id, isouter=True,
        ).filter(
            Submenu.menu_id == menu_id,
        ).group_by(Submenu.id).all()
        return submenu_list

    def update_submenu(self, menu_id, submenu_id, submenu: dict):
        session = self.session
        submenu_t = self.get_submenu(menu_id, submenu_id)
        if submenu_t is not None:
            submenu_ = submenu_t[0]
            submenu_.title = submenu["title"] \
                if submenu["title"] else submenu_.title
            submenu_.description = submenu["description"] \
                if submenu["description"] else submenu_.description
            session.add(submenu_)
            session.commit()
            session.refresh(submenu_)
            return submenu_

    def delete_submenu(self, menu_id, submenu_id):
        session = self.session
        submenu_t = self.get_submenu(menu_id, submenu_id)
        if submenu_t is not None:
            submenu = submenu_t[0]
            session.delete(submenu)
            session.commit()
            return True

    def add_dish(self, menu_id: int, submenu_id: int, dish: dict):
        session = self.session
        submenu_t = self.get_submenu(menu_id, submenu_id)
        if submenu_t is not None:
            submenu = submenu_t[0]
            dish = Dish(**dish, submenu_id=submenu_id)
            submenu.dish.append(dish)
            session.commit()
            session.refresh(dish)
            return dish

    def get_dish(self, menu_id: int, submenu_id: int, dish_id: int):
        dish = self.session.query(Dish).join(
            Submenu, Submenu.id == Dish.submenu_id,
        ).filter(
            Dish.id == dish_id,
            Submenu.id == submenu_id,
            Submenu.menu_id == menu_id,
        ).first()
        return dish

    def get_dish_list(self, menu_id: int, submenu_id: int):
        dish_list = self.session.query(Dish).join(
            Submenu, Submenu.id == Dish.submenu_id,
        ).filter(
            Submenu.id == submenu_id,
            Submenu.menu_id == menu_id,
        ).all()
        return dish_list

    def update_dish(
        self, menu_id: int, submenu_id: int,
        dish_id: int, dish: dict,
    ):
        session = self.session
        dish_ = self.get_dish(menu_id, submenu_id, dish_id)
        if dish_ is not None:
            dish_.title = dish["title"] \
                if dish["title"] else dish_.title
            dish_.description = dish["description"] \
                if dish["description"] else dish_.description
            dish_.price = dish["price"] \
                if dish["price"] else dish_.price
            session.add(dish_)
            session.commit()
            session.refresh(dish_)
            return dish_

    def delete_dish(self, menu_id: int, submenu_id: int, dish_id: int):
        session = self.session
        dish = self.get_dish(menu_id, submenu_id, dish_id)
        if dish is not None:
            session.delete(dish)
            session.commit()
            return True


def get_session():
    session = Sessions()
    try:
        yield session
    finally:
        session.close()


def create_tables():
    return Base.metadata.create_all(engine)


def delete_tables():
    return Base.metadata.drop_all(engine)


def clean_tables():
    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE menu CASCADE;"))
        conn.commit()
