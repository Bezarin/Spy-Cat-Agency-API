from typing import TYPE_CHECKING, Optional

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.mission import Mission


class Target(SQLModel, table=True):
    __tablename__ = "targets"

    id: Optional[int] = Field(default=None, primary_key=True)
    mission_id: int = Field(foreign_key="missions.id")
    name: str
    country: str
    notes: str = Field(default="")
    complete: bool = Field(default=False)

    mission: "Mission" = Relationship(back_populates="targets")

    __table_args__ = (
        UniqueConstraint("mission_id", "name", name="uq_target_name_per_mission"),
    )
