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
    submenus_count: Optional[int]
    dishes_count: Optional[int]


class ResponseSubmenuModel(ResponseBaseRestaurantModel):
    dishes_count: Optional[int]


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

