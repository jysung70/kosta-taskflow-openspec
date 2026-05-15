from typing import Optional, Literal
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
import models
import auth as auth_utils

router = APIRouter(tags=["tasks"])

class CreateTaskRequest(BaseModel):
    title: str
    assignee_id: Optional[int] = None

class UpdateTaskRequest(BaseModel):
    status: Optional[Literal["TODO", "DOING", "DONE"]] = None
    title: Optional[str] = None

class PatchStatusRequest(BaseModel):
    status: Literal["TODO", "DOING", "DONE"]

def _require_team_member(team_id: int, db: Session, current_user: models.User) -> models.Team:
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team or current_user not in team.members:
        raise HTTPException(status_code=403, detail={"code": "FORBIDDEN", "msg": "해당 팀에 접근 권한이 없습니다"})
    return team

def _task_dict(t: models.Task) -> dict:
    assignee_email = None
    if t.assignee_id and t.assignee:
        assignee_email = t.assignee.email
    return {
        "id": t.id, "title": t.title, "status": t.status,
        "creator_id": t.creator_id, "assignee_id": t.assignee_id,
        "assignee_email": assignee_email, "team_id": t.team_id,
    }

@router.post("/api/teams/{team_id}/tasks", status_code=201)
def create_task(
    team_id: int, req: CreateTaskRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    _require_team_member(team_id, db, current_user)
    task = models.Task(
        team_id=team_id, title=req.title, status="TODO",
        creator_id=current_user.id, assignee_id=req.assignee_id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return _task_dict(task)

@router.get("/api/teams/{team_id}/tasks")
def list_tasks(
    team_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    _require_team_member(team_id, db, current_user)
    tasks = db.query(models.Task).filter(models.Task.team_id == team_id).all()
    return [_task_dict(t) for t in tasks]

@router.get("/api/tasks/{task_id}")
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "msg": "태스크를 찾을 수 없습니다"})
    _require_team_member(task.team_id, db, current_user)
    return _task_dict(task)

@router.patch("/api/tasks/{task_id}/status")
def patch_task_status(
    task_id: int, req: PatchStatusRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "msg": "태스크를 찾을 수 없습니다"})
    _require_team_member(task.team_id, db, current_user)
    task.status = req.status
    db.commit()
    db.refresh(task)
    return {"id": task.id, "status": task.status}

@router.put("/api/tasks/{task_id}")
def update_task(
    task_id: int, req: UpdateTaskRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "msg": "태스크를 찾을 수 없습니다"})
    _require_team_member(task.team_id, db, current_user)
    if req.status is not None:
        task.status = req.status
    if req.title is not None:
        task.title = req.title
    db.commit()
    db.refresh(task)
    return _task_dict(task)

@router.delete("/api/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "msg": "태스크를 찾을 수 없습니다"})
    _require_team_member(task.team_id, db, current_user)
    db.delete(task)
    db.commit()
    return {"msg": "삭제되었습니다"}
