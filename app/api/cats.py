from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.cat import Cat
from app.schemas.cat import CatCreate, CatResponse, CatUpdate
from app.services.breeds import is_valid_breed

router = APIRouter(prefix="/cats", tags=["Cats"])


@router.post("/", response_model=CatResponse, status_code=status.HTTP_201_CREATED)
async def create_cat(cat_data: CatCreate, session: Session = Depends(get_session)):
    """
    Create a new spy cat.

    Validates the breed against TheCatAPI and creates a new cat record.
    """
    # Validate breed with TheCatAPI
    if not await is_valid_breed(cat_data.breed):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid breed: {cat_data.breed}. Please use a valid cat breed.",
        )

    new_cat = Cat(
        name=cat_data.name,
        years_experience=cat_data.years_experience,
        breed=cat_data.breed,
        salary=cat_data.salary,
    )

    session.add(new_cat)
    session.commit()
    session.refresh(new_cat)

    return new_cat


@router.get("/", response_model=List[CatResponse])
async def list_cats(session: Session = Depends(get_session)):
    """
    List all spy cats in the system.
    """
    statement = select(Cat)
    cats = session.exec(statement).all()
    return cats


@router.get("/{cat_id}", response_model=CatResponse)
async def get_cat(cat_id: int, session: Session = Depends(get_session)):
    """
    Get a single spy cat by ID.
    """
    cat = session.get(Cat, cat_id)
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cat with id {cat_id} not found",
        )
    return cat


@router.put("/{cat_id}", response_model=CatResponse)
async def update_cat(
    cat_id: int, cat_update: CatUpdate, session: Session = Depends(get_session)
):
    """
    Update spy cat information (currently only salary can be updated).
    """
    cat = session.get(Cat, cat_id)
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cat with id {cat_id} not found",
        )

    cat.salary = cat_update.salary
    session.add(cat)
    session.commit()
    session.refresh(cat)

    return cat


@router.delete("/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cat(cat_id: int, session: Session = Depends(get_session)):
    """
    Remove a spy cat from the system.
    """
    cat = session.get(Cat, cat_id)
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cat with id {cat_id} not found",
        )

    if cat.missions:
        active_missions = [
            mission for mission in cat.missions if not mission.is_complete
        ]
        if active_missions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete cat with active missions. Complete or reassign missions first.",
            )

    session.delete(cat)
    session.commit()
