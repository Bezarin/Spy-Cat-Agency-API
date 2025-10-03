from typing import Optional

from pydantic import BaseModel, Field


class TargetCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=1, max_length=100)
    notes: str = Field(default="", max_length=1000)


class TargetUpdate(BaseModel):
    notes: Optional[str] = Field(None, max_length=1000)
    complete: Optional[bool] = None


class TargetResponse(BaseModel):
    id: int
    mission_id: int
    name: str
    country: str
    notes: str
    complete: bool

    class Config:
        from_attributes = True
