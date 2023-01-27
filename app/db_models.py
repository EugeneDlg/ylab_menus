from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, func, distinct

from app.db_utils import Session
from app.models import MenuModel



Base = declarative_base()


class Menu(Base):
    __tablename__ = 'menu'
    id = Column(Integer(), primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(200), nullable=False)
    submenu = relationship('Submenu', back_populates="menu", cascade="all, delete")


class Submenu(Base):
    __tablename__ = 'submenu'
    id = Column(Integer(), primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(200), nullable=False)
    menu_id = Column(Integer, ForeignKey('menu.id'))
    menu = relationship('Menu',  back_populates="submenu")
    dish = relationship('Dish', back_populates="submenu", cascade="all, delete")


class Dish(Base):
    __tablename__ = 'dish'
    id = Column(Integer(), primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(200), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    submenu_id = Column(Integer(), ForeignKey('submenu.id'))
    submenu = relationship('Submenu', back_populates="dish")


class MenuDB:
    def __init__(self, session: Session):
        self.session = session

    def create_menu(self, menu: dict) -> Menu:
        menu = Menu(**menu.dict())
        self.session.add(menu)
        self.session.commit()
        self.session.refresh(menu)
        return menu

    def get_menu_item(self, menu_id: int) -> Menu:
        session = self.session
        menu = session.query(Menu, func.count(distinct(Submenu.id)), func.count(Dish.id)
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
