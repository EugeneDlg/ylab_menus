import os

from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine, func, distinct
from sqlalchemy.orm import sessionmaker, Session, relationship, backref

from db_models import Base, Menu, Submenu, Dish

load_dotenv(".env")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
TEST_DB_HOST = os.getenv("TEST_DB_HOST")
TEST_DB_NAME = os.getenv("TEST_DB_NAME")
TEST_DB_USER = os.getenv("TEST_DB_USER")
TEST_DB_PASSWORD = os.getenv("TEST_DB_PASSWORD")
DB_CONN_STRING_PRE = "postgresql+psycopg2"
DB_CONN_STRING = f"{DB_CONN_STRING_PRE}://{DB_USER}:{DB_PASSWORD}@" \
                 f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
TEST_DB_CONN_STRING = f"{DB_CONN_STRING_PRE}://{TEST_DB_USER}:{TEST_DB_PASSWORD}@" \
                      f"{TEST_DB_HOST}:{DB_PORT}/{TEST_DB_NAME}"

engine = create_engine(DB_CONN_STRING, echo=True)
Sessions = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def create_tables():
    return Base.metadata.create_all(engine)


def delete_tables():
    return Base.metadata.drop_all(engine)


def clean_tables():
    with engine.connect() as conn:
        conn.execute("TRUNCATE TABLE menu CASCADE;")


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
