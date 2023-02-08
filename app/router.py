from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse

from app.envconfig import BASE_URL
from app.models import (
    DishModel,
    MenuModel,
    ResponseDishModel,
    ResponseMenuModel,
    ResponseSubmenuModel,
    SubmenuModel,
    UpdateDishModel,
    UpdateMenuModel,
    UpdateSubmenuModel,
)
from app.service import (
    DishService,
    FileReportService,
    MenuService,
    SubmenuService,
    get_dish_service,
    get_menu_service,
    get_report_service,
    get_submenu_service,
)

router = APIRouter()


@router.post(
    "/",
    response_model=ResponseMenuModel,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new menu",
    tags=["menu"],
)
async def add_menu(
    menu: MenuModel,
    service: MenuService = Depends(get_menu_service),
) -> ResponseMenuModel:
    menu = await service.add_menu(menu.dict())
    return menu


@router.get(
    "/{menu_id}",
    response_model=ResponseMenuModel,
    status_code=status.HTTP_200_OK,
    summary="Get a certain menu",
    tags=["menu"],
)
async def get_menu(
    menu_id: int,
    service: MenuService = Depends(get_menu_service),
) -> ResponseMenuModel:
    menu = await service.get_menu(menu_id)
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="menu not found"
        )
    return menu


@router.get(
    "/",
    response_model=list[ResponseMenuModel],
    status_code=status.HTTP_200_OK,
    summary="Get a list of all menus",
    tags=["menu"],
)
async def get_menu_list(
    service: MenuService = Depends(get_menu_service),
) -> list[ResponseMenuModel]:
    menu_list = await service.get_menu_list()
    return menu_list


@router.patch(
    "/{menu_id}",
    response_model=ResponseMenuModel,
    status_code=status.HTTP_200_OK,
    summary="Edit a menu",
    tags=["menu"],
)
async def update_menu(
    menu_id: int,
    menu: UpdateMenuModel,
    service: MenuService = Depends(get_menu_service),
) -> ResponseMenuModel:
    menu = await service.update_menu(menu_id, menu.dict())
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="menu not found"
        )
    return menu


@router.delete(
    "/{menu_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a menu",
    tags=["menu"],
)
async def delete_menu(
    menu_id: int,
    service: MenuService = Depends(get_menu_service),
) -> dict:
    response = await service.delete_menu(menu_id)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="menu not found"
        )
    return {"status": True, "message": "The menu has been deleted"}


@router.post(
    "/{menu_id}/submenus",
    response_model=ResponseSubmenuModel,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new submenu",
    tags=["submenu"],
)
async def add_submenu(
    menu_id: int,
    submenu: SubmenuModel,
    service: SubmenuService = Depends(get_submenu_service),
) -> ResponseSubmenuModel:
    submenu = await service.add_submenu(menu_id, submenu.dict())
    if not submenu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="menu not found"
        )
    return submenu


@router.get(
    "/{menu_id}/submenus/{submenu_id}",
    response_model=ResponseSubmenuModel,
    status_code=status.HTTP_200_OK,
    summary="Get a certain submenu",
    tags=["submenu"],
)
async def get_submenu(
    menu_id: int,
    submenu_id: int,
    service: SubmenuService = Depends(get_submenu_service),
) -> ResponseMenuModel:
    submenu = await service.get_submenu(menu_id, submenu_id)
    if not submenu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found"
        )
    return submenu


@router.get(
    "/{menu_id}/submenus",
    response_model=list[ResponseSubmenuModel],
    status_code=status.HTTP_200_OK,
    summary="Get a list of all submenus within a certain menu",
    tags=["submenu"],
)
async def get_submenu_list(
    menu_id: int,
    service: SubmenuService = Depends(get_submenu_service),
) -> list[ResponseSubmenuModel]:
    submenu_list = await service.get_submenu_list(menu_id)
    return submenu_list


@router.patch(
    "/{menu_id}/submenus/{submenu_id}",
    response_model=ResponseSubmenuModel,
    status_code=status.HTTP_200_OK,
    summary="Edit a submenu",
    tags=["submenu"],
)
async def update_submenu(
    menu_id: int,
    submenu_id: int,
    submenu: UpdateSubmenuModel,
    service: SubmenuService = Depends(get_submenu_service),
) -> ResponseSubmenuModel:
    submenu = await service.update_submenu(menu_id, submenu_id, submenu.dict())
    if not submenu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found"
        )
    return submenu


