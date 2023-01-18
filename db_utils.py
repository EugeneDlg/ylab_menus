import os

from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine, func, distinct
from sqlalchemy.orm import sessionmaker, Session, relationship, backref

from db_models import Base, Menu, Submenu, Dish

load_dotenv(find_dotenv())
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
db_socket = os.getenv("DB_SOCKET")
db_name = os.getenv("DB_NAME")
db_conn_string_pre = "postgresql+psycopg2"
db_conn_string = f"{db_conn_string_pre}://{user}:{password}@{db_socket}/{db_name}"

engine = create_engine(db_conn_string, echo=True)
Sessions = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def create_tables():
    return Base.metadata.create_all(engine)


def delete_tables():
    return Base.metadata.drop_all(engine)


def get_menu_item(menu_id: int, db: Session):
    menu = db.query(Menu, func.count(distinct(Submenu.id)), func.count(Dish.id)
                    ).join(Submenu, Menu.id == Submenu.menu_id, isouter=True
                           ).join(Dish, Submenu.id == Dish.submenu_id, isouter=True
                                  ).filter(Menu.id == menu_id).group_by(Menu.id).first()

    return menu


def get_submenu_item(menu_id: int, submenu_id: int, db: Session):
    submenu = db.query(Submenu, func.count(Dish.id)
                       ).join(Dish, Dish.submenu_id == Submenu.id, isouter=True
                              ).filter(Submenu.menu_id == menu_id, Submenu.id == submenu_id
                                       ).group_by(Submenu.id).first()
    return submenu


def get_dish_item(menu_id: int, submenu_id: int, dish_id: int, db: Session):
    dish = db.query(Dish).join(Submenu, Submenu.id == Dish.submenu_id
                               ).filter(Dish.id == dish_id,
                                        Submenu.id == submenu_id,
                                        Submenu.menu_id == menu_id).first()
    return dish
