from fastapi import Depends

from app.cache import delete_cache, get_cache, set_cache
from app.db import Database, get_session


class Service:
    def __init__(self, session):
        self.session = session

    def add_menu(self, menu: dict):
        menu = Database(self.session).add_menu(menu)
        delete_cache("list::")
        return menu

    def get_menu(self, menu_id: int):
        menu = get_cache(f"{menu_id}::")
        if menu is None:
            menu_t = Database(self.session).get_menu(menu_id)
            if menu_t is not None:
                menu = add_counts_to_menu(menu_t)
                set_cache(f"{menu_id}::", menu)
        return menu

    def get_menu_list(self):
        menu_list = get_cache("list::")
        if menu_list is None:
            menu_list = Database(self.session).get_menu_list()
            menus_with_counts = []
            for e in menu_list:
                menus_with_counts.append(add_counts_to_menu(e))
            menu_list = menus_with_counts
            set_cache("list::", menu_list)
        return menu_list

    def update_menu(self, menu_id: int, menu: dict):
        menu = Database(self.session).update_menu(menu_id, menu)
        delete_cache("list::")
        delete_cache(f"{menu_id}::")
        return menu

    def delete_menu(self, menu_id: int):
        response = Database(self.session).delete_menu(menu_id)
        delete_cache("list::")
        # delete_cache(f"{menu_id}::")
        delete_cache(f"{menu_id}:", True)
        return response

    def add_submenu(self, menu_id: int, submenu: dict):
        menu = Database(self.session).add_submenu(menu_id, submenu)
        delete_cache("list::")
        delete_cache(f"{menu_id}::")
        delete_cache(f"{menu_id}:list:")
        return menu

    def get_submenu(self, menu_id: int, submenu_id: int):
        submenu = get_cache(f"{menu_id}:{submenu_id}:")
        if submenu is None:
            submenu_t = Database(self.session).get_submenu(menu_id, submenu_id)
            if submenu_t is not None:
                submenu = add_counts_to_submenu(submenu_t)
                set_cache(f"{menu_id}:{submenu_id}:", submenu)
        return submenu

    def get_submenu_list(self, menu_id: int):
        submenu_list = get_cache(f"{menu_id}:list:")
        if submenu_list is None:
            submenu_list = Database(self.session).get_submenu_list(menu_id)
            submenus_with_counts = []
            for e in submenu_list:
                submenus_with_counts.append(add_counts_to_submenu(e))
            submenu_list = submenus_with_counts
            set_cache(f"{menu_id}:list:", submenu_list)
        return submenu_list

    def update_submenu(self, menu_id: int, submenu_id: int, submenu: dict):
        submenu = Database(self.session).update_submenu(menu_id, submenu_id, submenu)
        # delete_cache(f"list::")
        delete_cache(f"{menu_id}:list:")
        delete_cache(f"{menu_id}:{submenu_id}:")
        return submenu

    def delete_submenu(self, menu_id: int, submenu_id: int):
        response = Database(self.session).delete_submenu(menu_id, submenu_id)
        delete_cache(f"{menu_id}::")
        delete_cache("list::")
        delete_cache(f"{menu_id}:{submenu_id}:", True)
        delete_cache(f"{menu_id}:list:")
        return response

    def add_dish(self, menu_id: int, submenu_id: int, dish: dict):
        dish = Database(self.session).add_dish(menu_id, submenu_id, dish)
        delete_cache("list::")
        delete_cache(f"{menu_id}::")
        delete_cache(f"{menu_id}:list:")
        delete_cache(f"{menu_id}:{submenu_id}:")
        delete_cache(f"{menu_id}:{submenu_id}:list")
        return dish

    def get_dish(self, menu_id: int, submenu_id: int, dish_id: int):
        dish = get_cache(f"{menu_id}:{submenu_id}:{dish_id}")
        if dish is None:
            dish = Database(self.session).get_dish(menu_id, submenu_id, dish_id)
            set_cache(f"{menu_id}:{submenu_id}:{dish_id}", dish)
        return dish

    def get_dish_list(self, menu_id, submenu_id):
        dish_list = get_cache(f"{menu_id}:{submenu_id}:list")
        if dish_list is None:
            dish_list = Database(self.session).get_dish_list(menu_id, submenu_id)
            set_cache(f"{menu_id}:{submenu_id}:list:", dish_list)
        return dish_list

    def update_dish(self, menu_id: int, submenu_id, dish_id: int, dish: dict):
        dish = Database(self.session).update_dish(menu_id, submenu_id, dish_id, dish)
        # delete_cache(f"list::")
        # delete_cache(f"{menu_id}:list:")
        delete_cache(f"{menu_id}:{submenu_id}:list")
        delete_cache(f"{menu_id}:{submenu_id}:{dish_id}")
        return dish

    def delete_dish(self, menu_id: int, submenu_id, dish_id: int):
        response = Database(self.session).delete_dish(menu_id, submenu_id, dish_id)
        delete_cache(f"{menu_id}::")
        delete_cache("list::")
        delete_cache(f"{menu_id}:{submenu_id}:")
        delete_cache(f"{menu_id}:list:")
        delete_cache(f"{menu_id}:{submenu_id}:{dish_id}")
        delete_cache(f"{menu_id}:{submenu_id}:list")
        return response


def get_service(session: Database = Depends(get_session)):
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
