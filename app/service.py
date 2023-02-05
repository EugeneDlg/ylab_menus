from fastapi import Depends

from app.cache import delete_cache, get_cache, set_cache
from app.db import Database, get_session


class Service:
    def __init__(self, session):
        self.session = session

    async def add_menu(self, menu: dict):
        menu = await Database(self.session).add_menu(menu)
        await delete_cache("list::")
        return menu

    async def get_menu(self, menu_id: int):
        menu = await get_cache(f"{menu_id}::")
        if menu is None:
            menu_t = await Database(self.session).get_menu(menu_id)
            if menu_t is not None:
                menu = add_counts_to_menu(menu_t)
                await set_cache(f"{menu_id}::", menu)
        return menu

    async def get_menu_list(self):
        menu_list = await get_cache("list::")
        if menu_list is None:
            menu_list = await Database(self.session).get_menu_list()
            menus_with_counts = []
            for e in menu_list:
                menus_with_counts.append(add_counts_to_menu(e))
            menu_list = menus_with_counts
            await set_cache("list::", menu_list)
        return menu_list

    async def update_menu(self, menu_id: int, menu: dict):
        menu = await Database(self.session).update_menu(menu_id, menu)
        await delete_cache("list::")
        await delete_cache(f"{menu_id}::")
        return menu

    async def delete_menu(self, menu_id: int):
        response = await Database(self.session).delete_menu(menu_id)
        await delete_cache("list::")
        # delete_cache(f"{menu_id}::")
        await delete_cache(f"{menu_id}:", True)
        return response

    async def add_submenu(self, menu_id: int, submenu: dict):
        menu = await Database(self.session).add_submenu(menu_id, submenu)
        await delete_cache("list::")
        await delete_cache(f"{menu_id}::")
        await delete_cache(f"{menu_id}:list:")
        return menu

    async def get_submenu(self, menu_id: int, submenu_id: int):
        submenu = await get_cache(f"{menu_id}:{submenu_id}:")
        if submenu is None:
            submenu_t = await Database(self.session).get_submenu(menu_id, submenu_id)
            if submenu_t is not None:
                submenu = add_counts_to_submenu(submenu_t)
                await set_cache(f"{menu_id}:{submenu_id}:", submenu)
        return submenu

    async def get_submenu_list(self, menu_id: int):
        submenu_list = await get_cache(f"{menu_id}:list:")
        if submenu_list is None:
            submenu_list = await Database(self.session).get_submenu_list(menu_id)
            submenus_with_counts = []
            for e in submenu_list:
                submenus_with_counts.append(add_counts_to_submenu(e))
            submenu_list = submenus_with_counts
            await set_cache(f"{menu_id}:list:", submenu_list)
        return submenu_list

    async def update_submenu(self, menu_id: int, submenu_id: int, submenu: dict):
        submenu = await Database(self.session).update_submenu(menu_id, submenu_id, submenu)
        # delete_cache(f"list::")
        await delete_cache(f"{menu_id}:list:")
        await delete_cache(f"{menu_id}:{submenu_id}:")
        return submenu

    async def delete_submenu(self, menu_id: int, submenu_id: int):
        response = await Database(self.session).delete_submenu(menu_id, submenu_id)
        await delete_cache(f"{menu_id}::")
        await delete_cache("list::")
        await delete_cache(f"{menu_id}:{submenu_id}:", True)
        await delete_cache(f"{menu_id}:list:")
        return response

    async def add_dish(self, menu_id: int, submenu_id: int, dish: dict):
        dish = await Database(self.session).add_dish(menu_id, submenu_id, dish)
        await delete_cache("list::")
        await delete_cache(f"{menu_id}::")
        await delete_cache(f"{menu_id}:list:")
        await delete_cache(f"{menu_id}:{submenu_id}:")
        await delete_cache(f"{menu_id}:{submenu_id}:list")
        return dish

    async def get_dish(self, menu_id: int, submenu_id: int, dish_id: int):
        dish = await get_cache(f"{menu_id}:{submenu_id}:{dish_id}")
        if dish is None:
            dish = await Database(self.session).get_dish(menu_id, submenu_id, dish_id)
            if dish is not None:
                await set_cache(f"{menu_id}:{submenu_id}:{dish_id}", dish)
        return dish

    async def get_dish_list(self, menu_id, submenu_id):
        dish_list = await get_cache(f"{menu_id}:{submenu_id}:list")
        if dish_list is None:
            dish_list = await Database(self.session).get_dish_list(menu_id, submenu_id)
            if dish_list is not None:
                await set_cache(f"{menu_id}:{submenu_id}:list:", dish_list)
        return dish_list

    async def update_dish(self, menu_id: int, submenu_id, dish_id: int, dish: dict):
        dish = await Database(self.session).update_dish(menu_id, submenu_id, dish_id, dish)
        # delete_cache(f"list::")
        # delete_cache(f"{menu_id}:list:")
        await delete_cache(f"{menu_id}:{submenu_id}:list")
        await delete_cache(f"{menu_id}:{submenu_id}:{dish_id}")
        return dish

    async def delete_dish(self, menu_id: int, submenu_id, dish_id: int):
        response = await Database(self.session).delete_dish(menu_id, submenu_id, dish_id)
        await delete_cache(f"{menu_id}::")
        await delete_cache("list::")
        await delete_cache(f"{menu_id}:{submenu_id}:")
        await delete_cache(f"{menu_id}:list:")
        await delete_cache(f"{menu_id}:{submenu_id}:{dish_id}")
        await delete_cache(f"{menu_id}:{submenu_id}:list")
        return response


async def get_service(session: Database = Depends(get_session)):
    return Service(session)


def add_counts_to_menu(menu_t: tuple):
    menu = menu_t[0]
    menu.submenus_count = menu_t[1]
    menu.dishes_count = menu_t[2]
    return menu


def add_counts_to_submenu(submenu_t: tuple):
    submenu = submenu_t[0]
    submenu.dishes_count = submenu_t[1]
    return submenu

    # @staticmethod
    # def to_dict(obj, model):
    #     breakpoint()
    #     dct = {key: getattr(obj, key) if hasattr(obj, key) else 0 for key in model.__fields__.keys()}
    #     breakpoint()
    #     return dct
