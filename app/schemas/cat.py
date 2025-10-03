from pydantic import BaseModel, Field


class CatCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    years_experience: int = Field(..., ge=0, le=50)
    breed: str = Field(..., min_length=1, max_length=100)
    salary: float = Field(..., gt=0)


class CatUpdate(BaseModel):
    salary: float = Field(..., gt=0)


class CatResponse(BaseModel):
    id: int
    name: str
    years_experience: int
    breed: str
    salary: float

    class Config:
        from_attributes = True
