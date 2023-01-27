from db_models import MenuDB
from models import MenuModel


class Service:
    model = MenuModel

    def __init__(self, session):
        self.session = session

    def create_menu(self, menu: dict) -> dict:
        menu_db = MenuDB(self.session).create_menu(menu)
        return menu_db

    def get_menu(self, session, menu_id: int) -> dict:
        menu_t = MenuDB.get_menu_item(session, menu_id)
        # if is_found(menu_t, "menu"):
        #     return add_counts_to_menu(menu_t)
        if menu_t is not None:
            return self.to_dict(add_counts_to_menu(menu_t))
        else:
            return None

    def to_dict(self, obj):
        breakpoint()
        print(self.model.dict())

        return {"id": obj.id, "title":obj.title, "description": obj.description, }


def get_service():
    return Service()


def add_counts_to_menu(menu_t: tuple):
    menu = menu_t[0]
    menu.submenus_count = menu_t[1]
    menu.dishes_count = menu_t[2]
    return menu


def add_counts_to_submenu(submenu_t: tuple):
    submenu = submenu_t[0]
    submenu.dishes_count = submenu_t[1]
    return submenu
