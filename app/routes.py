import json
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .db import get_db
from .models import Recipe
from .schemas import RecipeCreate, RecipeDetail, RecipeInList

router = APIRouter()


@router.get("/recipes", response_model=List[RecipeInList])
async def get_recipes(session: AsyncSession = Depends(get_db)):
    result = await session.execute(
        select(Recipe).order_by(Recipe.views.desc(), Recipe.cooking_time.asc())
    )
    return result.scalars().all()


@router.get("/recipes/{recipe_id}", response_model=RecipeDetail)
async def get_recipe_detail(
    recipe_id: int, session: AsyncSession = Depends(get_db)
):
    recipe = await session.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(404, "Рецепт не найден")
    recipe.views += 1
    await session.commit()

    return {
        "id": recipe.id,
        "title": recipe.title,
        "cooking_time": recipe.cooking_time,
        "ingredients": json.loads(recipe.ingredients),
        "description": recipe.description,
        "views": recipe.views,
    }


@router.post("/recipes", response_model=RecipeInList, status_code=201)
async def create_recipe(
    recipe_data: RecipeCreate, session: AsyncSession = Depends(get_db)
):
    data = recipe_data.model_dump()
    data["ingredients"] = json.dumps(data["ingredients"], ensure_ascii=False)
    new_recipe = Recipe(**data)
    session.add(new_recipe)
    await session.commit()
    await session.refresh(new_recipe)

    return new_recipe
