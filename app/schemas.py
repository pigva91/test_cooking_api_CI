from typing import List

from pydantic import BaseModel, Field


class RecipeCreate(BaseModel):
    title: str = Field(description="Название блюда")
    cooking_time: int = Field(description="Время приготовления в минутах")
    ingredients: List[str] = Field(description="Список ингредиентов")
    description: str = Field(description="Пошаговое описание или комментарий")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Паста карбонара",
                    "cooking_time": 20,
                    "ingredients": [
                        "Спагетти",
                        "Бекон",
                        "Яйца",
                        "Сыр",
                        "Масло",
                        "Чеснок",
                        "Соль",
                        "Перец",
                    ],
                    "description": "Классический итальянский рецепт пасты "
                    "карбонара ...",
                }
            ]
        }
    }


class RecipeInList(BaseModel):
    id: int
    title: str
    views: int
    cooking_time: int

    model_config = {"from_attributes": True}


class RecipeDetail(BaseModel):
    id: int
    title: str
    cooking_time: int
    ingredients: List[str]
    description: str
    views: int

    model_config = {"from_attributes": True}