@router.delete(
    "/{menu_id}/submenus/{submenu_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a submenu",
    tags=["submenu"],
)
async def delete_submenu(
    menu_id: int,
    submenu_id: int,
    service: SubmenuService = Depends(get_submenu_service),
) -> dict:
    response = await service.delete_submenu(menu_id, submenu_id)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found"
        )
    return {"status": True, "message": "The submenu has been deleted"}


@router.post(
    "/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=ResponseDishModel,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new dish",
    tags=["dish"],
)
async def add_dish(
    menu_id: int,
    submenu_id: int,
    dish: DishModel,
    service: DishService = Depends(get_dish_service),
) -> ResponseDishModel:
    dish = await service.add_dish(menu_id, submenu_id, dish.dict())
    if not dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found"
        )
    return dish


@router.get(
    "/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=ResponseDishModel,
    status_code=status.HTTP_200_OK,
    summary="Get a certain dish",
    tags=["dish"],
)
async def get_dish(
    menu_id: int,
    submenu_id: int,
    dish_id: int,
    service: DishService = Depends(get_dish_service),
) -> ResponseDishModel:
    dish = await service.get_dish(menu_id, submenu_id, dish_id)
    if not dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="dish not found"
        )
    return dish


@router.get(
    "/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=list[ResponseDishModel],
    status_code=status.HTTP_200_OK,
    summary="Get a list of all dishes with a certain submenu",
    tags=["dish"],
)
async def get_dish_list(
    menu_id: int,
    submenu_id: int,
    service: DishService = Depends(get_dish_service),
) -> list[ResponseDishModel]:
    dish_list = await service.get_dish_list(menu_id, submenu_id)
    return dish_list


@router.patch(
    "/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=ResponseDishModel,
    status_code=status.HTTP_200_OK,
    summary="Edit a dish",
    tags=["dish"],
)
async def update_dish(
    menu_id: int,
    submenu_id: int,
    dish_id: int,
    dish: UpdateDishModel,
    service: DishService = Depends(get_dish_service),
) -> ResponseDishModel:
    dish = await service.update_dish(menu_id, submenu_id, dish_id, dish.dict())
    if not dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="dish not found"
        )
    return dish


@router.delete(
    "/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a dish",
    tags=["dish"],
)
async def delete_dish(
    menu_id: int,
    submenu_id: int,
    dish_id: int,
    service: DishService = Depends(get_dish_service),
) -> dict:
    response = await service.delete_dish(menu_id, submenu_id, dish_id)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="dish not found"
        )
    return {"status": True, "message": "The dish has been deleted"}


@router.post(
    path="/populate-db",
    status_code=status.HTTP_200_OK,
    summary="Read json file with test menu structure and populate the database",
    tags=["Excel"],
)
async def read_and_populate(service: FileReportService = Depends(get_report_service)):
    await service.read_and_populate()
    return {"status": True, "message": "The database has been populated"}


@router.post(
    "/make-excel-file",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Send a request to make Excel file with all menus",
    tags=["Excel"],
)
async def make_xlsx_file(service: FileReportService = Depends(get_report_service)):
    task_id = await service.make_xlsx_file()
    return {"status": True, "message": f"Task has been created with task_id {task_id}"}


@router.get(
    "/get-task-status/{task_id}",
    status_code=status.HTTP_200_OK,
    summary="Display a status of the task and the link for to download the file",
    tags=["Excel"],
)
async def get_xlsx_status(
    task_id: str, service: FileReportService = Depends(get_report_service)
):
    result = await service.get_xlsx_file_status(task_id)
    if result.ready():
        filename = result.result["file_name"]
        return {
            "status": True,
            "message": f"Excel file is ready. You can download it here: "
            f"{BASE_URL}/api/v1/menus/download/{filename}",
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )


@router.get(
    path="/download/{filename}",
    status_code=status.HTTP_200_OK,
    summary="Download file by filename",
    response_class=FileResponse,
    tags=["Excel"],
)
async def download_file(
    filename: str, service: FileReportService = Depends(get_report_service)
):
    response = await service.download_file(filename)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )
    return response
