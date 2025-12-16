from typing import List

from .factories import RecipeCreateFactory


async def create_recipe_via_api(async_client, recipe_data):
    response = await async_client.post(
        "/recipes", json=recipe_data.model_dump()
    )
    assert response.status_code == 201
    return response.json()


async def test_create_recipe_with_factory(async_client):
    recipe_data = RecipeCreateFactory()
    created = await create_recipe_via_api(async_client, recipe_data)

    assert created["id"] > 0
    assert created["title"] == recipe_data.title
    assert created["cooking_time"] == recipe_data.cooking_time
    assert created["views"] == 0


async def test_get_recipes_list_sorting(async_client):
    recipes = []
    for time, title in [
        (45, "Обычный рецепт."),
        (15, "Быстрый рецепт."),
        (90, "Долгий рецепт."),
    ]:
        data = RecipeCreateFactory(title=title, cooking_time=time)
        created = await create_recipe_via_api(async_client, data)
        recipes.append(created)

    quick_id = [r for r in recipes if r["title"] == "Быстрый рецепт."][0]["id"]
    for _ in range(10):
        await async_client.get(f"/recipes/{quick_id}")

    response = await async_client.get("/recipes")
    assert response.status_code == 200
    recipes_list: List[dict] = response.json()

    assert len(recipes_list) == 3
    assert recipes_list[0]["title"] == "Быстрый рецепт."
    assert recipes_list[0]["views"] == 10
    assert recipes_list[1]["cooking_time"] == 45
    assert recipes_list[2]["cooking_time"] == 90


async def test_get_recipe_detail_and_increment_views(async_client):
    recipe_data = RecipeCreateFactory()
    created = await create_recipe_via_api(async_client, recipe_data)

    response = await async_client.get(f"/recipes/{created['id']}")
    assert response.status_code == 200
    detail = response.json()
    assert detail["views"] == 1
    assert detail["title"] == recipe_data.title
    assert detail["ingredients"] == recipe_data.ingredients
    assert detail["description"] == recipe_data.description

    response2 = await async_client.get(f"/recipes/{created['id']}")
    assert response2.json()["views"] == 2
