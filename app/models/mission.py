from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Index, text
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.cat import Cat
    from app.models.target import Target


class Mission(SQLModel, table=True):
    __tablename__ = "missions"

    id: Optional[int] = Field(default=None, primary_key=True)
    complete: bool = Field(default=False)
    cat_id: Optional[int] = Field(default=None, foreign_key="cats.id")

    cat: Optional["Cat"] = Relationship(back_populates="missions")
    targets: List["Target"] = Relationship(
        back_populates="mission",
        cascade_delete=True,
    )

    __table_args__ = (
        Index(
            "uq_active_mission_per_cat",
            "cat_id",
            unique=True,
            postgresql_where=text("cat_id IS NOT NULL AND complete = false"),
        ),
    )
