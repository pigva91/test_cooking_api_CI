from typing import Annotated

from sqlalchemy.orm import Mapped, mapped_column

from .db import Base

intpk = Annotated[int, mapped_column(primary_key=True)]
str_256 = Annotated[str, mapped_column(nullable=False, default="")]


class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[intpk]
    title: Mapped[str_256]
    cooking_time: Mapped[int] = mapped_column(nullable=False)
    ingredients: Mapped[str_256]
    description: Mapped[str_256]
    views: Mapped[int] = mapped_column(default=0, nullable=False)
