import json
import os

import aiofiles  # type: ignore
from celery.result import AsyncResult
from fastapi import Depends
from fastapi.responses import FileResponse

from app.cache import get_cache
from app.celery.tasks import celery_app
from app.db import DishDB, FileReportDB, MenuDB, SubmenuDB, get_db_session
from app.envconfig import BASE_DIR


class MenuService:
    def __init__(self, db_session, cache):
        self.db_session = db_session
        self.cache = cache

    async def add_menu(self, menu: dict):
        menu = await MenuDB(self.db_session).add_menu(menu)
        await self.cache.delete_cache("menu_list::")
        return menu

    async def get_menu(self, menu_id: int):
        menu = await self.cache.get_cache(f"menu_{menu_id}::")
        if menu is None:
            menu_t = await MenuDB(self.db_session).get_menu(menu_id)
            if menu_t is not None:
                menu = add_counts_to_menu(menu_t)
                await self.cache.set_cache(f"menu_{menu_id}::", menu)
        return menu

    async def get_menu_list(self):
        menu_list = await self.cache.get_cache("menu_list::")
        if menu_list is None:
            menu_list = await MenuDB(self.db_session).get_menu_list()
            menus_with_counts = []
            for e in menu_list:
                menus_with_counts.append(add_counts_to_menu(e))
            menu_list = menus_with_counts
            await self.cache.set_cache("menu_list::", menu_list)
        return menu_list

    async def update_menu(self, menu_id: int, menu: dict):
        menu = await MenuDB(self.db_session).update_menu(menu_id, menu)
        await self.cache.delete_cache("menu_list::")
        await self.cache.delete_cache(f"menu_{menu_id}::")
        return menu

    async def delete_menu(self, menu_id: int):
        response = await MenuDB(self.db_session).delete_menu(menu_id)
        await self.cache.delete_cache("menu_list::")
        await self.cache.delete_cache(f"menu_{menu_id}:", True)
        return response


class SubmenuService:
    def __init__(self, session, cache):
        self.db_session = session
        self.cache = cache

    async def add_submenu(self, menu_id: int, submenu: dict):
        menu = await SubmenuDB(self.db_session).add_submenu(menu_id, submenu)
        await self.cache.delete_cache("menu_list::")
        await self.cache.delete_cache(f"menu_{menu_id}::")
        await self.cache.delete_cache(f"menu_{menu_id}:submenu_list:")
        return menu

    async def get_submenu(self, menu_id: int, submenu_id: int):
        submenu = await self.cache.get_cache(f"menu_{menu_id}:submenu_{submenu_id}:")
        if submenu is None:
            submenu_t = await SubmenuDB(self.db_session).get_submenu(
                menu_id, submenu_id
            )
            if submenu_t is not None:
                submenu = add_counts_to_submenu(submenu_t)
                await self.cache.set_cache(
                    f"menu_{menu_id}:submenu_{submenu_id}:", submenu
                )
        return submenu

    async def get_submenu_list(self, menu_id: int):
        submenu_list = await self.cache.get_cache(f"menu_{menu_id}:submenu_list:")
        if submenu_list is None:
            submenu_list = await SubmenuDB(self.db_session).get_submenu_list(menu_id)
            submenus_with_counts = []
            for e in submenu_list:
                submenus_with_counts.append(add_counts_to_submenu(e))
            submenu_list = submenus_with_counts
            await self.cache.set_cache(f"menu_{menu_id}:submenu_list:", submenu_list)
        return submenu_list

    async def update_submenu(self, menu_id: int, submenu_id: int, submenu: dict):
        submenu = await SubmenuDB(self.db_session).update_submenu(
            menu_id, submenu_id, submenu
        )
        await self.cache.delete_cache(f"menu_{menu_id}:submenu_list:")
        await self.cache.delete_cache(f"menu_{menu_id}:submenu_{submenu_id}:")
        return submenu

    async def delete_submenu(self, menu_id: int, submenu_id: int):
        response = await SubmenuDB(self.db_session).delete_submenu(menu_id, submenu_id)
        await self.cache.delete_cache(f"menu_{menu_id}::")
        await self.cache.delete_cache("menu_list::")
        await self.cache.delete_cache(f"menu_{menu_id}:submenu_{submenu_id}:", True)
        await self.cache.delete_cache(f"menu_{menu_id}:submenu_list:")
        return response


