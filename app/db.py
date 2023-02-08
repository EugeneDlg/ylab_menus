from collections.abc import AsyncGenerator

from sqlalchemy import distinct, func, select, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.db_models import Base, Dish, Menu, Submenu
from app.envconfig import DB_CONN_STRING

engine = create_async_engine(
    DB_CONN_STRING,
    echo=True,
)

Sessions = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    class_=AsyncSession,
)


async def get_session() -> AsyncGenerator:
    try:
        session: AsyncSession = Sessions()
        yield session
    finally:
        await session.close()


class MenuDB:
    def __init__(self, session):
        self.session = session

    async def add_menu(self, menu: dict) -> Menu:
        menu = Menu(**menu)
        self.session.add(menu)
        await self.session.commit()
        await self.session.refresh(menu)
        return menu

    async def get_menu(self, menu_id: int) -> Menu:
        session = self.session
        menu = await session.execute(
            select(
                Menu,
                func.count(distinct(Submenu.id)),
                func.count(Dish.id),
            )
            .join(Submenu, Menu.id == Submenu.menu_id, isouter=True)
            .join(Dish, Submenu.id == Dish.submenu_id, isouter=True)
            .filter(Menu.id == menu_id)
            .group_by(Menu.id)
        )
        return menu.first()

    async def get_menu_list(self) -> list[Menu]:
        session = self.session
        menus = await session.execute(
            select(Menu, func.count(distinct(Submenu.id)), func.count(Dish.id))
            .join(
                Submenu,
                Menu.id == Submenu.menu_id,
                isouter=True,
            )
            .join(
                Dish,
                Submenu.id == Dish.submenu_id,
                isouter=True,
            )
            .group_by(Menu.id)
        )
        return menus.all()

    async def update_menu(self, menu_id: int, menu: dict) -> Menu:
        session = self.session
        menu_t = await self.get_menu(menu_id)
        if menu_t is not None:
            menu_ = menu_t[0]
            menu_.title = menu["title"] if menu["title"] else menu_.title
            menu_.description = (
                menu["description"] if menu["description"] else menu_.description
            )
            session.add(menu_)
            await session.commit()
            await session.refresh(menu_)
            return menu_

    async def delete_menu(self, menu_id: int) -> bool:
        session = self.session
        menu_t = await self.get_menu(menu_id)
        if menu_t is not None:
            menu = menu_t[0]
            await session.delete(menu)
            await session.commit()
            return True


class SubmenuDB:
    def __init__(self, session):
        self.session = session

    async def add_submenu(self, menu_id: int, submenu: dict):
        session = self.session
        menu_t = await MenuDB(session).get_menu(menu_id)

        if menu_t is not None:
            # menu = menu_t[0]
            submenu = Submenu(**submenu, menu_id=menu_id)
            session.add(submenu)
            # menu.submenu.append(submenu)
            await session.commit()
            await session.refresh(submenu)
            return submenu

    async def get_submenu(self, menu_id: int, submenu_id: int):
        submenu = await self.session.execute(
            select(
                Submenu,
                func.count(Dish.id),
            )
            .join(
                Dish,
                Dish.submenu_id == Submenu.id,
                isouter=True,
            )
            .filter(
                Submenu.menu_id == menu_id,
                Submenu.id == submenu_id,
            )
            .group_by(Submenu.id)
        )
        return submenu.first()

    async def get_submenu_list(self, menu_id: int):
        session = self.session
        submenu_list = await session.execute(
            select(
                Submenu,
                func.count(Dish.id),
            )
            .join(
                Dish,
                Dish.submenu_id == Submenu.id,
                isouter=True,
            )
            .filter(
                Submenu.menu_id == menu_id,
            )
            .group_by(Submenu.id)
        )
        return submenu_list.all()

    async def update_submenu(self, menu_id, submenu_id, submenu: dict):
        session = self.session
        submenu_t = await self.get_submenu(menu_id, submenu_id)
        if submenu_t is not None:
            submenu_ = submenu_t[0]
            submenu_.title = submenu["title"] if submenu["title"] else submenu_.title
            submenu_.description = (
                submenu["description"]
                if submenu["description"]
                else submenu_.description
            )
            session.add(submenu_)
            await session.commit()
            await session.refresh(submenu_)
            return submenu_

    async def delete_submenu(self, menu_id, submenu_id):
        session = self.session
        submenu_t = await self.get_submenu(menu_id, submenu_id)
        if submenu_t is not None:
            submenu = submenu_t[0]
            await session.delete(submenu)
            await session.commit()
            return True


