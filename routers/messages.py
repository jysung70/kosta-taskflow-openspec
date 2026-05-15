from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import get_db
import models
import auth as auth_utils

router = APIRouter(tags=["messages"])

class SendMessageRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)

def _require_team_member(team_id: int, db: Session, current_user: models.User) -> models.Team:
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team or current_user not in team.members:
        raise HTTPException(status_code=403, detail={"code": "FORBIDDEN", "msg": "해당 팀에 접근 권한이 없습니다"})
    return team

def _fmt(m: models.Message) -> dict:
    return {
        "id": m.id,
        "content": m.content,
        "user_id": m.user_id,
        "team_id": m.team_id,
        "created_at": m.created_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "sender_email": m.user.email,
    }

@router.post("/api/teams/{team_id}/messages", status_code=201)
def send_message(
    team_id: int,
    req: SendMessageRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    _require_team_member(team_id, db, current_user)
    msg = models.Message(team_id=team_id, user_id=current_user.id, content=req.content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    db.refresh(msg, ["user"])
    return _fmt(msg)

@router.get("/api/teams/{team_id}/messages")
def list_messages(
    team_id: int,
    since: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    _require_team_member(team_id, db, current_user)
    q = db.query(models.Message).filter(models.Message.team_id == team_id)
    if since:
        try:
            since_dt = datetime.strptime(since.replace("Z", ""), "%Y-%m-%dT%H:%M:%S")
            q = q.filter(models.Message.created_at > since_dt).order_by(models.Message.created_at.asc())
        except ValueError:
            q = q.order_by(models.Message.created_at.desc()).limit(50)
            return list(reversed([_fmt(m) for m in q.all()]))
    else:
        q = q.order_by(models.Message.created_at.desc()).limit(50)
        return list(reversed([_fmt(m) for m in q.all()]))
    return [_fmt(m) for m in q.all()]

@router.get("/api/messages/{message_id}")
def get_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    msg = db.query(models.Message).filter(models.Message.id == message_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "msg": "메시지를 찾을 수 없습니다"})
    _require_team_member(msg.team_id, db, current_user)
    return _fmt(msg)

@router.delete("/api/messages/{message_id}")
def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    msg = db.query(models.Message).filter(models.Message.id == message_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "msg": "메시지를 찾을 수 없습니다"})
    if msg.user_id != current_user.id:
        raise HTTPException(status_code=403, detail={"code": "FORBIDDEN", "msg": "본인 메시지만 삭제할 수 있습니다"})
    db.delete(msg)
    db.commit()
    return {"msg": "삭제되었습니다"}
