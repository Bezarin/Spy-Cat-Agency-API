from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.target import TargetCreate, TargetResponse


class MissionCreate(BaseModel):
    targets: List[TargetCreate] = Field(..., min_length=1, max_length=3)


class MissionAssign(BaseModel):
    cat_id: int = Field(..., gt=0)


class MissionResponse(BaseModel):
    id: int
    complete: bool
    cat_id: Optional[int]
    targets: List[TargetResponse]

    class Config:
        from_attributes = True


class MissionWithCat(BaseModel):
    id: int
    complete: bool
    cat_id: Optional[int]
    cat: Optional[dict] = None
    targets: List[TargetResponse]

    class Config:
        from_attributes = True
