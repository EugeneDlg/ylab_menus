from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.models import (DishModel, MenuModel, ResponseDishModel,
                        ResponseMenuModel, ResponseSubmenuModel, SubmenuModel,
                        UpdateDishModel, UpdateMenuModel, UpdateSubmenuModel)
from app.service import Service, get_service

router = APIRouter()


@router.post(
    "/",
    response_model=ResponseMenuModel,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new menu",
    tags=["menu"],
)
def add_menu(
        menu: MenuModel,
        service: Service = Depends(get_service),
) -> ResponseMenuModel:
    menu = service.add_menu(menu.dict())
    return menu


@router.get(
    "/{menu_id}",
    response_model=ResponseMenuModel,
    status_code=status.HTTP_200_OK,
    summary="Get a certain menu",
    tags=["menu"],
)
def get_menu(
        menu_id: int,
        service: Service = Depends(get_service),
) -> ResponseMenuModel:
    menu = service.get_menu(menu_id)
    if is_ok(menu, "menu"):
        return menu


@router.get(
    "/",
    response_model=List[ResponseMenuModel],
    status_code=status.HTTP_200_OK,
    summary="Get a list of all menus",
    tags=["menu"],
)
def get_menu_list(
        service: Service = Depends(get_service),
) -> List[ResponseMenuModel]:
    menu_list = service.get_menu_list()
    return menu_list


@router.patch(
    "/{menu_id}",
    response_model=ResponseMenuModel,
    status_code=status.HTTP_200_OK,
    summary="Edit a menu",
    tags=["menu"],
)
def update_menu(
        menu_id: int, menu: UpdateMenuModel,
        service: Service = Depends(get_service),
) -> ResponseMenuModel:
    menu = service.update_menu(menu_id, menu.dict())
    if is_ok(menu, "menu"):
        return menu


@router.delete(
    "/{menu_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a menu",
    tags=["menu"],
)
def delete_menu(
        menu_id: int,
        service: Service = Depends(get_service),
) -> dict:
    response = service.delete_menu(menu_id)
    if is_ok(response, "menu"):
        return {"status": True, "message": "The menu has been deleted"}


@router.post(
    "/{menu_id}/submenus",
    response_model=ResponseSubmenuModel,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new submenu",
    tags=["submenu"],
)
def add_submenu(
        menu_id: int, submenu: SubmenuModel,
        service: Service = Depends(get_service),
) -> ResponseSubmenuModel:
    submenu = service.add_submenu(menu_id, submenu.dict())
    if is_ok(submenu, "menu"):
        return submenu


@router.get(
    "/{menu_id}/submenus/{submenu_id}",
    response_model=ResponseSubmenuModel,
    status_code=status.HTTP_200_OK,
    summary="Get a certain submenu",
    tags=["submenu"],
)
def get_submenu(
        menu_id: int,
        submenu_id: int,
        service: Service = Depends(get_service),
) -> ResponseMenuModel:
    submenu = service.get_submenu(menu_id, submenu_id)
    if is_ok(submenu, "submenu"):
        return submenu


@router.get(
    "/{menu_id}/submenus",
    response_model=List[ResponseSubmenuModel],
    status_code=status.HTTP_200_OK,
    summary="Get a list of all submenus within a certain menu",
    tags=["submenu"],
)
def get_submenu_list(
        menu_id: int,
        service: Service = Depends(get_service),
) -> List[ResponseSubmenuModel]:
    submenu_list = service.get_submenu_list(menu_id)
    return submenu_list


@router.patch(
    "/{menu_id}/submenus/{submenu_id}",
    response_model=ResponseSubmenuModel,
    status_code=status.HTTP_200_OK,
    summary="Edit a submenu",
    tags=["submenu"],
)
def update_submenu(
        menu_id: int,
        submenu_id: int,
        submenu: UpdateSubmenuModel,
        service: Service = Depends(get_service),
) -> ResponseSubmenuModel:
    submenu = service.update_submenu(menu_id, submenu_id, submenu.dict())
    if is_ok(submenu, "submenu"):
        return submenu


@router.delete(
    "/{menu_id}/submenus/{submenu_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a submenu",
    tags=["submenu"],
)
def delete_submenu(
        menu_id: int,
        submenu_id: int,
        service: Service = Depends(get_service),
) -> dict:
    response = service.delete_submenu(menu_id, submenu_id)
    if is_ok(response, "submenu"):
        return {"status": True, "message": "The submenu has been deleted"}


@router.post(
    "/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=ResponseDishModel,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new dish",
    tags=["dish"],
)
def add_dish(
        menu_id: int,
        submenu_id: int,
        dish: DishModel,
        service: Service = Depends(get_service),
) -> ResponseDishModel:
    dish = service.add_dish(menu_id, submenu_id, dish.dict())
    if is_ok(dish, "submenu"):
        return dish


@router.get(
    "/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=ResponseDishModel,
    status_code=status.HTTP_200_OK,
    summary="Get a certain dish",
    tags=["dish"],
)
def get_dish(
        menu_id: int,
        submenu_id: int,
        dish_id: int,
        service: Service = Depends(get_service),
) -> ResponseDishModel:
    dish = service.get_dish(menu_id, submenu_id, dish_id)
    if is_ok(dish, "dish"):
        return dish


@router.get(
    "/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=List[ResponseDishModel],
    status_code=status.HTTP_200_OK,
    summary="Get a list of all dishes with a certain submenu",
    tags=["dish"],
)
def get_dish_list(
        menu_id: int,
        submenu_id: int,
        service: Service = Depends(get_service),
) -> List[ResponseDishModel]:
    dish_list = service.get_dish_list(menu_id, submenu_id)
    return dish_list


@router.patch(
    "/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=ResponseDishModel,
    status_code=status.HTTP_200_OK,
    summary="Edit a dish",
    tags=["dish"],
)
def update_dish(
        menu_id: int,
        submenu_id: int,
        dish_id: int,
        dish: UpdateDishModel,
        service: Service = Depends(get_service),
) -> ResponseDishModel:
    dish = service.update_dish(menu_id, submenu_id, dish_id, dish.dict())
    if is_ok(dish, "dish"):
        return dish


@router.delete(
    "/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a dish",
    tags=["dish"],
)
def delete_dish(
        menu_id: int,
        submenu_id: int,
        dish_id: int,
        service: Service = Depends(get_service),
) -> dict:
    response = service.delete_dish(menu_id, submenu_id, dish_id)
    if is_ok(response, "dish"):
        return {"status": True, "message": "The dish has been deleted"}


def is_ok(item, name):
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{name} not found")
    else:
        return True