class DishService:
    def __init__(self, session, cache):
        self.db_session = session
        self.cache = cache

    async def add_dish(self, menu_id: int, submenu_id: int, dish: dict):
        dish = await DishDB(self.db_session).add_dish(menu_id, submenu_id, dish)
        await self.cache.delete_cache("menu_list::")
        await self.cache.delete_cache(f"menu_{menu_id}::")
        await self.cache.delete_cache(f"menu_{menu_id}:submenu_list:")
        await self.cache.delete_cache(f"menu_{menu_id}:submenu_{submenu_id}:")
        await self.cache.delete_cache(f"menu_{menu_id}:submenu_{submenu_id}:dish_list")
        return dish

    async def get_dish(self, menu_id: int, submenu_id: int, dish_id: int):
        dish = await self.cache.get_cache(
            f"menu_{menu_id}:submenu_{submenu_id}:dish_{dish_id}"
        )
        if dish is None:
            dish = await DishDB(self.db_session).get_dish(menu_id, submenu_id, dish_id)
            if dish is not None:
                await self.cache.set_cache(
                    f"menu_{menu_id}:submenu_{submenu_id}:dish_{dish_id}", dish
                )
        return dish

    async def get_dish_list(self, menu_id, submenu_id):
        dish_list = await self.cache.get_cache(
            f"menu_{menu_id}:submenu_{submenu_id}:dish_list"
        )
        if dish_list is None:
            dish_list = await DishDB(self.db_session).get_dish_list(menu_id, submenu_id)
            if dish_list is not None:
                await self.cache.set_cache(
                    f"menu_{menu_id}:submenu_{submenu_id}:dish_list", dish_list
                )
        return dish_list

    async def update_dish(self, menu_id: int, submenu_id, dish_id: int, dish: dict):
        dish = await DishDB(self.db_session).update_dish(
            menu_id, submenu_id, dish_id, dish
        )
        await self.cache.delete_cache(f"menu_{menu_id}:submenu_{submenu_id}:dish_list")
        await self.cache.delete_cache(
            f"menu_{menu_id}:submenu_{submenu_id}:dish_{dish_id}"
        )
        return dish

    async def delete_dish(self, menu_id: int, submenu_id, dish_id: int):
        response = await DishDB(self.db_session).delete_dish(
            menu_id, submenu_id, dish_id
        )
        await self.cache.delete_cache(f"menu_{menu_id}::")
        await self.cache.delete_cache("menu_list::")
        await self.cache.delete_cache(f"menu_{menu_id}:submenu_{submenu_id}:")
        await self.cache.delete_cache(f"menu_{menu_id}:submenu_list:")
        await self.cache.delete_cache(
            f"menu_{menu_id}:submenu_{submenu_id}:dish_{dish_id}"
        )
        await self.cache.delete_cache(f"menu_{menu_id}:submenu_{submenu_id}:dish_list")
        return response


class FileReportService:
    def __init__(self, session):
        self.db_session = session

    async def read_and_populate(self):
        async with aiofiles.open("test_menu.json", mode="r") as f:
            content = await f.read()
        all_structure = json.loads(content)
        await FileReportDB(self.db_session).create_menu_structure(all_structure)

    async def make_xlsx_file(self):
        menu_list = await FileReportDB(self.db_session).get_all_items()
        menu_data = self.serialize(menu_list)
        result = celery_app.send_task(
            "tasks.generate_xlsx_file", kwargs={"menu_data": menu_data}
        )
        return result.id

    @staticmethod
    def serialize(in_data):
        all_menus = []
        for item in in_data:
            if item[0] is None:
                continue
            menu_id = item[0].id
            if len(all_menus) == 0 or all_menus[-1]["id"] != menu_id:
                menu = {
                    "id": item[0].id,
                    "title": item[0].title,
                    "description": item[0].description,
                    "submenus": [],
                }
                all_menus.append(menu)
            if item[1] is None:
                continue
            submenu_id = item[1].id
            submenu_ = all_menus[-1]["submenus"]
            if len(submenu_) == 0 or submenu_[-1]["id"] != submenu_id:
                submenu = {
                    "id": item[1].id,
                    "title": item[1].title,
                    "description": item[1].description,
                    "dishes": [],
                }
                all_menus[-1]["submenus"].append(submenu)
            if item[2] is None:
                continue
            dish = {
                "id": item[2].id,
                "title": item[2].title,
                "description": item[2].description,
                "price": float(item[2].price),
            }
            all_menus[-1]["submenus"][-1]["dishes"].append(dish)
        return all_menus

    @staticmethod
    async def get_xlsx_file_status(task_id: str) -> AsyncResult:
        result = celery_app.AsyncResult(id=task_id, app=celery_app)
        return result

    @staticmethod
    async def download_file(filename: str):
        try:
            os.stat(os.path.join(BASE_DIR, "data", f"{filename}"))
        except FileNotFoundError:
            return False
        headers = {"Content-Disposition": f"attachment; filename={filename}"}
        file_response = FileResponse(
            path=os.path.join(BASE_DIR, "data", f"{filename}"),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers=headers,
        )
        return file_response


async def get_menu_service(
    db_session: MenuDB = Depends(get_db_session), cache=Depends(get_cache)
):
    return MenuService(db_session, cache)


async def get_submenu_service(
    db_session: SubmenuDB = Depends(get_db_session), cache=Depends(get_cache)
):
    return SubmenuService(db_session, cache)


async def get_dish_service(
    db_session: DishDB = Depends(get_db_session), cache=Depends(get_cache)
):
    return DishService(db_session, cache)


async def get_report_service(session: FileReportDB = Depends(get_db_session)):
    return FileReportService(session)


def add_counts_to_menu(menu_t: tuple):
    menu = menu_t[0]
    menu.submenus_count = menu_t[1]
    menu.dishes_count = menu_t[2]
    return menu


def add_counts_to_submenu(submenu_t: tuple):
    submenu = submenu_t[0]
    submenu.dishes_count = submenu_t[1]
    return submenu
