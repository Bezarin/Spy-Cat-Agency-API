from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.mission import Mission


class Cat(SQLModel, table=True):
    __tablename__ = "cats"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    years_experience: int
    breed: str
    salary: float

    missions: List["Mission"] = Relationship(
        back_populates="cat",
        cascade_delete=True,
    )