class DishDB:
    def __init__(self, session):
        self.session = session

    async def add_dish(self, menu_id: int, submenu_id: int, dish: dict):
        session = self.session
        submenu_t = await SubmenuDB(session).get_submenu(menu_id, submenu_id)
        if submenu_t is not None:
            # submenu = submenu_t[0]
            dish = Dish(**dish, submenu_id=submenu_id)
            # submenu.dish.append(dish)
            session.add(dish)
            await session.commit()
            await session.refresh(dish)
            return dish

    async def get_dish(self, menu_id: int, submenu_id: int, dish_id: int):
        dish = await self.session.execute(
            select(Dish)
            .join(
                Submenu,
                Submenu.id == Dish.submenu_id,
            )
            .filter(
                Dish.id == dish_id,
                Submenu.id == submenu_id,
                Submenu.menu_id == menu_id,
            )
        )
        return dish.scalar()

    async def get_dish_list(self, menu_id: int, submenu_id: int):
        dish_list = await self.session.execute(
            select(Dish)
            .join(
                Submenu,
                Submenu.id == Dish.submenu_id,
            )
            .filter(
                Submenu.id == submenu_id,
                Submenu.menu_id == menu_id,
            )
        )
        return dish_list.scalars().all()

    async def update_dish(
        self,
        menu_id: int,
        submenu_id: int,
        dish_id: int,
        dish: dict,
    ):
        session = self.session
        dish_ = await self.get_dish(menu_id, submenu_id, dish_id)
        if dish_ is not None:
            dish_.title = dish["title"] if dish["title"] else dish_.title
            dish_.description = (
                dish["description"] if dish["description"] else dish_.description
            )
            dish_.price = dish["price"] if dish["price"] else dish_.price
            session.add(dish_)
            await session.commit()
            await session.refresh(dish_)
            return dish_

    async def delete_dish(self, menu_id: int, submenu_id: int, dish_id: int):
        session = self.session
        dish = await self.get_dish(menu_id, submenu_id, dish_id)
        if dish is not None:
            await session.delete(dish)
            await session.commit()
            return True


class FileReportDB:
    def __init__(self, session):
        self.session = session

    async def create_menu_structure(self, data: list[dict]):
        session = self.session
        for menu_ in data:
            menu_dict = {"title": menu_["title"], "description": menu_["description"]}
            new_menu = await MenuDB(session).add_menu(menu_dict)
            new_menu_id = int(new_menu.id)
            for submenu_ in menu_["submenus"]:
                submenu_dict = {
                    "title": submenu_["title"],
                    "description": submenu_["description"],
                }
                new_submenu = await SubmenuDB(session).add_submenu(
                    new_menu_id, submenu_dict
                )
                new_submenu_id = int(new_submenu.id)
                for dish_ in submenu_["dishes"]:
                    dish_dict = {
                        "title": dish_["title"],
                        "description": dish_["description"],
                        "price": dish_["price"],
                    }
                    await DishDB(session).add_dish(
                        new_menu_id, new_submenu_id, dish_dict
                    )
        return None

    async def get_all_items(self):
        items = await self.session.execute(
            select(Menu, Submenu, Dish)
            .join(
                Submenu,
                Menu.id == Submenu.menu_id,
                isouter=True,
            )
            .join(
                Dish,
                Submenu.id == Dish.submenu_id,
                isouter=True,
            )
        )
        return items.all()


async def create_tables():
    return await Base.metadata.create_all(engine)


async def delete_tables():
    return await Base.metadata.drop_all(engine)


async def clean_tables():
    async with engine.connect() as conn:
        await conn.execute(text("TRUNCATE TABLE menu CASCADE;"))
        await conn.commit()
