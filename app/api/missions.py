from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.cat import Cat
from app.models.mission import Mission
from app.models.target import Target
from app.schemas.mission import (
    MissionCreate,
    MissionResponse,
    MissionWithCat,
)

router = APIRouter(prefix="/missions", tags=["Missions"])


@router.post("/", response_model=MissionResponse, status_code=status.HTTP_201_CREATED)
async def create_mission(
    mission_data: MissionCreate, session: Session = Depends(get_session)
):
    """
    Create a new mission with 1-3 targets in a single request.
    """
    new_mission = Mission()
    session.add(new_mission)
    session.commit()
    session.refresh(new_mission)

    targets = []
    for target_data in mission_data.targets:
        target = Target(
            mission_id=new_mission.id,
            name=target_data.name,
            country=target_data.country,
            notes=target_data.notes,
        )
        session.add(target)
        targets.append(target)

    session.commit()

    for target in targets:
        session.refresh(target)

    session.refresh(new_mission)

    return new_mission


@router.get("/", response_model=List[MissionWithCat])
async def list_missions(session: Session = Depends(get_session)):
    """
    List all missions in the system with their targets and assigned cats.
    """
    statement = select(Mission).order_by(Mission.id)
    missions = session.exec(statement).all()

    result = []
    for mission in missions:
        mission_dict = {
            "id": mission.id,
            "complete": mission.complete,
            "cat_id": mission.cat_id,
            "cat": None,
            "targets": mission.targets,
        }

        if mission.cat:
            mission_dict["cat"] = {
                "id": mission.cat.id,
                "name": mission.cat.name,
                "breed": mission.cat.breed,
                "years_experience": mission.cat.years_experience,
            }

        result.append(mission_dict)

    return result


@router.get("/{mission_id}", response_model=MissionWithCat)
async def get_mission(mission_id: int, session: Session = Depends(get_session)):
    """
    Get a single mission by ID with its targets and assigned cat.
    """
    mission = session.get(Mission, mission_id)
    if not mission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mission with id {mission_id} not found",
        )

    mission_dict = {
        "id": mission.id,
        "complete": mission.complete,
        "cat_id": mission.cat_id,
        "cat": None,
        "targets": mission.targets,
    }

    if mission.cat:
        mission_dict["cat"] = {
            "id": mission.cat.id,
            "name": mission.cat.name,
            "breed": mission.cat.breed,
            "years_experience": mission.cat.years_experience,
        }

    return mission_dict


@router.delete("/{mission_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mission(mission_id: int, session: Session = Depends(get_session)):
    """
    Delete a mission. Cannot delete if mission is assigned to a cat.
    """
    mission = session.get(Mission, mission_id)
    if not mission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mission with id {mission_id} not found",
        )

    if mission.cat_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete mission that is assigned to a cat. Unassign first.",
        )

    session.delete(mission)
    session.commit()


@router.put("/{mission_id}/assign/{cat_id}", response_model=MissionResponse)
async def assign_cat_to_mission(
    mission_id: int, cat_id: int, session: Session = Depends(get_session)
):
    """
    Assign a cat to a mission. One cat can only have one active mission.
    """
    mission = session.get(Mission, mission_id)
    if not mission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mission with id {mission_id} not found",
        )

    cat = session.get(Cat, cat_id)
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cat with id {cat_id} not found",
        )

    if mission.complete:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot assign cat to completed mission",
        )

    if mission.cat_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mission is already assigned to another cat",
        )

    statement = select(Mission).where(Mission.cat_id == cat_id, not Mission.complete)
    existing_mission = session.exec(statement).first()
    if existing_mission:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cat is already assigned to mission {existing_mission.id}",
        )

    mission.cat_id = cat_id
    session.add(mission)
    session.commit()
    session.refresh(mission)

    return mission
