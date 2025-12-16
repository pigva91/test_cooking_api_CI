from ..app.schemas import RecipeCreate


async def test_create_recipe_fixed(async_client):
    fixed_data = RecipeCreate(
        title="Классическая паста карбонара",
        cooking_time=20,
        ingredients=["Спагетти", "Гуанчиале", "Яйца", "Пекорино", "Перец"],
        description="Настоящий итальянский рецепт без сливок.",
    )
    response = await async_client.post(
        "/recipes", json=fixed_data.model_dump()
    )
    assert response.status_code == 201
    created = response.json()
    assert created["title"] == fixed_data.title
    assert created["cooking_time"] == fixed_data.cooking_time
    assert created["views"] == 0


async def test_get_recipes_list_empty(async_client):
    response = await async_client.get("/recipes")
    assert response.status_code == 200
    assert response.json() == []


async def test_get_recipe_detail_not_found(async_client):
    response = await async_client.get("/recipes/99999")
    assert response.status_code == 404
    assert "Рецепт не найден" in response.json()["detail"]
