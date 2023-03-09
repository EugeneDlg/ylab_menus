from pydantic import BaseModel, validator


def price_format(price: float) -> str:
    return f"{price:.2f}"


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
    price: float

    _normalize_price = validator("price", allow_reuse=True)(price_format)


class MenuModel(BaseRestaurantModel):
    pass


class SubmenuModel(BaseRestaurantModel):
    pass


class DishModel(BaseRestaurantModel):
    price: float

    # _normalize_price = validator(
    #     "price",
    #     allow_reuse=True)(price_format)


class UpdateRestaurantModel(BaseModel):
    title: str | None
    description: str | None

    class Config:
        orm_mode = True


class UpdateMenuModel(UpdateRestaurantModel):
    pass


class UpdateSubmenuModel(UpdateRestaurantModel):
    pass


class UpdateDishModel(UpdateRestaurantModel):
    price: float | None

    # _normalize_price = validator(
    #     "price",
    #     allow_reuse=True)(price_format)
