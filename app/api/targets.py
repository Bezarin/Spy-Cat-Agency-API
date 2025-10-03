from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.db.session import get_session
from app.models.target import Target
from app.schemas.target import TargetResponse, TargetUpdate

router = APIRouter(prefix="/targets", tags=["Targets"])


@router.put("/{target_id}", response_model=TargetResponse)
async def update_target(
    target_id: int, target_update: TargetUpdate, session: Session = Depends(get_session)
):
    """
    Update target notes and/or completion status.
    Notes cannot be updated if target or mission is completed.
    """
    target = session.get(Target, target_id)
    if not target:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Target with id {target_id} not found",
        )

    if target_update.notes is not None:
        if target.complete:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot update notes for completed target",
            )

        if target.mission.complete:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot update notes for target in completed mission",
            )

        target.notes = target_update.notes

    if target_update.complete is not None:
        target.complete = target_update.complete

        if target_update.complete:
            mission = target.mission
            all_completed = all(t.complete for t in mission.targets)
            if all_completed:
                mission.complete = True
                session.add(mission)

    session.add(target)
    session.commit()
    session.refresh(target)

    return target