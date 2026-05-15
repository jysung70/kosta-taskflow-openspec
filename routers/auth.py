from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
import models
import auth as auth_utils

router = APIRouter(prefix="/api/auth", tags=["auth"])

class SignupRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/signup", status_code=201)
def signup(req: SignupRequest, db: Session = Depends(get_db)):
    if not req.email or not req.password:
        raise HTTPException(status_code=422, detail="이메일과 비밀번호를 입력하세요")
    if db.query(models.User).filter(models.User.email == req.email).first():
        raise HTTPException(status_code=409, detail={"code": "EMAIL_EXISTS", "msg": "이미 사용 중인 이메일입니다"})
    user = models.User(email=req.email, password_hash=auth_utils.hash_password(req.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    token = auth_utils.create_access_token(user.id)
    return {"token": token, "user": {"id": user.id, "email": user.email}}

@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == req.email).first()
    if not user or not auth_utils.verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail={"code": "INVALID_CREDENTIALS", "msg": "이메일 또는 비밀번호가 올바르지 않습니다"})
    token = auth_utils.create_access_token(user.id)
    return {"token": token, "user": {"id": user.id, "email": user.email}}

@router.get("/me")
def me(current_user: models.User = Depends(auth_utils.get_current_user)):
    return {"id": current_user.id, "email": current_user.email}

@router.post("/logout")
def logout(current_user: models.User = Depends(auth_utils.get_current_user)):
    return {"msg": "로그아웃 되었습니다"}
