from pydantic import BaseModel
from typing import Optional


class BaseRestaurantModel(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class ResponseBaseRestaurantModel(BaseRestaurantModel):
    id: str


class ResponseMenuModel(ResponseBaseRestaurantModel):
    submenus_count: int = 0
    dishes_count: int = 0


class ResponseSubmenuModel(ResponseBaseRestaurantModel):
    dishes_count: int = 0


class ResponseDishModel(ResponseBaseRestaurantModel):
    price: str


class MenuModel(BaseRestaurantModel):
    pass


class SubmenuModel(BaseRestaurantModel):
    pass


class DishModel(BaseRestaurantModel):
    price: float


class UpdateRestaurantModel(BaseModel):
    title: Optional[str]
    description: Optional[str]

    class Config:
        orm_mode = True


class UpdateMenuModel(UpdateRestaurantModel):
    pass


class UpdateSubmenuModel(UpdateRestaurantModel):
    pass


class UpdateDishModel(UpdateRestaurantModel):
    price: Optional[float]

