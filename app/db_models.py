from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from app.config import DB_CONN_STRING

engine = create_engine(DB_CONN_STRING, echo=True)
Sessions = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


class Menu(Base):
    __tablename__ = 'menu'
    id = Column(Integer(), primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(200), nullable=False)
    submenu = relationship(
        'Submenu',
        back_populates="menu",
        cascade="all, delete"
    )


class Submenu(Base):
    __tablename__ = 'submenu'
    id = Column(Integer(), primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(200), nullable=False)
    menu_id = Column(Integer, ForeignKey('menu.id'))
    menu = relationship('Menu', back_populates="submenu")
    dish = relationship(
        'Dish',
        back_populates="submenu",
        cascade="all, delete"
    )


class Dish(Base):
    __tablename__ = 'dish'
    id = Column(Integer(), primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(200), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    submenu_id = Column(Integer(), ForeignKey('submenu.id'))
    submenu = relationship(
        'Submenu',
        back_populates="dish"
    )
