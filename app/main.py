from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db import Base, engine
from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title="Кулинарная книга API",
    description="""
        API для кулинарной книги.
        Основные возможности:
        - Получить список всех рецептов (сортировка по популярности/по времени)
        - Получить информацию о рецепте (увеличивает счётчик просмотров)
        - Создать новый рецепт
        """,
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)
