import secrets
import string
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/api/teams", tags=["teams"])

def _generate_invite_code() -> str:
    letters = "".join(secrets.choice(string.ascii_uppercase) for _ in range(4))
    digits = "".join(secrets.choice(string.digits) for _ in range(4))
    return f"{letters}-{digits}"

def _require_member(team_id: int, db: Session, current_user: models.User) -> models.Team:
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team or current_user not in team.members:
        raise HTTPException(status_code=403, detail={"code": "FORBIDDEN", "msg": "해당 팀에 접근 권한이 없습니다"})
    return team

class CreateTeamRequest(BaseModel):
    name: str

class JoinTeamRequest(BaseModel):
    invite_code: str

@router.post("", status_code=201)
def create_team(
    req: CreateTeamRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    invite_code = _generate_invite_code()
    while db.query(models.Team).filter(models.Team.invite_code == invite_code).first():
        invite_code = _generate_invite_code()
    team = models.Team(name=req.name, invite_code=invite_code, owner_id=current_user.id)
    team.members.append(current_user)
    db.add(team)
    db.commit()
    db.refresh(team)
    return {"id": team.id, "name": team.name, "invite_code": team.invite_code, "owner_id": team.owner_id}

@router.get("")
def list_teams(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    return [{"id": t.id, "name": t.name, "invite_code": t.invite_code} for t in current_user.teams]

@router.post("/join")
def join_team(
    req: JoinTeamRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    team = db.query(models.Team).filter(models.Team.invite_code == req.invite_code).first()
    if not team:
        raise HTTPException(status_code=404, detail={"code": "INVALID_INVITE_CODE", "msg": "유효하지 않은 초대코드입니다"})
    if current_user in team.members:
        raise HTTPException(status_code=409, detail={"code": "ALREADY_MEMBER", "msg": "이미 소속된 팀입니다"})
    team.members.append(current_user)
    db.commit()
    return {"id": team.id, "name": team.name}

@router.get("/{team_id}/members")
def get_members(
    team_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth_utils.get_current_user),
):
    team = _require_member(team_id, db, current_user)
    return [{"id": m.id, "email": m.email} for m in team.members]
